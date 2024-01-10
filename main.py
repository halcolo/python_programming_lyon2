import os
import logging
import time
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash import Dash, dash_table, html, dcc
from dash.dependencies import Input, Output, State
from utils.tools import (
    clean_paragraph_util, 
    clean_text, 
    normalize_value,
    label_from_normalized_value,
)
from utils.program import (
    search_documents,
    search_engine,
    calculate_similarity_articles,
    process_similarity_pairs,
    calculate_word_freq_per_year,
)

path = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(f'{path}/data/subjects.csv', header=0)
df.rename(columns={0: 'Subject', 1: 'Subreddit'}, inplace=True)

PAGE_SIZE = 15

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# Define layout components
content_name = [
    html.H1("Search engine"),
    dbc.Alert(
        "Please set your credentials in the 'config.py' file",
        color="danger"
    ) if any(os.environ.get('CLIENT_SECRET') is None for _ in range(3)) else None
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
                dbc.Col(html.Div([html.H1("Results")])),
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
    if active_cell and keyword_text is not None:
        arxiv_kw = df.iloc[active_cell['row']]['Subject']
        subreddit_kw = df.iloc[active_cell['row']]['Subreddit']

        try:
            search_request = [
                {'type': 'reddit', 'keyword': subreddit_kw, 'topic': subreddit_kw, 'quantity': 100},
                {'type': 'arxiv', 'keyword': arxiv_kw, 'topic': subreddit_kw, 'quantity': 100}
            ]

            corpus = search_documents(search_request)
            tokens_kw = clean_paragraph_util(keyword_text)
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
                    s_cards = [html.Div([html.H4("Similar content")])]
                    if len(accordion_content) < 15:
                        if str(document['id']) in similarity_pairs[document['source']]:
                            for similar_document in similarity_pairs[document['source']][str(document['id'])]:
                                similar_doc = corpus.get_document(similar_document['similar_id'])
                                normalized_score = normalize_value(float(similar_document['similarity']), 0, 0.01)
                                score_etiquete = label_from_normalized_value(normalized_score)
                                s_cards.append(
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.H5(f"{similar_doc.source}", className="card-title"),
                                                    html.P(f"{similar_doc.title}"),
                                                    html.Hr(),
                                                    html.A("Article link", href=similar_doc.url, target="_blank"),
                                                    html.Br(),
                                                    dbc.FormText(f"Similarity score: {score_etiquete}"),
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

                        accordion_content.append(
                            dbc.AccordionItem(
                                html.Div(
                                    [
                                        html.H1(clean_text(document['title'])),
                                        html.P(document['text']),
                                        dbc.CardLink("Article link", href=document['url']),
                                        dbc.Row(similarity_cards)
                                    ]
                                ),
                                str(document),
                                title=f"{document['id']}-{clean_text(document['title'])}",
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

                fig = go.Figure()
                word_freq_per_year = calculate_word_freq_per_year(corpus, tokens_kw)
                count = 0
                for word in tokens_kw:
                    if count < 2:
                        word_freqs = {key[1]: value for key, value in word_freq_per_year.items() if key[0] == word}
                        years, frequency = zip(*sorted(word_freqs.items()))
                        
                        fig.add_trace(go.Scatter(x=years, y=frequency, mode='lines+markers', name=word))
                        
                fig.update_layout(
                    title='Evolution of Word Usage Over Time',
                    xaxis_title='Year',
                    yaxis_title='Word Count',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                )
                return response, fig
            else:
                return dbc.Alert(
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

    return dbc.Alert(
        [
            html.I(className="bi bi-info-circle-fill me-2"),
            "Please select a row and enter a keyword",
        ],
        color="info",
        className="d-flex align-items-center",
    ), go.Figure()


# @app.callback(
#     Output('word-evo-graph', 'figure'),
#     [Input("add-btn", "n_clicks"), State("keyword-text", "value") , State("tbl", "active_cell")]
# )
# def cb_words_evolution_graph(n_clicks, keyword_text, active_cell):
#     if active_cell and keyword_text is not None:
#         arxiv_kw = df.iloc[active_cell['row']]['Subject']
#         subreddit_kw = df.iloc[active_cell['row']]['Subreddit']
        
#         # time.sleep(4)
#         fig = go.Figure()
#         search_request = [
#             {'type': 'reddit', 'keyword': subreddit_kw, 'topic': subreddit_kw, 'quantity': 100},
#             {'type': 'arxiv', 'keyword': arxiv_kw, 'topic': subreddit_kw, 'quantity': 100}
#         ]
#         corpus = search_documents(search_request)
#         word_freq_per_year = calculate_word_freq_per_year(corpus, keyword_text)
#         count = 0
#         for word in keyword_text:
#             if count < 2:
#                 word_freqs = {key[1]: value for key, value in word_freq_per_year.items() if key[0] == word}
#                 years, frequency = zip(*sorted(word_freqs.items()))
                
#                 fig.add_trace(go.Scatter(x=years, y=frequency, mode='lines+markers', name=word))
                
#         fig.update_layout(
#             title='Evolution of Word Usage Over Time',
#             xaxis_title='Year',
#             yaxis_title='Word Count',
#             legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
#         )
#         return fig

if __name__ == '__main__':
    app.run_server(debug=True)