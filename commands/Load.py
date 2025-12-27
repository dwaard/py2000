import commands

class Load(commands.AbstractCommand):

    def print_help(self, context):
        print("Loads the transformed data to the configured datastore")


    def execute(self, context):
        # Clear the tables
        context.occurrence_repository.truncate()
        context.song_repository.truncate()
        context.artist_repository.truncate()
        # Fill with new data
        for a in context.transformed_data:
            a_id = context.artist_repository._insert_row([a.name])
            for s in a.songs:
                en_title = getattr(s, 'en_title', None)
                language = getattr(s, 'language', None)
                s_id = context.song_repository.append(a_id, s.title, s.year, language, en_title)
                for o in s.occurances:
                    context.occurrence_repository.append([s_id] + o.data)            
        # Write to the database
        context.commit()        
        return False
