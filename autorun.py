import re,pdb, os, csv
import pickle

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
#from get_values_sheet import *

## TODO: hardware setting for each paper
def fetch_setting(paper_idx, workload, voltage):
    gate_number_per_dff = 5
    if(paper_idx==1):
        setting = {
                "input_precision": 4,
                "weight_precision": 4,
                "output_precision": 4,
                "vdd": voltage,
                "D1": 256*4,
                "D2": 16*4,
                "technology": 22,
                "paper_idx": paper_idx,
                "workload": workload,
                "gate_number_per_dff": gate_number_per_dff, ## can set to any float number, >=0
                "core_row": 1,
                "input_bits_per_cycle": 1
                }
    elif(paper_idx==2):
        setting = {
                "input_precision": 4,
                "weight_precision": 4,
                "output_precision": 4,
                "vdd": voltage,
                "D1": 64*4,
                "D2": 64*4,
                "technology": 5,
                "paper_idx": paper_idx,
                "workload": workload,
                "gate_number_per_dff": gate_number_per_dff, ## can set to any float number, >=0
                "core_row": 4,
                "input_bits_per_cycle": 1
                }
    elif(paper_idx==3):
        setting = {
                "input_precision": 8,
                "weight_precision": 8,
                "output_precision": 8,
                "vdd": voltage,
                "D1": 4*8*8,
                "D2": 6*64,
                "technology": 28,
                "paper_idx": paper_idx,
                "workload": workload,
                "gate_number_per_dff": gate_number_per_dff, ## can set to any float number, >=0
                "core_row": 1,
                "input_bits_per_cycle": 2
                }
########################################
## inferred setting, no need to change
    setting["cgate"] = 0.02 * setting["technology"] + 0.196 ## Cgate formula. Also in classes/hardware/architecture/operational_unit.py, line 30
    print("technology node:", setting["technology"], ",Cgate:", setting["cgate"])
    setting["w_cost_weight_cell"] = setting["cgate"] * 0.5 * (setting["vdd"] **2)/1000 #w_cost for weight cell, unit: pJ
    setting["input_buffer_r_cost"]  = setting["cgate"] * setting["gate_number_per_dff"] * setting["input_precision"] * (setting["vdd"] **2)/1000 #r_cost for inupt buffer, unit: pJ
    setting["input_buffer_w_cost"]  = setting["cgate"] * setting["gate_number_per_dff"] * setting["input_precision"] * (setting["vdd"] **2)/1000
    setting["output_buffer_r_cost"] = setting["cgate"] * setting["gate_number_per_dff"] * setting["output_precision"] * (setting["vdd"] **2)/1000
    setting["output_buffer_w_cost"] = setting["cgate"] * setting["gate_number_per_dff"] * setting["output_precision"] * (setting["vdd"] **2)/1000
## inferred setting end
########################################
    return setting

