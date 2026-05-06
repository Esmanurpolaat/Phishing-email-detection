#!/usr/bin/env python3
"""
Phishing Detection API - Startup Script
========================================
Bu script, API'yi tek komutla başlatır.

Kullanım:
    python3 run.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Proje kök dizinini bul
PROJECT_ROOT = Path(__file__).parent
VENV_PATH = PROJECT_ROOT / "venv"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"


def print_header(text):
    """Başlık yazdır"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def check_venv():
    """Sanal ortamın var olup olmadığını kontrol et"""
    print_header("1/4 - Sanal Ortam Kontrolü")
    
    if not VENV_PATH.exists():
        print("❌ Sanal ortam bulunamadı!")
        print("   Oluşturmak için: python3 -m venv venv")
        sys.exit(1)
    
    print("✅ Sanal ortam mevcut")


def check_dependencies():
    """Kütüphanelerin yüklü olup olmadığını kontrol et"""
    print_header("2/4 - Kütüphane Kontrolü")
    
    # Python executable'ı bul (sanal ortamdaki)
    python_exe = VENV_PATH / "bin" / "python"
    
    # pip list çalıştır
    result = subprocess.run(
        [str(python_exe), "-m", "pip", "list"],
        capture_output=True,
        text=True
    )
    
    installed = result.stdout.lower()
    
    required = ["fastapi", "uvicorn", "pydantic"]
    missing = [pkg for pkg in required if pkg not in installed]
    
    if missing:
        print(f"⚠️  Eksik kütüphaneler: {', '.join(missing)}")
        print("   Yükleniyor...")
        
        subprocess.run([
            str(python_exe), "-m", "pip", "install", "-r", 
            str(REQUIREMENTS_FILE)
        ])
        
        print("✅ Kütüphaneler yüklendi")
    else:
        print("✅ Tüm kütüphaneler mevcut")


def check_structure():
    """Proje dosya yapısını kontrol et"""
    print_header("3/4 - Dosya Yapısı Kontrolü")
    
    required_files = [
        "app/main.py",
        "app/core/config.py",
        "app/models/schemas.py",
        "app/routes/predict.py",
        "app/services/phishing_detector.py"
    ]
    
    missing = []
    for file in required_files:
        if not (PROJECT_ROOT / file).exists():
            missing.append(file)
    
    if missing:
        print("❌ Eksik dosyalar:")
        for f in missing:
            print(f"   - {f}")
        sys.exit(1)
    
    print("✅ Dosya yapısı tamamlanmış")


def start_server():
    """Sunucuyu başlat"""
    print_header("4/4 - Sunucu Başlatılıyor")
    
    # Python executable'ı bul
    python_exe = VENV_PATH / "bin" / "python"
    
    # Uvicorn komutunu hazırla
    cmd = [
        str(python_exe), "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ]
    
    print("\n" + "=" * 60)
    print("  🛡️  Phishing Detection API")
    print("  📡 http://127.0.0.1:8000")
    print("  📚 http://127.0.0.1:8000/docs")
    print("  ⏹️  Durdurmak için: CTRL+C")
    print("=" * 60 + "\n")
    
    # Sunucuyu başlat
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n✅ Sunucu durduruldu")


if __name__ == "__main__":
    try:
        check_venv()
        check_dependencies()
        check_structure()
        start_server()
    except KeyboardInterrupt:
        print("\n\n⚠️  İşlem iptal edildi")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        sys.exit(1)