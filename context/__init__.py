from colorama import Fore, Back, Style
import os, sqlite3
import framework, commands
from framework.AbstractContext import AbstractContext
from context.storage.ArtistRepository import ArtistRepository
from context.storage.SongRepository import SongRepository
from context.storage.OccurrenceRepository import OccurrenceRepository


class Py2KContext(AbstractContext):
    welcome_text = f"""
{Back.WHITE}{Fore.RED} ___________________ _________________________  _______  _______    {Style.RESET_ALL}
{Back.WHITE}{Fore.RED} \__    ___/\_____  \\\\______   \_____  \   _  \ \   _  \ \   _  \   {Style.RESET_ALL}  
{Back.WHITE}{Fore.RED}   |    |    /   |   \|     ___//  ____/  /_\  \/  /_\  \/  /_\  \  {Style.RESET_ALL}
{Back.RED}{Fore.WHITE}   |    |   /    |    \    |   /       \  \_/   \  \_/   \  \_/   \ {Style.RESET_ALL}
{Back.RED}{Fore.WHITE}   |____|   \_______  /____|   \_______ \_____  /\_____  /\_____  / {Style.RESET_ALL}
{Back.RED}{Fore.WHITE}                    \/                 \/     \/       \/       \/  {Style.RESET_ALL}
"""

    # Storage
    artist_repository = None
    song_repository = None
    occurrence_repository = None


    # Status indicator: the latest extracted and transformed edition
    current_edition = 0

    # Holds all the currently extracted and transformed editions
    data = {}

    def init(self):
        super().init()
        db_path = os.environ["DB_FILE"]
        db_dir = os.path.dirname(db_path)

        # Create the directory if it doesn't exist
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        self._conn = sqlite3.connect(os.environ["DB_FILE"])
        self.artist_repository = ArtistRepository(self._conn)
        self.song_repository = SongRepository(self._conn)
        self.occurrence_repository = OccurrenceRepository(self._conn)
        commands.get_command('init').execute(self)


    def commit(self):
        self._conn.commit()

    def get_cursor(self):
        if self.current_edition==0:
            return f"{Style.BRIGHT}> {Style.RESET_ALL}"
        return f"{Fore.MAGENTA}{Style.BRIGHT}[{self.current_edition}]{Style.RESET_ALL}{Fore.WHITE}{Style.BRIGHT}> {Style.RESET_ALL}"


    def set_data(self, latest_edition, data):
        print(f"Setting current edition to {latest_edition}")
        self.current_edition = latest_edition
        self.data = data
