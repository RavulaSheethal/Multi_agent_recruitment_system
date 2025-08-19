from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class SkillScore(BaseModel):
    skill: str
    confidence: float = Field(ge=0.0, le=1.0)

class CareerStep(BaseModel):
    period: str
    role: str
    highlights: List[str] = []

class TalentIntelligenceReport(BaseModel):
    candidate_id: str
    name: str
    top_skills: List[SkillScore]
    experience_summary: str
    career_progression: List[CareerStep]
    repos_and_activity: List[str] = []
    red_flags_or_gaps: List[str] = []
    overall_fit_tags: List[str] = []

class Challenge(BaseModel):
    title: str
    prompt: str
    expected_competencies: List[str]

class AssessmentPackage(BaseModel):
    role: str
    level: str
    technical_challenges: List[Challenge]
    evaluation_framework: Dict[str, int]
    bias_mitigation_protocol: List[str]

class BehaviorTheme(BaseModel):
    theme: str
    confidence: float
    evidence: List[str] = []

class BehaviorReport(BaseModel):
    candidate_id: str
    summary: str
    themes: List[BehaviorTheme]

class MarketSummary(BaseModel):
    role: str
    location: str
    median: float
    p25: float
    p75: float
    recommended_channels: List[str]
