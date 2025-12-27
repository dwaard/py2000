import commands

class Undo(commands.AbstractCommand):
    """
    Basic command for undoing undoable commands.
    """

    def print_help(self, context):
        print(f"Undo the last undoable command.")


    def execute(self, context):
        cmd = context.pop_undo()
        cmd.undo(context)
        return False
