import csv, codecs, io

class Song:
    """
    Holds information about a T2000 song based on one or more editions. This
    class is responsible for getting the most representable data, including
    key and aliases and can merge two songs together
    """

    editions = []

    def __init__(self, row):
        self.editions.append(row)
        

class SimilarityMatrix:
    """
    Holds a matrix of similarity ratios between
    """



class AliasedDict:
    """
    Implements a dictionary where one or more keys can refer to the same value.
    Handles removal of key-values by removing all the other keys that refer to
    that value.
    """

    def __init__(self, data={}):
        self.data = data
        self.aliases = {}

    def __find_key(self, key):
        """
        Finds the correct key in either the keyset of the dict or the aliases
        """
        if key in self.data:
            return key
        if key in self.aliases:
            return self.aliases[key]
        raise KeyError(key)

    def add_aliases(self, aliases):
        """
        Adds all aliases in the specified dict.
        """
        for alias, key in aliases.items():
            self.aliases[alias] = key

    def get(self, key):
        """
        Gets the value specified by the given key or alias
        """
        return self.data[self.__find_key(key)]

    def add(self, key, value):
        """
        Adds the specifie key-value pair to the dict
        """
        self.data[key] = value

    def pop(self, key):
        """
        Pops the key-value pair from the dict. Also including all aliases that 
        refer to the same value
        """
        key = self.__find_key(key)
        # remove all aliases
        new_aliases = {}
        for alias, aliased_key in self.aliases.items():
            if aliased_key!=key:
                new_aliases[alias] = key
        self.aliases = new_aliases
        # pop from dict and return 
        return self.data.pop(key)



class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def __next__(self):
        return self.reader.__next__().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def __next__(self):
        row = self.reader.__next__()
        return [unicode(s, "utf-8") if isinstance(s, str) else s for s in row]

    def __iter__(self):
        return self



class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = io.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        # self.writer.writerow([s.encode("utf-8") if isinstance(s, str) else s for s in row])
        self.writer.writerow(row)
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

