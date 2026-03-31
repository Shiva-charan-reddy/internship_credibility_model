document.getElementById('verifyForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const companyName = document.getElementById('company_name').value;
    const salary = document.getElementById('salary').value;
    const link = document.getElementById('job_link').value;
    const description = document.getElementById('job_description').value;

    const payload = {
        job_description: description,
        company_name: companyName,
        email: "",
        salary: salary,
        job_link: link
    };

    const loader = document.getElementById('loader');
    const resultCard = document.getElementById('resultCard');

    // Show Loading
    resultCard.style.display = 'none';
    loader.style.display = 'flex';

    try {
        const response = await fetch('https://internship-credibility-model.onrender.com/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        const data = await response.json();

        // Hide loader
        loader.style.display = 'none';

        displayResults(data, description);

    } catch (error) {
        loader.style.display = 'none';
        alert("Failed to connect to the analysis server. Make sure the FastAPI backend is running.");
        console.error("API Error:", error);
    }
});

function displayResults(data, originalDesc) {
    const resultCard = document.getElementById('resultCard');
    const scoreText = document.getElementById('scoreText');
    const progressCircle = document.getElementById('progressCircle');
    const statusBadge = document.getElementById('statusBadge');
    const reasonsList = document.getElementById('reasonsList');
    const highlightDisplay = document.getElementById('highlightedTextDisplay');

    resultCard.style.display = 'block';

    // 1. Update Score and Circular Progress
    const isScam = data.prediction_label === "Scam";
    const confidence = data.confidence_score;

    // Animate the counter
    let currentScore = 0;
    const interval = setInterval(() => {
        currentScore++;
        scoreText.textContent = currentScore + '%';

        // Update circle gradient dynamically
        const color = isScam ? 'var(--scam-red)' : 'var(--legit-green)';
        const degrees = (currentScore / 100) * 360;
        progressCircle.style.background = `conic-gradient(${color} ${degrees}deg, var(--glass-bg) 0deg)`;

        if (currentScore >= confidence) {
            clearInterval(interval);
        }
    }, 15); // Adjust speed

    scoreText.style.color = isScam ? 'var(--scam-red)' : 'var(--legit-green)';

    // Update Badge
    statusBadge.textContent = isScam ? `High Risk: ${data.prediction_label}` : `Safe: ${data.prediction_label}`;
    statusBadge.className = isScam ? 'status-badge status-scam' : 'status-badge status-legit';

    // 2. Render Reasons
    reasonsList.innerHTML = '';
    data.reasons.forEach(reason => {
        const li = document.createElement('li');
        li.innerHTML = `<i class="fa-solid ${isScam ? 'fa-triangle-exclamation' : 'fa-check'}"></i> ${reason}`;
        if (isScam) li.style.borderLeftColor = 'var(--scam-red)';
        else li.style.borderLeftColor = 'var(--legit-green)';
        reasonsList.appendChild(li);
    });

    // 3. Highlight Text
    let highlightedText = originalDesc;
    if (data.highlighted_words && data.highlighted_words.length > 0) {
        // Simple replace for exact matches. For robust systems, regex boundary replaces are better.
        data.highlighted_words.forEach(word => {
            const regex = new RegExp(`(${word})`, 'gi');
            highlightedText = highlightedText.replace(regex, '<span class="scam-word">$1</span>');
        });
    }
    highlightDisplay.innerHTML = highlightedText;

    // Scroll down to results smoothly
    resultCard.scrollIntoView({ behavior: 'smooth' });
}
