from NAOStudienarbeit.server.util.consts import EXCLUDED_WORD_POS_TAGS, EXCLUDED_SPECIFIC_TAGS
from NAOStudienarbeit.server.word import Word
# Funktion erhält den erkannten Satz und verarbeitet diesen pro Wort in einer Schleife.
# Danach wird das Wort genauestens untersucht. Am Ende wird der Originalsatz mit dem nun gekürzten Satz verglichen.

found_words = []
token = None

def sentence_detection(sentence):
    
    new_sentence = ""

    for sentence_token in sentence:
        check_word()
    #print("Drin geblieben:"
    #      "\nPos - Tag - Lemma \n")
    #for checked_word in found_words:
    #    print(word.Word.get_word(checked_word))
    #print("-----------------------"
    #      "\nOriginalsatz:"
    #      "\n" + str(sentence) +
    #      "\n-----------------------")
    print("Neuer Satz:")
    new_sentence = " ".join(Word.get_lemma(checked_word) for checked_word in found_words)

    print(new_sentence + "\n-----------------------")

    #Build list of words which can be returned
    words = [Word.get_lemma(wd) for wd in found_words]
    
    return words


# Als erstes wird der POS untersucht. Wenn einer der Fälle eintritt, wird das Wort nicht weiter beachtet,
# sondern in der Konsole mit einigen Daten ausgegeben. Kommt das Wort in keinen der Fälle,
# wird es in einer weiteren Funktion auf den TAG überprüft.
def check_word():
    if not token.pos_ not in EXCLUDED_WORD_POS_TAGS:
        check_specific()
    #else:
    #    print("Rausgeflogen wegen POS:"
    #          " \nText: " + token.text +
    #          " \nLemma: " + token.lemma_ +
    #          " \nPos: " + token.pos_ +
    #          " \nTag: " + token.tag_ +
    #          " \nDep: " + token.dep_ +
    #          " \n-----------------------")


# Nach dem POS wird der TAG untersucht. Wenn einer der Fälle eintritt, wird das Wort nicht gespeichert,
# sondern in der Konsole mit einigen Daten ausgegeben. Kommt das Wort in keinen der Fälle wird es zusammen mit
# dem POS als Liste in die Liste "found_words" eingefügt.
def check_specific():
    if not token.tag_ not in EXCLUDED_SPECIFIC_TAGS:
        new_word = Word(token.pos_, token.tag_, token.lemma_, token.dep_)
        found_words.append(new_word)
    #else:
    #    print("Rausgeflogen wegen TAG:"
    #          " \nText: " + token.text +
    #          " \nLemma: " + token.lemma_ +
    #         " \nPos: " + token.pos_ +
    #          " \nTag: " + token.tag_ +
    #          " \nDep: " + token.dep_ +
    #          " \n-----------------------")