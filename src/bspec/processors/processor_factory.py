"""Factory for creating a processor."""

from typing import Any, Callable, Dict, List
from uuid import uuid4

from esper import Processor


"""
Dictionary of functions defined by the key 'processor_name' within a 
callable `Processor` function as the value
"""
processor_creation_funcs: Dict[str, Callable[..., Processor]] = {}
processor_names_uuids: Dict[str, List[str]] = {}
used_processor_uuids: Dict[str, List[str]] = {}


def register(processor_name: str, creator_fn: Callable[..., Processor]) -> None:
    """Register a new processor by name.

    Args:
        processor_name (str): the name of a processor so it can be looked up
            in the `processor_creation_funcs`
        creator_fn (Callable[..., Processor]): function that is callable,
            that will be used to register a processor
    """
    processor_uuid = str(uuid4())
    processor_names_list = processor_names_uuids.get(processor_name, None)
    if processor_names_list is None:
        processor_names_uuids[processor_name] = []

    processor_names_uuids[processor_name].append(processor_uuid)

    processor_creation_funcs[processor_uuid] = creator_fn


def unregister(processor_name: str) -> None:
    """Unregister a processor by name.

    Args:
        processor_name (str): the name of the processor to
            remove from the `processor_creation_funcs`
    """
    processor_creation_funcs.pop(processor_name, None)


def create(world_name: str, arguments: dict[str, Any]) -> Processor:
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
    processor_name = args_copy.pop("processor_name")
    try:
        processor_uuid = processor_names_uuids[processor_name].pop(0)

        used_processor_world_uuids = used_processor_uuids.get(world_name, None)
        if used_processor_world_uuids is None:
            used_processor_uuids[world_name] = {}

        processor_names_list = used_processor_uuids[world_name].get(
            processor_name, None
        )
        if processor_names_list is None:
            used_processor_uuids[world_name][processor_name] = []

        used_processor_uuids[world_name][processor_name].append(processor_uuid)

        creator_func = processor_creation_funcs[processor_uuid]
    except KeyError:
        raise ValueError(f"Unknown processor name: '{processor_name!r}'") from None
    return creator_func(**args_copy)
