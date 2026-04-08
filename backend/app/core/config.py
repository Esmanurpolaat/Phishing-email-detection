"""
Uygulama Ayarları
-----------------
API'nin genel ayarları burada tutulur.
Port numarası, izinler, proje adı gibi.
"""

class Settings:
    # Proje Bilgileri
    PROJECT_NAME: str = "Phishing Email Detection API"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = (
        "Kullanıcıların e-posta metinlerini analiz ederek "
        "phishing saldırısı içerip içermediğini tespit eden API"
    )

    # Sunucu Ayarları
    HOST: str = "0.0.0.0"  # Tüm ağlardan erişime açık
    PORT: int = 8000       # Sunucu portu

    # CORS Ayarları (Frontend bağlantısı için)
    # Frontend'in çalıştığı adresler buraya yazılır
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",     # React
        "http://localhost:5173",     # Vite
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"                          # Geliştirme aşamasında herkese açık
    ]


# Uygulama boyunca kullanılacak tek settings nesnesi
settings = Settings()