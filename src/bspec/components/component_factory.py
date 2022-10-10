"""Factory for creating a component."""

from typing import Dict, Any, Callable

from dataclasses import dataclass as component


"""
Dictionary of functions defined by the key 'component_name' within a 
callable function as the value
"""
component_creation_funcs: Dict[str, Callable[..., component]] = {}


def register(component_name: str, creator_fn: Callable[..., component]) -> None:
    """Register a new component by a name provided


    Args:
        component_name (str): the name of a component so it can be looked up
            in the `component_creation_funcs`
        creator_fn (Callable[..., component]): function that is callable,
            that will be used to register a component
    """
    component_creation_funcs[component_name] = creator_fn


def unregister(component_name: str) -> None:
    """Unregister a component by name.

    Args:
        component_name (str): the name of the component to
            remove from the `component_creation_funcs`
    """
    component_creation_funcs.pop(component_name, None)


def create(arguments: Dict[str, Any]) -> component:
    """Create a component of a specific name 'component_name', given JSON data,
    and use all other 'objects' as key-value properties to init the component class.

    Args:
        arguments (Dict[str, Any]): _description_

    Raises:
        ValueError: missing component name in `component_creation_funcs`

    Returns:
        component: the instantiated component function with it's own arguments
    """
    args_copy = arguments.copy()
    name = args_copy.pop("component_name")
    args_copy = args_copy["component_properties"]

    try:
        creator_func = component_creation_funcs[name]
    except KeyError:
        raise ValueError(f"Unknown component name: '{name}', please register")
    return creator_func(**args_copy)
