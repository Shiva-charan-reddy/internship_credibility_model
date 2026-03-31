import re
from urllib.parse import urlparse

# Scammer keyword dictionary expanding to newer fake posting trends
SCAM_KEYWORDS = [
    "pay fee", "registration fee", "security deposit", "wire transfer", 
    "bank details", "western union", "urgent hiring", "guaranteed", 
    "no interview required", "start immediately", "get rich quick",
    "payment required", "money order", "investment required",
    "training fee", "one-time fee", "need to pay", "paid training",
    "onboarding fee", "application fee", "buy equipment", "purchase equipment",
    "deposit required", "upfront payment", "mandatory training module (paid)",
    "pay a one-time", "pay an upfront", "refundable deposit",
    "pay a ", "training module", "fee to access"
]

FREE_EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "protonmail.com"
]

SUSPICIOUS_URL_SHORTENERS = [
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "buff.ly", "ow.ly"
]

def analyze_email_domain(email: str, company_name: str) -> dict:
    if not email:
        return {"suspicious": False, "reason": ""}
    
    parts = email.split('@')
    if len(parts) != 2:
        return {"suspicious": True, "reason": "Invalid email format."}
    
    domain = parts[1].lower()
    
    if domain in FREE_EMAIL_DOMAINS:
        return {"suspicious": True, "reason": f"Uses free/generic email domain ({domain}) for a corporate job."}
    
    # Check mismatch (basic heuristic)
    comp_clean = re.sub(r'[^a-zA-Z0-9]', '', company_name.lower())
    domain_name = domain.split('.')[0]
    
    if comp_clean and comp_clean not in domain_name and domain_name not in comp_clean:
         # It's a bit strict, but good for scoring
         return {"suspicious": True, "reason": f"Email domain '{domain}' does not match company name."}
         
    return {"suspicious": False, "reason": ""}

def analyze_keywords(job_desc: str) -> dict:
    desc_lower = job_desc.lower()
    found_keywords = [kw for kw in SCAM_KEYWORDS if kw in desc_lower]
    
    if found_keywords:
        return {
            "suspicious": True, 
            "reason": f"Suspicious keywords detected: {', '.join(found_keywords)}",
            "keywords": found_keywords
        }
    return {"suspicious": False, "reason": "", "keywords": []}

def analyze_url(url: str) -> dict:
    if not url:
        return {"suspicious": False, "reason": ""}
    
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if not domain:
            domain = parsed.path.lower() # fallback if no scheme
            
        is_shortener = any(short in domain for short in SUSPICIOUS_URL_SHORTENERS)
        if is_shortener:
             return {"suspicious": True, "reason": f"Uses URL shortener ({domain})."}
    except Exception:
        return {"suspicious": True, "reason": "Malformed URL."}
        
    return {"suspicious": False, "reason": ""}

def run_hybrid_checks(job_desc: str, company: str, email: str, url: str) -> dict:
    '''Runs all rule-based checks and returns a summary list of red flags.'''
    reasons = []
    suspicious_flags = 0
    highlights = []
    
    # 1. Email check
    email_res = analyze_email_domain(email, company)
    if email_res["suspicious"]:
        reasons.append(email_res["reason"])
        suspicious_flags += 1
        
    # 2. Keyword check
    kw_res = analyze_keywords(job_desc)
    if kw_res["suspicious"]:
        reasons.append(kw_res["reason"])
        highlights.extend(kw_res["keywords"])
        suspicious_flags += 2 # Heavier weight for scam keywords
        
    # 3. URL check
    url_res = analyze_url(url)
    if url_res["suspicious"]:
        reasons.append(url_res["reason"])
        suspicious_flags += 1
        
    # Extrapolate a base score penalty [0.0 to 1.0] - Aggressively scale for fake internships
    rule_score_penalty = min(0.35 * suspicious_flags, 0.95)
    
    return {
        "reasons": reasons,
        "rule_penalty": rule_score_penalty,
        "highlights": highlights
    }
