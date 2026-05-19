using System;
using System.IO;
using Microsoft.ML;
using Microsoft.ML.Data;

namespace PhishingDetectionApp
{
    public class ModelInput
    {
        [LoadColumn(0)] public string Text { get; set; }
        [LoadColumn(1)] public bool Label { get; set; }
    }

    public class ModelOutput
    {
        [ColumnName("PredictedLabel")] public bool Prediction { get; set; }
        public float Probability { get; set; }
        public float Score { get; set; }
    }

    class Program
    {
        private static string DataPath = "combined_dataset.csv";

        static void Main(string[] args)
        {
            var mlContext = new MLContext();
            Console.WriteLine("Sistem Hazırlanıyor (Öğrenme Modu Aktif)...");

            // Başlangıç modelini eğit
            var model = Train(mlContext);

            while (true)
            {
                Console.WriteLine("\nAnaliz edilecek metni girin (Çıkış: 'exit'):");
                string userInput = Console.ReadLine();

                if (string.IsNullOrWhiteSpace(userInput) || userInput.ToLower() == "exit") break;

                // KRİTİK: Analyze artık yeni eğitilmiş modeli geri döndürüyor ve ana değişkeni güncelliyor
                model = Analyze(mlContext, model, userInput);
            }
        }

        public static ITransformer Train(MLContext mlContext)
        {
            if (!File.Exists(DataPath)) throw new FileNotFoundException("Veri seti bulunamadı!");

            IDataView dataView = mlContext.Data.LoadFromTextFile<ModelInput>(
                DataPath, hasHeader: true, separatorChar: ',');

            var pipeline = mlContext.Transforms.Text.FeaturizeText("Features", nameof(ModelInput.Text))
                .Append(mlContext.BinaryClassification.Trainers.FastTree(
                    labelColumnName: nameof(ModelInput.Label),
                    numberOfLeaves: 20,
                    numberOfTrees: 100));

            return pipeline.Fit(dataView);
        }

        // Metot imzası ITransformer döndürecek şekilde güncellendi
        public static ITransformer Analyze(MLContext mlContext, ITransformer model, string text)
        {
            var predictionEngine = mlContext.Model.CreatePredictionEngine<ModelInput, ModelOutput>(model);
            var result = predictionEngine.Predict(new ModelInput { Text = text });

            // 0.7 Çarpanı ile olasılık hesabı
            double rawProbability = 1 / (1 + Math.Exp(-0.7 * result.Score));
            double confidence = 5 + (rawProbability * 90);

            Console.WriteLine("\n" + new string('=', 50));

            if (confidence >= 40 && confidence <= 60)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("DURUM: ??? ŞÜPHELİ / GRİ BÖLGE ???");
                Console.WriteLine($"Kararsızlık Puanı: %{confidence:F2}");
            }
            else if (confidence > 60)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("DURUM: !!! OLTALAMA TESPİT EDİLDİ !!!");
                Console.WriteLine($"Güven Oranı: %{confidence:F2}");
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("DURUM: ✅ GÜVENLİ");
                Console.WriteLine($"Güven Oranı: %{(100 - confidence):F2}");
            }

            Console.ResetColor();
            Console.WriteLine(new string('=', 50));

            Console.Write("[?] Tahmin doğru mu? (E/H): ");
            string feedback = Console.ReadLine()?.ToUpper();

            if (feedback == "H")
            {
                UpdateDataset(text, !result.Prediction, 5);
                Console.WriteLine("-> Model kalıcı olarak güncelleniyor ve ana hafızaya alınıyor...");

                // Yeni eğitilen modeli Main metoduna gönderiyoruz
                return Train(mlContext);
            }

            // Geri bildirim 'E' ise mevcut modeli koru
            return model;
        }

        private static void UpdateDataset(string text, bool label, int repeatCount)
        {
            string safeText = text.Replace(",", " ").Replace("\"", "");
            using (StreamWriter sw = File.AppendText(DataPath))
            {
                for (int i = 0; i < repeatCount; i++)
                {
                    sw.WriteLine($"{safeText},{label.ToString().ToLower()}");
                }
            }
        }
    }
}