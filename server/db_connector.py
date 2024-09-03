#!/usr/bin/python
# -*- coding:utf-8 -*-

# TODO: Specify Docs of function, add Doc for File and variables
import json
from NAOStudienarbeit.server.utils.functions import establish_connection


# TODO: Add check for empty list, raise EmptyListError
# TODO: change output to real json object

        
def get_all_synonyms() -> str:
    """Return all synonyms

    ADD DESCRIPTION

    :return: JSON as string
    :raise
    """
    con = establish_connection()

    cur = con.cursor()
    reqstr = f"SELECT synonym, id FROM synonyms ORDER BY id"
    cur.execute(reqstr)
    syn_list = [{'synonym': synonym, 'id': syn_id} for synonym, syn_id in cur]

    json_str = json.dumps(syn_list)
    con.close()
    return json_str


# TODO: add checks for wrong returns, raise Error
# TODO: change output to real json object
def get_all_generic_terms() -> str:
    """Return all generic terms

    ADD DESCRIPTION

    :return: JSON as string
    """
    con = establish_connection()

    cur = con.cursor()
    reqstr = f"SELECT id, generic_term FROM generic_terms ORDER BY id"
    cur.execute(reqstr)
    
    gt_list = [{'id': gt_id, 'generic_term': generic_term} for gt_id, generic_term in cur]
    
    json_str = json.dumps(gt_list)
    con.close()
    return json_str


# TODO: add checks for wrong returns, raise error
# TODO: change output to real json object
def get_all_answers():
    """Return all answers

    ADD DESCRIPTION

    :return: JSON as string
    """
    con = establish_connection()
    cur = con.cursor()
    reqstr= f"SELECT caseID, primary_keywords, secondary_keywords, answer FROM matching_table ORDER BY caseID"
    cur.execute(reqstr)
    ans_list = [
                {'caseID': case_id, 'primary_keywords': primary_keywords, 'secondary_keywords': secondary_keywords,'answer': answer} 
                for case_id, primary_keywords, secondary_keywords, answer in cur
        ]
    
    json_str = json.dumps(ans_list)
    con.close()
    return json_str


def get_all_keywords() -> list:
    con = establish_connection()
    cur = con.cursor()
    reqstr = f"SELECT primary_keywords, secondary_keywords FROM matching_table"
    cur.execute(reqstr)
    keywords = [kword for primary_keywords, secondary_keywords in cur for kword in primary_keywords.split(",") + secondary_keywords.split(",")]

    return keywords


# TODO: add checks for wrong returns, raise Error
def get_generic_term(synonym: str) -> str:
    """Search for the generic term of a synonym.

    :param synonym: String of the word for which the generic term should be found.
    :return: Returns the generic term as a string if there is one for the synonym.
    :raise RASENError: Generic term is not in the database table.
    """
    con = establish_connection()
    cur = con.cursor()

    # Get the synonym ID
    reqstr_get_synonym_id = f"SELECT id FROM synonyms WHERE synonym=%s"
    cur.execute(reqstr_get_synonym_id, (synonym,))
    synonym_id = cur.fetchone()
    
    if synonym_id is None:
        con.close()
        return None
    
    # Get the generic term associated with the synonym ID
    reqstr_get_gen_term = f"SELECT generic_term FROM generic_terms WHERE id=%s"
    cur.execute(reqstr_get_gen_term, (synonym_id[0],))
    gen_term = cur.fetchone()
    
    con.close()
    return gen_term[0] if gen_term else None


# TODO: add check for wrong case_id, raise InvalidCaseIDError
def get_answer(case_id: int) -> str:
    """Returns the answer for case_id

    ADD DESCRIPTION

    :param case_id: Integer of the specific answer.
    :return: Returns the answer as string if there is one.
    :raise InvalidCaseIDError: case_id is not in the database table.
    """
    con = establish_connection()

    # Get cursor
    cur = con.cursor()
    reqstr = f"SELECT answer FROM matching_table WHERE caseID={case_id}"
    cur.execute(reqstr)
    ans = "".join([answer[0] for answer in cur])
    
    con.close()
    return ans


def get_caseIDs_by_keywords(word: str):
    con = establish_connection()
    
    cur = con.cursor()
    reqstr = f"SELECT caseID FROM matching_table WHERE primary_keywords LIKE '%{word}%' OR secondary_keywords LIKE '%{word}%'"
    cur.execute(reqstr)
    cID = [caseID[0] for caseID in cur]
    
    if len(cID) == 0:
        con.close()
        return None
    con.close()
    return cID


