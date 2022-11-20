from typing import Generator, Callable, List, Tuple, Any
from classes.stages.Stage import Stage

import numpy as np
import logging

from classes.cost_model.cost_model import CostModelEvaluation
from classes.hardware.architecture.accelerator import Accelerator
from classes.mapping.spatial.spatial_mapping import SpatialMapping
from classes.mapping.temporal.temporal_mapping import TemporalMapping
from classes.workload.layer_node import LayerNode
import classes.io.input_config as inputs
logger = logging.getLogger(__name__)
import pdb


def merge_loops(temporal_mapping):
    tm_merged = {}
    tm = temporal_mapping.mapping_dic_origin
    for op in tm.keys():
        tm_merged[op] = []
        for lev in tm[op]:
            tm_level = []
            for ii_tm, tmx in enumerate(lev):
                if ii_tm > 0:
                    if tmx[0] == lev[ii_tm-1][0]:
                        tm_level[-1][1] *= tmx[1]
                    else:
                        tm_level.append([tmx[0], tmx[1]])
                else:
                    tm_level.append([tmx[0], tmx[1]])
            tm_merged[op].append(tm_level)
    for op in tm_merged.keys():
        tm_merged[op] = [[tuple(x) for x in lev] for lev in tm_merged[op]] 


    temporal_mapping.mapping_dic_origin = tm_merged
    return tm_merged


class CostModelStage(Stage):
    """
    Pipeline stage that calls a cost model to evaluate a mapping on a HW config.
    """
    def __init__(self, list_of_callables:List[Callable], *, accelerator, layer, spatial_mapping, temporal_mapping, **kwargs):
        """
        Initializes the cost model stage given main inputs
        """
        super().__init__(list_of_callables, **kwargs)
        self.accelerator, self.layer, self.spatial_mapping, self.temporal_mapping =\
            accelerator, layer, spatial_mapping, temporal_mapping
        self.mac_clock_domain = kwargs['mac_clock_domain']

    def run(self) -> Generator[Tuple[CostModelEvaluation, Any], None, None]:
        """
        Run the cost model stage by calling the internal zigzag cost model with the correct inputs.
        """
        self.cme = CostModelEvaluation(accelerator=self.accelerator,
                                       layer=self.layer,
                                       spatial_mapping=self.spatial_mapping,
                                       temporal_mapping=merge_loops(self.temporal_mapping),
                                       mac_clock_domain = self.mac_clock_domain)
        yield (self.cme, None)

    def is_leaf(self) -> bool:
        return True
