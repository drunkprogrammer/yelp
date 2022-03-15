# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from read_file import read_file
from clean_review import Review


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    yelp13_train = read_file('./data/yelp_13/yelp-2013-seg-20-20.train.ss')
    # yelp13_dev = read_file('./data/yelp_13/yelp-2013-seg-20-20.dev.ss')
    # yelp13_test = read_file('./data/yelp_13/yelp-2013-seg-20-20.test.ss')

    documents_processed = []
    for document in yelp13_train:
        user = document[0]
        product = document[1]
        text = document[2]
        label = document[3]

        document_processed = []
        yelp13_review = Review(text)
        sentences = yelp13_review.split_dtos(text)

        for sentence in sentences:
            sentence_cleaned = yelp13_review.clean_text(sentence)
            sentence_completed = yelp13_review.complete_contraction(sentence_cleaned)
            document_processed.append(sentence_completed)

        documents_processed.append(list([user, product, document_processed, label]))

    print(documents_processed[:5])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
