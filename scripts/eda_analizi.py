import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("[INFO] Kesifci Veri Analizi (EDA) Pipeline Baslatiliyor...")

# --- 1. DIZIN AYARLARI ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
DATA_PATH = os.path.join(PROCESSED_DIR, 'combined_dataset.csv')

# Klasor kontrolü
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Veriyi oku
df = pd.read_csv(DATA_PATH)

# --- 2. VERI TEMIZLEME VE FILTRELEME (KRITIK ADIM) ---
# Label sutunundaki kaymalari (metinleri) temizle, sadece 0 ve 1 birak
df['label'] = pd.to_numeric(df['label'], errors='coerce')
df = df.dropna(subset=['label'])
df = df[df['label'].isin([0, 1])]

# Grafikte 0 ve 1 yerine anlasilir isimler kullan
df['Kategori'] = df['label'].map({0.0: 'Temiz (Legit)', 1.0: 'Oltalama (Phishing)'})

# Metin uzunluklarini hesapla ve boslari doldur
df['cleaned_text'] = df['cleaned_text'].fillna('')
df['text_length'] = df['cleaned_text'].apply(len)

print(f"[INFO] Analiz edilen toplam temiz satir sayisi: {len(df)}")

# --- 3. GRAFIK 1: SINIF DAGILIMI (BAR CHART) ---
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Kategori', hue='Kategori', palette='Set2', legend=False)
plt.title('Veri Setindeki E-posta Kategorilerinin Dagilimi', fontsize=14, fontweight='bold')
plt.xlabel('E-posta Turu', fontsize=12)
plt.ylabel('Toplam Adet', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

dist_path = os.path.join(PROCESSED_DIR, 'sinif_dagilimi.png')
plt.savefig(dist_path, dpi=300) # Yuksek cozunurlukte kaydet
print(f"[BASARILI] 1. Grafik kaydedildi: {dist_path}")
plt.close()

# --- 4. GRAFIK 2: DETAYLI METIN UZUNLUGU (HISTOGRAM) ---
print("[INFO] Detayli uzunluk grafigi olusturuluyor (0-2000 Karakter Arasi)...")
plt.figure(figsize=(12, 7))

# Verinin %95'i 2000 karakterden az oldugu icin grafigi buraya odakliyoruz
df_filtered = df[df['text_length'] <= 2000]

sns.histplot(data=df_filtered, x='text_length', hue='Kategori', 
             bins=80, element="bars", palette='Set1', alpha=0.6)

plt.title('E-posta Metin Uzunluklarinin Detayli Dagilimi', fontsize=14, fontweight='bold')
plt.xlabel('Karakter Sayisi (Uzunluk)', fontsize=12)
plt.ylabel('E-posta Sayisi (Frekans)', fontsize=12)
plt.xlim(0, 2000) # Grafigi 2000 karakterle sınırla (Odaklanma)
plt.grid(axis='y', linestyle='--', alpha=0.3)

len_path = os.path.join(PROCESSED_DIR, 'metin_uzunlugu_dagilimi.png')
plt.savefig(len_path, dpi=300)
print(f"[BASARILI] 2. Grafik kaydedildi: {len_path}")

# --- 5. SONUC ---
print("\n[TAMAMLANDI] Tum analizler bitti ve grafikler 'data/processed' klasorune kaydedildi.")
plt.show() # Grafigi ekranda goster