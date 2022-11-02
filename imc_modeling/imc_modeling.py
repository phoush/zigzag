import get_values as gv
import pandas as pd
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go



if __name__ == "__main__":

    t = gv.get_values("14sOT8JJPU9aHC3rwLHjFkLKOu9jYdaPon6qBTLBuOeU", "AIMC!A1:AK100")
    t = t[t['Include'] == 'Yes']
    t = t[(t['TOP/s/W'] != '') & (t['Input precision'] != '') & (t['Weight precision'] != '') & (t['Rows'] != '') & (t['Columns'] != '') & (t['Frequency (MHz)'] != '')]
    t = t[(t['Voltage (V)'] != '')]
    
    t = t.astype({'Voltage (V)':float, 'TOP/s/W':float, 'Input precision':float, 'Weight precision':float, 'Rows':int, 'Columns':int, 'Frequency (MHz)':float}) 
    t['TOPSW_1B'] = t['TOP/s/W'] / (t['Rows'] * t['Columns'] * 1e-6 / t['Frequency (MHz)'])
    t['TOPSW_1B'] = t['TOP/s/W'] / ( 1e-6 / t['Frequency (MHz)'])
    t['TOPSW_1B'] = t['TOPSW_1B'] / (t['Weight precision'])

    fig = make_subplots(rows=1, cols=1)
    colors = px.colors.qualitative.Plotly
    
    fig = px.scatter(t, x='TOP/s/W', y='TOPSW_1B', text='Idx', hover_data=['Idx', 'Frequency (MHz)', 'Voltage (V)', 'Input precision', 'Weight precision', 'Rows', 'Columns'], color='Technology node [nm]')
    #for ii_tn, tn in enumerate(t['Technology node [nm]'].unique()):
    #    tx = t[t['Technology node [nm]'] == tn]
    #    fig.add_trace(go.Scatter(x=tx['TOP/s/W'], y=tx['TOPSW_1B'], hovertext=tx['Idx'], marker=dict(color=colors[ii_tn]), mode='markers'), row=1, col=1)
    fig.show()
    print(t[['TOPSW_1B']])
    fig.write_html('modeling.html')
    pass
