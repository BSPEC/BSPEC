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
    import plotly.express as px
except ImportError:
    module_name = "dash"
    dynamic_module_install(module_name, requirements_dict)
    from dash import dcc, html  # noqa: E402
    import plotly.express as px

T = TypeVar("T")


@dataclass
class DashComponentsFactory:
    ui_config: Dict
    components: Dict[str, T] = field(default=dict)
    _layout: Sequence[T] = field(default=list)

    @property
    def layout(self):
        self._layout = self.register_layout(
            self, ui_config=self.ui_config, layout=self.layout
        )
        return self._layout

    def register_layout(self, ui_config: Dict, layout: Sequence[T]):
        for class_name in ui_config:
            component = self.components.get(class_name)
            if component is None:
                component = self.load_component(class_name)
            children_ui_config = ui_config[class_name].pop("children_config")
            if children_ui_config is not None:
                layout.extend(
                    self.register_layout(ui_config=children_ui_config, layout=layout)
                )
            layout.append(component(ui_config[class_name]))
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
