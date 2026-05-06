"""
Phishing Detector Unit Testleri
================================
PhishingDetector sınıfının fonksiyonlarını test eder.

Çalıştırma:
    pytest tests/test_phishing_detector.py -v
"""

import pytest
from app.services.phishing_detector import detector


class TestPhishingDetector:
    """PhishingDetector sınıfı testleri"""
    
    def test_detect_urgent_keyword(self):
        """'urgent' kelimesi şüphe skorunu artırmalı"""
        text = "This is an URGENT message!"
        result = detector.analyze(text)
        
        assert result["confidence"] > 0.0
    
    def test_detect_multiple_keywords(self):
        """Birden fazla şüpheli kelime yüksek skor vermeli"""
        text = (
            "URGENT! Verify your account immediately! "
            "Your account will be suspended!"
        )
        result = detector.analyze(text)
        
        assert result["is_phishing"] == True
        assert result["confidence"] >= 0.4
    
    def test_detect_suspicious_url(self):
        """Şüpheli URL tespit edilmeli"""
        text = "Click here: http://192.168.1.1/verify"
        result = detector.analyze(text)
        
        assert result["confidence"] > 0.0
    
    def test_detect_money_amount(self):
        """Para miktarı tespit edilmeli"""
        text = "You have won $1,000,000 prize!"
        result = detector.analyze(text)
        
        assert result["confidence"] > 0.0
    
    def test_detect_excessive_exclamation(self):
        """Aşırı ünlem işareti tespit edilmeli"""
        text = "Win now!!!! Click here!!!!"
        result = detector.analyze(text)
        
        assert result["confidence"] > 0.0
    
    def test_safe_email_low_score(self):
        """Güvenli e-posta düşük skor almalı"""
        text = "Merhaba, toplantı saat 14:00'da. İyi çalışmalar."
        result = detector.analyze(text)
        
        assert result["is_phishing"] == False
        assert result["risk_level"] == "Düşük"
    
    def test_subject_included_in_analysis(self):
        """Konu başlığı analize dahil edilmeli"""
        result = detector.analyze(
            email_text="Normal metin",
            subject="URGENT VERIFY ACCOUNT"
        )
        
        # Konu başlığındaki kelimeler skorlamalı
        assert result["confidence"] > 0.0
    
    def test_confidence_range(self):
        """Güven skoru 0-1 arasında olmalı"""
        texts = [
            "Normal metin",
            "URGENT verify account",
            "URGENT!!! Click $1000000 http://192.168.1.1 verify account suspended!!!"
        ]
        
        for text in texts:
            result = detector.analyze(text)
            assert 0.0 <= result["confidence"] <= 1.0
    
    def test_risk_level_values(self):
        """Risk seviyesi sadece Düşük/Orta/Yüksek olmalı"""
        texts = [
            "Normal metin",
            "URGENT verify",
            "URGENT!!! verify account suspended http://192.168.1.1"
        ]
        
        for text in texts:
            result = detector.analyze(text)
            assert result["risk_level"] in ["Düşük", "Orta", "Yüksek"]