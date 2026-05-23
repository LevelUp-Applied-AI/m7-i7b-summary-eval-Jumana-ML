# Summarize-then-QA — Trade-Off Analysis Memo

> Replace each placeholder section. Memo target: ~1.5 pages. The TA rubric rewards quantitative thresholds and concrete examples.

## 1. Test Set Design

- Total questions: 20
- Article types chosen: Medium and Long tech/entertainment news articles (ranging from 400 to 900 tokens). We chose long articles specifically to trigger the overlapping chunking logic in Strategy A and the compression logic in Strategy B.
- Question types: Factual (40%), Entity-attribution (30%), Causal (20%), and Quote-based (10%). The distribution spans from top-of-document headlines to deep-in-document specific details.
- Why these choices: This design evaluates whether Strategy B (summarization) retains the "needles" (facts) found in the "haystack" (long article). By including causal and deep-document questions, we test the limits of what a 120-word summary can represent compared to a full-text chunked scan.

## 2. Strategy A Results — QA on the Full Article (with Chunking)

- Aggregate EM: 0.4000; Aggregate F1: 0.5508
- Where Strategy A wins: Strategy A performed better on deep factual questions like Q5 (USPS spending) and Q6 (reported losses). Because the answer was a specific dollar amount deep in a technical paragraph, Strategy A found it via a direct scan, whereas Strategy B's summary occasionally glossed over these specific figures.
- Where Strategy A loses: Strategy A suffered from "chunking noise" in Q1 and Q10. In Q1 (John Mayer condition), the model sometimes hallucinated the context from a neighboring chunk (mentioning 'lungs' instead of 'vocal cords'), leading to lower EM despite having the full text available.

## 3. Strategy B Results — QA on the Summary

- Aggregate EM: 0.4500; Aggregate F1: 0.5619
- Where Strategy B wins: Strategy B outperformed Strategy A on high-level news questions such as Q3 (Soulja Boy arrest location) and Q15 (Susan Boyle appearance). The summarizer successfully removed irrelevant details, presenting a clean context that allowed the QA model to find the correct answer more reliably (EM=0.4500).
- Where Strategy B loses: Strategy B failed on Q7 and Q8 (Eva Longoria's shoes/closet). The summarizer prioritized the emotional quote about her name change, completely omitting the specific brand names (Christian Louboutin) present in the source text.

## 4. Faithfulness Analysis (Strategy B)

**Required:** at least one example where the summary omitted the evidence Strategy B needed to answer correctly.

> Article (excerpt): "...Says she has Christian Louboutin espadrille wedges in every color. Her most-expensive item is a hot-pink crocodile Hermes Birkin bag."
>
> Summary: "I love my new name. In Texas people are formal, so now it's 'Mrs. Parker' I feel old! But I love it, says Parker. 'I've sprained my ankle walking on the cobblestones in Paris wearing them.'"
>
> Question: What brand of shoes does Eva Longoria have in every color?
> Strategy B prediction: [Empty / Parker]
> Gold: Christian Louboutin
>
> What was lost in summarization: The summarizer prioritized the "human interest" quote about the actress's name change and her feelings. In doing so, it discarded the specific brand entity "Christian Louboutin," leaving the QA model with no evidence to answer the factual question.

## 5. Recommendation

Specify quantitative thresholds for when to use each strategy. Anchor in your measured numbers.

| Use Strategy A when… | Use Strategy B when… |
|---|---|
| Article length > 500 tokens AND the question requires specific factual retrieval (e.g., prices, dates, or technical specs). | Article length < 1000 tokens AND the goal is high-level "gist" answering where noise reduction is prioritized (EM=0.45). |

Justification: Strategy B acts as an effective noise filter for general news headlines, as evidenced by its higher EM (0.45 vs 0.40). However, the faithfulness loss in Strategy B (omitting key entities like brands) means Strategy A remains necessary for domain-expert tasks where precision on secondary details is required.

---