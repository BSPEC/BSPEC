import sys
import os.path
import os
from dataclasses import dataclass as component
from typing import (
    List,
    Optional,
    Union,
)

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

#######################################
#  Import Required Component Modules: #
#######################################
try:
    import pandas as pd  # noqa: E402
except ImportError:
    module_name = "pandas"
    dynamic_module_install(module_name, requirements_dict)
    import pandas as pd  # noqa: E402


#########################################
#  Define some PD_DataFrames Component: #
#########################################
@versionadded(
    version="0.1.2",
    reason="This allows for generic input parameters for dropna using Pandas",
)
@component
class PD_Input_DropNA:
    """This allows for generic input parameters for dropna using Pandas

    Params:
        axis ({0 or 'index', 1 or 'columns'}, default 0):
                Determine if rows or columns which contain missing values are removed.
                * 0, or 'index' : Drop rows which contain missing values.
                * 1, or 'columns' : Drop columns which contain missing value.

        how ({'any', 'all'}, default 'any'):
                Determine if row or column is removed from DataFrame, when we have at least one NA or all NA.
                * 'any': If any NA values are present, drop that row or column.
                * 'all': If all values are NA, drop that row or column.

        thresh (int, optional):
                Require that many non-NA values. Cannot be combined with how.

        subset (column label or sequence of labels, optional):
                Labels along other axis to consider, e.g. if you are dropping rows these would be a
                 list of columns to include.

        inplace (bool, default False)
                Whether to modify the DataFrame rather than creating a new one.
    """

    axis: int = 0
    how: str = "any"
    thresh: Optional[int] = None
    subset: Optional[Union[str, List[str]]] = None
    inplace: Optional[bool] = False


def register() -> None:
    """use `component_factory` to register the `PD_Input_DropNA` component as 'pd_input_dropna'"""
    component_factory.register("pd_input_dropna", PD_Input_DropNA)
