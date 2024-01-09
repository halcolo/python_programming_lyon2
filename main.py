import os
import config
import logging
import pandas as pd
from modules.corpus import Corpus
from utils.tools import clean_text_util
from utils.program import search_documents, search_engine, calculate_similarity_articles
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from dash import (
    Dash, 
    dash_table,  
    html)
import gc

path = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(f'{path}/data/subjects.csv', header=0)
df.rename(columns={0: 'Subject', 1: 'Subreddit'}, inplace=True)


PAGE_ZISE = 15
TABLE_DICT_ROW_NAME = 'row'
last_active_cell = None
external_css = [f"{path}/css/custom_table_styling.css"]
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


content = list()
content_name = list()
content_name += [html.H1("Search engine")]

## Check if credentials are set and make an alert if not
if os.environ.get('CLIENT_SECRET') is None \
    or os.environ.get('CLIENT_SECRET') is None \
        or os.environ.get('CLIENT_SECRET') is None:
            content_name += [ dbc.Alert(
                "Please set your credentials in the 'config.py' file", 
                color="danger"
            )]


# Add table
data_table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': str(c), 'name': str(c)} for c in df.columns],
        style_cell={'textAlign': 'left'},
        # Options de pagination
        page_current=0,
        page_size=PAGE_ZISE,
        style_cell_conditional=[
            {
                'if': {'column_id': 'name'},
                'textAlign': 'left'
            },
        ], id='tbl'
    )


keyword_input = html.Div(
    [
        dbc.Label("Key Word", html_for="keyword-text"),
        dbc.Input(type="text", id="keyword-text", placeholder="Enter key word"),
        dbc.FormText(
            "Example Llama Machine learning",
            color="secondary",
        ),
    ],
    className="mb-6",
)


loading_obj = dbc.Spinner(
                id="tab-response",
                children=[html.Div([html.Div(id="loading-output-2")])],
                color="primary",
            )
button = dbc.Button("Submit", color="primary", className="me-1", id="add-btn")

form = dbc.Form([
        dbc.Row(content_name),
         
        dbc.Row([
            dbc.Col(html.Div(data_table)),
            dbc.Col(html.Div([keyword_input, button]))
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dbc.Col(html.Div([html.H1("Results")])),
                    html.Div([loading_obj]),
                    ])
                ),
            
        ]),
    ])

content += [form]
app.layout = dbc.Container(content, fluid=True)

@app.callback(
    Output('tab-response', 'children'), 
    [
        Input("add-btn", "n_clicks"),
        State("keyword-text", "value"),
        State("tbl", "active_cell")
    ]
)

