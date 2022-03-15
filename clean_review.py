import re
import spacy
from scispacy.abbreviation import AbbreviationDetector
from collections import Counter
import gensim
import heapq
from operator import itemgetter
from multiprocessing import Pool
from gingerit.gingerit import GingerIt

class Review:
    def __init__(self, text):
        self.text = text
        self.cleaned_text = ""
        self.sentences = []
        self.cleaned_sentences = []
        self.words = []
        self.parser = GingerIt()

    def split_dtos(self):
        """
        :param text:
        :return: split document into sentences
        """
        self.sentences = self.text.split("<sssss>")
        return self.sentences

    def split_stow(self):
        """
        :param text:
        :return: split sentence into words
        """
        self.words = self.sentences.split(" ")

    def clean_sentences(self):
        # re.sub：pattern, repl, string
        self.sentences = self.split_dtos()
        for sentence in self.sentences:
            new_sentence = " "
            for word in sentence:
                new_word = self.substitute_emoji(word)
                new_sentence += new_word

            sentence = new_sentence

            # Regular expressions
            sentence = re.sub(r" -lrb- ", " ", sentence)
            sentence = re.sub(r" -rrb- ", " ", sentence)
            sentence = re.sub(r"\s('\w)", r"\1", sentence)
            sentence = re.sub(r"[!?.,-]{2,}", "", sentence)
            sentence = re.sub(r"(\s-|-\s)", "", sentence)
            sentence = re.sub(r"(\s'')+\s", " ", sentence)
            sentence = re.sub(r"(\s``)+\s", " ", sentence)
            sentence = re.sub(r"\s([.,!?])", r"\1", sentence)
            sentence = re.sub(r"@[A-Za-z0-9]+", " ", sentence)
            sentence = re.sub(r"https?://[A-Za-z0-9./]+", " ", sentence)
            sentence = re.sub(r"[^A-Za-z.,!?\-'0-9]", " ", sentence)
            sentence = re.sub("\t", " ",  sentence)
            sentence = re.sub(r" +", " ", sentence)
            sentence = re.sub(r"\s+", " ", sentence)

            # GingerIt correct
            sentence = self.correct_spell(sentence)

            self.cleaned_sentences.append(sentence)
            self.cleaned_text += sentence
            return self.cleaned_text

    def correct_spell(self, text):
        # sentence level
        output = self.parser.parse(text)
        corrected_text = output['result']
        return corrected_text

    def substitute_emoji(self, word):
        # word level
        emoji = {":-)": "happy",
                 ":)": "happy",
                 ":-|": "indecision",
                 ":|": "indecision",
                 ":-(": "frown",
                 ":(": "frown",
                 ":-d": "laughing",
                 ":d": "laughing",
                 ";-)": "skepticism",
                 ";)": "skepticism"}

        if word in emoji:
            return emoji[word]

        return word


    def complete_contraction(self, text):
        # https://www.kdnuggets.com/2021/09/text-preprocessing-methods-deep-learning.html
        contraction_dict = { "n't": "not", "'ve": "have", "'ll": "will", "'s": "is", "'re": "are", "'m": "am", "'d": "would"}

        def get_contractions(contraction_dict):
            contraction_re = re.compile('(%s)' % '|'.join(contraction_dict.keys()))
            #print(contractions_re)
            return contraction_dict, contraction_re

        contractions, contractions_re = get_contractions(contraction_dict)

        def replace_contractions(text):
            def replace(match):
                return contractions[match.group(0)]

            return contractions_re.sub(replace, text)

        return replace_contractions(text)


    def complete_abbreviation(self, text):
        nlp = spacy.load("en_core_web_sm")
        abbreviation_pipe = AbbreviationDetector(nlp)
        nlp.add_pipe(abbreviation_pipe)

    def correct_word(self, text):
        # GoogleNews-vectors-negative300.bin.gz : https://drive.google.com/u/0/uc?id=0B7XkCwpI5KDYNlNUTTlSS21pQmM&export=download
        model = gensim.models.KeyedVectors.load_word2vec_format(
            '../input/embeddings/GoogleNews-vectors-negative300/GoogleNews-vectors-negative300.bin',
            binary=True)
        words = model.index2word

        w_rank = {}
        for i, word in enumerate(words):
            w_rank[word] = i

        WORDS = w_rank

        def words(text):
            return re.findall(r'\w+', text.lower())

        def P(word):
            "Probability of `word`."
            # use inverse of rank as proxy
            # returns 0 if the word isn't in the dictionary
            return - WORDS.get(word, 0)

        def correction(word):
            "Most probable spelling correction for word."
            return max(candidates(word), key=P)

        def candidates(word):
            "Generate possible spelling corrections for word."
            return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

        def known(words):
            "The subset of `words` that appear in the dictionary of WORDS."
            return set(w for w in words if w in WORDS)

        def edits1(word):
            "All edits that are one edit away from `word`."
            letters = 'abcdefghijklmnopqrstuvwxyz'
            splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
            deletes = [L + R[1:] for L, R in splits if R]
            transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
            replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
            inserts = [L + c + R for L, R in splits for c in letters]
            return set(deletes + transposes + replaces + inserts)

        def edits2(word):
            "All edits that are two edits away from `word`."
            return (e2 for e1 in edits1(word) for e2 in edits1(e1))

        def build_vocab(texts):
            sentences = texts.apply(lambda x: x.split()).values
            vocab = {}
            for sentence in sentences:
                for word in sentence:
                    try:
                        vocab[word] += 1
                    except KeyError:
                        vocab[word] = 1
            return vocab

        # train.question_text = "test"
        vocab = build_vocab()

        #heapq.nlargest(n, iterable, key=None) 从 iterable 所定义的数据集中返回前 n 个最大元素组成的列表。
        top_90k_words = dict(heapq.nlargest(90000, vocab.items(), key=itemgetter(1)))

        pool = Pool(4)
        corrected_words = pool.map(correction, list(top_90k_words.keys()))

        for word, corrected_word in zip(top_90k_words, corrected_words):
            if word != corrected_word:
                print(word, ":", corrected_word)