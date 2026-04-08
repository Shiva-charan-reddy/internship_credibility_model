# Job Link Verification Workflow
*How Extortion URLs and Hidden Domains are analyzed*

The **Job Link** input is an optional but incredibly critical field on the frontend. Scammers frequently use legitimate-sounding job descriptions but hide malicious phishing links or tracking malware inside the Apply URL. 

Here is the end-to-end workflow of exactly how the completely automated URL Analysis engine works:

---

## 1. Data Collection (Frontend)
When a user pastes a URL (e.g., `https://bit.ly/ApplyNow-Microsoft`) into the **Job Link** field on the website (`index.html`), JavaScript automatically binds it to the `job_link` string inside the POST Request payload alongside the Company Name and Description.

## 2. Extraction & Aggregation (Backend API)
When FastAPI receives the parameter, it doesn't just check the single link you provided. 
Inside `backend/utils/rules.py`, the `extract_urls()` function executes a massive Regular Expression (Regex) sweep over the *entire* Job Description paragraph, searching for any hidden `http` or `www.` links the scammer might have buried in the text.
The engine then mathematically combines the explicit Job Link with all the newly discovered hidden links into a single array to test them all simultaneously.

## 3. Domain Parsing (The Rule Engine)
For every URL found, the Python system utilizes the `urllib.parse.urlparse` library. This completely strips away the HTTP protocol and the URL path (the slashes at the end) to isolate the core **Domain Name** (the `netloc`).
> *Example: `https://tinyurl.com/a8f9ds` becomes just `tinyurl.com`.*

## 4. The Suspicious Domain Match
The isolated domain is cross-referenced against the `SUSPICIOUS_DOMAINS` blacklist array programmed into the security heuristic. This array explicitly targets **URL Shorteners**:
* `bit.ly`
* `tinyurl.com`
* `goo.gl`
* `t.co`

**Why?** Genuine corporate companies (like Google, Amazon, or Tata) use self-hosted secure Application Tracking Systems (e.g., `careers.google.com` or `workday.com`). They *never* use free URL-shorteners to funnel applicants. Therefore, a shortened link is a massive red flag indicating the author is hiding the true destination of the website, which is usually a fake login portal meant to steal passwords or credit cards.

## 5. Mathematical Penalization
If the Extortion Engine detects a blacklisted domain:
1. It immediately logs a specific **Reason Message** for the user interface: *"Suspicious shortened or untrusted URL found: bit.ly. Scammers use these to hide malicious sites."*
2. It increments the `suspicious_flags` integer by `+1`.
3. This adds an immediate numerical penalty of `+0.35` to the `rule_penalty` score.

Because the penalty is calculated as `> 0`, the backend math overrides the probability engine and forces the final result to jump to **Over 85% Scam Confidence**, instantly protecting the applicant from clicking the phishing link!