## TODO: modify DIMC_accelerator.py
def mdy_dimc_accelerator(setting):
    pt_precision = 'multiplier_input_precision = (.*)'
    pt_vdd = 'vdd\' : (.*),'
    pt_core_rows = 'CORE_ROWS\' : (.*),'
    pt_input_bits_per_cycle = 'INPUT_BITS_PER_CYCLE\': (.*),'
    pt_weight_bitcell = 'WEIGHT_BITCELL\' : (.*)'
    pt_dimensions = 'dimensions = (.*)'
    pt_technology = 'technology = (.*)'
    pt_input_buffer = 'input_buffer'
    pt_output_buffer = 'output_buffer'
    pt_buffer_size = 'size(.*),'
    with open("inputs/DIMC_accelerator.py","r") as rd:
        con = rd.readlines()
    for i in range(0, len(con)):
        if(re.search(pt_precision, con[i])):# update input/weight precision
            con[i] = re.sub(pt_precision, 'multiplier_input_precision = [%s, %s]' %(setting['input_precision'], setting['weight_precision']), con[i])
        elif(re.search(pt_vdd, con[i])):# update vdd
            con[i] = re.sub(pt_vdd, 'vdd\' : %s,' %setting['vdd'], con[i])
        elif(re.search(pt_core_rows, con[i])):# update CORE_ROWS
            con[i] = re.sub(pt_core_rows, 'CORE_ROWS\' : %s,' %setting['core_row'], con[i])
        elif(re.search(pt_input_bits_per_cycle, con[i])):# update INPUT_BITS_PER_CYCLE
            con[i] = re.sub(pt_input_bits_per_cycle, 'INPUT_BITS_PER_CYCLE\': %s,' %setting['input_bits_per_cycle'], con[i])
        elif(re.search(pt_weight_bitcell, con[i])):# update WEIGHT_BITCELL
            con[i] = re.sub(pt_weight_bitcell, 'WEIGHT_BITCELL\' : %s' %setting['weight_precision'], con[i]) # weight bitcell, equal to weight precision for now
        elif(re.search(pt_dimensions, con[i])):# update D1/D2
            con[i] = re.sub(pt_dimensions, 'dimensions = {\'D1\': %s, \'D2\':%s}' %(setting['D1'],setting['D2']), con[i])
        elif(re.search(pt_technology, con[i])):# update technology
            con[i] = re.sub(pt_technology, 'technology = %s' %setting['technology'], con[i])
        elif(re.search(pt_input_buffer, con[i])):# update bitwidth, w/r_cost for input buffer
            con[i+1] = re.sub(pt_buffer_size, 'size=%s,' %setting['input_precision'], con[i+1])
            con[i+2] = re.sub('r_bw.*, w_bw.*,', 'r_bw=%s, w_bw=%s,' %(setting['input_precision'], setting["input_precision"]), con[i+2])
            con[i+3] = re.sub('r_cost.*, w_cost.*,', 'r_cost=%s, w_cost=%s,' %(setting['input_buffer_r_cost'], setting["input_buffer_w_cost"]), con[i+3])
        elif(re.search(pt_output_buffer, con[i])):# udpate bitwidth, w/r_cost for output buffer
            con[i+1] = re.sub(pt_buffer_size, 'size=%s,' %setting['output_precision'], con[i+1])
            con[i+2] = re.sub('r_bw.*, w_bw.*,', 'r_bw=%s, w_bw=%s,' %(setting['output_precision'], setting["output_precision"]), con[i+2])
            con[i+3] = re.sub('r_cost.*, w_cost.*,', 'r_cost=%s, w_cost=%s,' %(setting['output_buffer_r_cost'], setting["output_buffer_w_cost"]), con[i+3])
    with open("inputs/DIMC_accelerator.py", "w") as wr:
        for i in range(0, len(con)):
            wr.write(con[i])

## TODO: modify AIMC_accelerator.py
def mdy_aimc_accelerator(setting):
    pt_precision = 'multiplier_input_precision'
    pt_adc_enob = 'ADC_ENOB(.*),'
    pt_dac_res = 'DAC_RES(.*),'
    pt_weight_bitcell = 'WEIGHT_BITCELL(.*),'
    pt_bl_per_adc = 'BL_PER_ADC(.*)}'
    pt_dimensions = 'dimensions = (.*)'
    pt_technology = 'technology = (.*)'
    pt_input_buffer = 'input_buffer'
    pt_output_buffer = 'output_buffer'
    pt_buffer_size = 'size(.*),'
    with open("inputs/AIMC_accelerator.py","r") as rd:
        con = rd.readlines()
    for i in range(0, len(con)):
        if(re.search(pt_precision, con[i])):
            re.sub(pt_precision, 'multiplier_input_precision = [%s, %s]' %(setting["input_precision"], setting["weight_precision"]), con[i])
        elif(re.search(pt_adc_enob, con[i])):
            re.sub(pt_adc_enob, 'ADC_ENOB\' : %s,' %setting["adc_enob"], con[i])
        elif(re.search(pt_dac_res, con[i])):
            re.sub(pt_dac_res, 'DAC_RES\' : %s,' %setting["dac_res"], con[i])
        elif(re.search(pt_weight_bitcell, con[i])):
            re.sub(pt_weight_bitcell, 'WEIGHT_BITCELL\' : %s,' %setting["weight_precision"], con[i])
        elif(re.search(pt_bl_per_adc, con[i])):
            re.sub(pt_bl_per_adc, 'BL_PER_ADC\' : %s}' %setting["bl_per_adc"], con[i])
        elif(re.search(pt_dimensions, con[i])):# update D1/D2
            con[i] = re.sub(pt_dimensions, 'dimensions = {\'D1\': %s, \'D2\':%s}' %(setting['D1'],setting['D2']), con[i])
        elif(re.search(pt_technology, con[i])):# update technology
            con[i] = re.sub(pt_technology, 'technology = %s' %setting['technology'], con[i])
        elif(re.search(pt_input_buffer, con[i])):# update bitwidth, w/r_cost for input buffer
            con[i+1] = re.sub(pt_buffer_size, 'size=%s,' %setting['input_precision'], con[i+1])
            con[i+2] = re.sub('r_bw.*, w_bw.*,', 'r_bw=%s, w_bw=%s,' %(setting['input_precision'], setting["input_precision"]), con[i+2])
            con[i+3] = re.sub('r_cost.*, w_cost.*,', 'r_cost=%s, w_cost=%s,' %(setting['input_buffer_r_cost'], setting["input_buffer_w_cost"]), con[i+3])
        elif(re.search(pt_output_buffer, con[i])):# udpate bitwidth, w/r_cost for output buffer
            con[i+1] = re.sub(pt_buffer_size, 'size=%s,' %setting['output_precision'], con[i+1])
            con[i+2] = re.sub('r_bw.*, w_bw.*,', 'r_bw=%s, w_bw=%s,' %(setting['output_precision'], setting["output_precision"]), con[i+2])
            con[i+3] = re.sub('r_cost.*, w_cost.*,', 'r_cost=%s, w_cost=%s,' %(setting['output_buffer_r_cost'], setting["output_buffer_w_cost"]), con[i+3])
    with open("inputs/AIMC_accelerator.py", "w") as wr:
        for i in range(0, len(con)):
            wr.write(con[i])

