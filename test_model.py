import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import os

def test_model():
    print("Veri yukleniyor...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data', 'processed', 'combined_dataset.csv')
    
    if not os.path.exists(file_path):
        print(f"Hata: {file_path} bulunamadi!")
        return
        
    df = pd.read_csv(file_path)
    
    # Drop rows with NaN texts
    df = df.dropna(subset=['cleaned_text'])
    
    X = df['cleaned_text']
    y = df['label']
    
    print("Metinler vektorlere donusturuluyor (TF-IDF)...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X_vec = vectorizer.fit_transform(X)
    
    print("Veri egitim ve test olarak ayriliyor...")
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
    
    print("Model egitiliyor (Logistic Regression)...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    
    print("Tahminler yapiliyor...")
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"\n--- MODEL BASARISI ---")
    print(f"Dogruluk Orani (Accuracy): {acc * 100:.2f}%")
    print("\nDetayli Rapor:")
    print(classification_report(y_test, y_pred, target_names=['Guvenli (0)', 'Phishing (1)']))
    
if __name__ == '__main__':
    test_model()
