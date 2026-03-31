import re

def clean_text(text: str) -> str:
    '''Cleans job description text by removing HTML tags, URLs, 
    and extra whitespaces to normalize the input.'''
    if not isinstance(text, str):
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', text)
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def prepare_input_text(job_desc: str, company_name: str, email: str, salary: str) -> str:
    '''Combines input features into a single normalized text block
    to be fed into the Transformer model.'''
    job_desc = clean_text(job_desc)
    company_name = clean_text(company_name)
    email = clean_text(email)
    salary = clean_text(salary)
    
    # We combine them into a single string. The transformer will learn the interactions.
    combined_text = f"[COMPANY] {company_name} [EMAIL] {email} [SALARY] {salary} [DESC] {job_desc}"
    return combined_text
