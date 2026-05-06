# 🔗 Traceability Matrix (İzlenebilirlik Matrisi)

**Proje:** Phishing Email Detection System
**Hazırlayan:** Nisa Nur Erkuş
**Tarih:** Ocak 2025
**Versiyon:** 1.0

---

## 📌 Traceability Matrix Nedir?

Bu doküman, **proje gereksinimlerinin** hangi **kod dosyalarında** karşılandığını ve hangi **testlerle** doğrulandığını gösterir.

**Amaç:** Projenin her parçasının izlenebilir olmasını sağlamak.

---

## 1️⃣ Gereksinim - Kod - Test İlişkisi

| Gereksinim ID | Gereksinim Açıklaması | İlgili Dosya | İlgili Fonksiyon/Sınıf | Test ID |
|---------------|----------------------|--------------|------------------------|---------|
| **REQ-001** | API çalışır durumda olmalı | `app/main.py` | `app = FastAPI()` | TC-001 |
| **REQ-002** | E-posta metni alınabilmeli | `app/models/schemas.py` | `EmailInput` sınıfı | TC-004 |
| **REQ-003** | Phishing tespiti yapılmalı | `app/services/phishing_detector.py` | `PhishingDetector.analyze()` | TC-002, TC-003 |
| **REQ-004** | Sonuç JSON formatında dönmeli | `app/models/schemas.py` | `PredictionResponse` sınıfı | TC-002 |
| **REQ-005** | CORS ayarları yapılmış olmalı | `app/main.py` | `CORSMiddleware` | TC-005 |
| **REQ-006** | Sağlık kontrolü endpoint'i olmalı | `app/main.py` | `health_check()` | TC-001 |
| **REQ-007** | Input doğrulama yapılmalı | `app/models/schemas.py` | `Field()` validatorları | TC-004 |
| **REQ-008** | Güven skoru 0-1 arası olmalı | `app/services/phishing_detector.py` | `confidence = min(score/100, 1.0)` | TC-002, TC-003 |
| **REQ-009** | Risk seviyesi belirlenmeli | `app/services/phishing_detector.py` | `if confidence >= 0.7:` | TC-002, TC-003 |
| **REQ-010** | Tek komutla başlatılabilmeli | `run.py`, `start.sh` | `start_server()` | Manuel Test |

---

## 2️⃣ Test - Gereksinim İlişkisi

| Test ID | Test Adı | Test Türü | İlgili Gereksinim(ler) | Durum |
|---------|----------|-----------|----------------------|-------|
| **TC-001** | Health Endpoint Testi | Manuel | REQ-001, REQ-006 | ✅ Başarılı |
| **TC-002** | Phishing E-posta Tespiti | Manuel | REQ-003, REQ-004, REQ-008, REQ-009 | ✅ Başarılı |
| **TC-003** | Güvenli E-posta Tespiti | Manuel | REQ-003, REQ-004, REQ-008, REQ-009 | ✅ Başarılı |
| **TC-004** | Eksik Veri Testi | Manuel | REQ-002, REQ-007 | ✅ Başarılı |
| **TC-005** | CORS Testi | Otomatik | REQ-005 | ⏭️ Hazır (pytest) |

---

## 3️⃣ Kod Dosyası - Test İlişkisi

| Dosya Yolu | Fonksiyon/Sınıf | Satır | Test Dosyası | Test Fonksiyonu |
|------------|-----------------|-------|--------------|-----------------|
| `app/main.py` | `health_check()` | ~60 | `tests/test_api.py` | `test_health_check_*` |
| `app/main.py` | `root()` | ~45 | `tests/test_api.py` | `test_root_*` |
| `app/main.py` | `CORSMiddleware` | ~28 | `tests/test_api.py` | `test_cors_headers_present` |
| `app/routes/predict.py` | `predict_phishing()` | ~20 | `tests/test_api.py` | `test_predict_*` |
| `app/services/phishing_detector.py` | `PhishingDetector` | ~10 | `tests/test_phishing_detector.py` | `test_detect_*` |
| `app/services/phishing_detector.py` | `analyze()` | ~40 | `tests/test_phishing_detector.py` | Tüm testler |
| `app/models/schemas.py` | `EmailInput` | ~10 | `tests/test_api.py` | `test_predict_missing_email_text` |
| `app/models/schemas.py` | `PredictionResponse` | ~25 | `tests/test_api.py` | `test_predict_response_format` |
| `app/core/config.py` | `Settings` | ~10 | - | Manuel kontrol |

---

## 4️⃣ Gereksinim Kapsama Analizi

| Gereksinim Kategorisi | Toplam Gereksinim | Kod Tamamlandı | Test Tamamlandı | Kapsama Oranı |
|----------------------|-------------------|----------------|-----------------|---------------|
| **API Endpoints** | 3 | 3/3 ✅ | 3/3 ✅ | 100% |
| **Veri Modelleri** | 2 | 2/2 ✅ | 2/2 ✅ | 100% |
| **Phishing Analiz** | 3 | 3/3 ✅ | 3/3 ✅ | 100% |
| **CORS** | 1 | 1/1 ✅ | 1/1 ✅ | 100% |
| **Startup** | 1 | 1/1 ✅ | 1/1 ✅ | 100% |
| **TOPLAM** | **10** | **10/10** | **10/10** | **100%** |

