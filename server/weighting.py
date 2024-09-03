#!/usr/bin/python
# -*- coding:utf-8 -*-

import db_connector


# calculate weightings of distinct keywords from input list
# TODO: check if calculation of weighting is correct
weightings = []

def calculate_weight() -> list:
    keywords = db_connector.get_all_keywords()
    
    keywords_amount = len(keywords)
    
    weightings = [distinct_list(keyword) for keyword in keywords]
    
    for i in range(len(weightings)):
        weightings[i]["count"] = 1 - (weightings[i]["count"] / keywords_amount)
    
    return weightings


# write distinct keywords with their count in a list and return
def distinct_list(keyword: str) -> list:
    
    for i in range(len(weightings)):
            if keyword ==  weightings[i].get("keyword"):
                weightings[i].update({"count":  weightings[i].get("count") + 1})
                
    dict_record = {"keyword": keyword, "count": 1}
    weightings.append(dict_record)
    return weightings