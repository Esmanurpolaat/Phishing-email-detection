"""
Phishing Detection API - Ana Uygulama
======================================
Bu dosya, FastAPI uygulamasını oluşturur ve tüm parçaları birleştirir.

Çalıştırmak için terminalde:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import predict
from app.models.schemas import HealthResponse

# ==========================================
# 1. FastAPI Uygulamasını Oluştur
# ==========================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    docs_url="/docs",       # Swagger UI adresi
    redoc_url="/redoc",     # ReDoc adresi (alternatif dokümantasyon)
)

# ==========================================
# 2. CORS Middleware Ekle
# ==========================================
"""
CORS (Cross-Origin Resource Sharing) Nedir?

Tarayıcılar güvenlik gereği, bir adresten (örn: localhost:3000) 
başka bir adrese (örn: localhost:8000) istek atmayı ENGELLER.

Frontend (React) localhost:3000'de, Backend localhost:8000'de çalışıyor.
CORS middleware eklemezsen frontend'den gelen istekler REDDEDİLİR.
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # Hangi adreslerden istek kabul edilsin
    allow_credentials=True,                   # Cookie gönderilmesine izin ver
    allow_methods=["*"],                      # Tüm HTTP metotlarına izin (GET, POST, vb.)
    allow_headers=["*"],                      # Tüm header'lara izin ver
)

# ==========================================
# 3. Route'ları Bağla
# ==========================================
# predict.py dosyasındaki router'ı uygulamaya ekle
app.include_router(predict.router)

# ==========================================
# 4. Kök Endpoint'ler
# ==========================================

@app.get(
    "/",
    summary="API Karşılama",
    description="API'nin çalıştığını doğrulamak için basit bir karşılama mesajı."
)
async def root():
    """
    Ana sayfa - API'nin ayakta olduğunu gösterir.
    Tarayıcıda http://localhost:8000 adresine gittiğinde bunu görürsün.
    """
    return {
        "message": "🛡️ Phishing Detection API'ye Hoş Geldiniz!",
        "docs": "Dokümantasyon için /docs adresini ziyaret edin",
        "version": settings.PROJECT_VERSION,
        "endpoints": {
            "health": "/health",
            "predict": "/api/v1/predict",
            "docs": "/docs"
        }
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Sağlık Kontrolü",
    description="Sistemin çalışır durumda olup olmadığını kontrol eder."
)
async def health_check():
    """
    Health Check Endpoint
    
    Neden gerekli?
    → Frontend, backend'in ayakta olup olmadığını kontrol edebilir
    → Deployment sonrası monitoring araçları bu endpoint'i kullanır
    → Kubernetes, Docker gibi sistemler sağlık kontrolü yapar
    """
    return HealthResponse()


# ==========================================
# 5. Uygulama Başlatma (Opsiyonel)
# ==========================================
if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print(f"  {settings.PROJECT_NAME}")
    print(f"  Sürüm: {settings.PROJECT_VERSION}")
    print(f"  Adres: http://localhost:{settings.PORT}")
    print(f"  Docs:  http://localhost:{settings.PORT}/docs")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True  # Kod değiştiğinde otomatik yeniden başlat
    )