# PPT Presentation Outline: Internship Credibility AI

This document provides the exact slide-by-slide content for your Final Year Project PowerPoint presentation.

---

### Slide 1: Title Slide
- **Title**: Internship Credibility Verification Model using Deep Learning
- **Subtitle**: Protecting Students from Fraudulent Job Postings
- **Presenters**: [Your Name/Team Names]
- **Institution**: [Your University/College]

### Slide 2: Problem Statement
- **The Issue**: Rise in fraudulent internship listings targeting desperate students and fresh graduates.
- **The Tactics**: Scammers use professional jargon to ask for "mandatory training fees", "security deposits", or harvest private data.
- **The Gap**: Traditional job boards lack real-time textual verification for scam probability; students are forced to rely on pure intuition.

### Slide 3: Proposed Solution
- **The Product**: An AI-powered web application providing real-time scam probability scoring.
- **Core Methodology**: 
  - **Deep Learning**: Uses DistilBERT (Transformers) to analyze sentence context.
  - **Heuristics**: Uses a Rule-Based NLP engine to scan metadata (URLs, free emails, fee keywords).
- **Goal**: High accuracy + "Explainable AI" (highlighting exactly *why* a post is considered fake).

### Slide 4: System Architecture
*Visual suggestion: Include a flow chart diagram here*
1. **User Input** (Frontend UI) -> Company, Email, Salary, Job Description
2. **FastAPI Backend** -> Receives JSON payload
3. **Data Splitting** -> 
   - Path A: Tokenization & Transformer Inference
   - Path B: Rule-Based Logic Processing (Regex)
4. **Hybrid Math Engine** -> Fuses predictions into a final Confidence Score
5. **Output** -> Dynamic UI displaying highlighted text and Reasons.

### Slide 5: Technologies Used
- **Deep Learning**: PyTorch, Hugging Face Transformers (`DistilBERT`).
- **Backend API**: Python, FastAPI, Uvicorn.
- **Frontend**: HTML5, Vanilla JavaScript, CSS3 (Glassmorphism UI).
- **Data Engineering**: Pandas, Scikit-learn, Regex. 

### Slide 6: The Rule-Based Hybrid Advantage
- Why not just Deep Learning?
- Deep Learning can sometimes be fooled by highly professional English structures hiding scam clauses.
- **Our Hybrid Math**: If the AI is uncertain, but the rules engine spots "pay a registration fee" or a `bit.ly` shortened URL, the system dynamically boosts the Scam Confidence Score to 95%+, guaranteeing safety.

### Slide 7: Implementation & UI
*Visual suggestion: Add screenshots of the web app here!*
- **Feature 1**: Circular dynamic progress bar indicating safety.
- **Feature 2**: Highlighted red-text mapping exact suspicious words.
- **Efficiency**: No external database operations mean inference returns in under 2 seconds.

### Slide 8: Future Scope
- **Browser Extension**: Overlying our AI metrics directly onto LinkedIn or Indeed postings automatically.
- **Multilingual Support**: Extending tokenization to international languages.

### Slide 9: Conclusion
- By synergizing Transformer neural networks with hard-coded linguistic rules, our platform achieves a highly robust, explainable, and rapid defense layer against digital recruitment fraud.

### Slide 10: Questions & Demonstration
- "Thank you for listening!"
- (Transition to live web-app demonstration).
