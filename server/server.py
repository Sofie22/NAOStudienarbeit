#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import flask
from flask import request

import db_connector
from transcription import audioToText
from NAOStudienarbeit.server.utils.functions import request_handling_get_answer

app = flask.Flask(__name__)
# Change to False when using in production
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def get_request():
    question = request.args.get('question')
    
    response = request_handling_get_answer(question)
    return response


@app.route('/', methods=['POST'])
def post_request():
    #get file from request flask
    file = request.files['file']
    file.save("audio.wav")
    question = audioToText(os.path.abspath("audio.wav"))
    
    response = request_handling_get_answer(question)
    return response


@app.route('/answers', methods=['GET', 'POST'])
def answers():
    if request.method == 'POST':
        case_id = request.form.get('caseID')
        keywords = request.form.get('keywords')
        answer = request.form.get('answer')
        db_connector.insert_answers(case_id, keywords, answer)
        return 'OK'
    else:
        return db_connector.get_all_answers()


@app.route('/genericTerms', methods=['GET', 'POST'])
def generic_terms():
    if request.method == 'POST':
        gn_id = request.form.get('id')
        generic_term = request.form.get('generic_term')
        db_connector.insert_generic_terms(gn_id, generic_term)
        return 'OK'
    else:
        return db_connector.get_all_generic_terms()


@app.route('/synonyms', methods=['GET', 'POST'])
def synonyms():
    if request.method == 'POST':
        synonym = request.form.get('synonym')
        syn_id = request.form.get('id')
        db_connector.insert_synonyms(synonym, syn_id)
        return 'OK'
    else:
        return db_connector.get_all_synonyms()


@app.route('/weights', methods=['GET'])
def weights():
    return db_connector.get_weights()