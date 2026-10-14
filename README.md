# AI-Powered Service Desk & Workflow Automation

[![Python unit tests](https://github.com/arqam3025/ai-service-desk-automation/actions/workflows/tests.yml/badge.svg)](https://github.com/arqam3025/ai-service-desk-automation/actions/workflows/tests.yml)


**Status:** Local portfolio application with SQLite ticket workflows and **synthetic-data machine learning experiments**. Not validated for real support operations.

## Implemented

- Create, route, view and update support tickets in a persistent SQLite database.
- Rule-based priority and team routing for the operational demo.
- A separate TF-IDF + logistic regression ticket-team classifier trained on **templated synthetic examples**.
- A simple logistic regression SLA-breach *simulation* based on priority, using simulated outcome labels.
- A 75/25 stratified train/test split, classification accuracy/report, ROC-AUC and Brier score.
- Streamlit evaluation panel comparing held-out synthetic model outputs.
- Automated unit tests.

## Local setup (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

To run tests:

```powershell
python -m unittest discover -s tests -v
```

## Architecture

Ticket form → transparent rule-based routing → SQLite → queue/status dashboard.

Separately: templated synthetic labelled tickets → TF-IDF and logistic regression → held-out classification metrics → optional ML suggestion in the interface.

Synthetic priority and outcome labels → logistic regression → simulated SLA-breach risk estimate.

**ML suggestions do not automatically overwrite the rule-based ticket routing.**

## Critical limitations

- Ticket examples are template-generated, and train/test splits can share similar wording. Classification scores cannot establish generalisation to real customer tickets.
- SLA labels are generated randomly from a specified probability by priority and asset. The model has not learned actual SLA outcomes and its probabilities are **not calibrated for real operations**.
- There is no authentication, audit logging, external service integration, production deployment or operational security review.
- For a credible production pilot, obtain authorised, de-identified historical tickets, split by time/customer, measure performance on unseen incidents, audit fairness and privacy, and require human review before automated routing.

## Next steps

Add authorised real-world evaluation data, confidence-based human escalation, read-only REST API, audit trails and security controls.