## TODO: modify default_mapping.py
def mdy_default_mapping(setting):
    pt_operand_precision = "operand_precision(.*),"
    with open("inputs/default_mapping.py","r") as rd:
        con = rd.readlines()
    for i in range(0, len(con)):
        if(re.search(pt_operand_precision, con[i])):
                con[i] = re.sub(pt_operand_precision, 'operand_precision\': {\'O\': %s, \'O_final\': %s, \'W\': %s, \'I\': %s},' %(setting['output_precision'],setting['output_precision'], setting['weight_precision'],setting['input_precision']), con[i])
    with open("inputs/default_mapping.py","w") as wr:
        for i in range(0, len(con)):
            wr.write(con[i])

## TODO: modify memory_hierarchy.py, line 44
def mdy_memory_hierarchy(setting):
    pt_w_cost = 'w_cost=(.*),'
    with open("classes/hardware/architecture/memory_hierarchy.py","r") as rd:
        con = rd.readlines()
    for i in range(0, len(con)):
        if(re.search(pt_w_cost, con[i])):
                con[i] = re.sub(pt_w_cost, 'w_cost=%s,' %(setting['w_cost_weight_cell']), con[i])
    with open("classes/hardware/architecture/memory_hierarchy.py","w") as wr:
        for i in range(0, len(con)):
            wr.write(con[i])

##TODO: modify main_onnx.py
def mdy_main_onnx(setting):
    pt_filename = 'outputs/(.*).json'
    with open("main_onnx.py","r") as fp:
        con = fp.readlines()
    for i in range(0, len(con)):
        if(re.search(pt_filename, con[i])):
            con[i] = re.sub(pt_filename, 'outputs/%s-%s-%s-{layer}-{datetime}.json' %(setting["paper_idx"], setting["vdd"], setting["workload"]), con[i])
    with open("main_onnx.py","w") as fp:
        for i in range(0, len(con)):
            fp.write(con[i])
