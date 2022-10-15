import subprocess
import sys
from typing import Dict, Optional


def dynamic_module_install(
    module_name: str, requirements: Dict[str, Optional[str]]
) -> None:
    """Dyanmically install a module at runtime using subprocess.
        The requirements dict should contain a version of the module
        if it does not then the latest version will be used.
        If subprocess fails, then an exception will be raised

    Args:
        module_name (str): Name of the module you wish to install
        requirements (dict): Dictionary of the system loaded from requirements.txt
            this will allow for dynamic versioning to be installed based on the module
            used.

    Raises:
        ImportError: Dynamic install failed, suggestion on what to run to install module
    """

    print(
        f"Failed to import the module: `{module_name}`, attempting to install module dynamically"
    )
    if requirements.get(module_name, None) is not None:
        module_import = "==".join([module_name, requirements.get(module_name, None)])
    else:
        module_import = module_name
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_import])
    except subprocess.CalledProcessError as e:
        raise ImportError(
            f"{e}: the module `{module_name}` is required to run this code. We could not automatically install the dependency, please run: `pip install {module_import}` on the terminal in your environment to install dependency."
        )
