import os
import logging
import time
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from config import img
from dash import Dash, dash_table, html, dcc
from dash.dependencies import Input, Output, State
from utils.tools import (
    clean_paragraph, 
    clean_text, 
    normalize_value,
    label_from_normalized_value,
)
from utils.func_processing import (
    calculate_similarity_articles,
    process_similarity_pairs,
)
from utils.func_retrieval import (
    search_documents,
    search_engine,   
)

path = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(f'{path}/data/subjects.csv', header=0)
df.rename(columns={0: 'Subject', 1: 'Subreddit'}, inplace=True)

PAGE_SIZE = 15

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# Define layout components
content_name = [
    dbc.Row([
        html.H1("Search engine", className="display-4", style={"textAlign": "center"}),
    ]),
    dbc.Row([
        dbc.Alert(
            "Please set your credentials in the 'config.py' file",
            color="danger"
        ) 
    if any(os.environ.get('CLIENT_SECRET') is None for _ in range(3)) else None ])
]

data_table = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': 'Subject', 'name': 'Subject'}],
    style_cell={'textAlign': 'left'},
    page_current=0,
    page_size=PAGE_SIZE,
    style_cell_conditional=[
        {'if': {'column_id': 'name'}, 'textAlign': 'left'},
    ],
    id='tbl'
)



keyword_input = html.Div(
    [
        html.H3("Keywords"),
        dbc.Input(type="text", id="keyword-text", placeholder="Enter keywords"),
        dbc.FormText(
            "Example Llama Machine learning",
            color="secondary",
        ),
        html.Br(),
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
        dbc.Col(html.Div([keyword_input, button])),
        dbc.Col(dcc.Graph(id="word-evo-graph"), md=6),
        
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                dbc.Col(html.Div([html.H2("Search Results")])),
                html.Div([loading_obj]),
            ])
        ),
    ]),
])

app.layout = dbc.Container(form, fluid=True)


