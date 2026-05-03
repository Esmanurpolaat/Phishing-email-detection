import pandas as pd
import re
import os

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove email headers like "Forwarded by", "Subject:", etc.
    text = re.sub(r'(?i)(forwarded by|original message|from:|to:|cc:|subject:|date:).*?\n', ' ', text)
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', ' ', text)
    # Remove non-alphanumeric characters but keep spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def process_datasets():
    print("Loading datasets...")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    
    os.makedirs(processed_dir, exist_ok=True)
    
    datasets = []
    
    # 1. Load Enron dataset
    enron_path = os.path.join(raw_dir, 'enron_spam_data.csv')
    if os.path.exists(enron_path):
        print("Processing Enron dataset...")
        df_enron = pd.read_csv(enron_path, usecols=['Subject', 'Message', 'Spam/Ham'], encoding='utf-8', on_bad_lines='skip')
        df_enron['text'] = df_enron['Subject'].fillna('') + " " + df_enron['Message'].fillna('')
        df_enron['label'] = df_enron['Spam/Ham'].apply(lambda x: 1 if str(x).lower() == 'spam' else 0)
        datasets.append(df_enron[['text', 'label']])
        
    # Helper to load other datasets
    def load_human_llm(folder_name):
        folder_path = os.path.join(raw_dir, folder_name)
        if not os.path.exists(folder_path):
            return
            
        print(f"Processing {folder_name} datasets...")
        for file_name in ['legit.csv', 'phishing.csv']:
            file_path = os.path.join(folder_path, file_name)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path, on_bad_lines='skip', low_memory=False)
                # Combine subject and body if they exist
                text_col = ""
                if 'subject' in df.columns and 'body' in df.columns:
                    text_col = df['subject'].fillna('') + " " + df['body'].fillna('')
                elif 'text' in df.columns:
                    text_col = df['text'].fillna('')
                else:
                    # Just combine all string columns
                    text_col = df.select_dtypes(include=['object']).fillna('').agg(' '.join, axis=1)
                
                df_clean = pd.DataFrame({'text': text_col})
                
                if 'label' in df.columns:
                    # Make sure labels are numeric 0 or 1
                    df_clean['label'] = pd.to_numeric(df['label'], errors='coerce').fillna(1 if 'phishing' in file_name else 0)
                else:
                    df_clean['label'] = 1 if 'phishing' in file_name else 0
                    
                df_clean['label'] = df_clean['label'].astype(int)
                datasets.append(df_clean[['text', 'label']])

    # 2. Load Human-generated
    load_human_llm('human-generated')
    
    # 3. Load LLM-generated
    load_human_llm('llm-generated')
    
    if not datasets:
        print("No datasets found!")
        return
        
    print("Combining datasets...")
    combined_df = pd.concat(datasets, ignore_index=True)
    
    print(f"Total rows before cleaning: {len(combined_df)}")
    
    # Drop empty rows
    combined_df.dropna(subset=['text'], inplace=True)
    
    print("Cleaning text data (this may take a minute)...")
    combined_df['cleaned_text'] = combined_df['text'].apply(clean_text)
    
    # Drop rows where cleaned text is empty
    combined_df = combined_df[combined_df['cleaned_text'].str.strip() != '']
    
    print(f"Total rows after cleaning: {len(combined_df)}")
    
    output_path = os.path.join(processed_dir, 'combined_dataset.csv')
    print(f"Saving to {output_path}...")
    combined_df[['cleaned_text', 'label']].to_csv(output_path, index=False)
    
    print("Data processing complete!")
    
    # Print some stats for EDA
    print("\nDataset Statistics:")
    print(combined_df['label'].value_counts())
    print(f"Phishing ratio: {combined_df['label'].mean():.2%}")

if __name__ == "__main__":
    process_datasets()