##TODO: fetch single output data
def fetch_single_output_data(paper_idx, workload, voltage, filename):
    list_data = []
    setting = fetch_setting(paper_idx, workload, voltage)
    res = {
        'paper_idx': paper_idx,
        'voltage': voltage,
        'workload': workload,
        'cgate': setting['cgate']
            }
    ##for simplicity
    if(workload=='mobilenet_v1'): res['workload']='mb_v1'
    if(workload=='deepautoencoder'): res['workload']='deepae'
    pt_loop_dimensions = 'loop_dimensions'
    pt_energy_total = '"energy_total":'
    pt_precharging_cell = '"precharging_cell":'
    pt_multiplication_energy = '"multiplication_energy":'
    pt_accumulation_energy = '"accumulation_energy":'
    pt_memory_energy = '"memory_energy":'
    pt_energy_breakdown_per_level = '"energy_breakdown_per_level":'
    pt_utilization = '"utilization":'
    pt_latency = '"latency":'
    res['layer_node'] = filename.split('-')[3]
    with open("outputs/%s" %filename,"r", encoding='utf8') as fp:
        print(f"fetching data from: {filename}")
        con = fp.readlines()
    for j in range(0, len(con)):
        ## locate dimension parameters
        if(re.search(pt_loop_dimensions, con[j])):
            ## start cal #MAC
            mac_number = 1
            for k in range(j+1,len(con)-j):
                if(not re.search('}',con[k])):
                    if(con[k].rstrip("\n").endswith(",")):
                        mac_number *= int((con[k].split()[-1]).split(',')[-2])
                    else:
                        mac_number *= int(con[k].split()[-1])
                else:
                    break
            ##aleady get #MAC here
            res['mac_number'] = mac_number
        elif(re.search(pt_energy_total, con[j])):
            res['Etotal'] = str(round(float((con[j].split()[-1]).split(',')[-2]),3))
            res['E_per_mac'] = str(round( float(res['Etotal'])/mac_number, 3))
        elif(re.search(pt_precharging_cell, con[j])):
            res['Ewlbl'] = str(round(float((con[j].split()[-1]).split(',')[-2]),3))
        elif(re.search(pt_multiplication_energy, con[j])):
            res['Emul'] = str(round(float((con[j].split()[-1]).split(',')[-2]),3))
        elif(re.search(pt_accumulation_energy, con[j])):
            res['Eadder'] = str(round(float(con[j].split()[-1]),3))
        elif(re.search(pt_memory_energy, con[j])):
            res['Emem'] = str(round(float((con[j].split()[-1]).split(',')[-2]),3))
        ## fetch memory energy breakdown
        elif(re.search(pt_energy_breakdown_per_level, con[j])):
            res['Emem_O'] = str(round(float((con[j+2].split()[-1]).split(',')[-2]),3))
            res['Emem_W'] = str(round(float((con[j+6].split()[-1]).split(',')[-2]),3))
            res['Emem_I'] = str(round(float((con[j+10].split()[-1]).split(',')[-2]),3))
        ## fetch utilization for i/w/o buffer
        elif(re.search(pt_utilization, con[j])):
            res['utilization_O'] = (con[j+2].split()[-1]).split(',')[-2]
            res['utilization_W'] = (con[j+6].split()[-1]).split(',')[-2]
            res['utilization_I'] = (con[j+10].split()[-1]).split(',')[-2]
        ## fetch latency
        elif(re.search(pt_latency, con[j])):
            res['latency_wo_onload_wo_offload'] = (con[j+1].split()[-1]).split(',')[-2]
            res['latency_w_onload_wo_offload'] = (con[j+2].split()[-1]).split(',')[-2]
            res['latency_w_onload_w_offload'] = con[j+3].split()[-1]
    #with open('data_energy_output.txt', 'a') as fp:
    #    con = f"{res['paper_idx']:<5}\t{res['voltage']:>5}\t{res['workload']:>7}\t{res['cgate']:>7}\t{res['energy_per_mac']:>5}\t{res['layer_node']:>15}\t{res['mac_number']:>10}\t{res['total_energy']:>10}\t{res['precharging_cell']:>10}\t{res['multiplication_energy']:>10}\t{res['accumulation_energy']:>10}\t{res['memory_energy']:>10}\t{res['memory_energy_breakdown_O']:>10}\t{res['memory_energy_breakdown_W']:>10}\t{res['memory_energy_breakdown_I']:>10}\n"
    #    fp.write( con )
    return res


