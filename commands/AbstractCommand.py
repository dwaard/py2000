
class AbstractCommand:
    """
    The base class of all commands.
    """

    """
    Defines if this command is undoable. If set to `True`, it will be pushed to
    the undo-stack after execution. This requires the `undo` method to be
    implemented as well. Default is `False`.
    """
    is_undoable = False

    def __init__(self, args):
        """
        Constructor. It might be overridden to set the `is_undoable` and to
        validate arguments. When validating, just raise a `ValueError` when
        validation fails.
        """
        self.args = args

    def print_help(self, context):
        """
        Print detailed help for the user about this command. Specify purpose 
        and arguments when applicable.
        """
        raise NotImplementedError
    
    def execute(self, context):
        """
        Execute this command on the given context. If the command is undoable, 
        some of its state must be stored in order to use it in the `undo` method.
        """
        raise NotImplementedError
    
    def undo(self, context):
        """
        Undo its command. Implementing classes can assume that the state of the
        context is exactly as right after this command was executed.
        """
        if self.is_undoable:
            raise NotImplementedError
        raise ValueError('This command cannot be undone')
  