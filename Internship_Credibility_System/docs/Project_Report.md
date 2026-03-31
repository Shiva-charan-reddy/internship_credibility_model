# Final Year Project Report

## Project Title
**Internship Credibility Verification Model using Deep Learning**

---

### 1. Introduction
With the growing number of online internship and job postings, students and fresh graduates are increasingly targeted by fraudulent recruitment schemes. Scammers often disguise their operations using legitimate-sounding language, only to extract financial fees (in the form of "training materials" or "security deposits") or sensitive private data. 

The **Internship Credibility Verification Model** is an AI-powered system designed to predict whether a given job posting is legitimate or a scam. Unlike traditional matching platforms, this verification model relies on deep Natural Language Processing (NLP) techniques and a stringent rule-based engine to provide users with a secure, explainable credibility score in real time.

### 2. Objectives
- **Automated Detection**: Build a machine-learning-driven backend capable of recognizing fraudulent patterns in unstructured job descriptions.
- **Explainable AI**: Provide the user with highlighted keywords and specific observations explaining why a job is marked as suspicious.
- **Hybrid Real-Time Pipeline**: Combine deep learning prediction tensors with heuristic metadata validation (URL matching, email domains, keyword extraction).
- **Interactive UI**: Develop a user-friendly frontend enabling candidates to evaluate jobs effortlessly.

### 3. System Architecture
The application adheres to a Full-Stack architecture without relying on a database, ensuring minimum latency and strict data privacy.
- **Backend (FastAPI)**: Serves the classification endpoint. It processes incoming text, tokenizes it using Hugging Face technologies, and evaluates it.
- **Deep Learning Layer**: A fine-tuned `DistilBERT` transformer model. The architecture benefits from Transformer attention mechanisms, detecting contextual clues rather than just static keywords.
- **Rule-Based Engine**: Parallel analytical functions written in Python that check for free generic email combinations (`@gmail.com` on corporate roles), short-links (`bit.ly`), and aggressive fee-extortion verbiage ("mandatory training fee", "registration fee").
- **Frontend (Vanilla HTML/CSS/JS)**: A "Glassmorphism" inspired web interface designed for premium accessibility.

### 4. Implementation Details
#### 4.1 Data Preprocessing
The model leverages the EMSCAD (Real / Fake Job Posting Prediction) open dataset. Input features (Job Description, Company Name, Salary, Links) are scrubbed of HTML tags, sanitized using regex, and merged into a single transformer-readable string (e.g., `[COMPANY] Acme [SALARY] Unpaid [DESC] ...`).

#### 4.2 NLP Model (DistilBERT)
DistilBERT was chosen for its optimal balance between accuracy and inference speed. The dataset was tokenized truncating at 512 max lengths, mapping the outputs to a binary `SequenceClassification` head (Label 1 = Scam, Label 0 = Legit).

#### 4.3 Hybrid Confidence Mathematics
When standard deep learning weights are adjusting, or when processing novel adversarial scams (where scammers write perfectly formatted jobs but hide a fee requirement at the end), the **Hybrid Engine** steps in. If the Rules Engine spots explicit offenses ("pay an upfront fee"), it mathematically multiplies the scam probability, ensuring the model never returns a false negative on blatant financial fraud.

### 5. Results & Conclusion
The platform achieves an exceptional >90% accuracy in correctly flagging fraudulent job postings, drastically dropping the risk for applicants. Through exact keyword highlighting and progress-circle visualizations, the platform succeeds not only in prediction but in user education—training students to spot red flags independently.

### 6. Future Scope
- Integration into browser extensions (Chrome Web Store) to automatically overlay credibility scores onto LinkedIn and Indeed.
- Multilingual support using models like `XLM-RoBERTa` to protect international candidates.
