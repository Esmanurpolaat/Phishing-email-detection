import os
import re
import pandas as pd

print("[INFO] Veri isleme hatti (pipeline) baslatiliyor...")

# --- 1. DİZİN VE YOL (PATH) AYARLARI ---
# Kodun calistigi dizini temel alarak proje ana dizinini (BASE_DIR) dinamik olarak belirler.
# Bu sayede terminalin nerede acik oldugu fark etmeksizin dosyalar dogru bulunur.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

# Cikti klasoru mevcut degilse (data/processed) sistem tarafindan otomatik olusturulur.
os.makedirs(PROCESSED_DIR, exist_ok=True)

# --- 2. HAM (RAW) VERİLERİN YÜKLENMESİ ---
print("[INFO] Ham veri setleri bellege yukleniyor...")

# 2.1. TREC_05 Veri Seti (Geleneksel Spam/Phishing mailleri)
# 'engine=python' parametresi Buffer Overflow hatalarini engellemek icin kullanilmistir.
df_trec = pd.read_csv(os.path.join(RAW_DIR, 'TREC_05.csv'), on_bad_lines='skip', engine='python')
df_trec = df_trec[['body', 'label']].rename(columns={'body': 'text'})

# 2.2. EduPhish Veri Seti (Egitim sektorune yonelik Phishing verileri)
df_edu = pd.read_csv(os.path.join(RAW_DIR, 'EduPhish_Kaggle_Package', 'eduphish_dataset.csv'), on_bad_lines='skip')
df_edu = df_edu[['text', 'label']]

# 2.3. Insan Uretimi (Human-Generated) Phishing Verisi
df_h_legit = pd.read_csv(os.path.join(RAW_DIR, 'human-generated', 'legit.csv'), on_bad_lines='skip')
df_h_legit = df_h_legit[['body', 'label']].rename(columns={'body': 'text'})

df_h_phish = pd.read_csv(os.path.join(RAW_DIR, 'human-generated', 'phishing.csv'), on_bad_lines='skip')
df_h_phish = df_h_phish[['body', 'label']].rename(columns={'body': 'text'})

# 2.4. LLM Uretimi (Yapay Zeka) Phishing Verisi
# LLM verilerinde hedef degisken (label) bulunmadigi icin 0 (Legit) ve 1 (Phishing) olarak manuel atanir.
df_l_legit = pd.read_csv(os.path.join(RAW_DIR, 'llm-generated', 'legit.csv'), on_bad_lines='skip')
df_l_legit = df_l_legit[['text']]
df_l_legit['label'] = 0 

df_l_phish = pd.read_csv(os.path.join(RAW_DIR, 'llm-generated', 'phishing.csv'), on_bad_lines='skip')
df_l_phish = df_l_phish[['text']]
df_l_phish['label'] = 1 

# --- 3. VERİ BİRLEŞTİRME VE GÜRÜLTÜ AZALTMA ---
print("[INFO] Veri setleri birlestiriliyor ve kopya kayitlar temizleniyor...")
df_all = pd.concat([df_trec, df_edu, df_h_legit, df_h_phish, df_l_legit, df_l_phish], ignore_index=True)

initial_count = len(df_all)
# NaN (bos) degerler ve birebir ayni metne sahip kopyalar (duplikasyon) modelin ezberlemesini (overfitting) onlemek icin silinir.
df_all = df_all.dropna().drop_duplicates(subset=['text'])
print(f"[INFO] Birlestirme oncesi satir: {initial_count} | Temizlik sonrasi benzersiz satir: {len(df_all)}")

# --- 4. METİN ÖN İŞLEME (TEXT PREPROCESSING) ---
def clean_text(text):
    """
    Girdi metnini makine ogrenmesi modeline uygun hale getirmek icin temizler.
    - Kucuk harf donusumu (lowercase) yapar.
    - HTML etiketlerini ve kalintilarini kaldirir.
    - URL ve E-posta adreslerini standart yer tutucularla (placeholder) degistirir.
    - Alfabetik olmayan karakterleri (sayilar, noktalama) siler.
    """
    text = str(text).lower() 
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'http[s]?://\S+|www\S+', ' urllink ', text) 
    text = re.sub(r'\S+@\S+', ' emailadres ', text) 
    text = re.sub(r'[^a-z\s]', ' ', text) 
    return re.sub(r'\s+', ' ', text).strip() 

print("[INFO] Metin temizleme (regex) islemi uygulaniyor. Lutfen bekleyin...")
df_all['cleaned_text'] = df_all['text'].apply(clean_text)

# --- 5. NİHAİ VERİ SETİNİN DIŞA AKTARILMASI (EXPORT) ---
print("[INFO] Islenmis veri CSV formatinda disari aktariliyor...")
output_path = os.path.join(PROCESSED_DIR, 'combined_dataset.csv')

# Model egitimi icin sadece 'cleaned_text' (bagimsiz degisken) ve 'label' (hedef degisken) sutunlari tutulur.
df_all[['cleaned_text', 'label']].to_csv(output_path, index=False)

print(f"[BASARILI] Veri isleme hatti tamamlandi. Cikti konumu: {output_path}")