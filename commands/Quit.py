import commands

class Quit(commands.AbstractCommand):
    """
    Basic command for exiting the program.
    """

    def print_help(self, context):
        print("Quit this adventure")


    def execute(self, context):
        confirm = input('Are you sure? (Y/n) ')

        if confirm != 'Y':
            return False
        
        print('Thank you for playing. Good bye.')
        return True
