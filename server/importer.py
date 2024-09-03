#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import db_connector
import weighting


def import_data():
    db_connector.clear_tables()
    
    answers = json.load(open('database_files/answers.json'))
    generic_terms = json.load(open('database_files/generic_terms.json'))
    synonyms = json.load(open('database_files/synonyms.json'))
    
    # Prepare data for batch insertion
    answers_batch = [(answer["caseID"], answer["primary_keywords"], answer["secondary_keywords"], answer["answer"]) for answer in answers]
    db_connector.insert_answers_batch(answers_batch)
    
    generic_terms_batch = [(generic_term["id"], generic_term["generic_term"]) for generic_term in generic_terms]
    db_connector.insert_generic_terms_batch(generic_terms_batch)
    
    synonyms_batch = [(synonym["synonym"], synonym["id"]) for synonym in synonyms]
    db_connector.insert_synonyms_batch(synonyms_batch)
    
    weights = weighting.calculate_weight()
    weights_batch = [(weight["keyword"], weight["count"]) for weight in weights]
    db_connector.insert_weights_batch(weights_batch)
    
    return True