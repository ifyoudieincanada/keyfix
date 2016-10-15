#!/usr/bin/env python3

import json
import hunspell
from difflib import SequenceMatcher

directions = ['left', 'top_left', 'top_right', 'right', 'bottom_left', 'bottom_right']

class Key(object):
    """This defines the Key object. It has a series of adjecent keys."""

    def __init__(self, lower_letter, upper_letter, caps_mod):
        self.lower_letter = lower_letter
        self.upper_letter = upper_letter
        self.caps_mod = caps_mod

    def __find_key__(self, key_list, key):
        """Find key by lowercase value in a list of key objects"""
        return next((key_obj for key_obj in key_list if key_obj.lower_letter == key), None)

    def set_surrounding_letters(self, key_dict, key_list):
        """Sets the surrounding keys"""
        self.keys = {}

        for direction in directions:
            try:
                self.keys[direction] = self.__find_key__(key_list, key_dict[direction])
            except:
                self.keys[direction] = None
        return self

    def shift(self, direction):
        """Returns the key in the proposed direction"""
        return self.keys[direction.lower()]

    def print_key(self):
        string = "  "
        string += self.keys['top_left'].lower_letter if self.keys['top_left'] else " "
        string += " "
        string += self.keys['top_right'].lower_letter if self.keys['top_right'] else " "
        string += "\n "
        string += self.keys['left'].lower_letter if self.keys['left'] else " "
        string += " "
        string += self.lower_letter
        string += " "
        string += self.keys['right'].lower_letter if self.keys['right'] else " "
        string += "\n  "
        string += self.keys['bottom_left'].lower_letter if self.keys['bottom_left'] else " "
        string += " "
        string += self.keys['bottom_right'].lower_letter if self.keys['bottom_right'] else " "
        print()
        print(string)
        print()

class Keyboard(object):
    """This defines a keyboard, or a collection of Keys."""

    def __init__(self, layout_file):
        with open(layout_file) as layout:
            data = json.load(layout)
        keys = list(map(self.__make_key__, data))
        self.keys = list(map(lambda key: key[0].set_surrounding_letters(key[1], list(zip(*keys))[0]), keys))

        self.key_dict = {}
        for key in self.keys:
            self.key_dict[key.lower_letter] = key
            self.key_dict[key.upper_letter] = key

    def __make_key__(self, key_dict):
        return (Key(key_dict['letter'], key_dict['upper'], key_dict['caps_mod']), key_dict)

    def __shift_keys__(self, keys, direction):
        return list(map(lambda key: key.shift(direction), keys))

    def __keys_to_string__(self, keys):
        return "".join(list(map(lambda key: key.lower_letter, keys)))

    def __caps_insert__(self,keys):
        return_list = []
        previous = "lower"
        current = "lower"

        for key, letter in keys:
            # After these checks, current may not == previous
            if letter == key.upper_letter:
                current = "upper"

            if letter == key.lower_letter:
                current = "lower"

            # If current != previous, we know that caps lock may have been pressed
            if previous != current:
                return_list.append(self.key_dict['caps'])

            return_list.append(key)

            # Update previous to most recent value
            previous = current

        return return_list

    def shift(self, word):
        """Shift provided word in every direction."""
        # Convert string to list of Keys
        keys = list(zip(map(lambda letter: self.key_dict[letter], word), word))

        # We have inserted the caps keys so we can properly shift
        caps_keys = self.__caps_insert__(keys)

        # For each direction, shift Keys into new Key lists
        words = map(lambda direction: self.__shift_keys__(caps_keys, direction), directions)

        # Filter out Key lists that contain a None character
        real_words = filter(lambda keys: None not in keys, words)

        # Convert Key lists into Strings
        strings = map(lambda keys: self.__keys_to_string__(keys), real_words)

        return [word] + list(strings)

    def print_keyboard(self):
        for key in self.keys:
            key.print_key()

en_US = hunspell.HunSpell("/usr/share/myspell/dicts/en_US.dic", "/usr/share/myspell/dicts/en_US.aff")

def word_with_approximation(word):
    suggestion = en_US.suggest(word)

    if len(suggestion) > 0:
        corrected = suggestion[0].decode("utf-8").lower()
        probability = SequenceMatcher(None, word, corrected).ratio()
        return (corrected, probability)
    else:
        return (word, 0)

def main():
    keyboard = Keyboard("qwerty.json")

    for word in ["y3oo9", "biow", "pkw0", "helli", "j8w7j834w5aje8jt", "boop", "bepo", "beepe", "AJ", "escEJ", "KOGvwr", "yu;rt", "rtkwe"]:
        shifted = keyboard.shift(word)

        found = False
        correct_word = None
        for spelling in shifted:
            if en_US.spell(spelling):
                found = True
                correct_word = spelling


        if not found:
            corrected    = map(word_with_approximation, shifted)
            correct_word = max(corrected, key=lambda pair: pair[1])[0]

        print("Word: " + word)
        print("  Probably: " + correct_word)


if __name__ == "__main__":
    main()