##TODO: fetch all output data
def fetch_all_output_data(design_deck):
    csv_file = "data_output.csv"
    csv_columns = ["paper_idx","voltage","workload","cgate","E_per_mac","layer_node","mac_number","Etotal","Ewlbl","Emul","Eadder","Emem","Emem_O","Emem_W","Emem_I",'utilization_O','utilization_W','utilization_I','latency_wo_onload_wo_offload','latency_w_onload_wo_offload','latency_w_onload_w_offload']
    dict_data = []
    #with open('data_energy_output.txt', 'w') as fp:
    #    con = "{0:<5}\t{1:>5}\t{2:>7}\t{3:>7}\t{4:>5}\t{5:>15}\t{6:>10}\t{7:>10}\t{8:>10}\t{9:>10}\t{10:>10}\t{11:>10}\t{12:>10}\t{13:>10}\t{14:>10}\n".format("idx","voltage","wkload","Cgate","E/MAC","layer_node","#MAC","Etotal","Ewlbl","Emul","Eadder","Emem","Emem_O","Emem_W","Emem_I","utilization_O","utilization_W","utilization_I")
    #    fp.write(con)
    for paper_idx in design_deck["paper_idx"]:
        for workload in design_deck["workload"]:
            for voltage in design_deck["voltage"]:
                files=os.listdir("outputs")
                pt_out_filename = '%s-%s-%s-(.*)-(.*).json' %(paper_idx, voltage, workload)
                for i in range(0,len(files)):
                    ## locate specific output report
                    if(re.search(pt_out_filename, files[i])):
                        dict_data.append( fetch_single_output_data(paper_idx, workload, voltage, files[i]) )# save each result in list
    # save data into csv file
    with open(csv_file, 'w') as fp:
        #csv_columns = dict_data[0].keys()
        writer = csv.DictWriter(fp, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
    # save data into pickle file. Is a dictionary
    data = pd.read_csv(csv_file)
    with open('data_output.pickle', 'wb') as infile:
        pickle.dump(data, infile)
    pass


########################################
## AIMC setting
#
#setting["adc_enob"] = setting["output_precision"] # partial sum precision, set to output_precision for now.
#setting["dac_res"] = 1 # DAC input precision (#bits/cycle per DAC). (#cycle number) inferred from here.
#setting["bl_per_adc"] = 1 # (#bitlines/ADC), set to 1 for now
#
## AIMC setting end
########################################


########################################
def single_design_validate(paper_idx, workload, voltage):
    setting = fetch_setting(paper_idx, workload, voltage)
    mdy_dimc_accelerator(setting)
    mdy_default_mapping(setting)
    mdy_memory_hierarchy(setting)
    mdy_main_onnx(setting)
    os.system("echo ###########################")
    os.system("python main_onnx.py --model onnx_workload/{workload}/{workload}_inferred_model.onnx --accelerator inputs.DIMC_accelerator --mapping inputs.default_mapping".format(workload=workload)) ## for DIMC
########################################



def all_design_validate(design_deck):
    os.system("rm -rf outputs/*")
    for paper_idx in design_deck["paper_idx"]:
        for workload in design_deck["workload"]:
            for voltage in design_deck["voltage"]:
                single_design_validate(paper_idx, workload, voltage)
########################################
#def dimc_validation_plot():
#    color = ['violet', 'orange', 'steelblue', 'palevioletred']
#    #table = get_values("14sOT8JJPU9aHC3rwLHjFkLKOu9jYdaPon6qBTLBuOeU", "AIMC model!A1:AX27")
#
#    plt.rcParams['text.usetex'] = True
#    x = table['Model / Paper'].values.tolist()
#    y = table['fJ/MAC'].values.tolist()
#    y2 = table['Total'].values.tolist()
#    n = table['Idx'].values.tolist()
#    x = [f'{abs(eval(xx))}\%' for xx in x]
#    y = [eval(yy) for yy in y]
#    y2 = [eval(yy) for yy in y2]
#    nx = np.array([nn for nn,_ in enumerate(n)])
#    n = [f'[{n}]' for n in n]
#    
#    plt.rcParams['figure.figsize'] = (20, 5)
#    plt.grid(visible=True, which='major', axis='y')
#    plt.bar(nx-0.2, y, width = 0.3, color=color[2], label='fJ/MAC reported')  
#    plt.bar(nx+0.2, y2, width = 0.3, color=color[3], label='fJ/MAC estimated')  
#    plt.legend(fontsize=15,loc='lower right')
#    plt.yscale('log')
#    plt.xticks(ticks=nx, labels=n, fontsize=12)
#    plt.yticks(fontsize=12)
#    plt.xlabel('Design', size=15)
#    plt.ylabel('fJ / MAC', size=15)
#    for i, nn in enumerate(x):
#        plt.annotate(nn, (nx[i], max(y[i], y2[i])*1.2), ha='center', size=12)
#    plt.tight_layout()
#    plt.show()
#
########################################
design_deck = {
    "paper_idx": [1,2,3],
    "workload": ["resnet8","mobilenet_v1","ds_cnn","deepautoencoder"],
    "voltage": [eval('v/10') for v in range(5,11,1)]
        }
#rdata=pd.read_pickle('data_output.pickle')

#all_design_validate(design_deck)
fetch_all_output_data(design_deck)
#dimc_validation_plot()
