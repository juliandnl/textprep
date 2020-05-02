"""Preprocessing for natural language processing.

@date: 02.05.2020
@author: Julian Kortendieck
@email: julian@dnlab.de
"""


class TextCleaner:
    def __init__(self, text=None):
        self.text = text

    def __repr__(self):
        return 'TextCleaner(text="{}")'.format(self.text)

    def remove_currencies(self):
        result = re.sub(CURRENCY_REGEX, "", self.text)
        return result


class TextExtractor(TextCleaner):
    def __init__(self, text=None):
        super(TextCleaner, self).__init__()
        self.text = text

    def __repr__(self):
        return 'TextExtractor(text="{}")'.format(self.text)


class TextMetrics(TextCleaner):
    def __init__(self, text=None):
        super(TextCleaner, self).__init__()
        self.text = text

    def __repr__(self):
        return 'TextMetrics(text="{}")'.format(self.text)
