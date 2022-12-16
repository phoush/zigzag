from typing import Dict, Set
import numpy as np
from classes.hardware.architecture.dimension import Dimension
from classes.hardware.architecture.operand_spatial_sharing import OperandSpatialSharing
from classes.hardware.architecture.operational_unit import OperationalUnit, Multiplier
from math import ceil
from abc import ABC, abstractmethod


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

    def get_MAC_cost(self, layer, mapping):
        return {'Digital MAC': layer.total_MAC_count * (self.unit.get_multiplier_energy() + self.unit.get_adder_energy())}


class AIMCArray(OperationalArray):
    def __init__(self, operational_unit: OperationalUnit, dimensions: Dict[str, int]):
        super().__init__(operational_unit, dimensions)
        self.type = 'AIMC'

    def get_area(self):
        area = self.unit.area['cell'] * self.total_unit_count + \
            self.unit.area['ADC'] * self.dimension_sizes[0] + \
            self.unit.area['DAC'] * self.dimension_sizes[1]
        return area

    def get_MAC_cost(self, layer, mapping):
        
        spatial_mapping = mapping.spatial_mapping.mapping_dict_origin 
        const_operand = 'W' if 'W' in spatial_mapping.keys() else 'B'
        input_operand = 'I' if const_operand =='W' else 'A'
        spatial_mapping = [j for i in spatial_mapping['O'] for j in i]
        
        FXu = np.prod([x[1] for x in spatial_mapping if x[0] == 'FX'])
        FYu = np.prod([x[1] for x in spatial_mapping if x[0] == 'FY'])
        OXu = np.prod([x[1] for x in spatial_mapping if x[0] == 'OX'])
        Cu = np.prod([x[1] for x in spatial_mapping if x[0] == 'C'])
        Ku = np.prod([x[1] for x in spatial_mapping if x[0] == 'K'])
        num_rows = Cu * (FXu * (OXu + FXu - 1))
        num_cols = OXu * Ku 
        
        cell = ((self.unit.cost['wl_cap'] * (self.unit.cost['wl_v']**2)) * self.dimensions[1].size * num_cols + \
            (self.unit.cost['bl_cap'] * (self.unit.cost['bl_v']**2) * self.dimensions[0].size * num_rows)) * \
            (self.unit.cost['WEIGHT_BITCELL']) * (layer.operand_precision[input_operand] / self.unit.cost['DAC_RES'])
    
        DAC_energy = num_rows * 50e-3 * self.unit.cost['DAC_RES'] * (layer.operand_precision[input_operand]/self.unit.cost['DAC_RES']) * (np.power(self.unit.cost['vdd'],2)) * (layer.operand_precision[const_operand] / self.unit.cost['WEIGHT_BITCELL']) 
        # all columns activated
        #ADC_energy = (100e-15 * self.unit.cost['ADC_ENOB'] + 1e-18 * (np.power(4, self.unit.cost['ADC_ENOB']))) * (np.power(self.unit.cost['vdd'],  2)) * (layer.operand_precision[input_operand] / self.unit.cost['DAC_RES']) * (layer.operand_precision[const_operand] / self.unit.cost['WEIGHT_BITCELL']) * (self.unit.cost['WEIGHT_BITCELL'] / self.unit.cost['BL_PER_ADC']) 
        ADC_energy = num_cols * (100e-3 * self.unit.cost['ADC_RES'] + 1e-6 * (np.power(4, self.unit.cost['ADC_RES']))) * (np.power(self.unit.cost['vdd'],  2)) * (layer.operand_precision[input_operand] / self.unit.cost['DAC_RES']) * (self.unit.cost['WEIGHT_BITCELL'] / self.unit.cost['BL_PER_ADC'])
    
        B = self.unit.cost['ADC_RES']
        N = self.dimensions[0].size * self.unit.cost['WEIGHT_BITCELL']#self.unit.cost['WEIGHT_BITCELL']
        accumulation_energy = self.unit.get_1b_adder_energy() * N *( B + ((N-2) / N) - (((B+np.log2(N) - 1)) / N)) * (layer.operand_precision[input_operand] / self.unit.cost['DAC_RES'])
        total_MAC = layer.total_MAC_count / (FXu * FYu * Cu * Ku * OXu)

        mac_cost =  {'cell' : cell * total_MAC,\
                'DAC': DAC_energy * total_MAC,\
                'ADC': ADC_energy * total_MAC, \
                'accumulation_energy' : accumulation_energy * total_MAC}
        return mac_cost


