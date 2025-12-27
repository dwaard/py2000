import os, yaml
from context.reader.CSVReader import CSVReader
from context.reader.XlrdReader import XlrdReader
from context.reader.OpenPyXlReader import OpenPyXlReader


def get_reader_for(filename, edition, **kwargs):
    filepath = os.path.join(os.environ["RAW_FOLDER"], filename)
    if filepath.endswith(".csv"):
        return CSVReader(filepath, edition, **kwargs)
    if filepath.endswith(".xls"):
        return XlrdReader(filepath, edition, **kwargs)
    if filepath.endswith(".xlsx"):
        return OpenPyXlReader(filepath, edition, **kwargs)
    raise ValueError(f"cannot open a reader for {filepath}")


def has_config_for(edition):
    filename = os.path.join(os.environ["CONFIG_FOLDER"], f"{edition}.yml")
    return os.path.exists(filename)


def get_config(edition):
    filename = os.path.join(os.environ["CONFIG_FOLDER"], f"{edition}.yml")
    with open(filename, 'r') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    config = data
    
    # Ensure 'fileconfig' key is always present
    if 'fileconfig' not in config:
        config['fileconfig'] = {}
    
    return config