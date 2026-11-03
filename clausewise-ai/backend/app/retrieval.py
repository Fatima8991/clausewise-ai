import re
import math
from collections import Counter
from .schemas import Clause

STOP = {"dans", "avec", "pour", "une", "des", "les", "est", "que", "qui", "sur", "par", "mon", "ma", "mes", "aux", "du", "de", "la", "le", "un", "et", "ou", "en", "au", "ce", "cette", "son", "sa", "ses", "the", "and", "for", "with", "from", "are", "was", "were", "into", "not", "this", "that", "contrat", "contrats", "assurance", "assuré", "assuree", "rembourse", "rembourser", "suis", "couvert", "couverte"}

def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zA-ZÀ-ÿ0-9]+", text.lower())
    return [w for w in words if len(w) > 2 and w not in STOP]

def rank_clauses(query: str, clauses: list[Clause], limit: int = 8) -> list[Clause]:
    q = tokenize(query)
    if not q or not clauses:
        return []
    docs = [tokenize(c.title + " " + c.text) for c in clauses]
    avgdl = sum(map(len, docs)) / max(len(docs), 1)
    df = Counter(term for doc in docs for term in set(doc))
    scored = []
    for clause, doc in zip(clauses, docs):
        tf = Counter(doc)
        score = 0.0
        for term in q:
            if term not in tf:
                continue
            idf = math.log(1 + (len(docs) - df[term] + 0.5) / (df[term] + 0.5))
            denom = tf[term] + 1.2 * (1 - 0.75 + 0.75 * len(doc) / max(avgdl, 1))
            score += idf * (tf[term] * 2.2) / denom
        # Small phrase overlap bonus, still deterministic and inspectable.
        if len(q) > 1 and " ".join(q[:2]) in " ".join(doc):
            score *= 1.08
        clause.score = round(score, 4)
        scored.append(clause)
    return sorted(scored, key=lambda c: c.score, reverse=True)[:limit]
