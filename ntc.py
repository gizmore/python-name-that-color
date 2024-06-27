import json
import os
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976
import numpy


def patch_asscalar(a):
    return a.item()


setattr(numpy, "asscalar", patch_asscalar)


class NTC:
    def __init__(self):
        self.current_locale = 'en'
        self.fallback_locale = 'en'
        self.dictionaries = {}
        self.dictionaries_path = {
            'shade': './shades',
            'color': './colors'
        }
        self.build_dictionaries()

    def build_dictionaries(self, locale=None):
        if locale is None:
            locale = self.current_locale

        self.dictionaries = {}

        for name, path in self.dictionaries_path.items():
            try:
                with open(os.path.join(os.path.dirname(__file__), path, f'{locale}.json'), 'r') as f:
                    self.dictionaries[name] = json.load(f)
            except FileNotFoundError:
                with open(os.path.join(os.path.dirname(__file__), path, f'{self.fallback_locale}.json'), 'r') as f:
                    self.dictionaries[name] = json.load(f)
                print(f"ntc: missing '{name}' table for '{locale}' locale, '{self.fallback_locale}' locale will be used as fallback")

        self.current_locale = locale

    def name(self, color, locale=None):
        if not self.is_valid_color(color):
            print(f"'{color}' is not in a recognized color format")
            return None

        if locale and locale != self.current_locale:
            self.build_dictionaries(locale)

        result = {}

        for name, dictionary in self.dictionaries.items():
            best_delta_e = float('inf')
            best_match = None

            for entry in dictionary:
                entry_color = entry[0]
                entry_name = entry[1]

                delta_e = self.calculate_delta_e(color, entry_color)

                if delta_e < best_delta_e:
                    best_match = {
                        'hex': '#' + entry_color,
                        'name': entry_name,
                        'exact': delta_e == 0
                    }
                    best_delta_e = delta_e

                    if delta_e == 0:
                        break

            result[name] = best_match

        return result

    @staticmethod
    def is_valid_color(color):
        try:
            sRGBColor.new_from_rgb_hex(color)
            return True
        except ValueError:
            return False

    @staticmethod
    def calculate_delta_e(color1, color2):
        color1_rgb = sRGBColor.new_from_rgb_hex(color1)
        color2_rgb = sRGBColor.new_from_rgb_hex(color2)

        color1_lab = convert_color(color1_rgb, LabColor)
        color2_lab = convert_color(color2_rgb, LabColor)

        return delta_e_cie1976(color1_lab, color2_lab)
