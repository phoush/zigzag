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
    multiplier_input_precision = [8, 2]
    AIMC_unit_costs = {'act_line_cap' : 0.00067,
            'sum_line_cap' : 0.000615,
            'act_line_v' : 0.8,
            'sum_line_v' : 0.6,
            'vdd' : 0.8,
            'ADC_cost' : 0.31,
            'DAC_cost' : 0.155,
            'mac_cost' : 1}
    AIMC_area = {'MAC_cell': 1, 'ADC': 1, 'DAC': 1}
    dimensions = {'D1': 64, 'D2': 512}

    aimc = AIMC(multiplier_input_precision, AIMC_unit_costs, AIMC_area)
    aimc_array = AIMCArray(aimc, dimensions)
    return aimc_array


def memory_hierarchy(multiplier_array):
    """Memory hierarchy variables"""
    ''' size = #bit '''

    # 2MB SRAM
    L2_sram = MemoryInstanceClocked(name="L2", 
            size=2097152, 
            r_bw=512, w_bw=512, 
            r_cost=0, w_cost=0, 
            r_port = 1, w_port = 1, 
            area=0, 
            clock_domain_rd = 1, clock_domain_wr = 1)
    
    # 256kB L1 SRAM
    L1_sram = MemoryInstanceClocked(name="L1", 
            size=262144, 
            r_bw=512, w_bw=512, 
            r_cost=7, w_cost=7, 
            r_port = 1, w_port = 1, 
            area=0, 
            clock_domain_rd = 1, clock_domain_wr = 1)

    # AIMC array weight cell
    weight_cell = MemoryInstanceClocked(name="weight_cell", 
            size=2, 
            r_bw=2, w_bw=2, 
            r_cost=0, w_cost=1.4e-3, 
            rw_port = 1, area=0, 
            clock_domain_rd = 1, clock_domain_wr = 1)

    # Input buffer
    input_buffer = MemoryInstanceClocked(name="input_buffer", 
            size=8, 
            r_bw=8, w_bw=8, 
            r_cost=0.1, w_cost=0.1, 
            r_port = 1, w_port = 1, 
            area=0, 
            clock_domain_rd = 1, clock_domain_wr = 1)

    # Output buffer
    output_buffer = MemoryInstanceClocked(name="output_buffer", 
            size=8, 
            r_bw=8, w_bw=8, 
            r_cost=0.1, w_cost=0.1, 
            r_port = 2, w_port = 2, 
            area=0, 
            clock_domain_rd = 1, clock_domain_wr = 1)

    # Create memory hierarchy graph object
    # Operational array has dimensions [1152 x 512]
    memory_hierarchy_graph = MemoryHierarchy(operational_array=multiplier_array)

    # Add AIMC array weight_cell
    memory_hierarchy_graph.add_memory(memory_instance=weight_cell, operands=('I1',), 
            served_dimensions=set())
    # Add Input buffer
    memory_hierarchy_graph.add_memory(memory_instance=input_buffer, operands=('I2',), 
            served_dimensions={(0,1)})
    # Add output buffer
    memory_hierarchy_graph.add_memory(memory_instance=output_buffer, operands=('O',), 
            port_alloc=({'fh':'w_port_1', 'fl': 'w_port_2', 'th': 'r_port_1', 'tl': 'r_port_2'},), 
            served_dimensions={(1,0)})
    # Add L1 memory
    memory_hierarchy_graph.add_memory(memory_instance=L1_sram, operands=('I2','O',), 
            served_dimensions='all')
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
