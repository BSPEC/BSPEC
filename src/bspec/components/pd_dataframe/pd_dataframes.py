import sys
import os.path
from dataclasses import dataclass as component
import dataclasses
from typing import Dict, List, TypeVar

from deprecated.sphinx import versionadded

from bspec.components import component_factory
from bspec.common_core.read_module_requirements import read_module_requirements
from bspec.common_core.dynamic_module_install import dynamic_module_install

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

####################################
#  Import Required System Modules: #
####################################
try:
    import pandas as pd  # noqa: E402
except ImportError:
    module_name = "pandas"
    dynamic_module_install(module_name, requirements_dict)
    import pandas as pd  # noqa: E402

PandasDataFrame = TypeVar("pandas.core.frame.DataFrame")

#########################################
#  Define some PD_DataFrames Component: #
#########################################
@versionadded(
    version="0.1.2",
    reason="This allows for generic input parameters for Pandas Dataframes to be used in a generic way",
)
@component
class PD_DataFrames:
    """This allows for generic input parameters for Pandas Dataframes to be used in a generic way

    Params:
        dataframe_1 (PandasDataFrame): The initial Pandas dataframe, and expected input dataframe

        dataframe_2 (PandasDataFrame): The expected output Pandas dataframe

        dataframe_3 (PandasDataFrame): Additional Pandas dataframe that can be used to store values
                                    like a state machine, allowing the standard pattern for dataframe_1
                                    to be input to systems and dataframe_2 to be outputs

        group_by_columns (List[str]): A list of columns to group by

        agg_columns (Dict[str, List[str]]): A dictionary of
                                    {column_name, list of aggregate functions as strings}
                                    this allows for the agg function to be used
                                    e.g.
                                        df1.groupby('Category').agg({'costs':['sum','mean','std']})
    """

    dataframe_1: PandasDataFrame = pd.DataFrame()
    dataframe_2: PandasDataFrame = pd.DataFrame()
    dataframe_3: PandasDataFrame = pd.DataFrame()
    group_by_columns: List[str] = dataclasses.field(default_factory=list)
    agg_columns: Dict[str, List[str]] = dataclasses.field(default_factory=dict)


def register() -> None:
    """use `component_factory` to register the `PD_DataFrames` component as 'pd_dataframes'"""
    component_factory.register("pd_dataframes", PD_DataFrames)
