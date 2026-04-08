
"use client";
import { useState } from 'react';
import { Shield, AlertTriangle, CheckCircle2, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from "framer-motion";

// Not: Buradaki “analiz” gerçek değil; sadece örnek olsun diye basit bir kontrol yapıyor.
// İleride gerçek analiz eklenecekse `analyzeEmail` içi değişir.
interface AnalysisResult {
  riskScore: number;
  status: 'safe' | 'phishing';
  reasons: string[];
}

const SAMPLE_EMAIL = {
  subject: "URGENT: Your account will be suspended!",
  content: `Dear Valued Customer,

We have detected unusual activity on your account. Your account will be SUSPENDED within 24 hours unless you verify your information immediately.

Click here to verify now: http://secure-bank-verify.suspicious-domain.com

Please provide the following information:
- Full Name
- Account Number
- Password
- Social Security Number

Failure to respond will result in permanent account closure.

Best regards,
Security Team`
};

export default function App() {
  // Kullanıcının yazdıklarını burada tutuyoruz.
  const [subject, setSubject] = useState('');
  const [emailContent, setEmailContent] = useState('');

  // Analiz devam ediyor mu, sonuç var mı?
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const analyzeEmail = () => {
    setIsAnalyzing(true);
    setResult(null);

    // 2 sn bekleyip bazı “şüpheli” kelimeleri arıyoruz.
    setTimeout(() => {
      const text = (subject + ' ' + emailContent).toLowerCase();
      
      const suspiciousPatterns = [
        { pattern: /urgent|immediate|suspended|verify now|act now/i, reason: 'Urgent language used to create pressure' },
        { pattern: /password|social security|ssn|credit card|account number/i, reason: 'Requests for sensitive personal information' },
        { pattern: /click here|verify account|confirm identity/i, reason: 'Suspicious call-to-action phrases' },
        { pattern: /http:\/\/|bit\.ly|tinyurl/i, reason: 'Suspicious or shortened links detected' },
        { pattern: /prize|winner|lottery|inheritance/i, reason: 'Too-good-to-be-true offers' },
        { pattern: /dear (valued )?customer|dear user/i, reason: 'Generic greeting instead of personal name' },
      ];

      const detectedReasons: string[] = [];
      suspiciousPatterns.forEach(({ pattern, reason }) => {
        if (pattern.test(text)) {
          detectedReasons.push(reason);
        }
      });

      // Ne kadar çok “şüpheli” işaret bulursa puan o kadar artar.
      const riskScore = Math.min(95, detectedReasons.length * 18);
      const status = riskScore >= 50 ? 'phishing' : 'safe';

      setResult({
        riskScore,
        status,
        reasons: detectedReasons.length > 0 
          ? detectedReasons 
          : ['No suspicious patterns detected', 'Sender appears legitimate', 'Content seems safe']
      });
      setIsAnalyzing(false);
    }, 2000);
  };

  const loadSample = () => {
    // Denemek için örnek bir e-posta koyar.
    setSubject(SAMPLE_EMAIL.subject);
    setEmailContent(SAMPLE_EMAIL.content);
    setResult(null);
  };

  return (
    <div className="h-screen overflow-hidden relative bg-gradient-to-br from-[#050B1A] via-[#071127] to-[#0B1B35] text-[#EAF1FF]">
    
      
      <div className="relative z-10 h-full flex flex-col">
        {/* Compact Header */}
        <motion.div 
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex-shrink-0 text-center py-6"
        >
          <div className="flex items-center justify-center gap-2">
            <Shield className="w-7 h-7 text-[#9DB9FF]" strokeWidth={1.5} />
            <h1 className="text-2xl font-bold bg-gradient-to-r from-[#7FA2FF] to-[#C9D7FF] bg-clip-text text-transparent">
              Phishing Email Detection
            </h1>
          </div>
          <p className="text-[#BFD1FF]/60 text-sm mt-1">
            Analyze suspicious emails and detect phishing risk
          </p>
        </motion.div>

        {/* Main Content - 2 Column Layout */}
        <div className="flex-1 px-6 pb-6 overflow-hidden">
          <div className="h-full grid lg:grid-cols-2 gap-6 max-w-7xl mx-auto">
            {/* Left Column - Input Form */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="flex flex-col h-full"
            >
              <div className="bg-gradient-to-br from-[#081428]/85 to-[#0D1F3D]/85 backdrop-blur-xl rounded-2xl p-6 border border-white/10 shadow-2xl shadow-black/30 flex flex-col h-full">
                <h3 className="text-lg font-semibold text-[#EAF1FF] mb-4 flex-shrink-0">
                  Email Content
                </h3>

                <div className="flex-1 flex flex-col overflow-hidden">
                  {/* Subject Input */}
                  <div className="mb-3 flex-shrink-0">
                    <label className="block text-xs text-[#BFD1FF]/75 mb-1.5">Subject Line</label>
                    <input
                      type="text"
                      value={subject}
                      onChange={(e) => setSubject(e.target.value)}
                      placeholder="Enter email subject..."
                      className="w-full bg-[#0F2447]/60 border border-white/10 rounded-lg px-3 py-2 text-sm text-[#EAF1FF] placeholder-[#9DB9FF]/35 focus:outline-none focus:border-[#9DB9FF]/60 focus:ring-1 focus:ring-[#9DB9FF]/20 transition-all"
                    />
                  </div>

                  {/* Email Content Textarea */}
                  <div className="flex-1 flex flex-col overflow-hidden mb-3">
                    <label className="block text-xs text-[#BFD1FF]/75 mb-1.5 flex-shrink-0">Email Body</label>
                    <textarea
                      value={emailContent}
                      onChange={(e) => setEmailContent(e.target.value)}
                      placeholder="Paste the email content here..."
                      className="flex-1 w-full bg-[#0F2447]/60 border border-white/10 rounded-lg px-3 py-2 text-sm text-[#EAF1FF] placeholder-[#9DB9FF]/35 focus:outline-none focus:border-[#9DB9FF]/60 focus:ring-1 focus:ring-[#9DB9FF]/20 transition-all resize-none"
                    />
                  </div>

                  {/* Action Buttons */}
                  <div className="flex gap-2 flex-shrink-0">
                    <button
                      onClick={analyzeEmail}
                      disabled={!emailContent.trim() || isAnalyzing}
                      className="flex-1 bg-gradient-to-r from-[#193B7A] to-[#2A5AA6] hover:from-[#1D448C] hover:to-[#2F67C0] disabled:from-[#1B2740] disabled:to-[#1B2740] text-white py-2.5 px-4 rounded-lg text-sm font-semibold shadow-lg shadow-black/30 hover:shadow-black/40 transition-all duration-300 disabled:cursor-not-allowed disabled:shadow-none flex items-center justify-center gap-2"
                    >
                      {isAnalyzing ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin" />
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <Shield className="w-4 h-4" />
                          Analyze Email
                        </>
                      )}
                    </button>
                    
                    <button
                      onClick={loadSample}
                      className="bg-[#0F2447]/70 hover:bg-[#132A52]/70 border border-white/10 hover:border-[#9DB9FF]/30 text-[#C9D7FF] py-2.5 px-4 rounded-lg text-sm font-semibold transition-all duration-300"
                    >
                      Load Sample
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Right Column - Results */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="flex flex-col h-full"
            >
              <div className="bg-gradient-to-br from-[#081428]/85 to-[#0D1F3D]/85 backdrop-blur-xl rounded-2xl p-6 border border-white/10 shadow-2xl shadow-black/30 flex flex-col h-full">
                <h3 className="text-lg font-semibold text-[#EAF1FF] mb-4 flex-shrink-0">Analysis Results</h3>

                <div className="flex-1 overflow-y-auto">
                  <AnimatePresence mode="wait">
                    {!result && !isAnalyzing && (
                      <motion.div
                        key="empty"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="flex flex-col items-center justify-center h-full text-center"
                      >
                        <div className="w-20 h-20 rounded-full bg-[#9DB9FF]/10 flex items-center justify-center mb-3">
                          <Shield className="w-10 h-10 text-[#9DB9FF]/55" />
                        </div>
                        <p className="text-[#BFD1FF]/60">
                          Enter an email to analyze
                        </p>
                        <p className="text-[#9DB9FF]/40 text-xs mt-1">
                          Results will appear here
                        </p>
                      </motion.div>
                    )}

                    {isAnalyzing && (
                      <motion.div
                        key="loading"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="flex flex-col items-center justify-center h-full"
                      >
                        <Loader2 className="w-14 h-14 text-[#9DB9FF] animate-spin mb-3" />
                        <p className="text-[#C9D7FF]">Analyzing email content...</p>
                        <p className="text-[#9DB9FF]/60 text-sm mt-1">Checking for suspicious patterns</p>
                      </motion.div>
                    )}

                    {result && (
                      <motion.div
                        key="results"
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.95 }}
                        transition={{ duration: 0.3 }}
                        className="space-y-5"
                      >
                        {/* Risk Score */}
                        <div>
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm text-[#BFD1FF]/70">Risk Score</span>
                            <span className={`text-3xl font-bold ${
                              result.status === 'phishing' ? 'text-[#D6C8FF]' : 'text-[#B8CBFF]'
                            }`}>
                              {result.riskScore}%
                            </span>
                          </div>
                          
                          {/* Progress Bar */}
                          <div className="relative h-2.5 bg-[#0F2447]/60 rounded-full overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${result.riskScore}%` }}
                              transition={{ duration: 1, ease: 'easeOut' }}
                              className={`h-full rounded-full ${
                                result.status === 'phishing'
                                  ? 'bg-gradient-to-r from-[#3B2C6E] to-[#2A4A6F]'
                                  : 'bg-gradient-to-r from-[#193B7A] to-[#3A78D6]'
                              }`}
                              style={{
                                boxShadow: result.status === 'phishing' 
                                  ? '0 0 15px rgba(142, 123, 255, 0.35)' 
                                  : '0 0 15px rgba(127, 162, 255, 0.35)'
                              }}
                            />
                          </div>
                        </div>

                        {/* Status Badge */}
                        <div>
                          <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full ${
                            result.status === 'phishing'
                              ? 'bg-[#3B2C6E]/25 border border-[#8E7BFF]/35 text-[#D6C8FF]'
                              : 'bg-[#193B7A]/25 border border-[#7FA2FF]/35 text-[#C9D7FF]'
                          }`}>
                            {result.status === 'phishing' ? (
                              <>
                                <AlertTriangle className="w-4 h-4" />
                                <span className="text-sm font-semibold">Phishing Detected</span>
                              </>
                            ) : (
                              <>
                                <CheckCircle2 className="w-4 h-4" />
                                <span className="text-sm font-semibold">Safe Email</span>
                              </>
                            )}
                          </div>
                        </div>

                        {/* Explanation List */}
                        <div>
                          <h4 className="text-xs font-semibold text-[#BFD1FF]/70 mb-2 uppercase tracking-wide">
                            {result.status === 'phishing' ? 'Warning Signs' : 'Analysis Details'}
                          </h4>
                          <div className="space-y-2">
                            {result.reasons.map((reason, index) => (
                              <motion.div
                                key={index}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className={`flex items-start gap-2 p-2.5 rounded-lg ${
                                  result.status === 'phishing'
                                    ? 'bg-[#120C22]/35 border border-[#3B2C6E]/50'
                                    : 'bg-[#0A1730]/35 border border-[#193B7A]/40'
                                }`}
                              >
                                {result.status === 'phishing' ? (
                                  <AlertTriangle className="w-3.5 h-3.5 text-[#D6C8FF] mt-0.5 flex-shrink-0" />
                                ) : (
                                  <CheckCircle2 className="w-3.5 h-3.5 text-[#B8CBFF] mt-0.5 flex-shrink-0" />
                                )}
                                <span className="text-xs text-[#EAF1FF]/85 leading-relaxed">{reason}</span>
                              </motion.div>
                            ))}
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}