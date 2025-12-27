import commands
import pandas as pd
import os, json, re
from langdetect import detect
from deep_translator import GoogleTranslator
from deep_translator import (GoogleTranslator,
                             batch_detection)

class Translate(commands.AbstractCommand):

    def print_help(self, context):
        print("Checks, fetches and caches translations for song titles")


    def execute(self, context):
        if not hasattr(context, "transformed_data") or context.transformed_data is None:
            print("Data not transformed yet, cannot translate")
            return True
        # load the existing cache data
        with open(os.environ["CACHED_TRANSLATIONS"], "r") as f:
            output = json.load(f)

        titles = []
        for row in self.yield_songs(context.transformed_data):
            title = self.clean_title(row.title)
            if title not in output and not title.isnumeric():
                titles.append(title)
        print('There are %d titles to translate' % len(titles))        
        # Fetch translations with auto language detection and add them to the output
        if len(titles) > 0:
            print("Asking Google for translations")
            translations = GoogleTranslator(source='auto', target='en').translate_batch(titles)
            for i in range(len(titles)):
                title = titles[i]
                translation = translations[i]
                language = 'en' if title==translation else 'other'
                output[title] = {
                    "language": language,
                    "translation": translation
                }
        # Detect the correct language
        others = {k:v for k, v in output.items() if 'language' in v and v['language']=='other'}
        keyset = list(others.keys())
        print(f"There are {len(keyset)} titles to detect the language")
        if len(keyset) > 0:
            print("Detecting languages")
            lang = batch_detection(keyset, api_key=os.environ["DETECT_LANGUAGE_API_KEY"])
            # Update the output with the detected languages
            for i in range(len(keyset)):
                key = keyset[i]
                language = lang[i]
                output[key]['language'] = language
            # # remove english translations
            # for k, v in output.items():
            #     if v["language"] == "en" and "translation" in v:
            #         del v["translation"]
        for k, v in output.items():
            if 'translation' in v:
                v['en_title'] = v['translation'].lower()
                del v['translation']
            else:
                v['en_title'] = k
        with open(os.environ["CACHED_TRANSLATIONS"], "w") as outfile:
            json.dump(output, outfile, indent=2) 
        # apply translations to the transformed data
        for song in self.yield_songs(context.transformed_data):
            clean_title = self.clean_title(song.title)
            if clean_title in output:
                entry = output[clean_title]
                if 'en_title' in entry:
                    song.en_title = entry['en_title']
                if 'language' in entry:
                    song.language = entry['language']
            else:
                print(f"No translation found for title: {song.title} (clean: {clean_title})")
                song.en_title = song.title
                song.language = 'en'
        # Return
        return False


    def yield_songs(self, data):
        for artist in data:
            for song in artist.songs:
                yield song


    def clean_title(self, title):
        # Zoek alles tussen haakjes
        patterns = re.findall(r'\(([^)]*)\)', title)

        # Sleutelwoorden die aangeven dat het om een niet-relevante toevoeging gaat
        ignore_keywords = ['version', 'versie', 'edit', 'mix']

        for p in patterns:
            p_lower = p.lower()
            if any(keyword in p_lower for keyword in ignore_keywords):
                # Verwijder exact deze haakjesinhoud (inclusief haakjes)
                title = re.sub(rf'\s*\({re.escape(p)}\)', '', title)

        # Verwijder dubbele spaties en strip de string
        return re.sub(r'\s{2,}', ' ', title).strip().lower()
