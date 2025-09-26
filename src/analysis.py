import json
import matplotlib.pyplot as plt

def analyze_results(baseline_file, execution_file, output_file, plot_file):
    with open(baseline_file, "r") as f:
        baseline = {item["task_id"]: item for item in json.load(f)}
    
    with open(execution_file, "r") as f:
        execution = {item["task_id"]: item for item in json.load(f)}
    
    summary = []
    total = 0
    agree = 0
    disagree = 0
    false_pos = 0
    false_neg = 0

    # Compare each task result
    for task_id, exec_res in execution.items():
        total += 1
        gt = exec_res["ground_truth"]
        base_judgment = baseline.get(task_id, {}).get("judgment", {})
        base_label = base_judgment.get("label", None)

        if base_label is None:
            continue

        if base_label == gt:
            agree += 1
        else:
            disagree += 1
            if base_label == "PASS" and gt == "FAIL":
                false_pos += 1
            elif base_label == "FAIL" and gt == "PASS":
                false_neg += 1

        summary.append({
            "task_id": task_id,
            "baseline_label": base_label,
            "ground_truth": gt,
            "agree": base_label == gt
        })

    results = {
        "total": total,
        "agree": agree,
        "disagree": disagree,
        "false_pos": false_pos,
        "false_neg": false_neg,
        "accuracy": agree / total if total > 0 else 0,
        "details": summary
    }

    # Save JSON report
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Analysis complete! Saved report to {output_file}")

    # Plot summary
    labels = ["Agree", "Disagree", "False Positives", "False Negatives"]
    values = [agree, disagree, false_pos, false_neg]

    plt.figure(figsize=(7, 5))
    bars = plt.bar(labels, values)
    plt.title("Baseline Judge vs Ground Truth")
    plt.ylabel("Count")

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.2,
                 str(height), ha='center', va='bottom')

    plt.savefig(plot_file)
    plt.close()
    print(f"Bar chart saved to {plot_file}")

if __name__ == "__main__":
    analyze_results(
        baseline_file="data/baseline_outputs.json",
        execution_file="data/execution_results.json",
        output_file="data/analysis_report.json",
        plot_file="data/analysis_plot.png"
    )
