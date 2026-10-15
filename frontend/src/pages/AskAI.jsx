import React, { useState, useRef, useEffect, useMemo } from 'react';
import { useTranslation } from '../services/LanguageContext';
import { askAI } from '../services/api';
import { 
  Bot, 
  Send, 
  Sparkles, 
  BookOpen, 
  ExternalLink, 
  MapPin, 
  FileText,
  User,
  Database,
  CheckCircle2,
  AlertTriangle,
  HelpCircle,
  Building,
  RotateCcw
} from 'lucide-react';

export const AskAI = () => {
  const { lang, t } = useTranslation();
  const [inputVal, setInputVal] = useState('');
  const [loading, setLoading] = useState(false);
  const [districtHint, setDistrictHint] = useState('');
  const messagesEndRef = useRef(null);

  const initialGreeting = useMemo(() => ({
    id: 'initial',
    role: 'assistant',
    text:
      lang === 'ta'
        ? 'வணக்கம்! நான் பெயர்வரலாறு AI வரலாற்று ஆய்வாளர். தமிழ்நாடு ஆவணக் காப்பகம், கல்வெட்டுகள் மற்றும் மாவட்ட அரசிதழ்கள் அடிப்படையில் தமிழக ஊர்ப் பெயர்களின் பரிணாமம், பழைய பெயர்கள் மற்றும் பெயர் மாற்றங்கள் பற்றிய உங்கள் கேள்விகளுக்குச் சான்றாதாரங்களுடன் பதிலளிக்க முடியும்.'
        : 'Welcome! I am the PeyarVaralaru AI Historical Research Assistant. Ask me about historical place names, official renamings, and inscriptional origins grounded in verified archival publications.',
    sources: [],
    passages: [],
    evidence_status: 'verified',
    isInitial: true,
  }), [lang]);

  const [chatHistory, setChatHistory] = useState([]);

  // Sync initial message when lang changes if chat is empty or initial
  useEffect(() => {
    setChatHistory((prev) => {
      if (prev.length === 0 || (prev.length === 1 && prev[0].isInitial)) {
        return [initialGreeting];
      }
      return prev.map(msg => msg.isInitial ? initialGreeting : msg);
    });
  }, [initialGreeting]);

  const suggestions = [
    {
      label_ta: 'ஆரணி என்ற ஊரின் பெயர் காரணம் என்ன?',
      label_en: 'Why is Arani called Arani?',
      q_ta: 'ஆரணி என்ற ஊரின் பெயர் வரலாறு மற்றும் கமண்டல நாக நதி தொடர்பு என்ன?',
      q_en: 'What is the historical origin of the name Arani and its link to the Kamandala Naga river?'
    },
    {
      label_ta: 'திருவண்ணாமலை சோழர் கல்வெட்டுகள் என்ன கூறுகின்றன?',
      label_en: 'What do Chola epigraphs say about Tiruvannamalai?',
      q_ta: 'திருவண்ணாமலை சோழர் மற்றும் விஜயநகர கல்வெட்டுகளில் எவ்வாறு ஆவணப்படுத்தப்பட்டுள்ளது?',
      q_en: 'How is Tiruvannamalai documented in Chola and Vijayanagara stone inscriptions?'
    },
    {
      label_ta: 'மெட்ராஸ் எப்போது சென்னை என அதிகாரப்பூர்வமாக மாறியது?',
      label_en: 'When was Madras officially renamed to Chennai?',
      q_ta: 'மெட்ராஸ் என்பது சென்னை என எப்போது மறுபெயரிடப்பட்டது? அரசாணை எண் என்ன?',
      q_en: 'When was Madras officially renamed to Chennai? What was the Government Order number?'
    },
    {
      label_ta: 'தஞ்சாவூர் பெயர்தோற்றம் வாய்மொழி மரபா அல்லது கல்வெட்டு உண்மையா?',
      label_en: 'Is the name Thanjavur folk legend or verified fact?',
      q_ta: 'தஞ்சாவூர் பெயர்தோற்றம் தலபுராண வாய்மொழி மரபா அல்லது நேரடி வரலாற்று உண்மையா?',
      q_en: 'Is the etymological origin of Thanjavur oral sthala purana legend or documented historical fact?'
    },
    {
      label_ta: 'களம்பூர் என்ற ஊரின் வரலாற்று மூலம் என்ன?',
      label_en: 'What is the historical origin of Kalambur?',
      q_ta: 'களம்பூர் என்ற ஊரின் பெயர் மற்றும் வரலாற்றுச் சான்றுகள் என்ன?',
      q_en: 'What are the historical inscriptions and origins for the town of Kalambur?'
    }
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, loading]);

  const handleSend = async (questionText = null) => {
    const q = (questionText || inputVal).trim();
    if (!q || loading) return;

    // Add user message
    const userMsg = {
      id: Date.now(),
      role: 'user',
      text: q,
    };
    setChatHistory((prev) => [...prev, userMsg]);
    setInputVal('');
    setLoading(true);

    try {
      const res = await askAI(q, lang, districtHint || null);
      const assistantMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        text: res.answer || (lang === 'ta' ? 'பதில் கிடைக்கவில்லை.' : 'No response generated.'),
        sources: res.sources_used || [],
        passages: res.passages_used || [],
        evidence_status: res.evidence_status || 'verified',
        evidence_classification: res.evidence_classification,
        is_fallback: res.is_fallback,
      };
      setChatHistory((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error('Ask error:', err);
      const errorMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        text:
          lang === 'ta'
            ? 'மன்னிக்கவும், வரலாற்றுத் தரவுதளத்தை அணுகுவதில் பிழை ஏற்பட்டது. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.'
            : 'Apologies, an error occurred while connecting to the historical database. Please retry.',
        sources: [],
        passages: [],
        evidence_status: 'unverified',
      };
      setChatHistory((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const getEvidenceBadge = (status) => {
    switch (status) {
      case 'verified':
      case 'documented_fact':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-900 border border-emerald-300">
            <CheckCircle2 className="w-3 h-3 text-emerald-700" />
            {lang === 'ta' ? 'சான்றாதார உண்மை' : 'Documented Fact'}
          </span>
        );
      case 'partially_verified':
      case 'scholarly_hypothesis':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-300">
            <AlertTriangle className="w-3 h-3 text-amber-700" />
            {lang === 'ta' ? 'அறிஞர் கருதுகோள்' : 'Scholarly Hypothesis'}
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-900 border border-rose-300">
            <HelpCircle className="w-3 h-3 text-rose-700" />
            {lang === 'ta' ? 'வாய்மொழி மரபு' : 'Folk Tradition'}
          </span>
        );
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto py-2">
      {/* Header Banner */}
      <div className="bg-[#172B40] text-white rounded-2xl p-6 border border-[#2A3E54] shadow-sm relative overflow-hidden">
        <div className="absolute right-0 top-0 w-72 h-72 bg-[#C5A66A]/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#C5A66A]/20 border border-[#C5A66A]/40 text-[#C5A66A] text-xs font-semibold">
            <Bot className="w-3.5 h-3.5" />
            <span>{lang === 'ta' ? 'சான்றாதார AI வரலாற்று ஆய்வாளர்' : 'Source-Grounded History AI'}</span>
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            {lang === 'ta'
              ? 'தமிழக ஊர்ப் பெயர்கள் குறித்து AI-யிடம் கேளுங்கள்'
              : 'Ask History AI — Backed by Archival Citations'}
          </h1>
          <p className="text-xs sm:text-sm text-gray-300 leading-relaxed">
            {lang === 'ta'
              ? 'கற்பனையான கூற்றுகளைத் தவிர்த்து, மாவட்ட அரசிதழ்கள் மற்றும் கல்வெட்டு வெளியீடுகளின் அடிப்படையில் சான்றுகளுடன் கூடிய பதில்களைப் பெறுங்கள்.'
              : 'Grounded exclusively in Tamil Nadu Gazetteers, Epigraphia Indica, and official Government Orders.'}
          </p>
        </div>
      </div>

      {/* Suggested Questions */}
      <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm space-y-2">
        <span className="text-xs font-bold text-gray-600 block">
          {lang === 'ta' ? 'பரிந்துரைக்கப்பட்ட வரலாற்று வினாக்கள்:' : 'Suggested historical inquiries:'}
        </span>
        <div className="flex flex-wrap gap-2">
          {suggestions.map((s, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(lang === 'ta' ? s.q_ta : s.q_en)}
              className="px-3 py-1.5 rounded-lg bg-[#F7F4ED] hover:bg-[#eae5d8] text-[#172B40] text-xs font-medium border border-gray-200 transition-colors text-left"
            >
              {lang === 'ta' ? s.label_ta : s.label_en}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Messages Stream */}
      <div className="space-y-4 min-h-[380px]">
        {chatHistory.map((msg) => {
          const isUser = msg.role === 'user';
          return (
            <div
              key={msg.id}
              className={`flex items-start gap-3 ${isUser ? 'flex-row-reverse' : ''}`}
            >
              <div
                className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 ${
                  isUser
                    ? 'bg-[#172B40] text-white shadow-sm'
                    : 'bg-[#C5A66A] text-[#172B40] shadow-sm font-bold'
                }`}
              >
                {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
              </div>

              <div
                className={`rounded-2xl p-4 sm:p-5 text-xs sm:text-sm leading-relaxed max-w-2xl shadow-sm ${
                  isUser
                    ? 'bg-[#172B40] text-white rounded-tr-none'
                    : 'bg-white text-[#172B40] border border-gray-200 rounded-tl-none space-y-3'
                }`}
              >
                {!isUser && (
                  <div className="flex items-center justify-between border-b border-gray-100 pb-2">
                    <span className="font-bold text-xs text-[#172B40]">
                      {lang === 'ta' ? 'வரலாற்று ஆய்வாளர்' : 'Research Assistant'}
                    </span>
                    {getEvidenceBadge(msg.evidence_status)}
                  </div>
                )}

                <div className="whitespace-pre-line font-medium leading-relaxed">
                  {msg.text}
                </div>

                {/* Footnotes & Cited Sources */}
                {!isUser && msg.sources && msg.sources.length > 0 && (
                  <div className="pt-2 border-t border-gray-100 space-y-1.5 text-[11px] text-gray-600">
                    <span className="font-bold text-gray-500 block">
                      {lang === 'ta' ? 'மேற்கோள் காட்டப்பட்ட சான்றுகள்:' : 'Cited Archival Citations:'}
                    </span>
                    {msg.sources.map((src, sIdx) => (
                      <div key={sIdx} className="flex items-start gap-1.5 bg-[#F7F4ED] p-2 rounded-lg border border-gray-100">
                        <BookOpen className="w-3.5 h-3.5 text-[#C5A66A] shrink-0 mt-0.5" />
                        <div>
                          <span className="font-bold text-[#172B40]">{src.title}</span>{' '}
                          {src.publication_year && <span>({src.publication_year})</span>}
                          {src.source_url && (
                            <a
                              href={src.source_url}
                              target="_blank"
                              rel="noreferrer"
                              className="text-[#C5A66A] underline ml-1 font-semibold"
                            >
                              {lang === 'ta' ? 'ஆவணம் காண்க' : 'View Archive'}
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="flex items-start gap-3">
            <div className="w-9 h-9 rounded-xl bg-[#C5A66A] text-[#172B40] flex items-center justify-center shrink-0">
              <Bot className="w-5 h-5" />
            </div>
            <div className="bg-white rounded-2xl p-4 border border-gray-200 shadow-sm flex items-center gap-2 text-xs font-semibold text-[#172B40]">
              <div className="animate-spin w-4 h-4 border-2 border-[#172B40] border-t-transparent rounded-full" />
              <span>{lang === 'ta' ? 'அரசிதழ் தரவுகளில் சான்றுகளைத் தேடுகிறது...' : 'Searching archival citations and epigraphy...'}</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Message Composer */}
      <div className="bg-white rounded-2xl p-3 border border-gray-200 shadow-md">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            placeholder={
              lang === 'ta'
                ? 'உங்கள் வரலாற்று வினாவை உள்ளிடுங்கள்... (எ.கா: மதுரை பெயர்க்காரணம் என்ன?)'
                : 'Ask any historical place inquiry... (e.g. Origin of Madurai?)'
            }
            className="flex-1 px-4 py-2.5 bg-[#F7F4ED] rounded-xl text-xs sm:text-sm text-[#172B40] focus:outline-none focus:ring-1 focus:ring-[#C5A66A] border border-gray-200 font-medium"
          />
          <button
            type="submit"
            disabled={!inputVal.trim() || loading}
            className="bg-[#172B40] hover:bg-[#20364F] disabled:opacity-50 text-white font-bold text-xs px-5 py-3 rounded-xl transition-colors flex items-center gap-1.5 shrink-0 shadow-sm"
          >
            <Send className="w-4 h-4 text-[#C5A66A]" />
            <span className="hidden sm:inline">{lang === 'ta' ? 'அனுப்புக' : 'Send'}</span>
          </button>
        </form>
      </div>
    </div>
  );
};

export default AskAI;
