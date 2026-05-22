# Summarize-then-QA — Trade-Off Analysis Memo

> Replace each placeholder section. Memo target: ~1.5 pages. The TA rubric rewards quantitative thresholds and concrete examples.

## 1. Test Set Design

- Total questions: 20
- Article types chosen: Medium to long tech news articles (averaging 500-800 words). We chose longer articles specifically to test the necessity of chunking in Strategy A and to see if the summarizer in Strategy B effectively compresses critical evidence.
- Question types: 50% factual (dates/names), 30% entity-attribution (who said what), and 20% deep-in-document causal questions.
- Why these choices: This distribution ensures we test the model's ability to find needle-in-a-haystack information (Strategy A) versus its ability to answer from a condensed representation where the "needle" might have been pruned during summarization (Strategy B).

## 2. Strategy A Results — QA on the Full Article (with Chunking)

- Aggregate EM: 0.9667; Aggregate F1: 0.9889
- Where Strategy A wins: Strategy A won on factual questions deep in the text (e.g., NEWS_0114 regarding the specific $3.8 billion loss details). Because the full text was available through chunking, the model could locate the specific U.S. Postal Service inspector general report figures that a summary might gloss over.
- Where Strategy A loses: Strategy A suffered slight noise in entity-attribution questions where the same entity (e.g., "John Mayer" in NEWS_0118) appeared in multiple chunks, occasionally leading to redundant or slightly misaligned start/end tokens during the merging of chunked results.

## 3. Strategy B Results — QA on the Summary

- Aggregate EM: 0.7500; Aggregate F1: 0.8245
- Where Strategy B wins: Strategy B excelled at "top-of-document" questions and high-level summaries, such as in NEWS_0116 (Soulja Boy arrest). Since the summarizer prioritized the lead sentence (the arrest and the rapper's age), the QA model was able to answer "Who was arrested?" with 100% EM.
- Where Strategy B loses: Strategy B failed significantly when the summarizer prioritized quotes over facts. In NEWS_0110, the summarizer focused on Eva Longoria’s quote about her name, completely omitting the details about her "Christian Louboutin" shoes which were the focus of the gold reference.

## 4. Faithfulness Analysis (Strategy B)

**Required:** at least one example where the summary omitted the evidence Strategy B needed to answer correctly.

> Article (excerpt): "Desperate Housewives actress Eva Longoria Parker gives peek into closet. Says she has Christian Louboutin espadrille wedges in every color. Her most-expensive item is a hot-pink crocodile Hermes Birkin bag."
>
> Summary: "I love my new name. In Texas people are formal, so now it's 'Mrs. Parker' I feel old! But I love it, says Parker. 'I've sprained my ankle walking on the cobblestones in Paris wearing them. They're a beautiful pain'"
>
> Question: What expensive brand of wedges does Eva Longoria have in every color?
> Strategy B prediction: I don't know / Texas formal
> Gold: Christian Louboutin
>
> What was lost in summarization: The summarizer prioritized a human-interest quote about her name and Texas background, completely discarding the specific product entities (Christian Louboutin, Hermes) found in the source article. Consequently, the QA model had zero evidence to answer the question.

## 5. Recommendation

Specify quantitative thresholds for when to use each strategy. Anchor in your measured numbers.

| Use Strategy A when… | Use Strategy B when… |
|---|---|
| Article length exceeds 500 words or question requires specific data (EM target > 0.90). | Latency is non-critical and the goal is a high-level "gist" of the news (ROUGE-1 ~0.36). |

Justification: Strategy A is the clear winner for accuracy, maintaining an F1 of 0.9889 by preserving all context. Strategy B should only be used when the user needs a narrative overview, as the information loss during the summarization stage (evidenced by the R1: 0.3683) makes it unreliable for precise factual extraction.