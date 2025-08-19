import argparse
from src.agents.candidate_profiler import run as run_profiler
from src.agents.assessment_designer import run as run_assessment
from src.agents.behavioral_analyzer import run as run_behavior
from src.agents.market_optimizer import run as run_market

def main():
    ap = argparse.ArgumentParser(prog="multi-agent-cli")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("profile")
    p1.add_argument("--candidate_id", required=True)

    p2 = sub.add_parser("assess")
    p2.add_argument("--candidate_id", required=True)
    p2.add_argument("--role", required=True)
    p2.add_argument("--level", default="Junior/Mid")

    p3 = sub.add_parser("behavior")
    p3.add_argument("--candidate_id", required=True)

    p4 = sub.add_parser("market")
    p4.add_argument("--role", required=True)
    p4.add_argument("--location", required=True)

    args = ap.parse_args()

    if args.cmd == "profile":
        run_profiler(args.candidate_id)
    elif args.cmd == "assess":
        run_assessment(args.candidate_id, args.role, args.level)
    elif args.cmd == "behavior":
        run_behavior(args.candidate_id)
    elif args.cmd == "market":
        run_market(args.role, args.location)

if __name__ == "__main__":
    main()
