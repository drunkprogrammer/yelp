from clean_review2 import split_dtos, clean_sentences, correct_spell
from clean_review import Review
import unittest


# ----------------------
# test case 1:
"""
 this place is great ! 
 <sssss> good food , and good service .
 <sssss> we had a large group hh and our server jay was very patient and happy to suggest plates over others . 
 <sssss> i told him my dad was back in the us from afghanistan and the owner came out to let me dad know all his drinks/meal were on the house ! 
 <sssss> whoot whoot !!
 <sssss> america !! 
 <sssss> f ** ck yea !! 
"""

# ----------------------

class TestReview(unittest.TestCase):

    def test_split_doc_to_sentences(self):
        text = "this place is great ! <sssss> good food , and good service . <sssss> we had a large group hh and our server jay was very patient and happy to suggest plates over others . <sssss> i told him my dad was back in the us from afghanistan and the owner came out to let me dad know all his drinks/meal were on the house ! <sssss> whoot whoot !! <sssss> america !! <sssss> f ** ck yea !! "
        s_text = ['this place is great ! ',
                 ' good food , and good service . ',
                 ' we had a large group hh and our server jay was very patient and happy to '
                 'suggest plates over others . ',
                 ' i told him my dad was back in the us from afghanistan and the owner came '
                 'out to let me dad know all his drinks/meal were on the house ! ',
                 ' whoot whoot !! ',
                 ' america !! ',
                 ' f ** ck yea !! ']
        review1 = Review(text)
        self.assertEqual(review1.split_dtos(), s_text)

    def test_clean_sentences(self):
        text = ":) haha <sssss> the restaruant is great!!!!! <sssss> -lrb i like the food, btw the char is nice <sssss> i ll go back again -rrb @ you "
        c_text = "happy haha the restaurant is great!  i like the food, btw the char is nice i will go back again you"
        self.assertEqual(clean_sentences(text), c_text)

    def test_correct_spell(self):
        text = "i ll got"
        cc_text = " I will go"
        print(correct_spell(text))

        #self.assertEqual(correct_spell(text), cc_text)

if __name__ == '__main__':
    unittest.main()