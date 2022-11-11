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
    from flask import Flask  # noqa: E402
except ImportError:
    module_name = "flask"
    dynamic_module_install(module_name, requirements_dict)
    from flask import Flask  # noqa: E402


#########################################
#  Define some PD_DataFrames Component: #
#########################################
@versionadded(
    version="0.1.11",
    reason="This is the app instance of flask",
)
@component
class Flask_App:
    """This is the app instance of flask

    Params:
        app (Flask): This is the app instance of flask
    """

    app: Flask = Flask(__name__, template_folder="templates")


def register() -> None:
    """use `component_factory` to register the `Flask_App` component as 'flask_app'"""
    component_factory.register("flask_app", Flask_App)