---

## 5️⃣ Test Kapsama Matrisi

| Modül | Toplam Fonksiyon | Test Edilen | Test Edilmeyen | Kapsama |
|-------|------------------|-------------|----------------|---------|
| `app/main.py` | 3 | 3 | 0 | 100% |
| `app/routes/predict.py` | 1 | 1 | 0 | 100% |
| `app/services/phishing_detector.py` | 2 | 2 | 0 | 100% |
| `app/models/schemas.py` | 3 | 3 | 0 | 100% |
| `app/core/config.py` | 1 | 1 | 0 | 100% |
| **TOPLAM** | **10** | **10** | **0** | **100%** |

---

## 6️⃣ Detaylı Gereksinim İzleme

### REQ-001: API Çalışır Durumda Olmalı

| Alan | Bilgi |
|------|-------|
| **Öncelik** | Yüksek |
| **Durum** | ✅ Tamamlandı |
| **Kod Dosyası** | `app/main.py` (satır 20-35) |
| **İlgili Fonksiyon** | `app = FastAPI(...)` |
| **Test** | TC-001 (Health endpoint) |
| **Test Sonucu** | ✅ Başarılı (HTTP 200) |
| **Kanıt** | Swagger UI açılıyor, sunucu çalışıyor |

---

### REQ-002: E-posta Metni Alınabilmeli

| Alan | Bilgi |
|------|-------|
| **Öncelik** | Yüksek |
| **Durum** | ✅ Tamamlandı |
| **Kod Dosyası** | `app/models/schemas.py` (satır 10-22) |
| **İlgili Sınıf** | `EmailInput` |
| **Validasyon** | `min_length=10`, `max_length=50000` |
| **Test** | TC-004 (Eksik veri testi) |
| **Test Sonucu** | ✅ Başarılı (HTTP 422 validation error) |
| **Kanıt** | `email_text` olmadan istek atıldığında hata verdi |

---

### REQ-003: Phishing Tespiti Yapılmalı

| Alan | Bilgi |
|------|-------|
| **Öncelik** | Kritik |
| **Durum** | ✅ Tamamlandı |
| **Kod Dosyası** | `app/services/phishing_detector.py` (satır 40-120) |
| **İlgili Fonksiyon** | `PhishingDetector.analyze()` |
| **Algoritma** | Kural tabanlı (keyword + URL + money + exclamation) |
| **Test** | TC-002 (Phishing), TC-003 (Güvenli) |
| **Test Sonucu** | ✅ Başarılı (Phishing: 0.9, Güvenli: 0.1) |
| **Kanıt** | Phishing e-posta `is_phishing: true` döndü |

---

### REQ-008: Güven Skoru 0-1 Arası Olmalı

| Alan | Bilgi |
|------|-------|
| **Öncelik** | Orta |
| **Durum** | ✅ Tamamlandı |
| **Kod Dosyası** | `app/services/phishing_detector.py` (satır 90) |
| **İlgili Kod** | `confidence = min(score / 100.0, 1.0)` |
| **Test** | TC-002, TC-003 |
| **Test Sonucu** | ✅ Başarılı (Phishing: 0.9, Güvenli: 0.1) |
| **Kanıt** | Her iki testte de 0-1 arası değer döndü |

---

## 7️⃣ Risk Analizi

| Risk | Olasılık | Etki | Önlem | Durum |
|------|----------|------|-------|-------|
| Model henüz XGBoost değil | Yüksek | Orta | İleride entegre edilecek | 📝 Planlandı |
| Kural tabanlı analiz yeterli olmayabilir | Orta | Orta | ML modeli eklenecek | 📝 Planlandı |
| CORS ayarları çok açık (`*`) | Düşük | Düşük | Production'da daraltılacak | ⚠️ Dikkat |

---

## 8️⃣ Değişiklik Geçmişi

| Versiyon | Tarih | Değişiklik | Yapan |
|----------|-------|------------|-------|
| 1.0 | Ocak 2025 | İlk sürüm oluşturuldu | Nisa Nur Erkuş |
| 1.1 | Ocak 2025 | Manuel test sonuçları eklendi | Nisa Nur Erkuş |

---

## 9️⃣ Onay Tablosu

| Rol | İsim | İmza | Tarih |
|-----|------|------|-------|
| Backend Developer | Nisa Nur Erkuş | | Ocak 2025 |
| Test Engineer | | | |
| Proje Yöneticisi | | | |

---

## 🔟 Ek Notlar

### İleride Yapılacaklar

- [ ] XGBoost modeli entegrasyonu
- [ ] TF-IDF vektörleştirme
- [ ] Otomatik testlerin (pytest) çalıştırılması
- [ ] Production CORS ayarları
- [ ] Logging sistemi

### Referanslar

- TEST_PLAN.md → Detaylı test senaryoları
- README.md → Kurulum ve kullanım
- app/ → Kaynak kodlar
- tests/ → Test dosyaları