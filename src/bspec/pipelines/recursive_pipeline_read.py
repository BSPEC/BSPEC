from typing import Dict, List, Union, Set

from bspec.plugin_core import loader as plugins_loader


def recursive_pipeline_read(
    data: Dict[str, Union[str, list, int, float, dict]],
    processor_plugins: Set[str],
    galaxy_config: List,
):
    pipelines: Dict = data.get("pipelines", {})
    for pipeline in pipelines:

        # Load Pipeline Module
        pipline_module = plugins_loader.import_module(pipeline["pipeline"])

        # Update Global plugins to import later
        processor_plugins.update(pipline_module.pipeline["processor_plugins"])

        # Recursive Pipeline check
        if pipline_module.pipeline.get("pipelines") is not None:
            returned_val = recursive_pipeline_read(
                data=pipline_module.pipeline,
                processor_plugins=processor_plugins,
                galaxy_config=galaxy_config,
            )
            processor_plugins.update(returned_val["processor_plugins"])
            galaxy_config = returned_val["galaxy_config"]

        # Get world details from pipeline
        world = pipline_module.pipeline["world"]

        # Override Pipeline Entities details from parent config
        world_entities: List = []
        for entity in world["entities"]:
            pipeline_entity = next(
                (item for item in pipeline["entities"] if item["id"] == entity["id"]),
                {},
            )
            pipeline_entity = {**entity, **pipeline_entity}
            world_entities.append(pipeline_entity)
        world["entities"] = world_entities

        # Override world name of pipeline with config world_name or default to pipeline name
        world["world_name"] = pipeline.get("world_name", world["world_name"])

        galaxy_config.append(world)

    return_var: Dict = {
        "processor_plugins": processor_plugins,
        "galaxy_config": galaxy_config,
    }

    return return_var
