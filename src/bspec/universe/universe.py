import platform
from typing import Callable, Dict, List, Union, Set

from esper import World

from bspec.plugin_core import loader as plugins_loader
from bspec.processors import processor_factory
from bspec.components import component_factory
from bspec.pipelines.recursive_pipeline_read import recursive_pipeline_read


print("Python Version: ", platform.python_version())

######################################
# Create a galaxy of named worlds: #
######################################
galaxy: Dict[str, World] = {}

############################################################
# Instantiate everything, and create your main logic loop: #
############################################################
def universe(
    data: Dict[str, Union[str, list, int, float, dict]],
    exception_at_duplicate_world_names: bool = True,
    timed: bool = False,
):
    """The main `universe` function that will load the plugins, register worlds to the
    galaxy and processing the starting world.

    Args:
        data (Dict[str, Union[str, list, int, float, dict]]): Config data dictionary

        exception_at_duplicate_world_names (bool): this is used to raise an exception if
                                                more than 1 world has the same name, to
                                                prevent unexpected application behavior

        timed (bool): using the package `esper` how will World be registered?
                     it will replace `_process` with `_timed_process` allowing you to benchmark
                     the runtime and understand how long each `Processor` will take to run the
                     `process` function, which is saved to the property `process_times`
    """

    # Set the starting world
    starting_world = data["starting_world"]

    processor_plugins: Set[str] = set(data["processor_plugins"])

    galaxy_config: List = data["galaxy"]

    # Load pipelines:
    returned_val = recursive_pipeline_read(
        data=data,
        processor_plugins=processor_plugins,
        galaxy_config=galaxy_config,
    )
    processor_plugins.update(returned_val["all_processor_plugins"])
    galaxy_config = returned_val["galaxy_config"]

    # load the processor plugins
    # currently using plugin_core loader which may need to change in the future
    plugins_loader.load_plugins(processor_plugins)

    # Highlight Duplicate World Names
    unique_world_names: List[str] = []

    # set up ECS requirements for global registration
    entities: Dict = {}
    processors: Dict[str, Dict[str, Dict[str, Union[Callable, int]]]] = {}
    components: Set[str] = set()

    for world in galaxy_config:
        # Create a World instance to hold Entities, Components and Processors:
        # Named instance will allow us to quickly and easily reference for traversal from other worlds
        #   by using "world_name"
        world_name: str = world["world_name"]

        # Highlight duplicate world_names
        if world_name not in unique_world_names:
            unique_world_names.append(world_name)
        else:
            warning_msg: str = f"""You have a duplicate `world_name`: {world_name}
            You may get unexpected results with duplicated world names as the `world_name` is used
            to look up and process a world within in a `galaxy` with:
            e.g.
            galaxy[world_name].process()

            Therefore a duplicate `world_name` may not run the expected code/ config

            If you are using pipelines, consider adding a more specific `world_name` to override the
            default pipeline `world_name` as other pipelines may use the same underlying pipeline
            and therefore have the same name.
            """
            print(warning_msg)

            # Exception at duplicate world_names
            if exception_at_duplicate_world_names:
                raise Exception(warning_msg)

        galaxy[world_name] = World(timed=timed)

        # create the processors
        for processor in world["processors"]:
            world_processors = processors.get(world_name, None)
            if world_processors is None:
                processors[world_name] = {}

            processors[world_name][processor["processor_name"]] = {
                "processor": processor_factory.create(world_name, processor),
                "priority": processor["priority"],
            }

        # [galaxy[world_name].add_processor(processor,priority = processor.priority['priority']) for processor in processors]
        for processor_name in processors[world_name]:
            galaxy[world_name].add_processor(
                processors[world_name][processor_name]["processor"],
                priority=processors[world_name][processor_name]["priority"],
            )
            processor_components = processors[world_name][processor_name][
                "processor"
            ].__dict__["components"]

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
        print(f"Entry World: {starting_world}")
        print()
        print()
        galaxy[starting_world].process()
    except KeyboardInterrupt:
        return
