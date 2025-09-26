import json
import argparse
from llm_wrapper import call_llm

JUDGE_PROMPT = """You are an expert code reviewer.
Given a coding problem and a candidate solution, decide if the solution is correct.
Answer strictly in JSON format:
{{"label":"PASS" or "FAIL","confidence": float between 0 and 1, "rationale":"<one-sentence reason>"}}

Problem:
{problem}

Candidate Solution:
{solution}
"""
def aggregate(judgments):
    """
    Aggregate multiple LLM judgments into one.
    Strategy: majority vote (label) + average confidence.
    """
    labels = [j["label"] for j in judgments if j and "label" in j]
    confs = [j["confidence"] for j in judgments if j and "confidence" in j]

    if not labels:
        return {"label": "UNKNOWN", "confidence": 0.0, "rationale": "No valid judgments"}

    # for the majority vote
    final_label = max(set(labels), key=labels.count)
    avg_conf = sum(confs) / len(confs) if confs else 0.0

    return {
        "label": final_label,
        "confidence": round(avg_conf, 2),
        "rationale": f"Ensemble of {len(judgments)} judges agreed by majority vote."
    }

def run_ensemble(input_file, output_file, models):
    with open(input_file, "r") as f:
        dataset = json.load(f)

    rows = dataset["rows"] if "rows" in dataset else dataset
    results = []

    for item in rows[:4]:
        row = item["row"]
        problem = row["prompt"]
        solution = row["solution"]

        judgments = []
        raw_responses = {}
        for m in models:
            prompt = JUDGE_PROMPT.format(problem=problem, solution=solution)
            resp = call_llm(prompt, model=m)

            # parsing JSON
            parsed = None
            try:
                parsed = json.loads(resp)
            except Exception:
                parsed = {"label": "UNKNOWN", "confidence": 0.0, "rationale": resp}

            judgments.append(parsed)
            raw_responses[m] = resp

        final = aggregate(judgments)

        results.append({
            "task_id": row["name"],
            "ensemble_judgment": final,
            "individual_judgments": judgments,
            "raw_responses": raw_responses
        })

        print(f"Processed {row['name']} with ensemble")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/humanevalcomm_subset.json")
    parser.add_argument("--output", default="data/ensemble_outputs.json")
    parser.add_argument("--models", nargs="+", default=["gpt-4o-mini", "gpt-3.5-turbo"])
    args = parser.parse_args()

    run_ensemble(args.input, args.output, args.models)


