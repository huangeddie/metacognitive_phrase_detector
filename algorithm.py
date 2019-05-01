import logging
import re
import string

from algorithm.data import MCOracle, Connotation, MCPhrase

class Annotation:
    BEGIN = 'BEGIN_MC_PHRASE'
    END = 'END_MC_PHRASE'
    BEGIN_POSITIVE = BEGIN + 'POSITIVE'
    BEGIN_NEGATIVE = BEGIN + 'NEGATIVE'

class TokenMask:
    mask_text = '[MASK]'
    def __init__(self, token, mask=False):
        self.token = token
        self.mask = mask

    @property
    def masked_token(self):
        return self.token if not self.mask else self.mask_text

class TextMask:
    def __init__(self, text):
        tokens = text.split()
        self.token_masks = list(map(lambda token: TokenMask(token), tokens))
        self.mask_tokens()

    @property
    def masked_text(self):
        tokens = list(map(lambda token_mask: token_mask.masked_token, self.token_masks))
        ret = ' '.join(tokens)
        return ret

    @property
    def raw_text(self):
        tokens = list(map(lambda token_mask: token_mask.token, self.token_masks))
        ret = ' '.join(tokens)
        return ret

    def update_token_masks(self, new_text):
        new_tokens = new_text.split()
        num_tokens = len(new_tokens)
        if num_tokens != len(self.token_masks):
            raise Exception("number of tokens do not match")

        for i in range(num_tokens):
            token = new_tokens[i]
            if token != TokenMask.mask_text:
                # edit the token
                token_mask = self.token_masks[i]
                token_mask.token = token
        self.mask_tokens()

    def mask_tokens(self):
        in_annotation = False
        for token_mask in self.token_masks:
            if Annotation.BEGIN in token_mask.masked_token:
                in_annotation = True
                token_mask.mask = True

            elif Annotation.END in token_mask.masked_token:
                in_annotation = False
                # Last token to mask in this annotation
                token_mask.mask = True

            elif in_annotation:
                # Currently in an annotated piece of text
                # Mask it
                token_mask.mask = True

            else:
                # Do nothing
                pass


def analyze_text(text, pos_begin='\033[42;37m', neg_begin='\033[41;37m', end='\033[m'):
    """
    Arguably the most important function.
    :param text:
    :return: the mc phrases, annotated bootstrap text
    """

    oracle = MCOracle()

    text = _lowercase_remove_punctuation(text)
    
    text = text.replace('790361b7e5', 'don')

    max_phrase_length = 5

    mc_phrases = []

    text_mask = TextMask(text)

    # Search for annotated phrases by regular expression
    for connotation, list in [(Connotation.NEGATIVE, oracle.white_list_regex.negative), (Connotation.POSITIVE, oracle.white_list_regex.positive)]:
        regex_positive_phrases, text_mask = _analyze_regex_phrases(text_mask, connotation, list)

        mc_phrases += regex_positive_phrases


    tokens = text_mask.raw_text.split()

    # Start looking for meta phrases
    count_down = -1
    negative = False
    in_annotation = False
    for i, word in enumerate(tokens):
        # If word is already marked as metacognitive, ignore it
        if Annotation.BEGIN in word:
            in_annotation = True
            continue
        elif Annotation.END in word:
            in_annotation = False
            # Start over
            count_down = -1
            negative = False
        elif in_annotation:
            continue

        elif word in oracle.pronouns.first:
            # Start fresh
            count_down = max_phrase_length
            negative = False

        elif word in oracle.pronouns.second:
            # Start over
            count_down = -1
            negative = False

        elif count_down >= 0:
            keyword = None

            if word in oracle.negations:
                negative = not negative
            elif word in oracle.words.positive:
                keyword = Connotation.POSITIVE
            elif word in oracle.words.negative:
                keyword = Connotation.NEGATIVE

            if keyword is not None:
                # inclusive, inclusive
                start_index, end_index = (i - (max_phrase_length - count_down), i)

                phrase = ' '.join([tokens[k] for k in range(start_index, end_index + 1)])

                if (keyword == Connotation.POSITIVE and not negative) or (keyword == Connotation.NEGATIVE and negative):
                    connotation = Connotation.POSITIVE
                else:
                    connotation = Connotation.NEGATIVE

                mc_phrase = MCPhrase(phrase, connotation)

                # Annotate it
                tokens[start_index] = (Annotation.BEGIN_POSITIVE if connotation == Connotation.POSITIVE else Annotation.BEGIN_NEGATIVE)\
                                      + tokens[start_index]
                tokens[end_index] += Annotation.END

                # Add phrase to list
                mc_phrases.append(mc_phrase)
        else:
            # Start over
            count_down = -1
            negative = False

        count_down -= 1
        count_down = max(-1, count_down)

    # Create the annotated post
    annotated_post = ' '.join(tokens)

    annotated_post = re.sub(Annotation.BEGIN_POSITIVE, pos_begin, annotated_post)
    annotated_post = re.sub(Annotation.BEGIN_NEGATIVE, neg_begin, annotated_post)

    annotated_post = re.sub(Annotation.END, end, annotated_post)

    return mc_phrases, annotated_post


def _lowercase_remove_punctuation(text):
    text = text.lower()
    exclude = set(string.punctuation + 'â€™')
    text = ''.join(ch for ch in text if ch not in exclude)
    return text


def _analyze_regex_phrases(text_mask, connotation, phrases):
    """
    Analyzes regular expressions
    :param text_mask:
    :param bootstrap_color:
    :param phrases:
    :return: A list of meta phrases found and the newly annotated text
    """

    mc_phrases = []

    for phrase in phrases:
        phrase = phrase.lower()
        if phrase.strip() == '':
            continue

        text = text_mask.masked_text

        matches = re.findall('(' + phrase + ')', text)
        text = re.sub('(' + phrase + ')', f'{Annotation.BEGIN_POSITIVE if connotation == Connotation.POSITIVE else Annotation.BEGIN_NEGATIVE}\\1{Annotation.END}', text)

        text_mask.update_token_masks(text)

        for match in matches:
            if type(match) == tuple:
                foo = match[0]
            else:
                foo = match
            mc_phrase = MCPhrase(foo, connotation)
            logging.debug('Found {}'.format(mc_phrase))
            mc_phrases.append(mc_phrase)

    return mc_phrases, text_mask


def number_of_phrases(mc_phrases):
    """
    Returns the number of positive and negative phrases in the list of
    MCPhrases
    :param mc_phrases:
    :return:
    """
    positive_phrases = list(filter(lambda phrase: phrase.connotation == Connotation.POSITIVE, mc_phrases))
    negative_phrases = list(filter(lambda phrase: phrase.connotation == Connotation.NEGATIVE, mc_phrases))

    return len(positive_phrases), len(negative_phrases)