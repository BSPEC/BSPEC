import sys
import os.path
from dataclasses import dataclass
from typing import List

from esper import Processor

from processors import processor_factory
from common_core.read_module_requirements import read_module_requirements
from common_core.dynamic_module_install import dynamic_module_install

from components.runtime_debug_print.runtime_debug_print import RuntimeDebugPrint
from components.input_file_csv.input_file_csv import Input_File_CSV
from components.pd_dataframe.pd_dataframes import PD_DataFrames

###########################################################################
#  Load System Modules module_requirements.txt to support dynamic import: #
###########################################################################
if getattr(sys, "frozen", False):
    # running as bundle (aka frozen)
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # running live
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

requirements_path = os.path.join(BASE_DIR, "requirements/module_requirements.txt")
requirements_dict = read_module_requirements(requirements_path)

#######################################
#  Import Required Processor Modules: #
#######################################
try:
    import pandas as pd  # noqa: E402
except ImportError:
    module_name = "pandas"
    dynamic_module_install(module_name, requirements_dict)

################################
#  Define some Systems:
################################


@dataclass
class PD_Read_CSV(Processor):
    """Read a CSV using Pandas `read_csv`

    Args:
        Processor (_type_): ECS framework `esper`'s Processor class

    Params:
        components (Sequence): Sequence of components that the system
            will use to function. This includes generic entity settings
            or persist data. Components include:
                * RuntimeDebugPrint
                * Input_File_CSV
                * PD_DataFrames
    """

    def __init__(self, **kwargs):
        self.components: List = [
            RuntimeDebugPrint,
            Input_File_CSV,
            PD_DataFrames,
        ]

    def process(self):
        """Generic naming convention `process` to allow for every processor to run
        specific logic, providing a generic interface for us to engage with.

        It uses the `components` parameter to fetch the components from the world
        """
        for ent, (
            runtime_debug_print,
            input_file_csv,
            pd_dataframes,
        ) in self.world.get_components(*self.components):
            input_file_csv_kwargs = vars(input_file_csv)
            pd_dataframes.dataframe_1 = pd.read_csv(**input_file_csv_kwargs)

            if runtime_debug_print.runtime_debug_flag is True:
                print()
                print("PD_Read_CSV")
                print("============")
                print()
                print("ent: ", ent)
                print()
                print("input_file_csv: ")
                print(input_file_csv)
                print()
                print("pd_dataframes:")
                print(pd_dataframes)
                if runtime_debug_print.pause_execution is True:
                    print()
                    input("Enter to continue execution:")


def register() -> None:
    """use `processor_factory` to register the `PD_Read_CSV` component as 'pd_read_csv'"""
    processor_factory.register("pd_read_csv", PD_Read_CSV)
