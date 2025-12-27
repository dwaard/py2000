from collections import deque
from colorama import Fore, Back, Style

class AbstractContext:
    """
    Base class for the custom program's context. Implementing classes must 
    override at least the `print_welcome` and `print_help` methods and may
    override the `get_cursor` method.
    """
    welcome_text = "Empty welcome text"

    undo_stack = deque()

    def init(self):
        """
        Print a welcome message
        """
        print(self.welcome_text)
    

    def print_help(self):
        raise NotImplementedError()


    def get_cursor(self):
        return f"{Style.BRIGHT}> {Style.RESET_ALL}"

    
    def push_executed(self, command):
        self.undo_stack.append(command)


    def pop_undo(self):
        return self.undo_stack.pop()

