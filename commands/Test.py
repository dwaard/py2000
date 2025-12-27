import os, yaml, csv
from datetime import datetime
import commands
from itertools import islice
from context import reader


class Test(commands.AbstractCommand):
    
    def print_help(self, context):
        print("Tries to read the given edition")


    def execute(self, context):
        if len(self.args) > 0:
            # The optional user argument is assumed to be the edition
            self.try_read(context, int(self.args[0]))
        else:
            edition_to_import_to = context.current_edition + 1
            while reader.has_config_for(edition_to_import_to):
                self.try_read(context, edition_to_import_to)
                edition_to_import_to += 1
        return False


    def try_read(self, context, edition):
        print(f"Testing edition {edition}")

        if (not reader.has_config_for(edition)):
            print(f"No config found for edition {edition}, skipping.")
            return

        config = reader.get_config(edition)

        for row in islice( reader.get_reader_for(config["filename"], edition, **config["fileconfig"]), 10):
            print(f"{row[4]}: Artist: {row[1]}; Title: {row[0]}; Year: {row[2]}; ")
