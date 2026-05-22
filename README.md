# Module 7 Week B — Integration Task: Summarization & Integrated Evaluation Report

This is the starter repo for the Module 7 Week B Integration Task. **The integrated evaluation report you produce here is the M7 deliverable.**

The full integration guide is at <a href="https://levelup-applied-ai.github.io/aispire-14005-pages/modules/module-7/496c1c2b" target="_blank">the integration guide page</a> — read it first.

## Quick start

```bash
pip install -r requirements.txt
make summarize    # runs full pipeline; first run downloads ~250 MB
```

The first call to `pipeline("summarization", ...)` downloads the model. Plan ~3 minutes for the first run; subsequent runs use cached weights. The full evaluation on 120 articles completes in ~6–8 minutes on CPU after the model is cached.

## What you will produce

Committed:
- `summarize.py` — your implementation
- Updated `README.md` — Model Identification and Architecture
The summarization pipeline utilizes the sshleifer/distilbart-cnn-6-6 model, which is a specialized version of the BART (Bidirectional and Auto-Regressive Transformers) architecture. This specific model is a "distilled" version, meaning it has been compressed from the original facebook/bart-large-cnn to provide a faster inference time without a significant loss in performance. It consists of 6 encoder layers and 6 decoder layers, making it highly efficient for CPU-based environments. The model was fine-tuned on the CNN/DailyMail dataset, which specializes in summarizing news articles by generating abstractive summaries that capture the most relevant entities and events in a concise format.

Tech News Corpus and Reference Data
The evaluation uses the M6 Tech News Corpus version, consisting of a filtered subset of 120 news articles focused on technology, entertainment, and digital culture. The reference summaries are provided in the data/tech_news_summaries_reference.csv file. These summaries serve as the "ground truth" for calculating our quality metrics. By comparing the model's generated output against these editor-authored references, we can measure how well the model handles technical jargon, product names, and journalistic narrative structures.

Reproducibility and Re-run Command
To ensure full reproducibility of the results and the generated metrics (summary_metrics.json), the evaluation can be executed using the automated Makefile. Anyone with access to this repository can re-run the full evaluation pipeline across the 120-article set by executing the following command in their terminal:
make summarize
This command orchestrates the loading of the CSV files, the initialization of the Hugging Face pipeline with deterministic beam search (num_beams=4), and the calculation of ROUGE-1, ROUGE-2, and ROUGE-L F1 scores using the rouge-score library with stemming enabled for more accurate linguistic matching.

- `summary_predictions.csv` — 120 rows with reference, predicted, and per-summary ROUGE
- `summary_metrics.json` — aggregate ROUGE-1/2/L F1
- `integrated-evaluation-report.md` — six-section integrated report (the M7 deliverable). Includes an optional Section 7 (Challenge Extensions) for learners completing challenge tiers — see the integration's learner guide.

**No model file** — pre-trained model loads from Hugging Face Hub at runtime.

## Data

- `data/tech_news_articles.csv` — 1,033 tech / entertainment / digital-culture news articles, curated from <a href="https://huggingface.co/datasets/glnmario/news-qa-summarization" target="_blank">glnmario/news-qa-summarization</a>. The full pool is here for inspection and stretch use; the integration evaluates on the 120-article subset that has reference summaries.
- `data/tech_news_summaries_reference.csv` — 120 reference summaries (one per evaluated article), shipped with the curated dataset (CNN editor-authored summaries from the source dataset).
- `data/tiny_articles_smoke.csv` + `data/tiny_refs_smoke.csv` — 3-row CI smoke fixtures (articles and references in separate files, matching the real-data schema).

## Make targets

```bash
make summarize    # full pipeline against the 120-article evaluation set
make smoke        # CI-only target — 3-row fixture
make clean        # remove generated outputs
```

## Submission

Open a Pull Request from your working branch into `main`. The autograder runs `make smoke` against the 3-row fixture and validates artifact schemas. PR description requirements are in the integration guide.

---

## License

This repository is provided for educational use only. See [LICENSE](LICENSE) for terms.

You may clone and modify this repository for personal learning and practice, and reference code you wrote here in your professional portfolio. Redistribution outside this course is not permitted.
