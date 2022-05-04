import dash
import plotly.graph_objs as go 
from dash import dcc
from dash import html
import pandas as pd
from .get_data_prix import load_df

class Prix():
    def __init__(self, application = None):

        self.df_beer, self.df_wine, self.df_spirits = load_df()

        self.data = dict(
        type = 'choropleth',
        locationmode = 'country names',
        ) 

        self.layout = dict(
            geo = dict(
            showframe = False,
            projection = {'type':'natural earth'}
            )
        )


        self.main_layout = html.Div(children=[
            html.H3(children='Prix des alcools face aux revenus'),
            html.Div([ dcc.Graph(id='pla-main-graph'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='pla-type', 
                                     options=[{'label':'Bières', 'value':0},
                                              {'label':'Vins', 'value':1},
                                              {'label':'Spiritueux', 'value':2},], 
                                     value=0,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Br(),
            dcc.Markdown("""
            Cette carte montre le prix d'un alcool (bière, vin ou spiritueux) comparativement au PIB par habitant.
            * Les données les plus complètes concernent le prix des bières, probablement car c'est la boisson alcolisée la plus populaire tandis que le vin et les spiritueux ne sont mêmes pas recensés dans certains pays africains et du Moyen-Orient, sûrement dû à des différences culturelles.
            * Les données manquantes dans certains pays peuvent aussi s'expliquer par la situation politique de certains pays en guerre comme le Soudan.
            * Les régions où la bière est la plus chère sont l'Afrique et le Moyen-Orient. En Afrique, cela peut s'expliquer par un PIB par habitant bien plus faible par rapport au reste du monde.
            * Les disparités les plus importantes concernent le prix des spiritueux. Alors qu'ils représentent moins de 0.1% du PIB dans les pays de l'hémisphère Nord, ils peuvent être deux à trois fois plus cher dans d'autres pays plus modestes comme le Nicaragua, le Kenya ou encore l'Indonésie.
            #### À propos
            * Sources : [Observatoire mondial de la Santé](https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/economic-aspects)
            * (c) 2022 Vincent Courty, Luca Moorghen
            """)
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
             }
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                    dash.dependencies.Output('pla-main-graph', 'figure'),
                    dash.dependencies.Input('pla-type', 'value'))(self.update_graph)

    def update_graph(self, mean):
        if mean == 0:
            self.change_df(self.df_beer)
        elif mean == 1:
            self.change_df(self.df_wine)
        elif mean == 2:
            self.change_df(self.df_spirits)

        choromap = go.Figure(data = [self.data],layout = self.layout)
        choromap.update_layout(margin=dict(l=0, r=0, t=50, b=0, autoexpand=True))
        return choromap

    def change_df(self, dfg):

        self.data['locations'] = dfg['pays']
        self.data['z'] = dfg['ratio']
        self.data['text'] = dfg['pays']
        self.data['colorbar'] = {'title' : 'Prix de l\'alcool par rapport au PIB'}
        
if __name__ == '__main__':
    prx = Prix()
    prx.app.run_server(debug=True, port=8051)
