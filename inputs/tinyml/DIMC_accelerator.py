import os
from classes.hardware.architecture.memory_hierarchy import MemoryHierarchy
from classes.hardware.architecture.memory_level import MemoryLevel
from classes.hardware.architecture.operational_unit import Multiplier, AIMC, DIMC
from classes.hardware.architecture.operational_array import MultiplierArray, AIMCArray, DIMCArray
from classes.hardware.architecture.memory_instance import MemoryInstance, MemoryInstanceClocked
from classes.hardware.architecture.accelerator import Accelerator
from classes.hardware.architecture.core import Core


def multiplier_array():
    """ Multiplier array variables """
    multiplier_input_precision = [8, 8]
    DIMC_unit_costs = {'vdd' : .8,
            'CORE_ROWS' : 8,
            'INPUT_BITS_PER_CYCLE': 4,
            'WEIGHT_BITCELL' : 8
            }

    DIMC_area = {'cell': 1, 'adder': 1, 'multiplier': 1}
    dimensions = {'D1': 8*6, 'D2':8*4, 'D3': 64*6}
    technology = 28
    imc_type = 'IMC'
    dimc = DIMC(multiplier_input_precision, DIMC_unit_costs, DIMC_area, technology, imc_type)
    dimc_array = DIMCArray(dimc, dimensions)
    return dimc_array




def memory_hierarchy(multiplier_array):
    """Memory hierarchy variables"""
    ''' size = #bit '''

    # 128MB SRAM
    L2_sram = MemoryInstance(name="L2", 
            size=64*2097152, 
            r_bw=8, w_bw=8, 
            r_cost=0, w_cost=0, 
            r_port = 1, w_port = 1, 
            area=0)
    

    # Input buffer
    input_buffer = MemoryInstance(name="input_buffer", 
            size=8, 
            r_bw=8, w_bw=8, 
            r_cost=0.030240000000000003, w_cost=0.030240000000000003, 
            r_port = 1, w_port = 1, 
            area=0) 

    # Output buffer
    output_buffer = MemoryInstance(name="output_buffer", 
            size=8, 
            r_bw=8, w_bw=8, 
            r_cost=0.030240000000000003, w_cost=0.030240000000000003, 
            r_port = 2, w_port = 2, 
            area=0) 

    # Create memory hierarchy graph object
    # Operational array has dimensions [128 x 16]
    memory_hierarchy_graph = MemoryHierarchy(operational_array=multiplier_array)

    # Add DIMC array weight_cell
#    memory_hierarchy_graph.add_memory(memory_instance=weight_cell, operands=('I1',), 
#            served_dimensions=set())
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
