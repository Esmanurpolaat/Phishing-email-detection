using Microsoft.ML.Data;

namespace PhishingRadar
{
    public class ModelInput
    {
        [ColumnName("cleaned_text"), LoadColumn(0)]
        public string Text { get; set; }

        [ColumnName("label"), LoadColumn(1)]
        public bool Label { get; set; }
    }

    public class ModelOutput
    {
        [ColumnName("PredictedLabel")]
        public bool Prediction { get; set; }

        [ColumnName("Score")]
        public float Score { get; set; }
    }
}