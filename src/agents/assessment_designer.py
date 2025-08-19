import json, os
from typing import Dict, List
from src.shared.schemas import AssessmentPackage, Challenge, TalentIntelligenceReport

REPORT_DIR = "reports"

ROLE_COMP_MAP: Dict[str, List[str]] = {
    "ML Engineer": ["Data Prep", "Modeling", "Evaluation", "Deployment"],
    "Data Engineer": ["ETL", "Batch/Streaming", "SQL", "Data Modeling"],
    "Backend Engineer": ["API Design", "Reliability", "Performance", "Testing"],
}

def load_tir(candidate_id: str) -> TalentIntelligenceReport:
    path = os.path.join(REPORT_DIR, f"{candidate_id}_TIR.json")
    with open(path, "r", encoding="utf-8") as f:
        return TalentIntelligenceReport.model_validate_json(f.read())

def personalize_challenges(role: str, tir: TalentIntelligenceReport) -> List[Challenge]:
    skills = [s.skill for s in tir.top_skills]
    challenges: List[Challenge] = []

    if role == "ML Engineer":
        # always include modeling
        challenges.append(Challenge(
            title="Build & Evaluate a Baseline Model",
            prompt=("Given a small CSV with features and a target, "
                    "train a baseline model, report metrics, and discuss error analysis."),
            expected_competencies=["Data Prep","Modeling","Evaluation"]
        ))
        # add deployment if MLOps is weaker
        if "MLOps" not in skills:
            challenges.append(Challenge(
                title="Package a Prediction Service",
                prompt=("Expose the trained model behind a simple REST endpoint "
                        "with input validation and a /health route."),
                expected_competencies=["Deployment","API","Reliability"]
            ))
        # add NLP if present
        if "NLP" in skills:
            challenges.append(Challenge(
                title="Simple Text Classifier",
                prompt=("Clean raw text, build a TF-IDF + linear model, compare with a small neural baseline."
                        " Provide a short write-up on preprocessing choices."),
                expected_competencies=["Text Processing","Modeling","Evaluation"]
            ))
    else:
        comps = ROLE_COMP_MAP.get(role, ["Problem Solving"])
        challenges.append(Challenge(
            title=f"Core {role} Task",
            prompt=f"Complete a task demonstrating: {', '.join(comps)}.",
            expected_competencies=comps
        ))
    return challenges

def make_rubric(role: str) -> Dict[str, int]:
    # weights sum to 100
    if role == "ML Engineer":
        return {"Problem-solving": 40, "Code quality": 30, "Communication": 30}
    return {"Problem-solving": 50, "Code quality": 30, "Communication": 20}

def bias_protocol() -> List[str]:
    return [
        "Evaluate using rubric only; ignore names, photos, demographics.",
        "Blind review: hide personal identifiers in submissions.",
        "Double-score borderline submissions with a second reviewer.",
        "Use structured feedback template with evidence-based comments.",
    ]

def run(candidate_id: str, role: str, level: str = "Junior/Mid"):
    tir = load_tir(candidate_id)
    challenges = personalize_challenges(role, tir)
    pkg = AssessmentPackage(
        role=role,
        level=level,
        technical_challenges=challenges,
        evaluation_framework=make_rubric(role),
        bias_mitigation_protocol=bias_protocol()
    )
    os.makedirs(REPORT_DIR, exist_ok=True)
    out_json = os.path.join(REPORT_DIR, f"{candidate_id}_{role.replace(' ','_')}_Assessment.json")
    out_md = os.path.join(REPORT_DIR, f"{candidate_id}_{role.replace(' ','_')}_Assessment.md")
    with open(out_json, "w", encoding="utf-8") as f:
        f.write(pkg.model_dump_json(indent=2))
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(f"# Assessment Package — {role} ({level})\n\n")
        for i, ch in enumerate(pkg.technical_challenges, 1):
            f.write(f"## {i}. {ch.title}\n{ch.prompt}\n\n**Competencies:** {', '.join(ch.expected_competencies)}\n\n")
        f.write("## Evaluation Framework\n")
        for k,v in pkg.evaluation_framework.items():
            f.write(f"- {k}: {v}\n")
        f.write("\n## Bias Mitigation Protocol\n")
        for step in pkg.bias_mitigation_protocol:
            f.write(f"- {step}\n")
    print(f"Generated: {out_json}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate_id", required=True)
    ap.add_argument("--role", required=True)
    ap.add_argument("--level", default="Junior/Mid")
    args = ap.parse_args()
    run(args.candidate_id, args.role, args.level)
