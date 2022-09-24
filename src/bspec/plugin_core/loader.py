"""import modules and load plugins, adapted from: https://youtu.be/iCE1bDoit9Q"""
import importlib
from typing import List

from plugin_core.plugin_module_interface import ModuleInterface


def import_module(module_name: str) -> ModuleInterface:
    """Imports a module with a given a name string.

    Args:
        module_name (str): a string of the module to import
                            string should be in dot notation as per standard
                            python imports

                            e.g.
                                import {module}.{class}.{module}

                                import typing.List

    Returns:
        ModuleInterface: an imported module with the ModuleInterface structure
    """
    return importlib.import_module(module_name)  # type: ignore


def load_plugins(plugins: List[str]) -> None:
    """Imports a list of plugins defined in the `plugins` parameter.

    Args:
        plugins (List[str]): a list of strings, of the modules to import
                             string should be in dot notation as per standard
                             python imports

                             e.g.
                                import {module}.{class}.{module}

                                import typing.List

    """
    for plugin_name in plugins:
        # Don't break program for bad config!
        try:
            plugin = import_module(plugin_name)
            plugin.register()
        except Exception as e:
            print(f"failed to import module: {plugin_name} with error: {e}")
