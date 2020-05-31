import collections
import re

from plover.steno import sort_steno_strokes
from plover import system

Suggestion = collections.namedtuple('Suggestion', 'text steno_list')


class StrokeDisplay:
    def __init__(self):
        self.number_map = {v.replace('-', ''): k.replace('-', '')
                           for k, v in system.NUMBERS.items()}
        self.re_digit_pattern = re.compile(r'\d')

    def swap_numbers_for_letters(self, stroke):
        if self.re_digit_pattern.search(stroke):
            digits_swapped = '#'
            for c in stroke:
                if self.re_digit_pattern.search(c):
                    digits_swapped += self.number_map[c]
                else:
                    digits_swapped += c
            return digits_swapped
        else:
            return stroke


class Suggestions:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.stroke_display = StrokeDisplay()

    def number_transform(self, strokes_list):
        return [[self.stroke_display.swap_numbers_for_letters(s) for s in sl]
                for sl in strokes_list]

    def find(self, translation):
        suggestions = []

        mods = [
            '%s',  # Same
            '{^%s}',  # Prefix
            '{^}%s',
            '{^%s^}',  # Infix
            '{^}%s{^}',
            '{%s^}',  # Suffix
            '%s{^}',
            '{&%s}',  # Fingerspell
            '{#%s}',  # Command
        ]

        possible_translations = {translation}

        # Only strip spaces, so patterns with \n or \t are correctly handled.
        stripped_translation = translation.strip(' ')
        if stripped_translation and stripped_translation != translation:
            possible_translations.add(stripped_translation)

        lowercase_translation = translation.lower()
        if lowercase_translation != translation:
            possible_translations.add(lowercase_translation)

        similar_words = self.dictionary.casereverse_lookup(translation.lower())
        if similar_words:
            possible_translations |= set(similar_words)

        for t in possible_translations:
            for modded_translation in [mod % t for mod in mods]:
                strokes_list = self.dictionary.reverse_lookup(modded_translation)
                if not strokes_list:
                    continue
                strokes_list = self.number_transform(sort_steno_strokes(strokes_list))
                suggestion = Suggestion(modded_translation, strokes_list)
                suggestions.append(suggestion)
        return suggestions

