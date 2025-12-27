import traceback
import commands
import os
import readline
from colorama import Fore, Back, Style
import argparse
import colorama
import os
from dotenv import load_dotenv
import colored_traceback


def complete(text, state):
    for cmd in commands.list_available_commands():
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1


def init_env():    
    """
    Initializes the environment by loading environment variables from a .env
    file, setting up colorama for colored console output, and configuring
    command line argument parsing with argparse.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    # Load the .env into environment variables
    load_dotenv(override=True)


def init(argparse_initialize_func=None):
    """
    Initializes the global context

    Parameters:
        argparse_initialize_func (ArgumentParser): Callback function to enable
                                               adding custom command line 
                                               options
    """
    init_env()
    # For the nice colors while printing to the console
    colorama.init()
    colored_traceback.add_hook()
    # Configure argparse for command line arguments
    parser = argparse.ArgumentParser(description="Processing command line parameters.")
    parser.add_argument('command', nargs='*', help='command to execute')
    parser.add_argument('-d', '--debug', action='store_true', help='debug mode: display stack traces and exits on Ctrl+C without confirmation')
    if argparse_initialize_func is not None:
        argparse_initialize_func(parser)
    # Parse the arguments
    args = parser.parse_args()
    # Add the parsed args to the OS environment variables. This overwrites
    # potential existing vars intentionally. It makes them highest priority
    for key, value in vars(args).items():
        if value is not None:
            os.environ[key.upper()] = str(value)
    #init autocomplete
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    return args


def run(context, argparse_initialize_func=None):
    """
    The main loop of the shell. IT reads user input from the command line and
    executes the command that corresponds with that.

    Parameters:
        context: The program context, an implementation of AbstractContext
        argparse_initialize_func (ArgumentParser): Callback function to enable
                                               adding custom command line 
                                               options
    """
    args = init(argparse_initialize_func)
    DEBUG = args.debug
    context.init()
    if len(args.command) > 0:
        # There is a command provided in the command line arguments, execute it and exit
        command = commands.get_command(' '.join(args.command))
        try:
            command.execute(context)
        except Exception as e:
            if DEBUG:
                raise e
            else:
                print(f"{Fore.YELLOW}{e}{Style.RESET_ALL}")
        return
    else:
        # No command provided, start the interactive shell
        print("")
        print(f"{Fore.YELLOW}Type 'help' if you need help and 'quit' to exit.{Style.RESET_ALL}")
        while True:
            try:
                try:
                    command = commands.get_command(input(context.get_cursor()))
                    if (command.execute(context)):
                        break
                    if hasattr(command, 'is_undoable') and command.is_undoable:
                        context.push_executed(command)
                except Exception as e:
                    if DEBUG:
                        raise e
                    else:
                        print(f"{Fore.YELLOW}{e}{Style.RESET_ALL}")
            except KeyboardInterrupt:
                if DEBUG or commands.get_command('quit').execute(context):
                    if DEBUG: 
                        print()
                    break
