# End-to-End System Workflow
*Internship Credibility Model Architecture & Data Flow*

This document breaks down the exact journey of a single job description from the moment a user clicks "Verify" to the moment the UI displays the Scam/Legit percentage.

---

### Phase 1: User Input (The Frontend Trigger)

1. **The Interface (`frontend/index.html`)**: 
   The user opens the web application and fills out a "Glassmorphism" styled form. They provide the **Company Name**, **Salary**, **Job Link**, and the large **Job Description** text.
2. **The Event Listener (`frontend/script.js`)**: 
   When the user clicks the main *Verify* button, JavaScript prevents the page from reloading (`e.preventDefault()`). It packages all four text inputs into a `JSON Payload` (a structured data object).
3. **The Loading State**: 
   JavaScript immediately hides the results card and brings up a spinning loader overlay, warning the user that the "Neural Network & Rule Engine" is spinning up.

---

### Phase 2: Data Transmission (Network Layer)

1. **The API Fetch (`frontend/script.js`)**: 
   A `fetch()` POST request transports the JSON payload directly over the internet to the **FastAPI Backend Server** (hosted on Render).
2. **The Router (`backend/main.py`)**: 
   FastAPI receives the payload at the explicit endpoint `@app.post("/predict")`. The schema strictly requires the data to match the `JobData` Pydantic class.

---

### Phase 3: Data Preprocessing (Sanitizing the Input)

1. **Text Normalization (`backend/utils/preprocessing.py`)**: 
   The raw job description is passed into the `clean_text()` function.
2. **Regex Operations**: 
   Python uses Regular Expressions (`re` library) to aggressively remove raw HTML tags (like `<b>` or `<p>`), trailing whitespaces, and unexpected Unicode symbols.
3. **Data Fusion**: 
   The parameters are combined into a single, standardized string of context for the AI: 
   `"[COMPANY] {name} [EMAIL] {email} [SALARY] {salary} [DESC] {job_description}"`

---

### Phase 4: The Dual Analysis Engines (The "Brain")

FastAPI now splits the data, running it through two distinct analytical systems simultaneously:

#### Path A: The NLP Heuristic Model (`backend/model/inference.py`)
Since the heavy Transformer tensors were disabled for cloud deployment, the lightweight "Production Surrogate Mode" activates:
- It technically measures the *physical characteristics* of the text.
- **Length Test**: If `< 150` characters, it heavily penalizes the text (+55% Scam Probability) because legitimate companies post extensive requirements.
- **Casing Test**: It calculates the ratio of UPPERCASE to lowercase letters. Scammers often 'shout' phrases like "URGENT HIRING START IMMEDIATELY". If the text is > 12% caps, the scam probability rises (+40%).
- **Result A**: Returns a Base Probability fraction (e.g., `0.20` base).

#### Path B: The Rule-Based Extortion Engine (`backend/utils/rules.py`)
This engine strictly reads the *meaning* and *semantics*.
- **Scam Dictionary Check**: It scans the text for a massive hardcoded dictionary array of scam phrases (e.g., *"mandatory training module"*, *"pay a fee"*, *"₹2,499"*, *"western union"*).
- **Domain Verification**: It extracts URLs mapped in the text to see if they are suspicious shorteners like `bit.ly`.
- **Result B**: If *any* of those keywords hit, it outputs a severe **Penalty Score** (up to 0.95), plus a list of text string **Reasons** for the user.

---

### Phase 5: The Hybrid Synthesis Math (`backend/main.py`)

1. **Combining The Two Paths**: 
   The server takes `Base Probability (Path A)` AND adds the `Penalty Score (Path B)`. 
2. **Override Logic**: 
   - If the penalty score is `0` (the rules caught nothing), it multiplies the Scam probability by `0.6`, dropping the fake probability drastically and forcing a clean high **"Legitimate"** score.
   - If the penalty score is `> 0` (even one single scam keyword was found), it aggressively overrides the score to be mathematically greater than `0.85` (**High Risk Scam**).
3. **Data Export**: 
   FastAPI bundles the final binary label (Scam/Legit), the 0-100 Confidence Percentage, and the array of Reasons/Highlights back into a JSON object and shoots it back as a `200 OK` HTTP Response to the Frontend.

---

### Phase 6: User Interface Rendering (The Display)

1. **Receiving Data (`frontend/script.js`)**: 
   The `await response.json()` function catches the data. It immediately dismisses the loading overlay spinner.
2. **Color Calculus**: 
   If `prediction_label` == `"Scam"`, it sets CSS variables to `var(--scam-red)`. If `"Legit"`, it forces `var(--legit-green)`.
3. **Micro-Animations**: 
   A `setInterval` loops quickly from `0%` scaling accurately up to the final Confidence Percentage. At the same time, the Glass CSS gradient dynamically rotates around the circle.
4. **Explainable Formatting**: 
   Using JavaScript's `.replace()` operation, the engine locates the dangerous scam keywords inside the original text box and wraps them in `<span class="scam-word">` tags, causing them to glow red within the UI so the user can see *exactly* what triggered the 95% fake score.
