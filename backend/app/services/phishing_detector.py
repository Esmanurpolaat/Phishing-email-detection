"""
Phishing Tespit Servisi
-----------------------
E-posta metinlerini analiz ederek phishing tespiti yapar.

ŞU AN: Kural tabanlı basit analiz (geçici).
İLERİDE: Eğitilmiş XGBoost modeli buraya eklenecek.
"""

import re
from typing import Dict


class PhishingDetector:
    """
    E-posta metinlerini analiz eden sınıf.
    """
    
    def __init__(self):
        """
        Phishing'e işaret eden anahtar kelimeleri tanımla.
        (İleride bunlar yerine ML modeli kullanılacak)
        """
        
        # Şüpheli kelimeler listesi
        self.suspicious_keywords = [
            # Aciliyet ifadeleri
            "urgent", "immediately", "act now", "limited time",
            "acil", "hemen", "derhal", "son şans",
            
            # Hesap güvenliği
            "verify your account", "confirm your identity",
            "account suspended", "account compromised",
            "hesabınız askıya alındı", "şifrenizi güncelleyin",
            "hesap doğrulama", "kimlik doğrulama",
            
            # Para/ödül
            "you have won", "congratulations", "prize",
            "lottery", "million dollars", "reward",
            "ödül kazandınız", "tebrikler", "piyango",
            
            # Giriş/şifre talepleri
            "click here to login", "reset your password",
            "update your information", "verify your identity",
            "giriş yapmak için tıklayın", "şifrenizi sıfırlayın",
            
            # Tehdit
            "your account will be closed", "unauthorized access",
            "suspicious activity", "security alert",
            "yetkisiz erişim", "güvenlik uyarısı",
        ]
        
        # Şüpheli URL kalıpları (regex)
        self.suspicious_url_patterns = [
            r'http[s]?://(?!www\.)[^\s]+',      # www olmayan linkler
            r'bit\.ly', r'tinyurl', r'goo\.gl',  # Kısaltılmış linkler
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',  # IP adresi
            r'@.*\.',                            # @ içeren URL'ler
        ]
    
    def analyze(self, email_text: str, subject: str = None) -> Dict:
        """
        E-posta metnini analiz eder ve phishing skoru hesaplar.
        
        Parametreler:
            email_text: Analiz edilecek e-posta metni
            subject: E-posta konu başlığı (opsiyonel)
        
        Dönüş:
            {
                "is_phishing": True/False,
                "confidence": 0.0-1.0,
                "risk_level": "Düşük/Orta/Yüksek",
                "message": "Açıklama mesajı"
            }
        """
        
        # Konu varsa metne ekle (konu da analiz edilsin)
        full_text = email_text.lower()
        if subject:
            full_text = subject.lower() + " " + full_text
        
        # --- SKOR HESAPLAMA ---
        score = 0.0         # Toplam şüphe skoru
        max_score = 100.0   # Maksimum olası skor
        findings = []       # Bulunan şüpheli unsurlar
        
        # 1. Anahtar kelime kontrolü
        keyword_hits = 0
        for keyword in self.suspicious_keywords:
            if keyword in full_text:
                keyword_hits += 1
        
        # Her anahtar kelime için +10 puan (maksimum 40 puan)
        score += min(keyword_hits * 10, 40)
        if keyword_hits > 0:
            findings.append(f"Şüpheli {keyword_hits} kelime bulundu")
        
        # 2. Şüpheli URL kontrolü
        url_hits = 0
        for pattern in self.suspicious_url_patterns:
            if re.search(pattern, full_text):
                url_hits += 1
        
        # Her URL pattern için +15 puan (maksimum 30 puan)
        score += min(url_hits * 15, 30)
        if url_hits > 0:
            findings.append(f"Şüpheli {url_hits} URL tespit edildi")
        
        # 3. Büyük harf kullanımı (bağırma)
        upper_ratio = sum(1 for c in email_text if c.isupper()) / max(len(email_text), 1)
        if upper_ratio > 0.3:  # %30'dan fazla büyük harf
            score += 10
            findings.append("Aşırı büyük harf kullanımı")
        
        # 4. Ünlem işareti fazlalığı
        exclamation_count = email_text.count('!')
        if exclamation_count > 3:
            score += 10
            findings.append(f"{exclamation_count} adet ünlem işareti")
        
        # 5. Para simgeleri
        if re.search(r'[$€£₺]\s*\d+', email_text):
            score += 10
            findings.append("Para miktarı belirtilmiş")
        
        # --- SONUÇ BELİRLEME ---
        # Skoru 0-1 arasına normalize et
        confidence = min(score / max_score, 1.0)
        
        # Risk seviyesi belirle
        if confidence >= 0.7:
            risk_level = "Yüksek"
            is_phishing = True
            message = (
                "⚠️ UYARI: Bu e-posta yüksek olasılıkla bir phishing saldırısıdır! "
                "Linklere tıklamayın ve kişisel bilgilerinizi paylaşmayın."
            )
        elif confidence >= 0.4:
            risk_level = "Orta"
            is_phishing = True
            message = (
                "⚠️ DİKKAT: Bu e-posta şüpheli unsurlar içermektedir. "
                "Gönderen adresi ve içeriği dikkatli inceleyin."
            )
        else:
            risk_level = "Düşük"
            is_phishing = False
            message = (
                "✅ Bu e-posta güvenli görünmektedir. "
                "Yine de bilinmeyen gönderenlerden gelen linklere dikkat edin."
            )
        
        return {
            "is_phishing": is_phishing,
            "confidence": round(confidence, 4),
            "risk_level": risk_level,
            "message": message,
        }


# Tek bir detector nesnesi oluştur (singleton pattern)
detector = PhishingDetector()