import analyzer
import db


class YearAnalyzer(analyzer.Analyzer):

    def _find_anomalies(self):
        print "finding songs with year=1800"
        for song in db.song_repository.read_all(where='year=1800'):
            yield song

    def _print_current_intro(self):
        song = self._get_current()
        artist = db.artist_repository.read_rowid(song['artist'])
        print 120 * "="
        print "Het jaar van dit nummer klopt niet: "
        print "%s - %s (%d)" % (artist['name'], song['title'], song['year'])
        print ""

    def _get_options(self):
        r = analyzer.DEFAULT_OPTIONS[:]
        r.insert(0, ('1801..9999', 'Het correcte jaar'))
        return r

    def _process_command(self, c):
        if not super(YearAnalyzer, self)._process_command(c):
            new_year = self.get_year(c)
            if not new_year:
                print "%s is een ongeldige keuze [1801..2099]" % c
                return
            song = self._get_current()
            artist = db.artist_repository.read_rowid(song['artist'])
            db.swaprule_repository.append([
                artist['name'],
                song['title'],
                song['year'],
                None,
                None,
                new_year,
                -1
            ])
            db.commit()
            self._next()


    def get_year(self, text):
        try:
            value = int(text)
            if 1800 < value < 2100:
                return value
            else:
                return 0
        except ValueError:
            return 0
