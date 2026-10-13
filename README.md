# Service Desk Workflow Automation — Working Baseline

**Status:** Working local service-desk demonstration. The current triage is **rule-based**, not an ML model. SLA-risk prediction, external API integration and production authentication are not yet implemented.

## Features

- Submit tickets with validation.
- Explainable priority and team assignment based on ticket text.
- Persistent SQLite ticket queue.
- Status transitions and priority dashboard.
- Unit tests for triage and workflow.

## Run

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Roadmap

1. Add synthetic labelled training data and compare ML classification to rules.
2. Add calibrated SLA-breach prediction and evaluation.
3. Add REST API and audit log.
4. Add permissions and deployment safeguards.

Demo only; do not use for real incident response.
