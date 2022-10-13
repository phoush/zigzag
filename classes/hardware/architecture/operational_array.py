from typing import Dict, Set
import numpy as np
from classes.hardware.architecture.dimension import Dimension
from classes.hardware.architecture.operand_spatial_sharing import OperandSpatialSharing
from classes.hardware.architecture.operational_unit import OperationalUnit, Multiplier
from math import ceil
from abc import ABC, abstractmethod
import pdb

class OperationalArray(ABC):
    def __init__(self, operational_unit: OperationalUnit, dimensions: Dict[str, int]):
        """
        This class captures multi-dimensional operational array size.

        :param operational_unit: an OperationalUnit object including precision and single operation energy, later we
                           can add idle energy also (e.g. for situations that one or two of the input operands is zero).

        :param dimensions: define the name and size of each multiplier array dimensions, e.g. {'D1': 3, 'D2': 5}.
        """
        self.unit = operational_unit
        self.total_unit_count = int(np.prod(list(dimensions.values()))) 
        base_dims = [Dimension(idx, name, size) for idx, (name, size) in enumerate(dimensions.items())]
        self.dimensions = base_dims
        self.dimension_sizes = [dim.size for dim in base_dims]
        self.nb_dimensions = len(base_dims)
        self.total_area = self.get_area()

    def __jsonrepr__(self):
        """
        JSON Representation of this class to save it to a json file.
        """
        return {"operational_unit": self.unit, "dimensions": self.dimensions}
   
    @abstractmethod
    def get_area(self):
        raise NotImplementedError('get_area() function not implemented for the operational array')

    @abstractmethod
    def get_MAC_cost(self):
        raise NotImplementedError('get_MAC_energy() function not implemented for the operational array')


class MultiplierArray(OperationalArray):
    #def __init__(self, operational_unit, dimensions):
    #    super().__init__(self, operational_unit, dimensions):

    def get_area(self):
        area = self.unit.area['MAC_unit'] * self.total_unit_count
        return area

    def get_MAC_cost(self, layer, spatial_mapping):
        return {'Digital MAC': layer.total_MAC_count * self.unit.cost['MAC_8b']}


class AIMCArray(OperationalArray):
    #def __init__(self, operational_unit, dimensions):
    #    super().__init__(operational_unit, dimensions):

    def get_area(self):
        area = self.unit.area['MAC_cell'] * self.total_unit_count + \
            self.unit.area['ADC'] * self.dimension_sizes[0] + \
            self.unit.area['DAC'] * self.dimension_sizes[1]
        return area

    def get_MAC_cost(self, layer, spatial_mapping):
        spatial_mapping = spatial_mapping.mapping_dict_origin 
        spatial_mapping = [j for i in spatial_mapping['W'] for j in i]
        DAC_cost_total, ADC_cost_total, write_cycles, imc_array_cost, imc_accumulation_cost, imc_array_write_cost, imc_array_internal_cost = 0, 0, 0, 0, 0, 0, 0
        FXu = np.prod([x[1] for x in spatial_mapping if x[0] == 'FX'])
        FYu = np.prod([x[1] for x in spatial_mapping if x[0] == 'FY'])
        OXu = np.prod([x[1] for x in spatial_mapping if x[0] == 'OX'])
        Cu = np.prod([x[1] for x in spatial_mapping if x[0] == 'C'])
        Ku = np.prod([x[1] for x in spatial_mapping if x[0] == 'K'])

        num_rows = Cu * (FXu * (OXu + FXu - 1))
        num_rowsx = np.prod([x[1] for x in spatial_mapping if x[0] in ['FX','FY','C']])
        num_cols = np.prod([x[1] for x in spatial_mapping if x[0] in ['OX','K']])
        eff_num_rows = ceil(num_rows/64)*64
        eff_num_cols = ceil(num_cols/64)*64
        
        energy_act_line = (eff_num_rows * (eff_num_cols * self.unit.cost['act_line_cap'] * self.unit.cost['act_line_v'] * self.unit.cost['vdd']))
        energy_sum_line = (eff_num_cols * (eff_num_rows * self.unit.cost['sum_line_cap'] * self.unit.cost['sum_line_v'] * self.unit.cost['vdd']))
        DAC_cost_totalx = eff_num_rows * self.unit.cost['DAC_cost']
        ADC_cost_totalx = eff_num_cols * self.unit.cost['ADC_cost']
        single_accumulation_cost = self.unit.cost['mac_cost']
        imc_array_single_cost = energy_act_line + energy_sum_line + DAC_cost_totalx + ADC_cost_totalx
        DAC_cost_total += eff_num_rows * self.unit.cost['DAC_cost'] * layer.total_MAC_count/(num_cols * num_rowsx)
        ADC_cost_total += eff_num_cols * self.unit.cost['ADC_cost'] * layer.total_MAC_count/(num_cols * num_rowsx)
        write_cycles = layer.loop_dim_size['C'] * (FXu + OXu - 1) * layer.loop_dim_size['FY'] * (layer.loop_dim_size['FX'] / FXu) 
        imc_array_cost += imc_array_single_cost * layer.total_MAC_count / (num_cols * num_rowsx)
        # TODO ACCUMULATION COST
        imc_accumulation_cost += 1 #accumulation_cycles * single_accumulation_cost
        imc_array_write_cost += write_cycles * self.unit.cost['imc_write_cost']

        imc_array_internal_cost += (energy_act_line + energy_sum_line) * layer.total_MAC_count/(num_cols * num_rowsx)
        mac_cost =  {'AIMC array' : imc_array_internal_cost,\
                'DAC': DAC_cost_total,\
                'ADC': ADC_cost_total,\
                'AIMC write': imc_array_write_cost,\
                'AIMC ps accumulation': imc_accumulation_cost}
        return mac_cost



def multiplier_array_example1():
    '''Multiplier array variables'''
    multiplier_input_precision = [8, 8]
    multiplier_energy = 0.5
    multiplier_area = 0.1
    dimensions = {'D1': 14, 'D2': 3, 'D3': 4}
    operand_spatial_sharing = {'I1': {(1, 0, 0)},
                       'O': {(0, 1, 0)},
                       'I2': {(0, 0, 1), (1, 1, 0)}}
    multiplier = Multiplier(multiplier_input_precision, multiplier_energy, multiplier_area)
    multiplier_array = MultiplierArray(multiplier, dimensions, operand_spatial_sharing)

    return multiplier_array


def multiplier_array_example2():
    '''Multiplier array variables'''
    multiplier_input_precision = [8, 8]
    multiplier_energy = 0.5
    multiplier_area = 0.1
    dimensions = {'D1': 14, 'D2': 12}
    operand_spatial_sharing = {'I1': {(1, 0)},
                             'O': {(0, 1)},
                             'I2': {(1, 1)}}
    multiplier = Multiplier(multiplier_input_precision, multiplier_energy, multiplier_area)
    multiplier_array = MultiplierArray(multiplier, dimensions, operand_spatial_sharing)

    return multiplier_array


if __name__ == "__main__":
    multiplier_array = multiplier_array_example1()
    for os in multiplier_array.operand_spatial_sharing:
        print(f'{os}\tdirection: {os.direction} operand: {os.operand} instances: {os.instances}')
