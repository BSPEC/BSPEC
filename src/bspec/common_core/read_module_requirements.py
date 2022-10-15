from typing import Dict, Optional


def read_module_requirements(requirements_path: str) -> Dict[str, Optional[str]]:
    _requirements = {}
    with open(requirements_path) as file:
        for line in file:
            module_split = line.strip().split("==")
            if len(module_split) == 1:
                if not module_split[0]:
                    continue
                key = module_split[0]
                value = None
            elif len(module_split) == 2:
                (key, value) = module_split
            _requirements[key] = value
    return _requirements
