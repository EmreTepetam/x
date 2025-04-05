import json
import os

class Settings:
    def __init__(self):
        self.current_language = 'tr'
        self.current_theme = 'light'
        self.languages = {
            'en': self.load_language_file('resources/languages/en.json'),
            'tr': self.load_language_file('resources/languages/tr.json')
        }

    def load_language_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    def set_language(self, language_code):
        if language_code in self.languages:
            self.current_language = language_code

    def translate(self, text):
        return self.languages[self.current_language].get(text, text)

    def set_theme(self, theme):
        self.current_theme = theme

    def get_theme(self):
        if self.current_theme == 'light':
            with open("resources/themes/light.qss", "r") as f:
                return f.read()
        else:
            with open("resources/themes/dark.qss", "r") as f:
                return f.read()