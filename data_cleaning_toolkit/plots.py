import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pandas as pd 
from scripts.utils import tools

colors_cfg = {
'Pastel Lavender': ['#E6E6FA',	(230, 230, 250)],
'Pastel Blue': ['#AEC6CF',	(174, 198, 207)],
'Pastel Green': ['#77DD77',	(119, 221, 119)],
'Pastel Pink': ['#FFB3BA',	(255, 179, 186)],
'Pastel Yellow': ['#FDFD96',	(253, 253, 150)],
'Pastel Purple': ['#CBAACB',	(203, 170, 203)],
'Pastel Orange': ['#FFB347',	(255, 179, 71)],
'Pastel Red': ['#FF6961',	(255, 105, 97)],
'Pastel Mint': ['#AAF0D1',	(170, 240, 209)],
'Pastel Peach': ['#FFDAB9',	(255, 218, 185)],
}




def plot_plots(df:pd.DataFrame, x_axis=None, y_axis=None, colors:list=None, title=None, darkmode=True):
    types = {'line':[np.int_, np.float64],
             'bar':[object, str]}
    traces = []
    colors = tools.either(colors, colors_cfg)
    
    for n,column in enumerate(df):
        color_names = list(colors.keys())
        color = colors[color_names[n]][0] if n in range(0,10) else colors[color_names[10-n]][0]

        if df[column].dtype in types['line']:
            trace = {'x':tools.either(df.index, x_axis),
                     'y':df[column],
                     'type':'scatter',
                     'mode':'lines',
                     'name':column,
                     'line':{'color':tools.either(color, 'blue')}}
        elif df[column].dtype in types['bar']:
            trace = {'x':tools.either(df.index, x_axis),
                     'y':df[column],
                     'type':'bar',
                     'marker':dict(color=color),
                     'name':column,
                     'line':{'color':tools.either(color, 'blue')}}
        else:
            pass
        if 'trace' in locals():
            traces.append(trace)
    
    if not traces:
        return None
    layout_lines = go.Layout(title=dict(text=tools.either(title, 'Plot Title'),
                                        font= {"color": "white"} if darkmode else None,
                                        y= 0.9,                   # Vertical position (0 = bottom, 1 = top)
                                        x= 0.5,                   # Horizontal position (0 = left, 1 = right)
                                        xanchor= "center",        # Anchor for the title position
                                        yanchor= "top"),
                             barmode='group',
                             barcornerradius=2.5,
                             bargap=0.2,
                             xaxis=dict(title='',
                                        tickfont={'color':'white'} if darkmode else None),
                            yaxis=dict(tickfont={'color':'white'} if darkmode else None),
                             legend=dict(orientation='h',
                                         font= {"color": "white"} if darkmode else None
                                        #  xanchor='center',
                                        #  yanchor='bottom',
                                        #  y=0.8
                                         ),
                            plot_bgcolor='rgb(17,17,17)' if darkmode else None,
                            paper_bgcolor ='rgb(10,10,10)' if darkmode else None,
                             )
    
    fig = go.Figure(data=traces, layout=layout_lines)
    fig.show()

