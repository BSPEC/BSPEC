from dataclasses import dataclass as component

from deprecated.sphinx import versionadded

from bspec.components import component_factory

###########################
# Define Debug Component: #
###########################
@versionadded(
    version="0.1.2",
    reason="This allows multiple entities to use debug flags to automate debugging from config",
)
@component
class RuntimeDebugPrint:
    """This allows multiple entities to use debug flags to automate debugging from config

    Params:
        runtime_debug_flag (bool): should the systems print out the variables at runtime

        pause_execution (bool): should the console pause execution requiring enter before
                                continuing
    """

    runtime_debug_flag: bool = False
    pause_execution: bool = False


def register() -> None:
    """use `component_factory` to register the `RuntimeDebugPrint` component as 'runtime_debug_print'"""
    component_factory.register("runtime_debug_print", RuntimeDebugPrint)
