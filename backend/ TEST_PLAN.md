# 🧪 Phishing Detection API - Test Planı

**Proje:** Phishing Email Detection System
**Hazırlayan:** Nisa Nur Erkuş
**Tarih:** 2025
**Versiyon:** 1.0

---

## 1. Test Kapsamı

Bu doküman, Phishing Detection API'nin backend tarafının test stratejisini ve test senaryolarını içerir.

### 1.1 Test Edilecek Bileşenler

| Bileşen | Dosya | Test Türü |
|---------|-------|-----------|
| Health Endpoint | `app/main.py` | API Test |
| Root Endpoint | `app/main.py` | API Test |
| Predict Endpoint | `app/routes/predict.py` | API Test |
| Phishing Detector | `app/services/phishing_detector.py` | Unit Test |
| CORS Ayarları | `app/main.py` | Integration Test |

### 1.2 Test Edilmeyecek Bileşenler

- Frontend arayüzü (ayrı ekip tarafından test edilecek)
- XGBoost ML modeli (ileride eklenecek)
- Veritabanı işlemleri (şu an yok)

---

## 2. Test Ortamı

### 2.1 Gereksinimler

| Bileşen | Versiyon |
|---------|----------|
| Python | 3.12 |
| FastAPI | 0.115.6 |
| Uvicorn | 0.34.0 |
| Pytest | 7.4.3 |
| Requests | 2.31.0 |

### 2.2 Test Komutları

```bash
# Sunucuyu başlat
./start.sh

# API testlerini çalıştır
pytest tests/test_api.py -v

# Unit testleri çalıştır
pytest tests/test_phishing_detector.py -v

# Tüm testleri çalıştır
pytest tests/ -v