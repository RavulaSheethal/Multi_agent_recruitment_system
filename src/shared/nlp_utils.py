import re
from typing import List, Tuple, Dict

# very simple keyword map; you can extend later
SKILL_KEYWORDS: Dict[str, List[str]] = {
    "Python": ["python", "numpy", "pandas"],
    "Machine Learning": ["ml", "machine learning", "scikit", "xgboost", "model", "training"],
    "Deep Learning": ["pytorch", "tensorflow", "nn", "neural network", "cnn", "rnn"],
    "MLOps": ["deployment", "docker", "api", "pipeline", "inference"],
    "Data Engineering": ["etl", "airflow", "spark", "sql", "warehouse"],
    "NLP": ["nlp", "text", "token", "bert", "llm"],
    "Backend": ["flask", "fastapi", "rest", "microservice"],
}

def extract_skills(text: str) -> List[Tuple[str, float]]:
    t = text.lower()
    results = []
    for skill, kws in SKILL_KEYWORDS.items():
        hits = sum(1 for kw in kws if re.search(rf"\b{re.escape(kw)}\b", t))
        if hits:
            # crude confidence: normalized by keyword count
            conf = min(1.0, 0.4 + 0.15 * hits)
            results.append((skill, round(conf, 2)))
    # sort by confidence desc
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def summarize_experience(roles: List[dict]) -> str:
    if not roles:
        return "No experience listed."
    latest = roles[-1]["role"]
    years = len(roles)  # placeholder
    domains = sorted({r.get("domain","General") for r in roles})
    return f"{years} role(s) across {', '.join(domains)}; latest role: {latest}."

def detect_fit_tags(skills: List[str]) -> List[str]:
    tags = []
    if "MLOps" in skills: tags.append("ML Platform")
    if "Data Engineering" in skills: tags.append("Data Eng")
    if "NLP" in skills or "Machine Learning" in skills: tags.append("Applied ML")
    return tags or ["Generalist"]