def render_tab_content(n_clicks, keyword_text, active_cell):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_cell and keyword_text is not None:
        
        
        # Getting values from table
        arxiv_kw = df.iloc[active_cell['row']]['Subject']
        subreddit_kw = df.iloc[active_cell['row']]['Subreddit']
    
    
        try:
            search_request = [
                {'type':'reddit', 'keyword':subreddit_kw},
                {'type':'arxiv', 'keyword':arxiv_kw}
                ]
            
            corpus = search_documents(search_request)
            # corpus_arxiv = search_documents(search_request_arxiv)
            tokens_kw = clean_text_util(keyword_text)
            df_corpus = corpus.to_dataframe()
            
            # Return a list with the documents that match the keywords filtered 
            response_search_engine = search_engine(corpus.docs_to_collection(), tokens_kw)
            
            # response_search_engine = sorted(response_search_engine, key=lambda x: x['Score'], reverse=True)
            df_scores = pd.DataFrame(response_search_engine)
            
            df_scores['id'] = df_scores['id'].astype(str)
            df_corpus['id'] = df_corpus['id'].astype(str)
            df_corpus['unique_id'] = df_corpus['source'] + '_' + df_corpus['id'].astype(str)
            
            df_corpus_filtered = df_corpus[df_corpus['id'].isin(df_scores['id'])]
            similarity_df = calculate_similarity_articles(df_corpus)
            
            
            similarity_pairs = dict()
            for idx in df_corpus['unique_id'].tolist():
                similarity_pairs[idx.split('_')[0]] = dict()
                similarity_pairs[idx.split('_')[0]][idx.split('_')[1]] = list()
                selected_rows = similarity_df.loc[df_corpus['unique_id'], idx]
                selected_df = selected_rows.reset_index()
                selected_df_sorted = selected_df.sort_values(by=idx, ascending=False)
                selected_df_sorted = selected_df_sorted.drop(selected_df_sorted[selected_df_sorted['unique_id'] == idx].index)
                selected_df_sorted = selected_df_sorted.drop(selected_df_sorted[selected_df_sorted[idx] <= float(0.0)].index)
                if len(selected_df_sorted) > 0:
                    selected_df_filtered = selected_df_sorted.tail(5)
                    for i in selected_df_filtered['unique_id'].tolist():
                        # df_corpus_filtered.loc[df_corpus_filtered['similar_source'] == idx.split('_')[0], 'similar_source'] = df_corpus_filtered.loc[df_corpus_filtered['similar_source'] == idx.split('_')[0], 'similar_source'].apply(lambda x: x.append(dict()))
                        similarity_pairs[idx.split('_')[0]][idx.split('_')[1]].append({'similar_source': i.split('_')[0], 'similar_id': i.split('_')[1], 'similarity': selected_df_filtered[selected_df_filtered['unique_id'] == i][idx].values[0]})
            
            similarity_df_reddit = None
            similarity_df_arxiv = None
            
            for source in similarity_pairs:
                for id in similarity_pairs[source]:
                    if source == 'reddit':
                        similarity_df_reddit = pd.DataFrame(similarity_pairs[source][id])
                    else:
                        similarity_df_arxiv = pd.DataFrame(similarity_pairs[source][id])

            
            table_scores = dbc.Table.from_dataframe(df_corpus_filtered, striped=True, bordered=True, hover=True, id='tbl_scores')
            # table_scores = dash_table.DataTable(
            #     data=df_corpus.to_dict('records'),
            #     columns=[{'id': str(c), 'name': str(c)} for c in df_corpus.columns],
            #     style_cell={'textAlign': 'left'},
            #     # Options de pagination
            #     page_current=0,
            #     page_size=PAGE_ZISE,
            #     style_cell_conditional=[
            #         {
            #             'if': {'column_id': 'name'},
            #             'textAlign': 'left'
            #         },
            #     ], id='tbl_scores'
            #     # striped=True, bordered=True, hover=True, id='tbl_scores',
            # )
            # dbc.Table.from_dataframe(df_corpus, striped=True, bordered=True, hover=True, id='tbl_scores')
            
            response = dbc.Row([
                dbc.Row([
                    html.Div([table_scores])
                    
                    # dbc.Spinner(
                    #     id="tab-similarity",
                    #     children=[html.Div([html.Div(id="loading-output-similarity")])],
                    #     color="primary",
                    # ),
                    # dbc.Col(html.Div([html.H1("Arxiv"), html.Div(id='tbl_arxiv')]))
                    # dbc.Col(html.Div([html.H1("Arxiv"), table_reddit])),
                ])
            ])
            
            return response
            
        except TypeError as t:
            logging.error(t)
            raise TypeError
        except ValueError as v:
            logging.error(v)
            raise ValueError
        

        
    return  dbc.Alert(
                "Please select a row and enter a key word", 
                color="danger"
            )

# @app.callback(
#     Output('tab-similarity', 'children'), 
#     [
#         # Input("tbl", "n_clicks"),
#         # State("keyword-text", "value"),
#         Input("tbl_scores", "active_cell")
#     ]
# )
# def rendre_table_similarity(active_cell):
#     return active_cell

    
if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
            
            # merged_df = pd.concat([df_reddit, df_arxiv])
            # vectorizer = TfidfVectorizer(stop_words='english')
            
            # tditdf_matrix = vectorizer.fit_transform(merged_df['text'])
            
            # cosine_similarity_matrix = cosine_similarity(tditdf_matrix, tditdf_matrix)

            # similarity_df = pd.DataFrame(cosine_similarity_matrix, index=merged_df['id'], columns=merged_df['id'])
            
            # # Mostrar los términos más relacionados
            # threshold = 0.5  # Puedes ajustar este umbral según tus necesidades
            # related_terms = {}

            # for idx in similarity_df.index:
            #     print(idx)
            #     related_texts = similarity_df[similarity_df[idx] > threshold].index.tolist()
            #     related_texts.remove(idx)  # Excluir el propio texto
            #     if related_texts:
            #         related_terms[idx] = related_texts
            # # print(related_terms)
                    
            # df_related_terms = pd.DataFrame.from_dict(df_reddit, orient='index')
            # table_reddit = dbc.Table.from_dataframe(df_reddit, striped=True, bordered=True, hover=True)

            