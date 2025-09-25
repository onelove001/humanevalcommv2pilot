
# README

# HumanEvalComm-V2: IMPROVING RELIABILITY OF COMMUNICATION-AWARE CODE LLM EVALUATION

This repository contains the code, dataset subset, and analysis scripts for **HumanEvalComm-V2**, a hybrid evaluation framework that improves the reliability of communication-aware code generation benchmarks. HumanEvalComm-V2 addresses a key limitation of the original [HumanEvalComm benchmark](https://arxiv.org/pdf/2406.00215): its reliance on a single LLM judge, which is often unreliable. The solution integrates **ensemble LLM judging**, and **execution-based ground truth**, producing more trustworthy and reproducible results.  

## Repository Structure

human-evalcomm-v2/

── data/
   humanevalcomm_subset.json      # Dataset subset (JSON)
   baseline_outputs.json          # Baseline LLM judge results
   ensemble_outputs.json          # Multiple LLM Judge results
   execution_results.json         # Execution-based test outcomes
   analysis_report.json           # Final analysis
   analysis_plot.png              # Bar chart visualization

── src/
   llm_wrapper.py                 # Calls LLM with a given prompt
   run_baseline.py                # Reproduce baseline (LLM judge)
   run_ensemble.py                # Reproduce multiple (LLM judges)
   run_execution.py               # Run execution tests
   analysis.py                    # Compare baseline vs. execution

── report/
   HumanEvalComm-V2.pdf           # Short Technical report

── README.md


## 🚀 Usage

### 1. Run Baseline LLM Judge

bash terminal:
python src/run_baseline.py --input data/humanevalcomm_subset.json --output data/baseline_outputs.json


* Reads `data/humanevalcomm_subset.json`
* Produces `data/baseline_outputs.json`

### 2. Run Ensemble LLM Judges

bash terminal:
python src/run_ensemble.py --input data/humanevalcomm_subset.json --output data/ensemble_outputs.json --models gpt-4o-mini gpt-3.5-turbo


* Reads `data/humanevalcomm_subset.json`
* Produces `data/ensemble_outputs.json`

### 3. Run Execution Harness

bash terminal:
python src/run_execution_eval.py --input data/humanevalcomm_subset.json --output data/execution_results.json

* Produces `data/execution_results.json`

### 4. Run Analysis

bash terminal:
python src/analysis.py


* Compares baseline vs. execution
* Produces `data/analysis_report.json` and `data/analysis_plot.png`


## Results

From our pilot (4 tasks evaluated):

* **Agreements (baseline vs execution):** 1/4 (25%)
* **Disagreements:** 3/4 (75%)
* **Failure mode:** baseline often produced *UNKNOWN* judgments
* **Conclusion:** Execution-based ground truth exposes unreliability in single-LLM judges

## Report

The technical report is available in the repo as highlighted above
It describes:

* Introduction & motivation
* Methodology (ensemble + execution + analysis)
* Pilot results & analysis
* Proposed HumanEvalComm-V2 design
* Conclusion & future work


## Author

* **Olatunde Akinrolabu**
* PhD Applicant, Michigan Technological University
* Contact: [davidolatundeakinrolab@gmail.com]