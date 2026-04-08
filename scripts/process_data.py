import pandas as pd
import numpy as np
import os
import glob
import re

print("[INFO] Veri isleme ve birlestirme adimi baslatiliyor...")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
os.makedirs(PROCESSED_DIR, exist_ok=True)

all_dataframes = []

# --- NÜKLEER METIN TEMIZLEME FONKSIYONU ---
def metinleri_temizle(df, text_col):
    df = df.rename(columns={text_col: 'text'})
    
    # 1. Tum veriyi string yap
    df['text'] = df['text'].astype(str)
    
    # 2. Enter (\n), Tab (\t) ve arka arkaya gelen tum bosluklari tek bir normal bosluga cevir
    df['text'] = df['text'].replace(r'\s+', ' ', regex=True).str.strip()
    
    # 3. 'nan', 'null' gibi yazilari gercek NaN yap ve sil
    df['text'] = df['text'].replace(['', 'nan', 'null', 'none', 'NaN', 'None', ' '], np.nan)
    df = df.dropna(subset=['text'])
    
    # 4. NÜKLEER FILTRE: İçinde en az 10 tane GERÇEK HARF (a-z, A-Z) olmayan satırları YOK ET!
    # (Bu sayede icinde sadece "......", "-----", "***" olan anlamsiz satirlar silinecek)
    df = df[df['text'].str.count(r'[a-zA-Z]') >= 10]
    
    return df

print("\n[INFO] --- 1. ASAMA: DOSYALAR OKUNUYOR VE ETIKETLENIYOR ---")

# A) ENRON VERI SETINI OKU
enron_path = os.path.join(RAW_DIR, 'enron_spam_data.csv')
if os.path.exists(enron_path):
    print(f"-> Enron dosyasi isleniyor...")
    df_enron = pd.read_csv(enron_path, on_bad_lines='skip', low_memory=False)
    text_c = 'Message' if 'Message' in df_enron.columns else 'text'
    df_enron = metinleri_temizle(df_enron, text_c)
    
    if 'Spam/Ham' in df_enron.columns:
        df_enron = df_enron.rename(columns={'Spam/Ham': 'label'})
    if 'label' in df_enron.columns:
        df_enron['label'] = df_enron['label'].astype(str).str.lower().str.strip()
        sozluk = {'spam': 1, 'phishing': 1, '1': 1, '1.0': 1, 'ham': 0, 'legit': 0, '0': 0, '0.0': 0}
        df_enron['label'] = df_enron['label'].map(sozluk)
        df_enron = df_enron.dropna(subset=['label'])
        df_enron['label'] = df_enron['label'].astype(int)
        all_dataframes.append(df_enron[['text', 'label']])

# B) KAGGLE VERI SETLERINI OKU
for folder_name in ['human-generated', 'llm-generated']:
    folder_path = os.path.join(RAW_DIR, folder_name)
    if os.path.exists(folder_path):
        csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
        for csv_file in csv_files:
            dosya_adi = os.path.basename(csv_file).lower()
            print(f"-> {folder_name} icindeki {dosya_adi} isleniyor...")
            df_temp = pd.read_csv(csv_file, on_bad_lines='skip', low_memory=False)
            
            bulunan_text_col = None
            for col in df_temp.columns:
                if str(col).lower() in ['text', 'message', 'email text', 'content', 'mail', 'body']:
                    bulunan_text_col = col
                    break
            
            if bulunan_text_col:
                df_temp = metinleri_temizle(df_temp, bulunan_text_col)
                if 'phishing' in dosya_adi:
                    df_temp['label'] = 1
                elif 'legit' in dosya_adi:
                    df_temp['label'] = 0
                else:
                    continue
                all_dataframes.append(df_temp[['text', 'label']])

print("\n[INFO] --- 2. ASAMA: TUM TEMIZ VERILER BIRLESTIRILIYOR ---")
if len(all_dataframes) > 0:
    df_combined = pd.concat(all_dataframes, ignore_index=True)
    baslangic_satir = len(df_combined)
    
    # Kopyalari sil
    df_combined = df_combined.drop_duplicates(subset=['text']).reset_index(drop=True)
    
    # Model egitimi icin ekstra sutun
    df_combined['cleaned_text'] = df_combined['text']
    
    # Kaydet
    output_path = os.path.join(PROCESSED_DIR, 'combined_dataset.csv')
    df_combined.to_csv(output_path, index=False)
    
    silinen_kopya = baslangic_satir - len(df_combined)
    print(f"-> Birlestirme sonrasi {silinen_kopya} adet kopya ve hayalet satir silindi.")
    print(f"\n[BASARILI] Gercek harf filtresi uygulandi! Pürüzsüz veri seti hazir.")
    print(f"[BILGI] Final Net Satir Sayisi: {len(df_combined)}")
else:
    print("[HATA] Islenecek veri bulunamadi!")