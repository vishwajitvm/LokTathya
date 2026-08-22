import hashlib
import json

class DocumentDiffEngine:
    def __init__(self):
        pass

    def diff_text(self, text_a: str, text_b: str) -> dict:
        """
        Produce a deterministic diff between two texts.
        In a real implementation, this would use diff-match-patch or difflib.
        """
        import difflib
        matcher = difflib.SequenceMatcher(None, text_a, text_b)
        ratio = matcher.ratio()
        
        return {
            "similarity_ratio": ratio,
            "status": "UNCHANGED" if ratio == 1.0 else "MODIFIED",
            "changes": [
                {"tag": tag, "i1": i1, "i2": i2, "j1": j1, "j2": j2}
                for tag, i1, i2, j1, j2 in matcher.get_opcodes()
                if tag != 'equal'
            ]
        }

    def diff_tables(self, tables_a: list, tables_b: list) -> dict:
        """
        Compare two lists of extracted tables.
        """
        added = []
        removed = []
        modified = []

        # Simplified logic: compare hashes of tables
        dict_a = {self._hash_obj(t): t for t in tables_a}
        dict_b = {self._hash_obj(t): t for t in tables_b}

        for k in dict_a:
            if k not in dict_b:
                removed.append(dict_a[k])
        for k in dict_b:
            if k not in dict_a:
                added.append(dict_b[k])
        
        # Real logic would do row-level diffing for modified tables

        return {
            "added": added,
            "removed": removed,
            "modified": modified,
            "status": "UNCHANGED" if not added and not removed and not modified else "MODIFIED"
        }

    def diff_documents(self, doc_a: dict, doc_b: dict) -> dict:
        """
        Compare full document representations.
        doc_a and doc_b could be page-level dictionaries.
        """
        return {
            "text_diff": self.diff_text(doc_a.get("text", ""), doc_b.get("text", "")),
            "table_diff": self.diff_tables(doc_a.get("tables", []), doc_b.get("tables", [])),
            "pages_added": max(0, doc_b.get("page_count", 0) - doc_a.get("page_count", 0)),
            "pages_removed": max(0, doc_a.get("page_count", 0) - doc_b.get("page_count", 0))
        }

    def _hash_obj(self, obj) -> str:
        s = json.dumps(obj, sort_keys=True)
        return hashlib.sha256(s.encode('utf-8')).hexdigest()
