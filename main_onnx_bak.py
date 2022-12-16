from classes.stages import *
import argparse

# Get the onnx model, the mapping and accelerator arguments
parser = argparse.ArgumentParser(description="Setup zigzag inputs")
parser.add_argument('--model', metavar='path', required=True, help='path to onnx model, e.g. inputs/examples/my_onnx_model.onnx')
parser.add_argument('--mapping', metavar='path', required=True, help='path to mapping file, e.g., inputs.examples.my_mapping')
parser.add_argument('--accelerator', metavar='path', required=True, help='module path to the accelerator, e.g. inputs.examples.accelerator1')
args = parser.parse_args()

# Initialize the logger
import logging as _logging
_logging_level = _logging.INFO
# _logging_format = '%(asctime)s - %(name)s.%(funcName)s +%(lineno)s - %(levelname)s - %(message)s'
_logging_format = '%(asctime)s - %(funcName)s +%(lineno)s - %(levelname)s - %(message)s'
_logging.basicConfig(level=_logging_level,
                     format=_logging_format)

# Initialize the MainStage which will start execution.
# The first argument of this init is the list of stages that will be executed in sequence.
# The second argument of this init are the arguments required for these different stages.
mainstage = MainStage([  # Initializes the MainStage as entry point
    ONNXModelParserStage,  # Parses the ONNX Model into the workload
    AcceleratorParserStage,  # Parses the accelerator
    CompleteSaveBestStage,  # Saves all received CMEs information to a json
    WorkloadStage,  # Iterates through the different layers in the workload
    SpatialMappingGeneratorStage,  # Generates multiple spatial mappings (SM)
    MinimalLatencyStage,  # Reduces all CMEs, returning minimal latency one
    LomaStage,  # Generates multiple temporal mappings (TM)
    CostModelStage  # Evaluates generated SM and TM through cost model
],
    onnx_model=args.model,  # required by ONNXModelParserStage
    mapping_path=args.mapping,  # required by ONNXModelParserStage
    accelerator_path=args.accelerator,  # required by AcceleratorParserStage
    dump_filename_pattern="outputs/{layer}-{datetime}.json",  # output file save pattern
    loma_lpf_limit=6,  # required by LomaStage
    mac_clock_domain=1
)

# Launch the MainStage
mainstage.run()
