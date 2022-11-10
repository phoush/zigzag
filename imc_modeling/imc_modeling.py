import get_values as gv
import pandas as pd
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pdb


def aimc_model():
    # Fetch data from google sheets
    t = gv.get_values("14sOT8JJPU9aHC3rwLHjFkLKOu9jYdaPon6qBTLBuOeU", "AIMC_zimmer!A1:AK100")
    
    # Include only the rows that have cell value equal to 'Yes' in column 'Include'
    t = t[t['Include'] == 'Yes']

    # Remove rows that have empty cells in specfic columns
    #t = t[(t['TOP/s/W'] != '') & (t['Output precision'] != '') & (t['Input precision'] != '') & (t['Weight precision'] != '') & (t['Rows'] != '') & (t['Columns'] != '') & (t['Frequency (MHz)'] != '')]
    t = t[(t['TOP/s/W'] != '') & (t['Output precision'] != '') & (t['Input precision'] != '') & (t['Weight precision'] != '') & (t['Rows'] != '') & (t['Columns'] != '')]
    t = t[(t['Voltage (V)'] != '')]
    
    # Convert value in specific columns from string to float/int
    #t = t.astype({'Idx': int, 'Technology node [nm]':int, 'Voltage (V)':float, 'TOP/s/W':float, 'Output precision': float, 'Input precision':float, 'Weight precision':float, 'Rows':int, 'Columns':int, 'Frequency (MHz)':float}) 
    t = t.astype({'Idx': int, 'Div factor' : float, 'Voltage (V)': float, 'TOP/s/W':float, 'Weight precision': float, 'Input precision': float, 'Output precision': float, 'Rows':int, 'Columns':int}) 
   


    # Zimmer model from 10.1145/3316781.3317770
    t['Eadc_zimmer'] = 0
    #t = t.assign(Eadc_zimmer=lambda x: np.power(10, 0.1 * (6.02 * (x['Output precision'] - 68.25)))*1e-12 if x['Output precision'] > 10.5 else 0.3)
    t['Eadc_zimmer'] = np.where(t['Output precision'] > 10.5, np.power(10, 0.1 * (6.02 * t['Output precision'] - 68.25))*1e-12, np.where(t['Output precision'] < 10.5, 0.3e-12, 0))
    # t['Emac_zimmer'] = (1/(t['Rows'] * t['Input precision'] * t['Weight precision'])) * t['Eadc_zimmer']
    t['Emac_zimmer'] = (1/(t['Rows'] )) * t['Eadc_zimmer']

     # Murmann ADC model from 10.1109/TVLSI.2020.3020286 
    t['Eadc_murmann'] = 0
    #t = t.assign(Eadc_zimmer=lambda x: np.power(10, 0.1 * (6.02 * (x['Output precision'] - 68.25)))*1e-12 if x['Output precision'] > 10.5 else 0.3)
    activity_cell = 1
    def get_cap_cell(x):
        cap_cell = {'28':0.5e-15, '16':0.2e-15, '65':0.5e-15, '12':0.5e-15, '22':0.6e-15, '7':0.5e-15, '55':0.5e-15, '180':0.5e-15, '45':0.5e-15, '0': 0.5e-15}
        cap_cell = {'28':0.5e-15, '16':0.2e-15, '65':0.5e-15, '12':0.5e-15, '22':0.6e-15, '7':0.5e-15, '55':0.5e-15, '180':0.5e-15, '45':0.5e-15, '0': 0.5e-15}
        return cap_cell[x]
    def get_adc_conv(x):
        adc_conv_step = {'28':0.1e-12, '16':0.1e-12, '65':0.1e-12, '12':0.1e-12, '22':0.3e-12/6, '7':0.1e-12, '55':0.1e-12, '180':0.1e-12, '45':0.1e-12, '0': 0.1e-12}
        return adc_conv_step[x]


    t['Eadc_conv_step'] = t['Technology node [nm]']
    t['Eadc_conv_step'] = t['Eadc_conv_step'].apply(get_adc_conv)

    t['Eadc_murmann'] = t['Eadc_conv_step'] * t['Output precision'] + 1e-18 * np.power(4, t['Output precision'])
    t['Unit capacitance'] = t['Technology node [nm]']
    t['Unit capacitance'] = t["Unit capacitance"].apply(get_cap_cell)
    t['Ecap_murmann'] = activity_cell * t['Unit capacitance'] * np.power(t['Voltage (V)'], 2) * np.power(t['Weight precision'], 1)
    t['Elogic_murmann'] = 0.1 * 0.3e-15 * np.power(t['Weight precision'], 1) * 4
    t['Emac_murmann'] = (1/(t['Rows'] )) * t['Eadc_murmann']
    # Compute TOPSW/1B
    t['TOPSW_zimmer'] = 1/ t['Emac_zimmer'] / 1e12
    t['TOPSW_murmann'] = 1/ (t['Elogic_murmann'] + t['Emac_murmann'] + t['Ecap_murmann']) / t['Div factor'] /  1e12
    t['Zimmer_diff'] = t['TOPSW_zimmer'] / t['TOP/s/W']
    t['Murmann_diff'] = t['TOPSW_murmann'] / t['TOP/s/W']
    #t['TOPSW_1B'] = t['TOPSW_1B'] * (t['Technology node [nm]'])
    

    fig = make_subplots(rows=1, cols=2)
    colors = px.colors.qualitative.Plotly
    scatter_labels, topsw_paper, topsw_zimmer, topsw_murmann = [], [], [], []
    for i,r in t.iterrows():
        #scatter_labels.append(f'{r.Rows}x{r.Columns}')
        scatter_labels.append(f'{r["Technology node [nm]"]}')
        topsw_paper.append(r["TOP/s/W"])
        topsw_zimmer.append(r["TOPSW_zimmer"])
        topsw_murmann.append(r["TOPSW_murmann"])

    t['Technology node [nm]'] = t['Technology node [nm]'].astype(str) 
    fig.add_trace(go.Scatter(x=t['Idx'], y=t['TOP/s/W'],mode='markers', name='TOPS/W Paper'))
    fig.add_trace(go.Scatter(x=t['Idx'], y=t['TOPSW_zimmer'],mode='markers+text',text=scatter_labels, name='TOPS/W Zimmer'), row=1,col=1)
    fig.add_trace(go.Scatter(x=t['Idx'], y=t['TOPSW_murmann'],mode='markers+text',text=scatter_labels, name='TOPS/W murmann'), row=1,col=1)
#    fig.add_trace(go.Scatter(x=t['Idx'], y=t['Zimmer_diff'],mode='markers+text',text=scatter_labels, name='Zimmer / Paper', 
#        customdata=np.stack((topsw_paper, topsw_zimmer), axis=-1), hovertemplate='x:%{x}<br>y:%{y}<br>%{text}<br>TOPs/W paper %{customdata[0]:.2f}<br>TOPs/W Zimmer %{customdata[1]:.2f}'), row=1,col=2)
    fig.add_trace(go.Scatter(x=t['Idx'], y=t['Murmann_diff'],mode='markers+text',text=scatter_labels, name='Murmann / Paper', 
        customdata=np.stack((topsw_paper, topsw_murmann), axis=-1), hovertemplate='x:%{x}<br>y:%{y}<br>%{text}<br>TOPs/W paper %{customdata[0]:.2f}<br>TOPs/W Murmann %{customdata[1]:.2f}'), row=1, col=2)
    fig.update_yaxes(type='log')
    fig.show()
#    fig.write_html('modeling.html')


if __name__ == "__main__":
    aimc_model()
    pass
