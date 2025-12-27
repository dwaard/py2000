from colorama import Fore, Back, Style
import commands
from context.Artist import Artist
from context.Occurance import Occurance

class Transform(commands.AbstractCommand):

    def print_help(self, context):
        print("Transforms the datastructure into the Artist-Song-Occurance Hierarchy")


    def execute(self, context):
        artists = self.transorm_data(context.data)
        if self.validate(artists):
            context.transformed_data = artists
        return False


    def transorm_data(self, data):
        artists = []

        for s in data:
            # find exact match
            found = False
            for a in artists:
                if a.is_exact_match(s):
                    a.add_song(s)
                    found=True
                    break
            # TODO find simillarities
            # add as new
            if not found:
                artists.append(Artist(s))
                
        print(f"Extracted {len(artists)} artists")
        return artists


    def validate(self, artists):
        songs_with_no_year = []
        for a in artists:
            for s in a.songs:
                if not hasattr(s, 'year'):
                    songs_with_no_year.append(s.artist)
        color = Fore.GREEN
        count = len(songs_with_no_year)
        if count > 0:
            color = Fore.RED
        print(f"{color}Aantal songs zonder jaar: {count}{Style.RESET_ALL}")  

        songs_with_multiple_year = []
        MAX_DIFFERENCE = 10
        for a in artists:
            for s in a.songs:
                yMin = None
                yMax = None
                m = False
                for o in s.occurances:
                    year = o.data[Occurance.YEAR_INDEX]
                    if yMin is None:
                        yMin = year
                    if yMax is None:
                        yMax = year
                    if year < yMin:
                        yMin = year
                    if year > yMax:
                        yMax = year
                if yMax - yMin > MAX_DIFFERENCE:
                    songs_with_multiple_year.append(s)
                    
        print("Aantal songs met teveel spreiding in jaren: {}".format(len(songs_with_multiple_year)))
        for s in songs_with_multiple_year:
            print(s)
            for o in s.occurances:
                print("{} : {}".format(o.data[Occurance.EDITION_INDEX], o))

        #TODO Similarities van artiestnamen per artiest
        #TODO Similarities van artiestnamen binnen songs van een artiest
        #TODO Similarities van titels per song
        #TODO Top 10 meest op elkaar lijkende liedjes: boven een bepaalde similarity grens
        return True
      