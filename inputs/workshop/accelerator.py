import os
from classes.hardware.architecture.memory_hierarchy import MemoryHierarchy
from classes.hardware.architecture.memory_level import MemoryLevel
from classes.hardware.architecture.operational_unit import Multiplier, AIMC
from classes.hardware.architecture.operational_array import MultiplierArray, AIMCArray
from classes.hardware.architecture.memory_instance import MemoryInstance
from classes.hardware.architecture.accelerator import Accelerator
from classes.hardware.architecture.core import Core


def multiplier_array():
    """ Multiplier array variables """
    #multiplier_input_precision = [8, 8]
    #multiplier_energy = 0.04
    #multiplier_area = 1
    #dimensions = {'D1': 4}

    #multiplier = Multiplier(multiplier_input_precision, multiplier_energy, multiplier_area)
    #multiplier_array = MultiplierArray(multiplier, dimensions)

    multiplier_input_precision = [8, 2]
    AIMC_unit_costs = {'act_line_cap' : 0.00067,
            'sum_line_cap' : 0.000615,
            'act_line_v' : 0.8,
            'sum_line_v' : 0.6,
            'vdd' : 0.8,
            'ADC_cost' : 0.31,
            'DAC_cost' : 0.155,
            'mac_cost' : 1,
            'imc_write_cost' : 0.455*2}

    AIMC_area = {'MAC_cell': 1, 'ADC': 1, 'DAC': 1}
    dimensions = {'D1_c': 64, 'D1_fx': 3, 'D1_fy': 3, 'D2': 512}

    aimc = AIMC(multiplier_input_precision, AIMC_unit_costs, AIMC_area)
    aimc_array = AIMCArray(aimc, dimensions)

    return aimc_array


def memory_hierarchy(multiplier_array):
    """Memory hierarchy variables"""
    ''' size = #bit '''

    dram = MemoryInstance(name="dram", size=10000000000, r_bw=64, w_bw=64, r_cost=700, w_cost=750, area=0)

    memory_hierarchy_graph = MemoryHierarchy(operational_array=multiplier_array)
    memory_hierarchy_graph.add_memory(memory_instance=dram, operands=('I1', 'I2', 'O'), served_dimensions='all')

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
