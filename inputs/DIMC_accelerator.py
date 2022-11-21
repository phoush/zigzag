import os
from classes.hardware.architecture.memory_hierarchy import MemoryHierarchy
from classes.hardware.architecture.memory_level import MemoryLevel
from classes.hardware.architecture.operational_unit import Multiplier, AIMC
from classes.hardware.architecture.operational_array import MultiplierArray, AIMCArray
from classes.hardware.architecture.memory_instance import MemoryInstance, MemoryInstanceClocked
from classes.hardware.architecture.accelerator import Accelerator
from classes.hardware.architecture.core import Core


def multiplier_array():
    """ Multiplier array variables """
    multiplier_input_precision = [8, 8]
    multiplier_energy = {'MAC_8b' : 0.08}
    multiplier_area = {'MAC_unit': 1}
    dimensions = {'D1': 128, 'D2': 16}

    multiplier = Multiplier(multiplier_input_precision, multiplier_energy, multiplier_area)
    multiplier_array = MultiplierArray(multiplier, dimensions)

    return multiplier_array



def memory_hierarchy(multiplier_array):
    """Memory hierarchy variables"""
    ''' size = #bit '''

    # 128MB SRAM
    L2_sram = MemoryInstance(name="L2", 
            size=64*2097152, 
            r_bw=2048, w_bw=2048, 
            r_cost=10, w_cost=10, 
            r_port = 1, w_port = 1, 
            area=0)
    

    # DIMC array weight cell
    weight_cell = MemoryInstance(name="weight_cell", 
            size=512, 
            r_bw=8, w_bw=8, 
            r_cost=0.078, w_cost=0.078, 
            rw_port = 1, area=0)

    # Input buffer
    input_buffer = MemoryInstance(name="input_buffer", 
            size=8, 
            r_bw=8, w_bw=8, 
            r_cost=0.1, w_cost=0.1, 
            r_port = 1, w_port = 1, 
            area=0) 

    # Output buffer
    output_buffer = MemoryInstance(name="output_buffer", 
            size=8, 
            r_bw=8, w_bw=8, 
            r_cost=0, w_cost=0, 
            r_port = 2, w_port = 2, 
            area=0) 

    # Create memory hierarchy graph object
    # Operational array has dimensions [128 x 16]
    memory_hierarchy_graph = MemoryHierarchy(operational_array=multiplier_array)

    # Add DIMC array weight_cell
    memory_hierarchy_graph.add_memory(memory_instance=weight_cell, operands=('I1',), 
            served_dimensions=set())
    # Add Input buffer
    memory_hierarchy_graph.add_memory(memory_instance=input_buffer, operands=('I2',), 
            served_dimensions={(0,1)})
    # Add output buffer
    memory_hierarchy_graph.add_memory(memory_instance=output_buffer, operands=('O',), 
            port_alloc=({'fh':'w_port_1', 'fl': 'w_port_2', 'th': 'r_port_1', 'tl': 'r_port_2'},), 
            served_dimensions={(1,0)})
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
