# Hybrid Decentralized Learning Framework for Media Integrity Verification

A beginner-friendly Python prototype inspired by the project report. It combines:
- NLP text features using TF-IDF and a Logistic Regression classifier
- A reward-guided decision layer (DRVGA-inspired prototype)
- A tamper-evident SHA-256 hash-chain audit log
- A Flask web interface for submitting text and viewing results

## Important scope note
This is a **prototype**, not a validated research implementation. The included sample dataset is tiny and illustrative; its metrics must not be reported as research results. The audit log is a local hash chain, **not a deployed decentralized blockchain**. The reward-guided module demonstrates the idea but is not a trained reinforcement-learning agent. For a real experiment, use a documented dataset, train/test split, baselines, and a deployed blockchain such as a local Ethereum test network.

## Requirements
- Python 3.10 or newer
- pip

## Run on Windows (VS Code / Command Prompt)

```bash
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python train_model.py
python app.py
```

Open http://127.0.0.1:5000 in your browser.

If `py` is unavailable, use `python` instead.

## Project structure

```text
media_integrity_verification/
├── app.py
├── train_model.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── sample_news.csv
├── models/                  # created by train_model.py
├── media_verifier/
│   ├── __init__.py
│   ├── nlp_detector.py
│   ├── drvga.py
│   └── audit_chain.py
├── templates/
│   └── index.html
└── audit_logs/               # created when the app runs
```

## GitHub upload

1. Create a new repository on GitHub, for example `media-integrity-verification`.
2. Extract this ZIP file.
3. Open the extracted folder in VS Code.
4. Open Terminal in that folder and run:

```bash
git init
git add .
git commit -m "Initial media integrity verification prototype"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/media-integrity-verification.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username and use the repository URL GitHub provides. Never upload passwords, API keys, private datasets, or virtual environments.

## How it works
1. The user submits a text claim.
2. The NLP model predicts `authentic` or `fake` based on its training examples.
3. The DRVGA-inspired layer combines the model probability with simple consistency signals to produce a demo credibility score.
4. A SHA-256 hash of the input and result is appended to a local hash-linked audit log.
5. The web page displays the prediction, score, and audit hash.

## Limitations and next steps
- Add a proper, licensed fake-news dataset and cite its source.
- Evaluate with a stratified train/test split and report accuracy, precision, recall, and F1.
- Add image/video analysis only after implementing and testing a suitable model.
- Replace the local hash-chain with a real smart contract and blockchain network if decentralized on-chain verification is required.
- Add tests, input limits, error handling, and deployment security before public hosting.
