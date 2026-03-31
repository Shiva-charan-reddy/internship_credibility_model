import os
import torch
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments, AutoTokenizer
from datasets import load_dataset
import sys

# adding backend dir to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocessing import clean_text, prepare_input_text

def process_data(examples):
    '''Prepare the input format from the EMSCAD dataset.
    EMSCAD dataset contains columns like title, location, department, salary_range...'''
    job_descs = examples.get('description', [""] * len(examples['title']))
    company_profiles = examples.get('company_profile', [""] * len(examples['title']))
    salaries = examples.get('salary_range', [""] * len(examples['title']))
    
    # EMCSAD doesn't have an explicit 'email' column usually, we'll pass empty strings
    emails = [""] * len(examples['title'])
    
    combined_texts = []
    for i in range(len(job_descs)):
        desc = job_descs[i] if job_descs[i] else ""
        comp = company_profiles[i] if company_profiles[i] else ""
        sal = salaries[i] if salaries[i] else ""
        em = emails[i]
        
        combined_text = prepare_input_text(desc, comp, em, sal)
        combined_texts.append(combined_text)
    
    labels = examples.get('fraudulent', [0] * len(combined_texts))
    return {"text": combined_texts, "label": labels}

def train_model(model_name="distilbert-base-uncased", max_samples=None, epochs=2):
    print("Loading dataset 'amarnanth/fake-job-posting-prediction'...")
    try:
        # Load the EMSCAD fake job dataset
        dataset = load_dataset("amarnanth/fake-job-posting-prediction", split='train')
    except Exception as e:
        print(f"Failed to load dataset from HF: {e}")
        print("Falling back to local CSV if exists... (data/fake_job_postings.csv)")
        dataset = load_dataset('csv', data_files='data/fake_job_postings.csv', split='train')

    # Mapping 'fraudulent' into 'label'
    print("Preprocessing data...")
    dataset = dataset.map(process_data, batched=True, remove_columns=dataset.column_names)
    
    if max_samples:
        print(f"Limiting to {max_samples} samples for quick demonstration.")
        dataset = dataset.shuffle(seed=42).select(range(min(max_samples, len(dataset))))

    # Train/test split
    dataset = dataset.train_test_split(test_size=0.2, seed=42)
    
    # Tokenization
    print("Tokenizing data...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    
    # Model
    print("Initializing model...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2).to(device)
    
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=epochs,
        weight_decay=0.01,
        save_strategy="epoch",
        load_best_model_at_end=True
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"]
    )
    
    print("Starting training...")
    trainer.train()
    
    print("Saving model and tokenizer...")
    save_path = os.path.join(os.path.dirname(__file__), "saved_model")
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)
    print(f"Model saved to {save_path}")

if __name__ == "__main__":
    train_model(max_samples=200, epochs=1)
