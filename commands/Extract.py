import json, os
from colorama import Fore, Back, Style
from datetime import datetime
import commands
from context import reader
from context.EditionProcessor import EditionProcessor

class Extract(commands.AbstractCommand):
    
    def print_help(self, context):
        print("Tries to import data from the current edition up to the given edition")


    def execute(self, context):
        edition_to_import = context.current_edition + 1
        if len(self.args) > 0:
            # The optional user argument is assumed to be the edition
            edition_to_import_to = int(self.args[0])
            # validate
            if edition_to_import_to <= context.current_edition:
                raise ValueError("already imported up to this edition")
        else:
            edition_to_import_to = datetime.now().year

        while reader.has_config_for(edition_to_import) and edition_to_import <= edition_to_import_to:
            self.extract_transform(context, edition_to_import)
            edition_to_import += 1

        # Save the context data to a json cache file
        with open(os.environ["CACHED_DATA"], "w") as outfile:
            json.dump([song.to_dict() for song in context.data], outfile, indent=2)        
            
        return False


    def extract_transform(self, context, edition):
        print(f"{Fore.GREEN}Extracting edition {edition}{Style.RESET_ALL}")

        config = reader.get_config(edition)

        processor = EditionProcessor(edition_reader=reader.get_reader_for(config["filename"], edition, **config["fileconfig"]), 
                                    existing_data=context.data,
                                    min_certain_ratio=config["min_certain_ratio"],
                                    min_relevant_ratio=config["min_relevant_ratio"])

        processor.process_new_songs()
        processor.process_exact_matches()
        processor.process_manual_matches(config["manual_matches"])
        processor.process_near_matches()
        processor.process_rest_as_new()
        processor.print_status()
        if processor.has_problems():
            processor.print_problems()
            raise ValueError(f"found problems in edition {edition}")
        context.set_data(edition, processor.merge(context.data))
