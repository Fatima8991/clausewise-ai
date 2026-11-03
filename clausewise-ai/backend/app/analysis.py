from .schemas import Clause, Evidence, AnalysisResponse
from .retrieval import rank_clauses, tokenize

EXCLUSION_TERMS = ("exclu", "non couvert", "ne sont pas garant", "sauf", "à l'exclusion", "non indemnis")
COVER_TERMS = ("vol", "garanti", "garantie", "couvert", "dommage", "responsabilité", "incendie", "dégât")
UNCERTAINTY_TERMS = ("sous réserve", "sous condition", "dans la limite", "franchise", "déclaration", "fermé à clé", "effraction", "local commun")

def classify_role(clause: Clause) -> str:
    text = clause.text.lower()
    if any(t in text for t in EXCLUSION_TERMS):
        return "limiting"
    if any(t in text for t in COVER_TERMS):
        return "supporting"
    return "context"

def analyze(question: str, contract_id: str, clauses: list[Clause]) -> AnalysisResponse:
    ranked = rank_clauses(question, clauses, limit=8)
    # Keep only actual lexical matches. A low score is not evidence.
    relevant = [c for c in ranked if c.score > 0]
    evidence = [Evidence(
        clause_id=c.id, title=c.title, page=c.page,
        excerpt=c.text[:650] + ("…" if len(c.text) > 650 else ""),
        relevance=c.score, role=classify_role(c)
    ) for c in relevant[:5]]

    if not relevant or relevant[0].score < 0.25:
        return AnalysisResponse(
            contract_id=contract_id, question=question, verdict="needs_review",
            verdict_label="Analyse insuffisante", summary="Je n'ai pas retrouvé de clause suffisamment pertinente pour étayer une conclusion.",
            reasoning=["Aucune preuve contractuelle suffisamment proche de la question n'a été retrouvée."],
            evidence=evidence, limitations=["La recherche lexicale peut manquer des synonymes ou des formulations indirectes.", "Aucune conclusion de couverture ne doit être tirée sans examen humain."], abstained=True)

    joined = " ".join(c.text.lower() for c in relevant[:5])
    q = question.lower()
    has_cover = any(t in joined for t in COVER_TERMS)
    has_exclusion = any(t in joined for t in EXCLUSION_TERMS)
    mentions_key_condition = any(t in joined for t in UNCERTAINTY_TERMS)
    asks_about_unlocked = any(t in q for t in ("pas fermé", "non fermé", "ouvert", "clé", "cle"))
    unlocked_exception = asks_about_unlocked and any(t in joined for t in ("fermé à clé", "effraction", "local commun"))

    if has_exclusion and (unlocked_exception or not has_cover):
        verdict = "needs_review"
        label = "Point d'exclusion à vérifier"
        summary = "Des clauses limitatives ou d'exclusion apparaissent dans les passages retrouvés. Leur application au cas décrit doit être vérifiée avant toute décision."
        reasons = ["Au moins un passage retrouvé contient une formulation potentiellement limitative.", "La portée exacte de cette clause dépend du contexte et des autres dispositions du contrat."]
        abstained = True
    elif has_cover and has_exclusion:
        verdict = "needs_review"
        label = "Analyse contradictoire"
        summary = "Des éléments de garantie et des éléments limitatifs coexistent. Le contrat ne permet pas ici de produire un verdict fiable sans interprétation complémentaire."
        reasons = ["Des clauses favorables et restrictives ont été retrouvées.", "Il faut vérifier leur articulation, les définitions et les conditions particulières."]
        abstained = True
    elif has_cover:
        verdict = "potentially_covered"
        label = "Garantie potentiellement applicable"
        summary = "Une clause évoque une garantie pertinente, mais les exclusions, conditions particulières, plafonds et franchises doivent encore être contrôlés."
        reasons = ["Un passage relatif à une garantie pertinente a été retrouvé.", "La présence d'une clause de garantie ne suffit pas, à elle seule, à confirmer l'indemnisation."]
        abstained = False
    else:
        verdict = "not_established"
        label = "Couverture non établie"
        summary = "Les passages retrouvés ne suffisent pas à établir que le risque décrit est garanti. Cela ne signifie pas nécessairement qu'il est exclu."
        reasons = ["Aucune clause de garantie suffisamment explicite n'a été identifiée parmi les résultats.", "Une recherche complémentaire dans le contrat complet et ses annexes est nécessaire."]
        abstained = True

    limits = ["Prototype de démonstration : le résultat n'est ni un avis juridique ni une décision d'indemnisation.", "La recherche actuelle est lexicale ; elle peut manquer des équivalences sémantiques et des dépendances entre clauses."]
    if mentions_key_condition:
        limits.append("Des conditions, franchises ou formalités sont mentionnées dans les passages retrouvés : elles doivent être vérifiées dans leur contexte complet.")
    return AnalysisResponse(contract_id=contract_id, question=question, verdict=verdict, verdict_label=label, summary=summary, reasoning=reasons, evidence=evidence, limitations=limits, abstained=abstained)
