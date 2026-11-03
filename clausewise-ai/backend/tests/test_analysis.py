from app.schemas import Clause
from app.analysis import analyze
from app.retrieval import rank_clauses

CLAUSES = [
    Clause(id="c1", title="Garantie vol", page=2, text="La garantie vol couvre le vol des biens mobiliers situés dans le logement assuré, sous réserve des conditions de sécurité prévues au contrat."),
    Clause(id="c2", title="Exclusion des locaux communs", page=5, text="Le vol dans les locaux communs non fermés à clé ou accessibles librement est exclu de la garantie."),
    Clause(id="c3", title="Franchise", page=7, text="Une franchise contractuelle de 150 euros reste à la charge de l'assuré.")
]

def test_retrieval_returns_relevant_clause():
    ranked = rank_clauses("vol local commun fermé à clé", CLAUSES)
    assert ranked
    assert ranked[0].score > 0

def test_unlocked_common_area_requires_review():
    result = analyze("Mon vélo est volé dans le local commun qui n'était pas fermé à clé. Suis-je couvert ?", "test", CLAUSES)
    assert result.verdict == "needs_review"
    assert result.abstained is True
    assert any(e.clause_id == "c2" for e in result.evidence)

def test_unmatched_question_abstains():
    result = analyze("Le contrat rembourse-t-il mon voyage en avion ?", "test", CLAUSES)
    assert result.verdict == "needs_review"
    assert result.abstained is True
