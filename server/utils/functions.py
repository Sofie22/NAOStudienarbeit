import sys
from flask import Response, jsonify
import spacy

from typing import Any
from mariadb import Connection, Error, connect

from NAOStudienarbeit.server import db_connector, sentence_algorithm
from NAOStudienarbeit.server.counter import Counter


def request_handling_get_answer(question: str | None) ->  str  | Response: 
    
    if question is None or len(question) < 1:
        return jsonify("This is the server of nao.")
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(question)
    found_words = sentence_algorithm.sentence_detection(doc)
    
    for i in range(len(found_words)):
        lower_word = found_words[i].lower()
        wd = db_connector.get_generic_term(lower_word)
        if wd is None:
            i += 1
            continue
        found_words[i] = wd
        
    counter = Counter(found_words)
    
    caseID = counter.count_ids()
    
    if caseID is None:
        case_ID_is_non_text = "Ich habe diese Frage nicht verstanden oder ich habe dazu leider keine Antwort."
        print(case_ID_is_non_text)
        return jsonify(case_ID_is_non_text)
    
    answer = db_connector.get_answer(caseID)
    if answer is None:
        answer_is_non_text = "-1"
        print(answer_is_non_text)
        return jsonify(answer_is_non_text)
    
    return answer

def establish_connection()-> Any | Connection: 
    try:
        con = connect(
            host='127.0.0.1',
            port=3306,
            user="root",
            password="passwort",
            database="nao")
        return con
    except Error as e:
        print("Error connecting to MariaDB Platform: ", e)
        sys.exit(1)