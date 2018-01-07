DEFAULT_PROMPT = 'Kies een optie'
DEFAULT_OPTIONS = [
    ('I', 'Deze anomalie overslaan'),
    ('Q', 'Analyseren van jaren afsluiten')
]


class Analyzer(object):

    def __init__(self):
        self.__anomalies = []
        self.__current = None

    def start(self):
        self.__anomalies = []
        for song in self._find_anomalies():
            self.__anomalies.append(song)
        self._next()

    def _find_anomalies(self):
        print "finding anomalies"
        return None

    def handle_anomalies(self):
        self._print_intro()
        while self.__current:
            self._print_current_intro()
            self._process_command(self._get_command())

    def _get_command(self):
        for key, value in self._get_options():
            print '%s: %s' % (key, value)
        return raw_input('%s: ' % self._get_prompt()).upper()

    def _get_options(self):
        return DEFAULT_OPTIONS

    def _get_prompt(self):
        return DEFAULT_PROMPT

    def _process_command(self, c):
        if c == 'Q':
            print "Analyse wordt afgebroken"
            self.__anomalies = []
            self._next()
            return True
        if c == 'I':
            print "Afwijking wordt overgeslagen"
            self._next()
            return True
        return False

    def _next(self):
        if self._get_current() in self.__anomalies:
            self.__anomalies.remove(self.__current)
        if len(self.__anomalies) > 0:
            self.__current = self.__anomalies[0]
        else:
            self.__current = None

    def _get_current(self):
        return self.__current

    def _print_intro(self):
        if self.__current:
            print "%d mogelijke afwijkingen gevonden" % len(self.__anomalies)

    def _print_current_intro(self):
        print 120 * "="
        print self.__current