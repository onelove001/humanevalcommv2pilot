import json
import argparse
import ast
import builtins

def strip_type_hints(code: str) -> str:
    """Remove all type hints from a Python function using AST."""
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            node.returns = None
            for arg in node.args.args:
                arg.annotation = None
            for arg in node.args.kwonlyargs:
                arg.annotation = None
        elif isinstance(node, ast.AnnAssign):
            node.annotation = None

    return ast.unparse(tree)  # Python 3.9+

def run_test_case(func_code, test_case):
    try:
       
        func_code = "\n".join(
            [ln for ln in func_code.splitlines() if not ln.strip().startswith("from typing")]
        )
        func_code = strip_type_hints(func_code)

        safe_globals = {"__builtins__": builtins.__dict__}
        local_ns = {}

        exec(func_code, safe_globals, local_ns)

        func_name = [k for k, v in local_ns.items() if callable(v)][0]
        func = local_ns[func_name]

        # Parse inputs
        args = eval(test_case["input"])
        if not isinstance(args, tuple):
            args = (args,)

        result = func(*args)
        expected = eval(test_case["output"])
        relation = test_case.get("relation", "==")

        if relation == "==":
            return result == expected
        elif relation == "!=":
            return result != expected
        elif relation == ">":
            return result > expected
        elif relation == "<":
            return result < expected
        else:
            return False
    except Exception as e:
        return f"ERROR: {str(e)}"



def run_execution_eval(input_file, output_file):
    with open(input_file, "r") as f:
        dataset = json.load(f)

    rows = dataset["rows"] if "rows" in dataset else dataset
    results = []

    for item in rows[:4]:
        row = item["row"]
        solution = row["solution"]
        task_id = row["name"]
        try:
            test_cases = eval(row["test_case"])
        except Exception:
            test_cases = []

        case_results = []
        all_passed = True
        for tc in test_cases:
            res = run_test_case(solution, tc)
            case_results.append(res)
            if res is not True:
                all_passed = False

        results.append({
            "task_id": task_id,
            "ground_truth": "PASS" if all_passed else "FAIL",
            "case_results": case_results
        })

        print(f"Executed {task_id}: {'PASS' if all_passed else 'FAIL'}")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/humanevalcomm_subset.json")
    parser.add_argument("--output", default="data/execution_results.json")
    args = parser.parse_args()

    run_execution_eval(args.input, args.output)
