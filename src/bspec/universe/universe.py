import platform
from typing import Callable, Dict, Union, Set

from esper import World

from bspec.plugin_core import loader as plugins_loader
from bspec.processors import processor_factory
from bspec.components import component_factory


print("Python Version: ", platform.python_version())

######################################
# Create a galaxy of named worlds: #
######################################
galaxy: Dict[str, World] = {}

############################################################
# Instantiate everything, and create your main logic loop: #
############################################################
def universe(data: Dict[str, Union[str, list, int, float, dict]], timed: bool = False):
    """The main `universe` function that will load the plugins, register worlds to the
    galaxy and processing the starting world.

    Args:
        data (Dict[str, Union[str, list, int, float, dict]]): Config data dictionary

        timed (bool): using the package `esper` how will World be registered?
                     it will replace `_process` with `_timed_process` allowing you to benchmark
                     the runtime and understand how long each `Processor` will take to run the
                     `process` function, which is saved to the property `process_times`!
    """

    # Set the starting world
    starting_world = data["starting_world"]

    # load the processor plugins
    # currently using plugin_core loader which may need to change in the future
    plugins_loader.load_plugins(data["processor_plugins"])

    entities: Dict = {}
    processors: Dict[str, Dict[str, Union[Callable, int]]] = {}
    components: Set[str] = set()

    for world in data["galaxy"]:
        # Create a World instance to hold Entities, Components and Processors:
        # Named instance will allow us to quickly and easily reference for traversal from other worlds
        #   by using "world_name"
        world_name = world["world_name"]
        galaxy[world_name] = World(timed=timed)

        # create the processors
        for processor in world["processors"]:
            processors[processor["processor_name"]] = {
                "processor": processor_factory.create(processor),
                "priority": processor["priority"],
            }

        # [galaxy[world_name].add_processor(processor,priority = processor.priority['priority']) for processor in processors]
        for processor_name in processors:
            galaxy[world_name].add_processor(
                processors[processor_name]["processor"],
                priority=processors[processor_name]["priority"],
            )
            processor_components = processors[processor_name]["processor"].__dict__[
                "components"
            ]

            for component in processor_components:
                components.add(component.__dict__["__module__"])

        # load the component plugins
        # currently using plugin_core loader which may need to change in the future
        plugins_loader.load_plugins(components)

        for entity in world["entities"]:
            entity_id = entity["id"]
            entities[entity_id] = galaxy[world_name].create_entity()
            for component in entity["components"]:
                galaxy[world_name].add_component(
                    entities[entity_id], component_factory.create(component)
                )

    try:
        print()
        print("----------------------")
        print("galaxy: ", galaxy)
        print("----------------------")
        print()
        print()
        print(f"Entry World: {starting_world}")
        print()
        galaxy[starting_world].process()
    except KeyboardInterrupt:
        return
