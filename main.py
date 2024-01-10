import os
import config
import logging
import pandas as pd
from utils.tools import clean_paragraph_util, clean_text
from utils.program import search_documents, search_engine, calculate_similarity_articles
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
# import gc
# from modules.corpus import Corpus
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import TfidfVectorizer
from dash import (
    Dash, 
    dash_table,  
    html)

path = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(f'{path}/data/subjects.csv', header=0)
df.rename(columns={0: 'Subject', 1: 'Subreddit'}, inplace=True)


PAGE_ZISE = 15
TABLE_DICT_ROW_NAME = 'row'
last_active_cell = None
external_css = [f"{path}/css/custom_table_styling.css"]
app = Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP, 
    dbc.icons.BOOTSTRAP])


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
        # columns=[{'id': str(c), 'name': str(c)} for c in df.columns],
        columns=[{'id': 'Subject', 'name': 'Subject'}],
        style_cell={'textAlign': 'left'},
        # Options de pagination.to_dict
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
                {'type':'reddit', 
                 'keyword':subreddit_kw, 
                 'topic': subreddit_kw,
                 'quantity': 100,
                 },
                {'type':'arxiv',
                 'keyword':arxiv_kw,
                 'topic': subreddit_kw,
                 'quantity': 100,}
                ]
            
            corpus = search_documents(search_request)
            # corpus_arxiv = search_documents(search_request_arxiv)
            tokens_kw = clean_paragraph_util(keyword_text)
            df_corpus = corpus.to_dataframe()
            
            # Return a list with the documents that match the keywords filtered 
            response_search_engine = search_engine(corpus.docs_to_collection(), tokens_kw)
            
            # response_search_engine = sorted(response_search_engine, key=lambda x: x['Score'], reverse=True)
            df_scores = pd.DataFrame(response_search_engine)
            if len(df_scores) > 0:
                df_scores['id'] = df_scores['id'].astype(str)
                df_corpus['id'] = df_corpus['id'].astype(str)
                df_corpus['unique_id'] = df_corpus['source'] + '_' + df_corpus['id'].astype(str)
                
                df_corpus_filtered = df_corpus[df_corpus['id'].isin(df_scores['id'])]
                similarity_df = calculate_similarity_articles(df_corpus)
                
                
                similarity_pairs = dict((('reddit', dict()),('arxiv', dict())))
                for idx in df_corpus['unique_id'].tolist():
                    # similarity_pairs[idx.split('_')[0]] = dict()
                    similarity_pairs[idx.split('_')[0]][idx.split('_')[1]] = list()
                    selected_rows = similarity_df.loc[df_corpus['unique_id'], idx]
                    selected_df = selected_rows.reset_index()
                    selected_df_sorted = selected_df.sort_values(by=idx, ascending=False)
                    selected_df_sorted = selected_df_sorted.drop(selected_df_sorted[selected_df_sorted['unique_id'] == idx].index)
                    selected_df_sorted = selected_df_sorted.drop(selected_df_sorted[selected_df_sorted[idx] <= float(0.0)].index)
                    if len(selected_df_sorted) > 0:
                        selected_df_filtered = selected_df_sorted.tail(3)
                        for i in selected_df_filtered['unique_id'].tolist():
                            # df_corpus_filtered.loc[df_corpus_filtered['similar_source'] == idx.split('_')[0], 'similar_source'] = df_corpus_filtered.loc[df_corpus_filtered['similar_source'] == idx.split('_')[0], 'similar_source'].apply(lambda x: x.append(dict()))
                            similarity_pairs[idx.split('_')[0]][idx.split('_')[1]].append({'similar_source': i.split('_')[0], 'similar_id': i.split('_')[1], 'similarity': selected_df_filtered[selected_df_filtered['unique_id'] == i][idx].values[0]})
                

                # for source in similarity_pairs:
                #     for id in similarity_pairs[source]:
                #         if source == 'reddit':
                #             similarity_df_reddit = pd.DataFrame(similarity_pairs[source][id])
                #         elif source == 'arxiv':
                #             similarity_df_arxiv = pd.DataFrame(similarity_pairs[source][id])

                accordion_content = list()
                counter = 0
                for document in df_corpus_filtered.to_dict('records'):
                    s_cards = [html.Div([html.H4("Similar content")])]
                    if counter < 15:
                        similarity_cards = list()
                        if str(document['id']) in similarity_pairs[document['source']]:
                            for similar_document in similarity_pairs[document['source']][str(document['id'])]:
                                similar_doc = corpus.get_document(similar_document['similar_id'])
                                s_cards.append(dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.H5(f"{similar_doc.source}", className="card-title"),
                                                    html.P(f"{similar_doc.title}"),
                                                    html.Hr(),
                                                    html.A("Article link", href=similar_doc.url, target="_blank"),
                                                    html.Br(),
                                                    html.A(f"Similarity score: {similar_document['similarity']}"),
                                                ]
                                            )
                                        ],style={"width": "18rem"},
                                    ))

                        similarity_cards =  dbc.Row(
                            # +
                            [dbc.Col(card, width="auto")
                             if len(s_cards) > 0 
                             else html.Div([html.H4("No similar content")]) for card in s_cards]
                        
                    )
                        accordion_content += dbc.AccordionItem(                            
                            html.Div(
                                [
                                    html.H1(clean_text(document['title'])), 
                                    html.P(document['text']),
                                    dbc.CardLink("Article link", href=document['url']),
                                    dbc.Row(
                                        similarity_cards
                                    )
                            ]),
                            str(document), 
                            title=f"{document['id']}-{clean_text(document['title'])}",
                            item_id=f"item-{counter}",
                        ),
                    else:
                        break
                    counter += 1
                    
                
                table_scores = dbc.Table.from_dataframe(df_corpus_filtered, striped=True, bordered=True, hover=True, id='tbl_scores')

                response = dbc.Row([
                    dbc.Row([
                        html.Div(
                            dbc.Accordion(
                                accordion_content,
                                flush=True,
                                active_item="item-0",
                            ),
                        )

                    ])
                ])
                
                return response
            else:
                return  dbc.Alert(
                [
                    html.I(className="bi bi-exclamation-triangle-fill me-2"),
                    "No data founded for this topic an key word combination",
                ],
                color="warning",
                className="d-flex align-items-center",
            )
            
        except TypeError as t:
            logging.error(t)
            raise TypeError
        except ValueError as v:
            logging.error(v)
            raise ValueError
        

        
    return  dbc.Alert(
                [
                    html.I(className="bi bi-info-circle-fill me-2"),
                    "Please select a row and enter a key word",
                ],
                color="info",
                className="d-flex align-items-center",
            )

    
if __name__ == '__main__':
    app.run_server(debug=True)