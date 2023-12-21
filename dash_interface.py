import dash
from dash import dcc, html
from dash.dash_table import DataTable
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# Chargez les données Velib
df = pd.read_excel('C:/Users/hp/Desktop/TD Python/velib.xlsx')

# Créez l'application Dash
app = dash.Dash(__name__)

# Créez un composant dcc.Store pour stocker l'information de la cellule active
app.layout = html.Div([
    html.H1("Tableau Velib"),
    
    # Ajoutez un composant dcc.Store
    dcc.Store(id='selected-cell-info', data=None),
    
    # Ajoutez le DataTable avec les champs de pagination
    DataTable(
        id='velib-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        
        # Style du tableau
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        
        # Options de pagination
        page_current=0,
        page_size=10,
        
        # Style de sélection des cellules
        style_data_conditional=[
            {
                'if': {'state': 'selected'},
                'backgroundColor': 'rgba(0, 116, 217, 0.3)',
                'border': '1px solid rgb(0, 116, 217)',
            }
        ],
    ),
    
    # Ajoutez un composant dcc.Graph pour afficher l'histogramme
    dcc.Graph(id='station-usage-histogram'),
    
    # Ajoutez un composant html.Div pour afficher le contenu de la cellule active
    html.Div(id='selected-cell-content'),
    
    # Ajoutez un nouveau tableau pour calculer la charge totale par station
    html.H2("Tableau de statistiques par station"),
    DataTable(
        id='station-stats-table',
        columns=[
            {'name': 'Station_Name', 'id': 'Station_Name'},
            {'name': 'Charge_Totale', 'id': 'Charge_Totale'},
            {'name': 'Sur_Colline', 'id': 'Sur_Colline'}
        ],
        # Initialisez les données du tableau avec une fonction callback
        data=[]
    ),
    
    # Ajoutez un composant dcc.Input pour permettre à l'utilisateur d'entrer le nom d'une station
    dcc.Input(id='station-input', type='text', placeholder='Nom de la station'),
    
    # Ajoutez un composant html.Button pour déclencher la mise à jour du tableau avec les statistiques
    html.Button(id='update-stats-button', n_clicks=0, children='Mettre à jour les statistiques')

])

# Ajoutez un callback pour mettre à jour le contenu de dcc.Store en fonction de la cellule active et de la pagination
@app.callback(
    Output('selected-cell-info', 'data'),
    Input('velib-table', 'active_cell'),
    Input('velib-table', 'page_current'),
    Input('velib-table', 'page_size')
)
def update_selected_cell_info(active_cell, page_current, page_size):
    if active_cell is not None:
        # Ajoutez les informations de pagination à l'objet active_cell
        active_cell['page_current'] = page_current
        active_cell['page_size'] = page_size
    return active_cell

# Ajoutez un autre callback pour afficher le contenu de la cellule active dans html.Div
@app.callback(
    Output('selected-cell-content', 'children'),
    Input('selected-cell-info', 'data')
)
def display_selected_cell_content(selected_cell_info):
    if selected_cell_info:
        row = selected_cell_info['row']
        col = selected_cell_info['column_id']
        cell_content = df.iloc[row + selected_cell_info['page_current'] * selected_cell_info['page_size']][col]
        return f"Contenu de la cellule ({row}, {col}): {cell_content}"
    else:
        return "Sélectionnez une cellule"

# Ajoutez un autre callback pour afficher l'histogramme en fonction de la cellule active
@app.callback(
    Output('station-usage-histogram', 'figure'),
    Input('selected-cell-info', 'data')
)
def display_station_usage_histogram(selected_cell_info):
    if selected_cell_info:
        row = selected_cell_info['row']
        station_name = df.iloc[row + selected_cell_info['page_current'] * selected_cell_info['page_size']]['Station_Name']
        
        # Filtrer les données pour la station sélectionnée
        station_data = df[df['Station_Name'] == station_name]
        
        # Créer un histogramme d'utilisation de la station
        fig = px.bar(station_data, x='Timestamp', y='Usage', title=f"Utilisation de la station {station_name}")
        
        # Mettez en forme l'histogramme
        fig.update_layout(
            xaxis_title='Timestamp',
            yaxis_title='Usage',
            yaxis_range=[0, 1]
        )
        
        return fig
    else:
        # Retourner une figure vide si aucune cellule n'est sélectionnée
        return {}

# Ajoutez un callback pour mettre à jour les statistiques par station en fonction du bouton de mise à jour
@app.callback(
    Output('station-stats-table', 'data'),
    Input('update-stats-button', 'n_clicks'),
    State('station-input', 'value')
)
def update_station_stats_table(n_clicks, station_name):
    try:
        df_stats_table = pd.DataFrame()
        df_stats_table[['Station_Name', 'Charge_Totale', 'Sur_Colline']] = None 
        if n_clicks > 0 and station_name:
            # Filtrer les données pour la station sélectionnée
            df_stats_table['Station_Name'] == str(station_name)
            # Calculer les statistiques
            df_stats_table['Charge_Totale'] = 0
            df_stats_table['Sur_Colline'] = False
            # df_stats_table['Sur_Colline'] = "Oui" if df['Sur_Colline'].any() else "Non"
            
            # # Retourner les statistiques sous forme de liste de dictionnaires
            return [{'Station_Name':  df_stats_table['Station_Name'], 
                     'Charge_Totale':  df_stats_table['Charge_Totale'], 
                     'Sur_Colline':  df_stats_table['Sur_Colline']}]
        # else:
        #     # Retourner une liste vide si le bouton n'a pas été cliqué ou si aucun nom de station n'est saisi
        #     return []
    except Exception as e:
        print(('error :'),e)

if __name__ == '__main__':
    app.run_server(debug=True)
