# AI Task Automation Agent (Digital Worker)

A hackathon-ready Streamlit app that acts like a virtual operations employee.
It turns plain-English requests into executable task plans for:

- Email drafting
- Scheduling workflows
- Data-entry / data normalization
- Tool integrations (webhook handoff)

## What it does

1. Accepts a natural-language business request.
2. Uses Anthropic Claude to convert the request into structured JSON tasks.
3. Simulates autonomous execution with an execution log (dry-run friendly).
4. Exports a complete run artifact as JSON for auditability.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Environment

Set your API key via Streamlit secrets or environment variable:

- `ANTHROPIC_API_KEY`

## Why this is hackathon-friendly

- Works end-to-end today in dry-run mode.
- Easy to extend with real integrations (Gmail, Calendar, CRM, Slack, Notion, Airtable).
- Codebase is minimal and git-uploadable as-is.
