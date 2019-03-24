from enum import Enum

data_dir = 'algorithm/data/'

positive_connotation = 'positive'
negative_connotation = 'negative'

first_person = 'first'
second_person = 'second'

pronoun_dir = data_dir + 'pronouns/'
pronoun_first_file_path = pronoun_dir + first_person
pronoun_second_file_path = pronoun_dir + second_person

white_list_regex_dir = data_dir + 'white_list_regex/'
white_list_positive_regex_file_path = white_list_regex_dir + positive_connotation
white_list_negative_regex_file_path = white_list_regex_dir + negative_connotation

words_dir = data_dir + 'words/'
words_positive_file_path = words_dir + positive_connotation
words_negative_file_path = words_dir + negative_connotation

negations_file_path = data_dir + 'negations'
meta_cognition_dir = 'algorithm/data/'

def new_name_list(file_path):
    list = []
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            list.append(line)

    return list

class MCComponents:
    def __init__(self, positive_file, negative_file):
        self.positive = new_name_list(positive_file)
        self.negative = new_name_list(negative_file)

class Pronouns:
    def __init__(self, first_file, second_file):
        self.first = new_name_list(first_file)
        self.second = new_name_list(second_file)

class MCPhrase:

    def __init__(self, phrase, connotation):
        self.phrase = phrase
        self.connotation = connotation

    def __str__(self):
        return "{} | {}".format(self.phrase, self.connotation)
    def __repr__(self):
        return self.__str__()

class MCOracle:
    def __init__(self):
        self.pronouns = Pronouns(pronoun_first_file_path, pronoun_second_file_path)

        self.white_list_regex = MCComponents(white_list_positive_regex_file_path, white_list_negative_regex_file_path)

        self.words = MCComponents(words_positive_file_path, words_negative_file_path)

        self.negations = new_name_list(negations_file_path)


class Connotation(Enum):
    NEGATIVE = -1
    POSITIVE = 1

    @property
    def bootstrap_color(self):
        if self == Connotation.NEGATIVE:
            return "danger"
        else:
            return "success"
    def __str__(self):
        if self == Connotation.NEGATIVE:
            return "NEG"
        else:
            return "POS"