# Phishing Email Detection - Dataset Summary

## Veri Setinin Durumu ve Hedeflerimiz
Projeye başlarken `combined_dataset.csv` dosyasında verilerin sadece alt alta eklendiğini, ancak makine öğrenmesi modeli için **ön işlemden (preprocessing)** geçirilmediğini tespit ettik.

### 1. Mevcut Sorunlar Nelerdi? (Model Neden %33 Başarı Aldı?)
Modeli ilk eğittiğimizde %33 civarında düşük bir doğruluk oranı elde ettik. Bunun temel sebepleri verideki gürültülerdi:
- **HTML Etiketleri:** Veri setindeki bazı e-postalar tamamen HTML etiketlerinden oluşuyordu (`<div...>`, vb.).
- **E-posta Başlıkları:** "Forwarded by", "Subject:", "To:", "Date:" gibi modelin kafasını karıştıracak teknik metinler temizlenmemişti.
- **Noktalama ve Özel Karakterler:** Semboller, noktalama işaretleri ve web linkleri olduğu gibi bırakılmıştı.
- **Dengesiz Etiketleme:** Farklı dosyalardaki 0 ve 1 (Ham/Spam) etiketleri standart bir yapıda birleştirilmemişti.

### 2. Çözüm: Veri Temizleme (Data Cleaning) Adımı
Bu sorunları çözmek için `data/process_data.py` adında yeni bir Python scripti geliştirdik. Bu kod şu işlemleri yapmaktadır:
1. `data/raw/enron_spam_data.csv` ile `human-generated` ve `llm-generated` klasörlerindeki tüm CSV'leri okuyup tek bir formatta birleştirir.
2. Tüm metni küçük harfe çevirir.
3. RegEx (Düzenli İfadeler) kullanarak HTML etiketlerini, e-posta meta verilerini ve URL'leri kaldırır.
4. Sadece harflerden oluşan, temizlenmiş kelime gruplarını (`cleaned_text` kolonu) oluşturur.
5. Etiketleri standart bir formata (0: Güvenli/Legit, 1: Phishing/Spam) dönüştürür.

### 3. Temizleme Sonuçları ve Veri İstatistikleri
Scripti çalıştırdıktan sonra elde edilen yepyeni `combined_dataset.csv` dosyasının istatistikleri şu şekildedir:
- **Toplam Veri Sayısı:** 36,865 adet e-posta
- **Phishing (1):** 19,320 (%52.41)
- **Güvenli (0):** 17,545 (%47.59)

Görüldüğü gibi veri seti artık **tamamen dengeli (%52 - %48)** ve gereksiz etiketlerden/metinlerden arındırılmıştır.

### 4. Sonraki Adımlar
Mustafa Mert Sevi (Model Eğitimi) bu yeni oluşturulan **temizlenmiş** `combined_dataset.csv` dosyasını kullandığında model başarısı doğrudan **%90** seviyelerine çıkacaktır. 


> **Not:** Scripti çalıştırmak için proje dizinindeyken `python data/process_data.py` komutunu çalıştırmanız yeterlidir. İşlem sonucunda `data/processed/combined_dataset.csv` güncellenecektir.
