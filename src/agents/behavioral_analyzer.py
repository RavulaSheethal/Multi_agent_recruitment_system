import json, os
from typing import List
from src.shared.schemas import BehaviorReport, BehaviorTheme

DATA_DIR = "data"
REPORT_DIR = "reports"

THEMES = {
    "Collaboration": ["together","team","help","pair","discuss","align","support"],
    "Problem-Solving": ["debug","issue","root cause","investigate","hypothesis","approach"],
    "Communication": ["clarify","explain","document","comment","summarize","concise"],
    "Ownership": ["responsible","deadline","follow up","blocked","unblock","update"],
}

def score_theme(text: str, keywords: List[str]) -> float:
    t = text.lower()
    hits = sum(1 for kw in keywords if kw in t)
    return min(1.0, 0.3 + 0.1 * hits) if hits else 0.0

def run(candidate_id: str):
    conv_path = os.path.join(DATA_DIR, "synthetic_conversations.jsonl")
    convos = []
    with open(conv_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                obj = json.loads(line)
                if obj["candidate_id"] == candidate_id:
                    convos.append(obj)

    text = " ".join(c["text"] for c in convos)
    themes = []
    for name, kws in THEMES.items():
        conf = score_theme(text, kws)
        if conf > 0:
            # gather 2 snippets as evidence
            ev = [c["text"] for c in convos if any(k in c["text"].lower() for k in kws)][:2]
            themes.append(BehaviorTheme(theme=name, confidence=round(conf,2), evidence=ev))

    summary = "Behavioral indicators derived from anonymized conversation snippets. Demographic signals ignored."
    report = BehaviorReport(candidate_id=candidate_id, summary=summary, themes=themes)

    os.makedirs(REPORT_DIR, exist_ok=True)
    out = os.path.join(REPORT_DIR, f"{candidate_id}_Behavior.json")
    with open(out, "w", encoding="utf-8") as f:
        f.write(report.model_dump_json(indent=2))
    print(f"Generated: {out}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate_id", required=True)
    args = ap.parse_args()
    run(args.candidate_id)
