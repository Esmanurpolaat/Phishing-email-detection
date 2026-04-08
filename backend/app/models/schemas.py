"""
Pydantic Veri Modelleri
-----------------------
API'ye gelen isteklerin ve dönen yanıtların şeklini tanımlar.
Pydantic, verileri otomatik olarak doğrular (validation).
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EmailInput(BaseModel):
    """
    Kullanıcıdan gelecek e-posta verisi.
    
    Kullanıcı POST /predict adresine bu formatta veri gönderecek:
    {
        "email_text": "Dear user, your account...",
        "subject": "Security Alert"
    }
    """
    
    email_text: str = Field(
        ...,  # ... = zorunlu alan demek
        min_length=10,  # En az 10 karakter olmalı
        max_length=50000,  # En fazla 50000 karakter
        description="Analiz edilecek e-posta metni",
        examples=["URGENT: Your account has been compromised!"]
    )
    
    subject: Optional[str] = Field(
        default=None,  # Opsiyonel (göndermese de olur)
        max_length=500,
        description="E-posta konu başlığı (opsiyonel)"
    )


class PredictionResponse(BaseModel):
    """
    API'nin kullanıcıya döneceği tahmin sonucu.
    
    API şu formatta cevap verecek:
    {
        "is_phishing": true,
        "confidence": 0.85,
        "risk_level": "Yüksek",
        "message": "Bu e-posta şüpheli!",
        "timestamp": "2025-01-15T14:30:00"
    }
    """
    
    is_phishing: bool = Field(
        description="True ise phishing, False ise güvenli"
    )
    
    confidence: float = Field(
        ge=0.0,  # Minimum 0
        le=1.0,  # Maksimum 1
        description="Modelin tahmin güven skoru (0.0 - 1.0 arası)"
    )
    
    risk_level: str = Field(
        description="Risk seviyesi: 'Düşük', 'Orta', 'Yüksek'"
    )
    
    message: str = Field(
        description="Kullanıcıya gösterilecek açıklama mesajı"
    )
    
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Analiz yapılan zaman"
    )


class HealthResponse(BaseModel):
    """
    Sağlık kontrolü yanıtı.
    GET /health endpointinde kullanılır.
    """
    status: str = "healthy"
    service: str = "Phishing Detection API"
    version: str = "1.0.0"