import re
from gingerit.gingerit import GingerIt

def split_dtos(text):
    """
    :param text:
    :return: split document into sentences
    """
    sentences = text.split("<sssss>")
    return sentences


def split_stow(sentence):
    """
    :param text:
    :return: split sentence into words
    """
    words = sentence.split(" ")
    return words

def clean_sentences(text):
    # re.sub：pattern, repl, string
    sentences = split_dtos(text)
    cleaned_text = ""
    for sentence in sentences:
        new_sentence = " "
        for word in sentence:
            new_word = substitute_emoji(word)
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
        sentence = re.sub("\t", " ", sentence)
        sentence = re.sub(r" +", " ", sentence)
        sentence = re.sub(r"\s+", " ", sentence)

        # GingerIt correct
        sentence = correct_spell(sentence)

        cleaned_text += sentence
        return cleaned_text


def correct_spell(text):
    # sentence level
    parser = GingerIt()
    output = parser.parse(text)
    corrected_text = output['result']
    return corrected_text


def substitute_emoji(word):
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

if __name__ == '__main__':
    text = ":) haha <sssss> the restaruant is great!!!!! <sssss> -lrb i like the food, btw the char is nice <sssss> i ll go back again -rrb @ you "
    c_text = "happy haha the restaurant is great!  i like the food, btw the char is nice i will go back again you"
    print(clean_sentences(text))