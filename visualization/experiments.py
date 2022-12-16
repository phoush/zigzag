import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import json
import os
import pandas as pd

def plot_energy_breakdown():

    dict_data = []
    for accel in ['dimc', 'aimc', 'aimc_dimc']:
        dir_list = ['../outputs/'+accel+'/mobilenet', '../outputs/'+accel+'/resnet8', '../outputs/'+accel+'/ds-cnn', '../outputs/'+accel+'/ae']
        workload = ['mobilenet', 'resnet8', 'ds-cnn', 'autoencoder']
        for ii_d, directory in enumerate(dir_list):
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".json"):
                    layer_index = filename.split("-")
                    layer_index = layer_index[0].split("_")
                    layer_index = eval(layer_index[1])
                    with open(directory + '/' + filename) as infile:
                        values = json.load(infile)
                    for energy_type, energy_val in values['outputs']['energy']['operational_energy_breakdown'].items():
                        dict_data.append({})
                        dict_data[-1]['workload'] = workload[ii_d]
                        dict_data[-1]['layer'] = layer_index
                        dict_data[-1]['energy'] = energy_val
                        dict_data[-1]['type'] = energy_type
                        dict_data[-1]['accelerator'] = accel
                    for energy_type, energy_val in values['outputs']['energy']['energy_breakdown_per_level'].items():
                        dict_data.append({})
                        dict_data[-1]['workload'] = workload[ii_d]
                        dict_data[-1]['layer'] = layer_index
                        dict_data[-1]['energy'] = energy_val[0]
                        dict_data[-1]['type'] = energy_type
                        dict_data[-1]['accelerator'] = accel

    df = pd.DataFrame(dict_data)
    
    df.sort_values(by=['layer'], ignore_index=True, ascending=True, inplace=True)
    #fig = px.bar(df[df.accelerator == 'aimc'], x='layer', y='energy', color='type', facet_row='workload')
    #fig.show()

    df = df.groupby(['workload', 'type', 'accelerator']).agg({'energy': 'sum'})
    df = df.reset_index()
    fig = px.bar(df, x='accelerator', y='energy', color='type', facet_col='workload', log_y=False)
    fig.update_yaxes(matches=None)
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
    fig.update_traces(textfont_size=24)
    fig.show()

if __name__ == "__main__":
    plot_energy_breakdown()
    pass
