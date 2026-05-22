# Module 7 Integrated Evaluation Report — Fine-Tuning vs. Pre-Trained Inference

> The Module 7 deliverable. Synthesizes Lab 7A (fine-tuning), Integration 7A (domain shift), Lab 7B (QA), and Integration 7B (summarization).
>
> **Replace this template's placeholders with your numbers and analysis. Each of the six numbered sections below is required.** Section 7 (Challenge Extensions) is optional — only required if you complete one or more challenge tiers from the learner guide.

---

## 1. Comparison Table

Paste your numbers from `metrics.json` (Lab 7A), `qa_metrics.json` (Lab 7B), and `summary_metrics.json` (this integration). The TA cross-checks that these match your submitted files.

| Task | Approach | Model | Training cost | Inference cost | Quality metric | Value |
|---|---|---|---|---|---|---|
| Sentiment classification (Lab 7A) | Fine-tuning | DistilBERT | ~30 min CPU + 3K labels | ~50 ms / example | Macro-F1 | 0.6066 |
| Domain transfer (Integration 7A) | Fine-tuned model out-of-domain | (same) | already trained | ~50 ms / example | Domain-shift judgment | Qualitative: Visible breakdown; tech news labeled as negative due to jargon. |
| Extractive QA (Lab 7B) | Pre-trained inference | distilbert-base-cased-distilled-squad | 0 | ~50 ms / example | EM / token-F1 | EM: 0.9667 / F1: 0.9889 |
| Summarization (Integration 7B) | Pre-trained inference | distilbart-cnn-6-6 | 0 | ~3 sec / example | ROUGE-1 / 2 / L F1 | R1: 0.3683 / R2: 0.1572 / RL: 0.2670 |

## 2. Findings

3–5 bullet points characterizing what each approach excels at and where it breaks. Tied to your specific numbers.

- QA Superiority: The pre-trained QA model achieved the highest performance (F1: 0.9889), proving that SQuAD-trained models are highly robust for literal information extraction from news articles.

- Classification Struggle: Sentiment classification (Lab 7A) showed a Macro-F1 of 0.6066, with the "neutral" class being particularly difficult (F1: 0.51), highlighting that fine-tuning requires more diverse data to handle nuanced sentiments.

- Inference Latency bottleneck: Summarization is significantly slower (~3s per example) compared to QA and classification (~50ms), making it the primary bottleneck for real-time production pipelines.

- Keyword vs. Phrasing: The gap between ROUGE-1 (0.3683) and ROUGE-2 (0.1572) indicates that while the model captures individual key concepts well, it struggles to reproduce the exact phrase structures found in human reference summaries.

## 3. Faithfulness Check

Pick three summaries from `summary_predictions.csv` (one high-ROUGE, one mid-ROUGE, one low-ROUGE). For each:

- Quote the article excerpt and the predicted summary.
- Mark whether the summary is faithful (every claim in the summary appears in the article).
- Comment on what ROUGE caught or missed for this case.

### Example A — high ROUGE

> Article excerpt: John Mayer says he has a granuloma next to his vocal cords. Granuloma is a small area of tissue inflammation...
> Predicted summary: John Mayer has suffered from a granuloma, a small area of tissue inflammation in the lungs. The singer and songwriter said he had undergone months of monitoring...
> ROUGE-1: 0.6575; ROUGE-2: 0.4507; ROUGE-L: 0.6027_
> Faithful? No/Partial. While the description of a granuloma is faithful to the text, the model hallucinated the location as "lungs" instead of "vocal cords." ROUGE remained high because most keywords matched perfectly.

### Example B — mid ROUGE
> Article excerpt: "Rapper Soulja Boy arrested after allegedly running from police in Georgia. Officers responded to a report of a large group..."
> Predicted summary: "Atlanta rapper DeAndre Cortez Way, 19, charged with obstruction after running from police. Rapper was among a large group that had gathered at a home..."
> ROUGE-1: 0.5161; ROUGE-2: 0.1758; ROUGE-L: 0.3011
> Faithful? Yes. Every claim in the summary appears in the article. ROUGE is moderate because the model used the rapper's real name while the reference used his stage name.

### Example C — low ROUGE

> Article excerpt: "Desperate Housewives actress Eva Longoria Parker gives peek into closet. Says she has Christian Louboutin espadrille wedges..."
> Predicted summary: "I love my new name. In Texas people are formal, so now it's 'Mrs. Parker' I feel old! But I love it, says Parker..."
> ROUGE-1: 0.1316; ROUGE-2: 0.0; ROUGE-L: 0.1053
> Faithful? No. The model focused on a direct quote regarding her name change rather than summarizing the actual content (the closet tour) described in the reference summary.

## 4. Production Decision Matrix

For each scenario, recommend fine-tuning or pre-trained inference. **Justify with one specific sentence tied to your measured numbers.**

| Scenario | Recommendation | Justification |
|---|---|---|
| Real-time app store review triage dashboard for a product team | Fine-tuning | Low latency (~50ms) is essential for real-time dashboards, and the measured 0.60 Macro-F1 is sufficient for initial automated sorting. |
| Daily tech / entertainment news summary digest for an internal newsroom | Pre-trained inference | A ROUGE-1 of 0.3683 is adequate for "gisting" for internal staff without the high cost of manual labeling for summarization. |
| Domain-expert QA on legal contracts | Fine-tuning | Despite 0.98 F1 on news, legal contracts require extreme precision where pre-trained models often fail due to lack of domain-specific logical training. |

## 5. What You Would Do Differently

One paragraph on what you would change about your approach if you had a labeled summarization dataset for the tech/entertainment news domain. Be concrete — what investment would meaningfully change the numbers?

If a labeled summarization dataset were available, I would fine-tune the DistilBART model specifically on the tech/entertainment domain to improve the ROUGE-2 scores (currently 0.1572). This would train the model to better handle technical terminology and avoid hallucinations (like swapping vocal cords for lungs). Furthermore, I would apply model quantization to reduce the 3-second inference time, making it viable for higher-volume news feeds.

## 6. Limits of the Evaluation

One paragraph on what these numbers do **not** tell you. Faithfulness, calibration, latency under load, etc. Pick the limits that matter most for the production scenarios in Section 4.

These numbers do not capture factual faithfulness; as seen in Example A, a high ROUGE score can coexist with factual errors (hallucinations). Additionally, the EM/Token-F1 for QA (Lab 7B) is based on literal extractive questions, which does not prove the model can handle abstract reasoning. Finally, latency was measured on a single CPU, which does not reflect performance under a high-concurrency production load or the potential speedups of GPU hardware.

---

<!--
Section 7 below is **optional** — only required if you complete one or more challenge tiers (see the integration's learner guide → "Challenge Extensions").
- Tier 1 — Cross-Modal Speech-to-Text → fill in Section 7.1
- Tier 3 — Summarizer Pareto Frontier → fill in Section 7.2
- Tier 2 — Faithfulness Audit at Scale → rewrites Section 3 above (does NOT add to Section 7)
Delete this Section 7 block if you are not completing any challenge tier.
-->

## 7. Challenge Extensions (optional)

### 7.1 — Cross-Modal Observation (Tier 1, if completed)

_(your paragraph + 3-clip "what the model heard wrong" table; also add a new row to the Section 1 comparison table using your corpus WER from `asr_metrics.json`)_

### 7.2 — Multi-Model Production Selection (Tier 3, if completed)

_(your Pareto-plot embed or precise prose description + per-scenario model recommendations grounded in measured ROUGE-L / latency from `model_comparison.csv`)_
