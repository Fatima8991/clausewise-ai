from pydantic import BaseModel, Field
from typing import Literal

class Clause(BaseModel):
    id: str
    title: str
    text: str
    page: int
    score: float = 0.0

class AnalyzeRequest(BaseModel):
    contract_id: str
    question: str = Field(min_length=8, max_length=1500)

class Evidence(BaseModel):
    clause_id: str
    title: str
    page: int
    excerpt: str
    relevance: float
    role: Literal["supporting", "limiting", "context"]

class AnalysisResponse(BaseModel):
    contract_id: str
    question: str
    verdict: Literal["potentially_covered", "not_established", "needs_review"]
    verdict_label: str
    summary: str
    reasoning: list[str]
    evidence: list[Evidence]
    limitations: list[str]
    abstained: bool