@app.callback(
    Output('tab-response', 'children'),
    Output('word-evo-graph', 'figure'),
    [Input("add-btn", "n_clicks"), State("keyword-text", "value"), State("tbl", "active_cell")]
)
def render_tab_content(n_clicks, keyword_text, active_cell):
    
    # default response
    response = dbc.Alert(
        [
            html.I(className="bi bi-info-circle-fill me-2"),
            "Please select a row and enter a keyword",
        ],
        color="info",
        className="d-flex align-items-center",
    ),
    
    fig = go.Figure()
    if active_cell and keyword_text is not None:
        arxiv_kw = df.iloc[active_cell['row']]['Subject']
        subreddit_kw = df.iloc[active_cell['row']]['Subreddit']

        try:
            search_request = [
                {'type': 'reddit', 'keyword': subreddit_kw, 'topic': subreddit_kw, 'quantity': 100},
                {'type': 'arxiv', 'keyword': arxiv_kw, 'topic': subreddit_kw, 'quantity': 100}
            ]

            corpus = search_documents(search_request)
            tokens_kw = clean_paragraph(keyword_text)
            df_corpus = corpus.to_dataframe()

            response_search_engine = search_engine(corpus.docs_to_collection(), tokens_kw)
            df_scores = pd.DataFrame(response_search_engine)
            
            if len(df_scores) > 0:
                df_scores['id'] = df_scores['id'].astype(str)
                df_corpus['id'] = df_corpus['id'].astype(str)
                df_corpus['unique_id'] = df_corpus['source'] + '_' + df_corpus['id'].astype(str)

                df_corpus_filtered = df_corpus[df_corpus['id'].isin(df_scores['id'])]
                similarity_df = calculate_similarity_articles(df_corpus)

                similarity_pairs = process_similarity_pairs(df_corpus, similarity_df)
                accordion_content = []

                for document in df_corpus_filtered.to_dict('records'):
                    s_cards = [dbc.Col(html.Div([html.H4("Similar content")])), html.Br()]
                    if len(accordion_content) < 15:
                        if str(document['id']) in similarity_pairs[document['source']]:
                            for similar_document in similarity_pairs[document['source']][str(document['id'])]:
                                similar_doc = corpus.get_document(similar_document['similar_id'])
                                normalized_score = normalize_value(float(similar_document['similarity']), 0, 0.01)
                                score = label_from_normalized_value(normalized_score)
                                if score == 2:
                                    score_etiqute = dbc.Button("Very Hight", size="sm", color="success", href=similar_doc.url, target="_blank"),
                                elif score == 1:
                                    score_etiqute = dbc.Button("High", size="sm", color="info", href=similar_doc.url, target="_blank"),
                                else:   
                                    score_etiqute = dbc.Button("Low", size="sm", color="secondary", href=similar_doc.url, target="_blank"),
                                    
                                if similar_doc.source == 'reddit':
                                    img_path = img.get('reddit_logo')
                                else:
                                    img_path = img.get('arxiv_logo')
                                s_cards.append(
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    dbc.Row([
                                                        dbc.Col(html.H5(f"{similar_doc.source}", className="card-title")),
                                                        dbc.Col(html.Img(src=img_path, width="25", height="25"),width="auto")
                                                    ]),
                                                    html.P(f"{similar_doc.title}"),
                                                    html.Hr(),
                                                    html.A("Article link", href=similar_doc.url, target="_blank"),
                                                    html.Br(),
                                                    dbc.Row([
                                                        dbc.Col(dbc.FormText(f"Similarity etiquet:"), width="auto"),
                                                        dbc.Col(score_etiqute, width="auto")
                                                    ]),
                                                ]
                                            )
                                        ],
                                        style={"width": "18rem"},
                                    )
                                )

                        similarity_cards = dbc.Row(
                            [dbc.Col(card, width="auto") if len(s_cards) > 0 else html.Div([html.H4("No similar content")])
                             for card in s_cards]
                        )
                        if document['source'] == 'reddit':
                            acc_img_path = img.get('reddit_logo')
                        else:  
                            acc_img_path = img.get('arxiv_logo')
                            
                        accordion_content.append(
                            dbc.AccordionItem(
                                html.Div(
                                    [   
                                        
                                        dbc.Row([
                                            dbc.Col(html.Img(src=acc_img_path, width="25", height="25"),width="auto"),
                                            dbc.Col(html.H1(clean_text(document['title']))), 
                                        ]),
                                        dbc.Col(html.P(document['text'])),
                                        dbc.Col(dbc.FormText(f"Author: {document['author']}")),
                                        dbc.Col(dbc.CardLink("Article link", href=document['url'],target="_blank")),
                                        dbc.Col(dbc.Row(similarity_cards))
                                    ]
                                ),
                                str(document),
                                title=f"{document['id']}-{clean_text(document['title'])} - {document['source']}",
                                item_id=f"item-{len(accordion_content)}"
                            )
                        )
                    else:
                        break

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

                
                word_freq_per_year = corpus.calculate_word_freq_per_year(tokens_kw)
                for word in tokens_kw:
                    word_freqs = {key[1]: word_freq_per_year[(word.lower(), key[1])] for key in word_freq_per_year if key[0] == word.lower()}
                    years, frequency = zip(*sorted(word_freqs.items()))
                    fig.add_trace(go.Scatter(x=years, y=frequency, mode='lines+markers', name=word))
                 
                fig.update_layout(
                    title='Evolution of Word Usage Over Time',
                    xaxis_title='Year',
                    yaxis_title='Word Count',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                )
                response
            else:
                response =  dbc.Alert(
                    [
                        html.I(className="bi bi-exclamation-triangle-fill me-2"),
                        "No data found for this topic and keyword combination",
                    ],
                    color="warning",
                    className="d-flex align-items-center",
                )

        except (TypeError, ValueError) as e:
            logging.error(e)
            raise e

    return response, fig

if __name__ == '__main__':
    app.run_server(debug=True)