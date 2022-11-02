import get_values as gv
import pandas as pd
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go



if __name__ == "__main__":
    # Fetch data from google sheets
    t = gv.get_values("14sOT8JJPU9aHC3rwLHjFkLKOu9jYdaPon6qBTLBuOeU", "AIMC!A1:AK100")
    
    # Include only the rows that have cell value equal to 'Yes' in column 'Include'
    t = t[t['Include'] == 'Yes']

    # Remove rows that have empty cells in specfic columns
    t = t[(t['TOP/s/W'] != '') & (t['Input precision'] != '') & (t['Weight precision'] != '') & (t['Rows'] != '') & (t['Columns'] != '') & (t['Frequency (MHz)'] != '')]
    t = t[(t['Voltage (V)'] != '')]
    
    # Convert value in specific columns from string to float/int
    t = t.astype({'Technology node [nm]':int, 'Voltage (V)':float, 'TOP/s/W':float, 'Input precision':float, 'Weight precision':float, 'Rows':int, 'Columns':int, 'Frequency (MHz)':float}) 
    
    # Compute TOPSW/1B
    t['TOPSW_1B'] = t['TOP/s/W'] / (t['Rows'] * t['Columns'] * 1e-6 / t['Frequency (MHz)'])
    t['TOPSW_1B'] = t['TOP/s/W'] / ( 1e-6 / t['Frequency (MHz)'])
    #t['TOPSW_1B'] = t['TOPSW_1B'] * (t['Technology node [nm]'])

    fig = make_subplots(rows=1, cols=1)
    colors = px.colors.qualitative.Plotly
    
    t['Technology node [nm]'] = t['Technology node [nm]'].astype(str) 
    fig = px.scatter(t, x='TOP/s/W', y='TOPSW_1B', text='Idx', hover_data=['Idx', 'Frequency (MHz)', 'Voltage (V)', 'Input precision', 'Weight precision', 'Rows', 'Columns'], color='Technology node [nm]')
    fig.show()
    fig.write_html('modeling.html')
    pass
