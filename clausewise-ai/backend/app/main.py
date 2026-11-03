import json, re, uuid
from pathlib import Path
from typing import Any
import fitz
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import Clause, AnalyzeRequest, AnalysisResponse
from .analysis import analyze

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
SAMPLE = ROOT.parent / "sample-data" / "synthetic_home_policy.txt"
app = FastAPI(title="ClauseWise AI API", version="0.1.0", description="Evidence-first insurance contract analysis demo")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "https://*.vercel.app"], allow_origin_regex=r"https://.*\.vercel\.app", allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


def split_clauses(text: str, page: int) -> list[Clause]:
    # Headings such as "2. Vol" or "ARTICLE 3 — Exclusions" form clause boundaries.
    chunks = re.split(r"(?m)(?=^(?:(?:ARTICLE|SECTION)\s+\d+|\d+(?:\.\d+)*\.?\s+)[^\n]{2,100}$)", text)
    out = []
    for chunk in chunks:
        clean = re.sub(r"\s+", " ", chunk).strip()
        if len(clean) < 35:
            continue
        title = clean[:100]
        out.append(Clause(id=f"p{page}-c{len(out)+1}", title=title, text=clean, page=page))
    if not out and text.strip():
        out.append(Clause(id=f"p{page}-c1", title=f"Page {page}", text=re.sub(r"\s+", " ", text).strip(), page=page))
    return out


def save_contract(contract_id: str, name: str, clauses: list[Clause]) -> dict[str, Any]:
    record = {"id": contract_id, "name": name, "clauses": [c.model_dump() for c in clauses]}
    (DATA_DIR / f"{contract_id}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return record


def load_contract(contract_id: str) -> dict[str, Any]:
    path = DATA_DIR / f"{contract_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Contrat introuvable")
    return json.loads(path.read_text(encoding="utf-8"))

@app.get("/health")
def health():
    return {"status": "ok", "service": "clausewise-api"}

@app.get("/api/contracts")
def list_contracts():
    records = []
    for path in DATA_DIR.glob("*.json"):
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
            records.append({"id": d["id"], "name": d["name"], "clause_count": len(d["clauses"])})
        except Exception:
            continue
    return {"contracts": records}

@app.post("/api/demo/seed")
def seed_demo():
    if not SAMPLE.exists():
        raise HTTPException(status_code=500, detail="Fichier de démonstration absent")
    text = SAMPLE.read_text(encoding="utf-8")
    clauses = split_clauses(text, 1)
    record = save_contract("demo-home-policy", "Contrat habitation — exemple synthétique", clauses)
    return {"id": record["id"], "name": record["name"], "clause_count": len(clauses)}

@app.post("/api/contracts/upload")
async def upload_contract(file: UploadFile = File(...)):
    filename = file.filename or "contrat"
    content = await file.read()
    if len(content) > 15 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Fichier limité à 15 Mo dans cette démonstration")
    clauses: list[Clause] = []
    if filename.lower().endswith(".pdf"):
        try:
            doc = fitz.open(stream=content, filetype="pdf")
            for idx, page in enumerate(doc, start=1):
                clauses.extend(split_clauses(page.get_text("text"), idx))
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"PDF illisible : {exc}")
    elif filename.lower().endswith(".txt"):
        clauses = split_clauses(content.decode("utf-8", errors="replace"), 1)
    else:
        raise HTTPException(status_code=415, detail="Formats acceptés : PDF texte et TXT")
    if not clauses:
        raise HTTPException(status_code=422, detail="Aucun texte exploitable. Les PDF scannés nécessitent un OCR non inclus dans ce MVP.")
    contract_id = str(uuid.uuid4())[:8]
    record = save_contract(contract_id, filename, clauses)
    return {"id": record["id"], "name": record["name"], "clause_count": len(clauses)}

@app.post("/api/analyze", response_model=AnalysisResponse)
def analyze_contract(payload: AnalyzeRequest):
    record = load_contract(payload.contract_id)
    clauses = [Clause(**c) for c in record["clauses"]]
    return analyze(payload.question, payload.contract_id, clauses)

@app.get("/api/contracts/{contract_id}")
def contract_detail(contract_id: str):
    record = load_contract(contract_id)
    return {"id": record["id"], "name": record["name"], "clauses": record["clauses"]}
