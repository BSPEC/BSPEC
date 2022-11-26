import sys
import os.path
from dataclasses import dataclass, field
from typing import Dict, Sequence, TypeVar

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
#  Import Required Processor Modules: #
#######################################
try:
    from dash import dcc, html  # noqa: E402
    import plotly.express as px  # noqa: E402
except ImportError:
    module_name = "dash"
    dynamic_module_install(module_name, requirements_dict)
    from dash import dcc, html  # noqa: E402
    import plotly.express as px  # noqa: E402

T = TypeVar("T")


@dataclass
class DashComponentsFactory:
    ui_config: Dict
    components: Dict[str, T] = field(default_factory=dict)
    _layout: Sequence[T] = field(default_factory=list)

    @property
    def layout(self):
        self._layout = self.register_layout(
            ui_config=self.ui_config, layout=self._layout
        )
        return self._layout

    def register_layout(self, ui_config: Dict, layout: Sequence[T]):
        for class_name in ui_config:
            component = self.components.get(class_name)
            children_ui_config: Dict = None
            if component is None:
                component = self.load_component(class_name)
            if isinstance(ui_config[class_name], dict):
                children_ui_config = ui_config[class_name].pop("children_config", None)
            children = {}
            if children_ui_config is not None:
                children = {
                    "children": self.register_layout(
                        ui_config=children_ui_config, layout=[]
                    )
                }
            ui_config_details = ui_config[class_name]
            if isinstance(ui_config_details, dict):
                ui_config_details = {**ui_config_details, **children}
                layout.append(component(**ui_config_details))
            else:
                layout.append(component(ui_config_details))
        return layout

    def load_component(self, class_name: str):
        if hasattr(html, class_name):
            self.components[class_name] = getattr(html, class_name)
        elif hasattr(dcc, class_name):
            self.components[class_name] = getattr(dcc, class_name)
        elif hasattr(px, class_name):
            self.components[class_name] = getattr(px, class_name)
        else:
            raise ImportError(
                f"Cannot import `{class_name}` from `dash.html`, `dash.dcc` or `plotly.express`"
            )
        return self.components[class_name]
