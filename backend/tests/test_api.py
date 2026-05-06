"""
API Endpoint Testleri
=====================
Backend API'nin tüm endpoint'lerini test eden script.

Çalıştırma:
    pip install requests pytest
    pytest tests/test_api.py -v
"""

import requests
import pytest

# Test için API base URL
BASE_URL = "http://127.0.0.1:8000"


class TestHealthEndpoint:
    """Sağlık kontrolü endpoint testleri"""
    
    def test_health_check_status_code(self):
        """Health endpoint 200 dönmeli"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
    
    def test_health_check_response_format(self):
        """Health endpoint doğru formatı dönmeli"""
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert data["status"] == "healthy"


class TestRootEndpoint:
    """Ana sayfa endpoint testleri"""
    
    def test_root_status_code(self):
        """Ana sayfa 200 dönmeli"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
    
    def test_root_has_endpoints_info(self):
        """Ana sayfa endpoint bilgilerini içermeli"""
        response = requests.get(f"{BASE_URL}/")
        data = response.json()
        
        assert "message" in data
        assert "endpoints" in data
        assert "predict" in data["endpoints"]


class TestPredictEndpoint:
    """Phishing tahmin endpoint testleri"""
    
    def test_predict_phishing_email(self):
        """Phishing e-posta doğru tespit edilmeli"""
        payload = {
            "email_text": (
                "URGENT!!! Your account has been compromised! "
                "Click here immediately: http://192.168.1.1/verify "
                "You have won $1,000,000 prize!!! Act now!!!"
            ),
            "subject": "SECURITY ALERT - IMMEDIATE ACTION REQUIRED"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/predict", json=payload)
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["is_phishing"] == True
        assert data["risk_level"] == "Yüksek"
        assert data["confidence"] >= 0.7
    
    def test_predict_safe_email(self):
        """Güvenli e-posta doğru tespit edilmeli"""
        payload = {
            "email_text": (
                "Merhaba, yarınki toplantı saat 14:00'da yapılacaktır. "
                "Katılımınızı bekliyoruz. İyi çalışmalar."
            ),
            "subject": "Toplantı Bildirimi"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/predict", json=payload)
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["is_phishing"] == False
        assert data["risk_level"] == "Düşük"
    
    def test_predict_missing_email_text(self):
        """email_text eksikse hata dönmeli"""
        payload = {
            "subject": "Test"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/predict", json=payload)
        
        assert response.status_code == 422  # Validation Error
    
    def test_predict_short_email_text(self):
        """10 karakterden kısa metin hata vermeli"""
        payload = {
            "email_text": "kısa"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/predict", json=payload)
        
        assert response.status_code == 422  # Validation Error
    
    def test_predict_response_format(self):
        """Response doğru formatı içermeli"""
        payload = {
            "email_text": "Bu bir test e-postasıdır. Urgent verify account."
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/predict", json=payload)
        data = response.json()
        
        # Gerekli alanlar var mı?
        assert "is_phishing" in data
        assert "confidence" in data
        assert "risk_level" in data
        assert "message" in data
        assert "timestamp" in data
        
        # Tipler doğru mu?
        assert isinstance(data["is_phishing"], bool)
        assert isinstance(data["confidence"], float)
        assert isinstance(data["risk_level"], str)
        assert isinstance(data["message"], str)
        
        # Değer aralıkları doğru mu?
        assert 0.0 <= data["confidence"] <= 1.0
        assert data["risk_level"] in ["Düşük", "Orta", "Yüksek"]


class TestCORS:
    """CORS ayarları testleri"""
    
    def test_cors_headers_present(self):
        """CORS header'ları mevcut olmalı"""
        response = requests.options(
            f"{BASE_URL}/api/v1/predict",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            }
        )
        
        # CORS header'ları var mı?
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        assert "access-control-allow-origin" in headers_lower


if __name__ == "__main__":
    # pytest olmadan çalıştırılırsa
    print("Testleri çalıştırmak için:")
    print("  pip install requests pytest")
    print("  pytest tests/test_api.py -v")