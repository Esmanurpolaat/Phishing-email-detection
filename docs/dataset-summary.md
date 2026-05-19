# Phishing Detection Dataset Summary Report
**Hazırlayan:** Mert Sevet (Veri Uzmanı & Veri İşleme)

## 1. Veri Seti Kaynakları
Makine öğrenmesi modelinin gerçek dünya senaryolarına dayanıklı olabilmesi ve modern tehditleri tanıyabilmesi için üç farklı ve güncel veri seti kullanılarak karma (combined) bir veri havuzu oluşturulmuştur:

1. **TREC_05 Dataset:** Akademik literatürde altın standart olarak kabul edilen, gerçek hayattan sızdırılmış geniş çaplı spam/ham e-posta veri seti. Modelin geleneksel kelime kalıplarını öğrenmesini sağlar.
2. **EduPhish Dataset:** Özellikle eğitim sektörünü hedef alan modern oltalama saldırılarını içerir.
3. **Human & LLM Generated Phishing:** ChatGPT gibi Büyük Dil Modelleri (LLM) tarafından üretilmiş, kusursuz gramere sahip yeni nesil oltalama e-postalarını barındırır. Modelin yapay zeka destekli oltalama saldırılarına karşı eğitilmesini sağlar.

## 2. Karşılaşılan Zorluklar ve Veri Anomalileri
Ham veriler (raw data) incelendiğinde şu anomaliler tespit edilmiştir:
* **Duplikasyonlar (Tekrarlar):** Gerçek hayat senaryolarına uygun olarak, aynı spam mailinin binlerce kopyası bulunmaktaydı. Modelin ezberlemesini (overfitting) önlemek için bu kopyalar temizlendi.
* **Hexadecimal ve Encoding Kalıntıları:** E-postaların gövdelerinde (body) Base64 şifrelemeler, URL encoding (`%20`) ve Quoted-Printable HTML kalıntıları (`=E2=80=99`) tespit edildi.

## 3. Veri Ön İşleme (Preprocessing) Adımları
Veriyi makine öğrenmesi (ML) algoritmalarına uygun hale getirmek için Python pipeline'ı üzerinden şu NLP (Doğal Dil İşleme) adımları uygulanmıştır:

1. **Sütun Standardizasyonu:** Tüm farklı CSV formatları birleştirilerek bağımsız değişken `text` (metin) ve hedef değişken `label` (0: Legit/Temiz, 1: Phishing/Oltalama) olacak şekilde tek formata indirgendi.
2. **Gürültü Temizliği (Noise Reduction):** `.drop_duplicates()` ve `.dropna()` metodları ile kopya ve boş mailler silindi.
3. **Regex ile Metin Temizliği:** - Tüm metinler küçük harfe (`lowercase`) çevrildi.
   - HTML etiketleri (`<br>`, `<html>` vb.) silindi.
   - Hexadecimal kodlar, sayılar ve noktalama işaretleri temizlenerek sadece alfabetik karakterler bırakıldı.
   - Modelin kalıpları daha iyi öğrenmesi için URL'ler `urllink`, e-posta adresleri ise `emailadres` yer tutucularıyla (placeholder) değiştirildi.

## 4. Nihai Çıktı
Tüm bu işlemler sonucunda ML uzmanının doğrudan model eğitiminde kullanabileceği, tamamen temizlenmiş ve dengelenmiş `data/processed/combined_dataset.csv` dosyası elde edilmiştir.