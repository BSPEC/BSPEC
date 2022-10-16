"""Factory for creating a processor."""

from typing import Any, Callable

from esper import Processor


"""
Dictionary of functions defined by the key 'processor_name' within a 
callable `Processor` function as the value
"""
processor_creation_funcs: dict[str, Callable[..., Processor]] = {}


def register(processor_name: str, creator_fn: Callable[..., Processor]) -> None:
    """Register a new processor by name.

    Args:
        processor_name (str): the name of a processor so it can be looked up
            in the `processor_creation_funcs`
        creator_fn (Callable[..., Processor]): function that is callable,
            that will be used to register a processor
    """
    processor_creation_funcs[processor_name] = creator_fn


def unregister(processor_name: str) -> None:
    """Unregister a processor by name.

    Args:
        processor_name (str): the name of the processor to
            remove from the `processor_creation_funcs`
    """
    processor_creation_funcs.pop(processor_name, None)


def create(arguments: dict[str, Any]) -> Processor:
    """Create a processor of a specific name 'processor_name', given JSON data,
    and use all other 'objects' as key-value properties to init the processor class.

    Args:
        arguments (dict[str, Any]): any arguments for the processor

    Raises:
        ValueError: missing processor name in `processor_creation_funcs`

    Returns:
        Processor:  the instantiated processor function with it's own arguments
    """
    args_copy = arguments.copy()
    name = args_copy.pop("processor_name")
    try:
        creator_func = processor_creation_funcs[name]
    except KeyError:
        raise ValueError(f"Unknown processor name: '{name!r}'") from None
    return creator_func(**args_copy)
