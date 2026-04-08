# `app/page.tsx` (Türkçe açıklama)

Bu dosya, uygulamanın ana ekranını gösterir: E‑posta metnini yapıştırırsın, “Analyze” dersin, sağ tarafta sonuç çıkar.

## Kısaca dosyada neler var?

- **Üstteki import’lar**: ikonlar ve küçük animasyonlar için.
- **`AnalysisResult`**: Sonucun nasıl görüneceğini tarif eden “şablon” (puan, durum, nedenler).

## `SAMPLE_EMAIL` ne işe yarıyor?

“Load Sample” butonuna basınca, denemelik bir e‑posta otomatik doldurulur.

## Ekranda hatırlanan bilgiler

- **`subject`**: Konu satırı.
- **`emailContent`**: E‑posta gövdesi.
- **`isAnalyzing`**: “Şu an analiz yapılıyor” bilgisidir.
- **`result`**: Çıkan sonuç (yoksa boş).

## “Analyze Email” basınca ne oluyor? (`analyzeEmail`)

Bu proje şu an **gerçek analiz yapmıyor**. Sadece basit bir örnek kontrol yapıyor:

- Önce “analiz başladı” diye ekranı loading’e alır.
- 2 saniye bekler (sanki analiz yapıyormuş gibi).
- Metnin içinde bazı şüpheli kelimeleri arar (ör. “urgent”, “password”, link gibi).
- Buldukça “neden şüpheli” listesini doldurur.
- Bulduklarının sayısına göre bir yüzde puanı hesaplar.
- Puan yüksekse “Phishing Detected”, düşükse “Safe Email” gösterir.

## “Load Sample” basınca ne oluyor? (`loadSample`)

Örnek e‑postayı konu + gövde alanlarına koyar ve önceki sonucu siler.

## Ekranın düzeni

Sayfa ikiye bölünür:

### Sol taraf (yazma alanı)

- Konu alanı
- Metin alanı
- Analyze / Load Sample butonları

### Sağ taraf (sonuç alanı)

- Hiç analiz yoksa: “sonuçlar burada görünecek” gibi bir yazı
- Analiz sürüyorsa: dönen bir yükleniyor işareti
- Sonuç varsa: puan, durum ve nedenler listesi

## Lacivert tema

Renkler lacivert ağırlıklı olsun diye bu dosyada doğrudan renk kodları kullanıldı.

