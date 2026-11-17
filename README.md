# AI Job Matching MVP

## Features
- Resume PDF text extraction
- Dictionary-based skill detection
- TF-IDF + Cosine Similarity
- Ranked job recommendations
- Recruiter candidate ranking
- Sample jobs included

## Run locally
Requires Python 3.10+.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install and run:
```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed in the terminal (usually http://localhost:8501).

## Limitations
This is an MVP, not a production-ready hiring platform. It does not yet have authentication, persistent database, job-posting management, scanned-PDF OCR, or deployment. Scores indicate text similarity, not the probability a candidate is qualified. Use fictional/demo data.
