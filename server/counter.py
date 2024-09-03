import db_connector


class Counter: 
    def __init__(self, question: list): 
        self.question = question
        self.counters = []

    def count_ids(self) -> int:
        for word in self.question:
            self.process_word(word)

        return self.check_for_highest_id()

    def process_word(self, word: str) -> None:
        keyword_weight = db_connector.get_weight_of_keyword(word) or 0

        ids = db_connector.get_caseIDs_by_keywords(word)
        if ids is None:
            return

        for case_id in ids:
            self.counters = self.update_counters(case_id, keyword_weight)

    def update_counters(self, case_id: int, weight: float) -> list:
        for counter in self.counters:
            if case_id == counter["case_id"]:
                counter["count"] += weight
                break
        else:
            self.counters.append({"case_id": case_id, "count": weight})
        
        return self.counters

    def check_for_highest_id(self) -> int:
        if not self.counters:
            return None

        highest_count = max(self.counters, key=lambda x: x["count"])["count"]
        candidates = [counter for counter in self.counters if counter["count"] == highest_count]
        
        if len(candidates) > 1:
            return self.resolve_tie(candidates)
        return candidates[0]["case_id"]

    def resolve_tie(self, candidates: list) -> int:
        case_ids = [candidate["case_id"] for candidate in candidates]
        return max(case_ids, key=lambda cid: self.compare_keyword_match(cid))

    def compare_keyword_match(self, case_id: int) -> int:
        case_id_keywords = db_connector.get_primary_keywords_by_caseID(case_id)
        if not case_id_keywords:
            return 0
        return len([word for word in self.question if word in case_id_keywords])