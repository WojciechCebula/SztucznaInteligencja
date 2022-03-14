import importlib
import typing
import types
import os

import dotenv

dotenv.load_dotenv()


def _get_module(module_name: str) -> types.ModuleType:
    return importlib.import_module(module_name)


def _get_attributes(mod: types.ModuleType) -> typing.Generator[typing.Tuple[str, typing.Any], None, None]:
    variables = vars(mod)
    for key in variables:
        if "__" not in key and key not in _OMITTED_NAMES:
            yield key, variables[key]


def _set_attribute(module: types.ModuleType, key: str, value: typing.Any) -> None:
    value_type = type(value)
        
    # if not isinstance(value, (int, str, float)):
    #     raise AttributeError(f'Attribute "{key}" has an unsupported type of "{value_type}". Supported types: int, str, float.')
    
    new_value = os.getenv(key, None)
    if new_value:
        try:
            parsed_value = value_type(new_value)
            setattr(module, key, parsed_value)
        except ValueError:
            raise ValueError(f'Error has occurred while parsing "{key}" environment variable with value "{new_value}" to type "{value_type}".')


def load_env(module_name: str) -> None:
    module = _get_module(module_name)
    for key, value in _get_attributes(module):
        _set_attribute(module, key, value)


_OMITTED_NAMES = [
    "_OMITTED_MODULES",
    __name__,
    *[key for key in globals()]
]