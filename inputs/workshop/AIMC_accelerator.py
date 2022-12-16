import os
from classes.hardware.architecture.memory_hierarchy import MemoryHierarchy
from classes.hardware.architecture.memory_level import MemoryLevel
from classes.hardware.architecture.operational_unit import Multiplier, AIMC
from classes.hardware.architecture.operational_array import MultiplierArray, AIMCArray
from classes.hardware.architecture.memory_instance import MemoryInstance, MemoryInstanceClocked
from classes.hardware.architecture.accelerator import Accelerator
from classes.hardware.architecture.core import Core


def multiplier_array():
    AIMC_unit_costs = {'vdd' : 0.8, 
            'ADC_RES' : 4, 
            'DAC_RES' : 4, 
            'WEIGHT_BITCELL' : 4, 
            'mac_clock_domain' :1,
            'BL_PER_ADC': 1} 

    AIMC_area = {'cell': 1, 'ADC': 1, 'DAC': 1}
    dimensions = {'D1': 512, 'D2':1152, 'D3':4}
    technology = 28
    aimc = AIMC([0,0], AIMC_unit_costs, AIMC_area, technology)
    aimc_array = AIMCArray(aimc, dimensions)
    return aimc_array


def memory_hierarchy(multiplier_array):
    """Memory hierarchy variables"""
    ''' size = #bit '''
    L2_sram = MemoryInstance(name="L2", 
            size=64*2097152, 
            r_bw=512, w_bw=512, 
            r_cost=0, w_cost=0, 
            r_port = 1, w_port = 1, 
            area=0)
    

    # Input buffer
    input_buffer = MemoryInstance(name="input_buffer", 
            size=4, 
            r_bw=4, w_bw=4, 
            r_cost=0.03, w_cost=0.03, 
            r_port = 1, w_port = 1, 
            area=0) 

    # Output buffer
    output_buffer = MemoryInstance(name="output_buffer", 
            size=4, 
            r_bw=4, w_bw=4, 
            r_cost=0.03, w_cost=0.03, 
            r_port = 2, w_port = 2, 
            area=0) 

    # Create memory hierarchy graph object
    memory_hierarchy_graph = MemoryHierarchy(operational_array=multiplier_array)

    # Add DIMC array weight_cell
    # Add Input buffer
    memory_hierarchy_graph.add_memory(memory_instance=input_buffer, operands=('I2',), 
            served_dimensions={(1,0,0)})
    # Add output buffer
    memory_hierarchy_graph.add_memory(memory_instance=output_buffer, operands=('O',), 
            port_alloc=({'fh':'w_port_1', 'fl': 'w_port_2', 'th': 'r_port_1', 'tl': 'r_port_2'},), 
            served_dimensions={(0,1,0)})
    # Add L2 memory
    memory_hierarchy_graph.add_memory(memory_instance=L2_sram, operands=('I1','I2','O',), 
            served_dimensions='all')


    return memory_hierarchy_graph



def cores():
    multiplier_array1 = multiplier_array()
    memory_hierarchy1 = memory_hierarchy(multiplier_array1)
    core1 = Core(1, multiplier_array1, memory_hierarchy1)
    return {core1}


acc_name = "MyAccelerator"
acc_cores = cores()
global_buffer = None
accelerator = Accelerator(acc_name, acc_cores, global_buffer)

a = 1