def get_weight_of_keyword(keyword: str) -> float:
    con = establish_connection()
    cur = con.cursor()
    reqstr = f"SELECT weight FROM weights WHERE keyword=%s"
    cur.execute(reqstr, (keyword,))
    weight = cur.fetchone()

    con.close()
    return weight[0] if weight else 0


def get_primary_keywords_by_caseID(caseID: int):
    con = establish_connection()
    
    cur = con.cursor()
    reqstr = f"SELECT primary_keywords FROM matching_table WHERE caseID='{caseID}'"
    cur.execute(reqstr)
    pri_key = [primary_keywords[0] for primary_keywords in cur] or None

    con.close()
    return pri_key


def get_weights():
    con = establish_connection()
    
    cur = con.cursor()
    reqstr = f"SELECT keyword, weight FROM weights"
    cur.execute(reqstr)
    weights = []
    weights = [{'keyword': keyword, 'weight': weight} for keyword, weight in cur]
    
    json_str = json.dumps(weights)
    con.close()
    return json_str


# TODO: Add checks for arguments to catch wrong data
def insert_answers_batch(answers: list):
    """Insert multiple answers into the matching table in a single batch.

    :param answers: A list of tuples where each tuple contains (case_id, primary_keywords, secondary_keywords, answer)
    """
    con = establish_connection()
    cur = con.cursor()
    cur.executemany(
        "INSERT INTO matching_table (caseID, primary_keywords, secondary_keywords, answer) VALUES (%s, %s, %s, %s)",
        answers
    )
    con.commit()
    con.close()
    print(f"{len(answers)} answers inserted.")
    
    
# TODO: Add checks for arguments to catch wrong data
def insert_generic_terms_batch(generic_terms_batch: list):
    """Insert multiple generic terms into the generic_terms table in a single batch.

    :param generic_terms_batch: A list of tuples where each tuple contains (id, generic_term)
    """
    con = establish_connection()
    cur = con.cursor()
    
    cur.executemany(
        "INSERT INTO generic_terms (id, generic_term) VALUES (%s, %s)",
        generic_terms_batch
    )
    
    con.commit()
    con.close()
    print(f"{len(generic_terms_batch)} generic terms inserted.")

# TODO: Add checks for arguments to catch wrong data
def insert_synonyms_batch(synonyms_batch: list):
    """Insert multiple synonyms into the synonyms table in a single batch.

    :param synonyms_batch: A list of tuples where each tuple contains (synonym, id)
    """
    con = establish_connection()
    cur = con.cursor()
    
    cur.executemany(
        "INSERT INTO synonyms (synonym, id) VALUES (%s, %s)",
        synonyms_batch
    )
    
    con.commit()
    con.close()
    print(f"{len(synonyms_batch)} synonyms inserted.")

def insert_weights_batch(weights_batch: list):
    """Insert multiple weights into the weights table in a single batch.

    :param weights_batch: A list of tuples where each tuple contains (keyword, weight)
    """
    con = establish_connection()
    cur = con.cursor()
    
    cur.executemany(
        "INSERT INTO weights (keyword, weight) VALUES (%s, %s)",
        weights_batch
    )
    
    con.commit()
    con.close()
    print(f"{len(weights_batch)} weights inserted.")
    
def clear_tables():
    """Clears all 4 tables in the database

    :return: no return
    """
    con = establish_connection()
    # Get cursor
    cur = con.cursor()
    cur.execute("DELETE FROM matching_table")
    cur.execute("DELETE FROM synonyms")
    cur.execute("DELETE FROM generic_terms")
    cur.execute("DELETE FROM weights")
    con.commit()
    con.close()

# def init_db_connection():
#     """Initialize Database Connection
#
#     Initializes the connection to the database with specific data.
#     """
#     try:
#         global conn
#         conn = connect(
#             host='127.0.0.1',
#             port=3306,
#             user="root",
#             password="passwort",
#             database="nao"
#         )
#     except Error as e:
#         print("Error connecting to MariaDB Platform: ", e)
#         sys.exit(1)
#
#     # Get cursor
#     global cur
#     cur = conn.cursor()
#     print("Database connection initialized!")


# def close_db_connection():
#     """Close Database Connection
#     """
#     conn.close()
#     print("Database connection closed!")