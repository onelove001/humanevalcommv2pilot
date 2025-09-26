import json
import argparse
from llm_wrapper import call_llm

BASELINE_PROMPT = """You are an expert code reviewer.
Given a coding problem and a candidate solution, decide if the solution is correct.
Answer strictly in JSON format:
{{"label":"PASS" or "FAIL","confidence": float between 0 and 1, "rationale":"<one-sentence reason>"}}

Problem:
{problem}

Candidate Solution:
{solution}
"""

def run_baseline(input_file, output_file, model="gpt-4o-mini"):
    with open(input_file, "r") as f:
        dataset = json.load(f)

    rows = dataset["rows"] if "rows" in dataset else dataset

    results = []
    for idx, item in enumerate(rows[:5]):
        row = item["row"]
        problem = row["prompt"]
        solution = row["solution"]

        prompt = BASELINE_PROMPT.format(problem=problem, solution=solution)

        if idx < 2:
            print("=" * 40)
            print(f"DEBUG Prompt for {row['name']}:")
            print(prompt)
            print("=" * 40)

        try:
            response = call_llm(prompt, model=model)
            # parsing LLM response as JSON
            parsed = None
            try:
                parsed = json.loads(response)
            except json.JSONDecodeError:
                parsed = {"label": "UNKNOWN", "confidence": 0.0, "rationale": response}

            results.append({
                "task_id": row["name"],
                "judgment": parsed,
                "raw_response": response
            })
            print(f"Processed {row['name']}")
        except Exception as e:
            results.append({
                "task_id": row["name"],
                "judgment": None,
                "error": str(e)
            })

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/humanevalcomm_subset.json")
    parser.add_argument("--output", default="data/baseline_outputs.json")
    parser.add_argument("--model", default="gpt-4o-mini")
    args = parser.parse_args()

    run_baseline(args.input, args.output, args.model)





