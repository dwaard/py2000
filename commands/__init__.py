import importlib
import inspect
import os
from colorama import Fore, Back, Style
from commands.AbstractCommand import AbstractCommand


def get_command(command_line):
    """
    Parses the given command line and returns the conforming command.
    """
    splitted = command_line.split()
    if (len(splitted) < 1):
        raise ValueError('Please type a command')
    command = splitted[0]
    class_name = command.title()
    args = splitted[1:]
    module_path = f"commands.{class_name}"
    try:
        module = importlib.import_module(module_path)
    except Exception as e:
        raise ValueError(f"{command}? I don't know what you mean")
    class_ = getattr(module, class_name)
    return class_(args)


def print_available_commands():
    """
    Prints all the available commands
    """
    print("Your command words are:")
    print(', '.join(list_available_commands()))


def list_available_commands():
    """
    List all the available commands in the commands package folder. a Command is 
    assumed to be a class in a file with the same name.
    """
    classes = []
    package_prefix = "commands"

    # Iterate over every file in the package folder
    for filename in os.listdir(f"./{package_prefix}"):
        # Skip non-Python files, __init__.py and files starting with Abstract
        if not filename.endswith(".py") or filename.startswith("_") or filename.startswith("Abstract"):
            continue

        module_name = filename[:-3]  # Strip .py extension
        full_module_name = f"{package_prefix}.{module_name}"
        # Try to dynamically import the module
        module = importlib.import_module(full_module_name)

        # Inspect module members and collect classes defined in the module
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == full_module_name:
                classes.append(name.lower())

    return classes
