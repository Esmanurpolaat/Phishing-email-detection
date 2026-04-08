"""
Predict Route (Tahmin Endpointi)
--------------------------------
/predict POST endpointini tanımlar.
Kullanıcıdan e-posta metni alır, analiz eder, sonuç döner.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import EmailInput, PredictionResponse
from app.services.phishing_detector import detector
from datetime import datetime

# Router oluştur
# prefix="/api/v1" demek: Tüm endpoint'ler /api/v1 ile başlar
# tags=["Prediction"] demek: Swagger'da "Prediction" grubu altında görünür
router = APIRouter(
    prefix="/api/v1",
    tags=["Prediction"]
)


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="E-posta Phishing Tespiti",
    description="Verilen e-posta metnini analiz ederek phishing olup olmadığını belirler."
)
async def predict_phishing(email_input: EmailInput):
    """
    E-posta phishing analizi yapar.
    
    İşlem Akışı:
    1. Kullanıcıdan EmailInput formatında veri alır
    2. PhishingDetector servisine gönderir
    3. PredictionResponse formatında sonuç döner
    
    Neden 'async def' kullanıyoruz?
    → FastAPI asenkron çalışır, birden fazla isteği aynı anda karşılayabilir
    → İleride model tahmini uzun sürebilir, diğer istekler bloklanmasın
    """
    
    try:
        # Phishing detector servisini çağır
        result = detector.analyze(
            email_text=email_input.email_text,
            subject=email_input.subject
        )
        
        # Sonucu PredictionResponse formatında döndür
        return PredictionResponse(
            is_phishing=result["is_phishing"],
            confidence=result["confidence"],
            risk_level=result["risk_level"],
            message=result["message"],
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        # Beklenmeyen hata durumunda 500 hatası döndür
        raise HTTPException(
            status_code=500,
            detail=f"Analiz sırasında bir hata oluştu: {str(e)}"
        )