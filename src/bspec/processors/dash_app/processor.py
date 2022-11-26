import sys
import os.path
from dataclasses import dataclass
from typing import Sequence

from esper import Processor

from bspec.processors import processor_factory
from bspec.common_core.read_module_requirements import read_module_requirements
from bspec.common_core.dynamic_module_install import dynamic_module_install

from bspec.components.runtime_debug_print.runtime_debug_print import RuntimeDebugPrint
from bspec.components.dash_ui.dash_ui import Dash_Ui
from bspec.processors.dash_app.dash_component_factory import DashComponentsFactory

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
    from dash import Dash, html, dcc  # noqa: E402
    import plotly.express as px  # noqa: E402
except ImportError:
    module_name = "dash"
    dynamic_module_install(module_name, requirements_dict)
    from dash import Dash, html, dcc  # noqa: E402
    import plotly.express as px  # noqa: E402

#########################
#  Define some Systems: #
#########################


@dataclass
class Dash_App(Processor):
    """Read a CSV using Pandas `read_csv`

    Args:
        Processor (_type_): ECS framework `esper`'s Processor class

    Params:
        components (Sequence): Sequence of components that the system
            will use to function. This includes generic entity settings
            or persist data. Components include:
                * RuntimeDebugPrint
                * Dash_Ui
    """

    def __init__(self, **kwargs):
        # super().__init__(kwargs)
        self.components: Sequence = [
            RuntimeDebugPrint,
            Dash_Ui,
        ]

    def process(self):
        """Generic naming convention `process` to allow for every processor to run
        specific logic, providing a generic interface for us to engage with.

        It uses the `components` parameter to fetch the components from the world
        """
        for ent, (
            runtime_debug_print,
            dash_ui,
        ) in self.world.get_components(*self.components):
            dash_ui = dash_ui.__dict__

            external_stylesheets = dash_ui.pop("external_stylesheets", [])
            app = Dash(__name__, external_stylesheets=external_stylesheets)

            layout = DashComponentsFactory(ui_config=dash_ui).layout

            print(layout)

            app.layout = html.Div(layout)

            # app.run_server(debug=runtime_debug_print.runtime_debug_flag)
            app.run_server()

            if runtime_debug_print.runtime_debug_flag is True:
                print()
                print("Dash_App")
                print("============")
                print()
                print("ent: ", ent)
                print()
                print("dash_ui:")
                print(dash_ui)
                print()
                print("app:")
                print(app)
                print()
                if runtime_debug_print.pause_execution is True:
                    print()
                    input("Enter to continue execution:")


def register() -> None:
    """use `processor_factory` to register the `Dash_App` component as 'dash_app'"""
    processor_factory.register("dash_app", Dash_App)
