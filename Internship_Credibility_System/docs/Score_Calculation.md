# How the Confidence Percentage is Calculated
*A transparent breakdown of the Internship Credibility Math Engine*

The final visual percentage shown on the frontend (e.g., "94% Scam" or "92% Legit") is not entirely arbitrary. It is mathematically forged by a strict **Two-Part Scoring Engine** that combines Natural Language Processing (NLP) heuristics with a Rule-Based penalty system.

Here is exactly how the backend builds that specific percentage number, step-by-step:

---

## 1. The Base NLP Heuristic Score
*(Located in `backend/model/inference.py`)*

The system assumes baseline optimism. Every single job description begins with a **Base Scam Probability of `0.20` (20%)**. The engine then technically measures the string structure:

* **The Length Test**: 
  * If the text is shorter than 150 characters, it is highly suspicious (real jobs are detailed). The math adds `+0.55` to the probability.
  * If the text is massive and highly detailed (> 1200 characters), it is rewarded. The math subtracts `-0.12`.
* **The "Shouting" Test (Capitalization Ratio)**: 
  * Scammers love to use ALL CAPS (e.g., "URGENT PAYMENT REQUIRED START NOW!"). If the system calculates that more than 12% of the total letters are uppercase, it adds `+0.40` to the probability.
* **The Ghost Employer Test**:
  * If the user fails to provide a physical Company Name, the system recognizes a "generic template" and adds `+0.45` to the probability.

At the end of this phase, the Base Score is permanently constrained between `0.02` (Extremely Safe) and `0.98` (Extremely Dangerous).

---

## 2. The Semantic Extortion Penalty
*(Located in `backend/utils/rules.py`)*

Parallel to the NLP math, the text is run through a live Regex dictionary targeting over 25 hardcoded extortion schemes (e.g., *"training fee"*, *"western union"*, *"bank details"*).

* **The Multiplier**: Every time one of these keywords triggers, `suspicious_flags` increments by 1.
* **The Calculation**: The system applies a base penalty using the formula: `min(0.35 * suspicious_flags, 0.95)`.
   * *1 Scam Keyword Found = `0.35` Penalty.*
   * *2 Scam Keywords Found = `0.70` Penalty.*
   * *3+ Scam Keywords Found = `0.95` Penalty.*

---

## 3. The Final Synthesis Overrides
*(Located in `backend/main.py`)*

Once both engines produce their numbers, they are fused together:
`Final Probability = Base NLP Score + Extortion Penalty`

To guarantee safety, we use absolute **Overrides**:

### Scenario A: The Clean Pass (Safe Job)
If the Extortion Penalty is exactly `0` (no suspicious scams were demanded), the system mathematically multiplies the entire Final Probability by `0.6`.
> *Example: A well-written long job gets an NLP score of `0.10`. Rules caught nothing (`0`). `0.10 * 0.6 = 0.06 Scam Probability`. The Frontend displays **94% Safe**.*

### Scenario B: The Violation Bypass (Dangerous Fake)
If the Extortion Penalty is `> 0` (even just ONE scam keyword appeared), the math assumes the job is maliciously structured to bypass standard NLP. It mathematically forces the probability to automatically snap to **> 85% Scam**.
> *Example: A user copies the perfect Microsoft Job template (NLP Score `0.08`), but the scammer added "Candidates must pay an onboarding fee" at the bottom (Penalty `0.35`). The system triggers the override: `max(Final, 0.85 + (0.35 * 0.05))`. The Frontend displays **86% High Risk Scam**, ignoring the perfect Microsoft formatting.*
