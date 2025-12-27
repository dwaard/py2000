import commands

class Help(commands.AbstractCommand):
    """
    Basic help command that either:
    - prints a generic help message that consists of a help from the context 
      and the available commands
    - prints detailed help about a specific command when this is specified
    """
    
    def print_help(self, context):
        commands.print_available_commands()
        print("")
        print("Type 'help command' to get detailed help for each command.")


    def execute(self, context):
        if len(self.args) > 0:
            # The optional user argument is assumed to be the name of a command
            cmd = commands.get_command(self.args[0])
            # Print the help on that command
            cmd.print_help(context)
        else:
            # When no argument is supplied: print this help
            self.print_help(context)
        return False


