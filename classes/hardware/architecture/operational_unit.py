from typing import List, Dict
import numpy as np


class OperationalUnit:
    def __init__(self, input_precision: List[int], output_precision: int, unit_cost: Dict[str, float], unit_area: Dict[str, float], technology: int):
        """
        General class for a unit that performs a certain operation. For example: a multiplier unit.

        :param input_precision: The bit precision of the operation inputs.
        :param output_precision: The bit precision of the operation outputs.
        :param unit_cost: The energy cost of performing a single operation.
        :param unit_area: The area of a single operational unit.
        """
        self.input_precision = input_precision
        self.output_precision = output_precision
        self.precision = input_precision + [output_precision]
        self.cost = unit_cost
        self.technology = technology
        self.area = unit_area
        if 'gates_per_adder' in unit_cost.keys():
            self.gate_per_adder = unit_cost['gates_per_adder']
        else:
            self.gate_per_adder = 5
        if 'mac_clock_domain' in unit_cost.keys():
            self.cost['mac_clock_domain'] = unit_cost['mac_clock_domain']
        else:
            self.cost['mac_clock_domain'] = 1



    def __jsonrepr__(self):
        """
        JSON Representation of this class to save it to a json file.
        """
        return self.__dict__

    def get_cap_gate(self):
        return (self.technology * 0.02 + 0.196)*1e-3

    def get_cap_inv(self):
        return self.get_cap_gate()/2

    def get_1b_adder_energy(self):
        gate_per_adder = self.gate_per_adder
        return  self.get_cap_gate() * (self.cost['vdd']**2) * gate_per_adder

    def get_adder_energy(self):
        gate_per_adder = self.gate_per_adder
        return  self.get_cap_gate() * (self.cost['vdd']**2) * gate_per_adder

    def get_multiplier_energy(self):
        return  (self.get_cap_gate() / 1.56) * (1.9 * np.power(max(self.input_precision),2) * np.log2(max(self.input_precision))) * (self.cost['vdd']**2) 



class Multiplier(OperationalUnit):
    def __init__(self, input_precision: List[int], energy_cost: Dict[str, float], area: Dict[str, float]):
        """
        Initialize the Multiplier object.

        :param input_precision: The bit precision of the multiplication inputs.
        :param output_precision: The bit precision of the multiplication outputs.
        :param energy_cost: The energy cost of performing a single multiplication.
        :param area: The area of a single multiplier.
        """
        output_precision = sum(input_precision)
        super().__init__(input_precision, output_precision, energy_cost, area)


class AIMC(OperationalUnit):
    def __init__(self, input_precision: List[int], energy_cost: Dict[str, float], area: Dict[str, float], technology: int):
        """
        Initialize the AIMC object.

        :param input_precision: The bit precision of the multiplication inputs.
        :param output_precision: The bit precision of the multiplication outputs.
        :param energy_cost: The energy cost of performing a single multiplication.
        :param area: The area of a single multiplier.
        """
        output_precision = sum(input_precision)
        super().__init__(input_precision, output_precision, energy_cost, area, technology)

        if 'wl_cap' not in self.cost:
            self.cost['wl_cap'] = self.get_cap_inv()
        if 'bl_cap' not in self.cost:
            self.cost['bl_cap'] = self.get_cap_inv()
        if 'wl_v' not in self.cost:
            self.cost['wl_v'] = self.cost['vdd']
        if 'bl_v' not in self.cost:
            self.cost['bl_v'] = self.cost['vdd']

        if 'WEIGHT_BITCELL' not in self.cost:
            self.cost['WEIGHT_BITCELL'] = self.input_precision[1]

class DIMC(OperationalUnit):
    def __init__(self, input_precision: List[int], energy_cost: Dict[str, float], area: Dict[str, float], technology: int):
        """
        Initialize the DIMC object.

        :param input_precision: The bit precision of the multiplication inputs.
        :param output_precision: The bit precision of the multiplication outputs.
        :param energy_cost: The energy cost of performing a single multiplication.
        :param area: The area of a single multiplier.
        """
        output_precision = sum(input_precision)
        super().__init__(input_precision, output_precision, energy_cost, area, technology)
        self.imc_type = 'IMC'
        if 'wl_cap' not in self.cost:
            self.cost['wl_cap'] = self.get_cap_inv()
        if 'bl_cap' not in self.cost:
            self.cost['bl_cap'] = self.get_cap_inv()
        if 'WEIGHT_BITCELL' not in self.cost:
            self.cost['WEIGHT_BITCELL'] = self.input_precision[1]

