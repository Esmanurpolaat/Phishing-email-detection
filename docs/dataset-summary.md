# Phishing Detection Dataset Summary Report
**Hazırlayan:** Mert Sevet (Veri Uzmanı & Veri İşleme)

1. Veri Seti Kaynakları ve Stratejik Seçim
Modelin eğitim süresini optimize etmek ve en güncel tehditlere odaklanmak amacıyla literatürdeki en verimli veri setleri dinamik bir pipeline ile birleştirilmiştir:

Enron Spam Dataset: Kurumsal yazışma dilini ve klasik spam kalıplarını temsil eden, gerçek dünya verilerinden oluşan temel veri seti.

Kaggle Human & LLM Generated Dataset: - Human-Generated: İnsanlar tarafından kurgulanmış güncel oltalama e-postaları.

LLM-Generated: ChatGPT/LLM tabanlı, dil bilgisi kusursuz yeni nesil "AI-Powered Phishing" saldırıları.
(Not: Proje verimliliği ve performans dengesi gözetilerek çok eski tarihli TREC_05 verisi yerine bu modern setlere odaklanılmıştır.)

2. Karşılaşılan Teknik Zorluklar
Ham veriler (raw data) üzerinde yapılan derin analizlerde şu kritik sorunlar saptanmış ve çözülmüştür:

Hayalet Karakterler (Ghost Data): Sadece boşluk ( ), enter (\n) veya anlamsız Unicode karakterlerinden oluşan 30 binden fazla "boş" görünen ama aslında veri kaplayan satır tespit edildi.

Etiketleme Karmaşası: Farklı kaynaklarda "phishing", "legit", "spam", "ham" gibi metinsel ifadelerle tutulan etiketler, ML algoritmalarının anlayacağı sayısal (0/1) formata dönüştürülürken sistem çökmelerini önlemek için özel bir sözlük (mapping) mimarisi kuruldu.

3. Gelişmiş Veri Ön İşleme (Nükleer Temizlik Pipeline)
Veri setini pürüzsüz hale getirmek için geliştirilen Python scripti şu ileri seviye adımları uygulamaktadır:

Dinamik Dosya Analizi: Veriler, dosya isimlerinden (phishing.csv / legit.csv) otomatik olarak etiketlenerek manuel hata payı sıfıra indirilmiştir.

Nükleer Filtre (Regex Harf Filtresi): İçerisinde en az 10 adet gerçek alfabetik karakter (a-z) barındırmayan; sadece noktalama işaretlerinden, sayılardan veya görünmez boşluklardan oluşan tüm satırlar elimine edilmiştir.

Mükemmel Tekilleştirme (De-duplication): Aynı e-postanın binlerce kez tekrar etmesi engellenerek modelin ezber yapması (overfitting) önlenmiş, veri seti hacmi kalite odaklı olarak optimize edilmiştir.

Sentetik Metin Standardizasyonu: Çoklu boşluklar tek boşluğa indirilmiş, metinler strip() edilerek temiz bir tokenizasyon ortamı hazırlanmıştır.

4. İstatistiksel Özet ve Sonuç
Ham Veri Toplamı: ~37.311 Satır

Çıktı Konumu: data/processed/combined_dataset.csv

Bu süreç sonunda elde edilen veri seti; anlamsız gürültüden arındırılmış, dengeli ve modern phishing saldırılarını en iyi temsil eden nihai eğitim materyalidir.
