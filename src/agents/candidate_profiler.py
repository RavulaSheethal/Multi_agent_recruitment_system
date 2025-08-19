import json, os
from typing import List
from src.shared.schemas import TalentIntelligenceReport, SkillScore, CareerStep
from src.shared.nlp_utils import extract_skills, summarize_experience, detect_fit_tags

DATA_DIR = "data"
REPORT_DIR = "reports"

def load_profiles(path: str) -> List[dict]:
    profiles = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                profiles.append(json.loads(line))
    return profiles

def build_tir(profile: dict) -> TalentIntelligenceReport:
    text_blobs = [
        profile.get("summary",""),
        " ".join(profile.get("skills", [])),
        " ".join(" ".join(r.get("bullets", [])) for r in profile.get("roles", [])),
        " ".join(profile.get("repos", [])),
    ]
    skills = extract_skills(" \n".join(text_blobs))
    skill_objs = [SkillScore(skill=s, confidence=c) for s,c in skills]
    exp = summarize_experience(profile.get("roles", []))
    progression = [
        CareerStep(period=r.get("period",""), role=r.get("role",""), highlights=r.get("bullets", []))
        for r in profile.get("roles", [])
    ]
    fit_tags = detect_fit_tags([s for s,_ in skills])
    tir = TalentIntelligenceReport(
        candidate_id=profile["id"],
        name=profile.get("name",""),
        top_skills=skill_objs[:8],
        experience_summary=exp,
        career_progression=progression,
        repos_and_activity=profile.get("repos", []),
        red_flags_or_gaps=profile.get("gaps", []),
        overall_fit_tags=fit_tags
    )
    return tir

def save_report(tir: TalentIntelligenceReport):
    os.makedirs(REPORT_DIR, exist_ok=True)
    # JSON
    jpath = os.path.join(REPORT_DIR, f"{tir.candidate_id}_TIR.json")
    with open(jpath, "w", encoding="utf-8") as f:
        f.write(tir.model_dump_json(indent=2))
    # Markdown
    mpath = os.path.join(REPORT_DIR, f"{tir.candidate_id}_TIR.md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(f"# Talent Intelligence Report — {tir.name}\n\n")
        f.write(f"**Candidate ID:** {tir.candidate_id}\n\n")
        f.write("## Top Skills\n")
        for s in tir.top_skills:
            f.write(f"- {s.skill} ({s.confidence:.2f})\n")
        f.write("\n## Experience Summary\n")
        f.write(tir.experience_summary + "\n\n")
        f.write("## Career Progression\n")
        for step in tir.career_progression:
            f.write(f"- **{step.period} — {step.role}**\n")
            for h in step.highlights:
                f.write(f"  - {h}\n")
        f.write("\n## Fit Tags\n")
        f.write(", ".join(tir.overall_fit_tags) + "\n")
    return jpath

def run(candidate_id: str):
    profiles = load_profiles(os.path.join(DATA_DIR, "synthetic_profiles.jsonl"))
    prof = next((p for p in profiles if p["id"] == candidate_id), None)
    if not prof:
        raise SystemExit(f"Candidate {candidate_id} not found.")
    tir = build_tir(prof)
    out = save_report(tir)
    print(f"Generated: {out}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate_id", required=True)
    args = ap.parse_args()
    run(args.candidate_id)