class DIMCArray(OperationalArray):
    def __init__(self, operational_unit: OperationalUnit, dimensions: Dict[str, int]):
        super().__init__(operational_unit, dimensions)
        self.type = 'DIMC'


    def get_area(self):
        area = self.unit.area['cell'] * self.total_unit_count + \
            self.unit.area['adder'] * self.dimension_sizes[1] + \
            self.unit.area['multiplier'] * self.dimension_sizes[1] * self.dimension_sizes[0]
        return area

    def get_MAC_cost(self, layer, mapping):
        spatial_mapping = mapping.spatial_mapping.mapping_dict_origin 
        const_operand = 'W' if 'W' in spatial_mapping.keys() else 'B'
        input_operand = 'I' if const_operand =='W' else 'A'
        spatial_mapping = [j for i in spatial_mapping['O'] for j in i]
        
        FXu = np.prod([x[1] for x in spatial_mapping if x[0] == 'FX'])
        FYu = np.prod([x[1] for x in spatial_mapping if x[0] == 'FY'])
        OXu = np.prod([x[1] for x in spatial_mapping if x[0] == 'OX'])
        OYu = np.prod([x[1] for x in spatial_mapping if x[0] == 'OY'])
        Cu = np.prod([x[1] for x in spatial_mapping if x[0] == 'C'])
        Ku = np.prod([x[1] for x in spatial_mapping if x[0] == 'K'])
        core_depth = self.unit.cost['CORE_ROWS']

        #to be fixed
        num_cols = self.dimensions[1].size
        total_MAC = layer.total_MAC_count

        precharging_cell = 0
        if core_depth > 1:
            precharging_cycles = mapping.unit_mem_data_movement[const_operand][0].data_elem_move_count.rd_out_to_low / mapping.ir_loop_size_per_level[const_operand][1]
            precharging_cell = (self.unit.cost['wl_cap'] * ((self.unit.cost['vdd']/2)**2) + \
                (self.unit.cost['bl_cap'] * (self.unit.cost['vdd']**2) * (core_depth - 1))) * \
                (self.unit.cost['WEIGHT_BITCELL']) * precharging_cycles

        if self.unit.imc_type == 'NMC':
            B = max(layer.operand_precision[const_operand], layer.operand_precision[input_operand])
            multiplication_energy = (self.unit.cost['wl_cap']/1.56) * (1.9 * np.power(B,2) * np.log2(B)) * (self.unit.cost['vdd']**2) *(layer.operand_precision['I'] / self.unit.cost['INPUT_BITS_PER_CYCLE']) * total_MAC
            multiplication_energy = self.unit.get_multiplier_energy() *(layer.operand_precision[input_operand] / self.unit.cost['INPUT_BITS_PER_CYCLE']) * total_MAC
        if self.unit.imc_type == 'IMC':
            multiplication_energy = (self.unit.cost['wl_cap'] * (self.unit.cost['vdd']**2) + \
                (self.unit.cost['bl_cap'] * (self.unit.cost['vdd']**2) * core_depth)) * \
                (self.unit.cost['WEIGHT_BITCELL']) * (layer.operand_precision[input_operand] / self.unit.cost['INPUT_BITS_PER_CYCLE']) * total_MAC
        
        B = self.unit.cost['WEIGHT_BITCELL']

        accumulation_energy = 0
        # to divide by reuse at each level for outputs!
        for ii_lev, lev in enumerate(mapping.spatial_mapping.unroll_size_ir['O'][:-1]):
            N = self.dimension_sizes[0]
            #breakpoint()
            if ii_lev > 0:
                B = max(layer.operand_precision[const_operand], layer.operand_precision[input_operand])
                N = lev
            if N > 1:
                accumulation_energy += self.unit.get_1b_adder_energy() * N * ( B + ((N-2) / N) - ((B + np.log2(N) - 1) / N) ) *(layer.operand_precision[input_operand] / self.unit.cost['INPUT_BITS_PER_CYCLE']) * mapping.unit_mem_data_movement['O'][ii_lev].data_elem_move_count.wr_in_by_low
                single_accumulation_energy = self.unit.get_1b_adder_energy() * ( B + ((N-2) / N) - ((B + np.log2(N) - 1) / N) ) * (layer.operand_precision[input_operand] / self.unit.cost['INPUT_BITS_PER_CYCLE'])
            
        #breakpoint()
        mac_cost =  {'precharging_cell' : precharging_cell,\
                'multiplication_energy': multiplication_energy,
                'accumulation_energy' : accumulation_energy }
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
