#!/usr/bin/env python3

import json

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
        if direction.lower() == "left":
            return self.keys['left']
        elif direction.lower() == "up_left":
            return self.keys['top_left']
        elif direction.lower() == "up_right":
            return self.keys['top_right']
        elif direction.lower() == "right":
            return self.keys['right']
        elif direction.lower() == "down_right":
            return self.keys['bottom_right']
        elif direction.lower() == "down_left":
            return self.keys['bottom_left']
        else:
            return None

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

    def __make_key__(self, key_dict):
        return (Key(key_dict['letter'], key_dict['upper'], key_dict['caps_mod']), key_dict)

    def print_keyboard(self):
        for key in self.keys:
            key.print_key()

def main():
    keyboard = Keyboard("qwerty.json")

if __name__ == "__main__":
    main()
