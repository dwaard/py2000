import framework

from context import Py2KContext

if __name__ == '__main__':
    def configure_command_line_arguments(parser):
      # Add command line arguments, see: https://docs.python.org/3/library/argparse.html
      pass

    framework.run(Py2KContext(), 
        argparse_initialize_func=configure_command_line_arguments)