import React, { useState } from 'react';
import { useTranslation } from '../services/LanguageContext';
import { askAI } from '../services/api';
import { 
  Bot, 
  Send, 
  Sparkles, 
  BookOpen, 
  ExternalLink, 
  ShieldAlert, 
  MapPin, 
  FileText,
  User,
  Database
} from 'lucide-react';

export const AskAI = () => {
  const { lang, t } = useTranslation();
  const [inputVal, setInputVal] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([
    {
      role: 'assistant',
      text:
        lang === 'ta'
          ? 'வணக்கம்! நான் பெயர்வரலாறு AI வரலாற்று ஆய்வாளர். தமிழ்நாடு ஆவணக் காப்பகம் மற்றும் அரசிதழ் பதிவுகள் அடிப்படையில் தமிழக ஊர்ப் பெயர்களின் பரிணாமம், பெயர் மாற்றங்கள் மற்றும் பழைய வடிவங்கள் பற்றிய உங்கள் கேள்விகளுக்குப் பதிலளிக்க முடியும்.'
          : 'Welcome! I am PeyarVaralaru AI Research Assistant. Ask me about historical place names, official renamings, and spelling variants grounded in Tamil Nadu archival records.',
      sources: [],
      places: [],
      isInitial: true,
    },
  ]);

  const suggestions = [
    {
      label:
        lang === 'ta'
          ? 'மெட்ராஸ் என்ற பெயரின் வரலாறு என்ன?'
          : 'What is the history of the name Madras?',
      q:
        lang === 'ta'
          ? 'மெட்ராஸ் என்ற பெயரின் வரலாறு என்ன?'
          : 'What is the history of the name Madras?',
    },
    {
      label:
        lang === 'ta'
          ? 'பிளாக் டவுன் எப்போது ஜார்ஜ் டவுன் என மாற்றப்பட்டது?'
          : 'When was Black Town renamed to George Town?',
      q:
        lang === 'ta'
          ? 'பிளாக் டவுன் எப்போது ஜார்ஜ் டவுன் என மாற்றப்பட்டது?'
          : 'When was Black Town renamed to George Town?',
    },
    {
      label:
        lang === 'ta'
          ? 'திருச்சிராப்பள்ளி மற்றும் தஞ்சாவூரின் ஆங்கில வரலாற்றுப் பெயர்கள் என்ன?'
          : 'What were the historical English forms of Tiruchirappalli and Thanjavur?',
      q:
        lang === 'ta'
          ? 'திருச்சிராப்பள்ளி மற்றும் தஞ்சாவூரின் ஆங்கில வரலாற்றுப் பெயர்கள் என்ன?'
          : 'What were the historical English forms of Tiruchirappalli and Thanjavur?',
    },
    {
      label:
        lang === 'ta'
          ? 'அதிகாரப்பூர்வ பெயர் மாற்றத்திற்கும் வரலாற்று எழுத்துப் பிழைக்கும் உள்ள வேறுபாடு என்ன?'
          : 'What is the difference between an official renaming and a spelling variant?',
      q:
        lang === 'ta'
          ? 'அதிகாரப்பூர்வ பெயர் மாற்றத்திற்கும் வரலாற்று எழுத்துப் பிழைக்கும் உள்ள வேறுபாடு என்ன?'
          : 'What is the difference between an official renaming and a spelling variant?',
    },
  ];

  const handleSend = async (questionToSend) => {
    const q = (questionToSend || inputVal).trim();
    if (!q || loading) return;

    // Add user message
    const newChat = [...chatHistory, { role: 'user', text: q }];
    setChatHistory(newChat);
    setInputVal('');
    setLoading(true);

    try {
      const response = await askAI(q, lang);
      setChatHistory([
        ...newChat,
        {
          role: 'assistant',
          text: response.answer,
          sources: response.sources_used || [],
          places: response.places_found || [],
          aiGenerated: response.ai_generated,
          fallback: response.fallback,
        },
      ]);
    } catch (err) {
      console.error('Error asking AI:', err);
      setChatHistory([
        ...newChat,
        {
          role: 'assistant',
          text:
            lang === 'ta'
              ? 'மன்னிக்கவும், வரலாற்றுத் தரவுகளைப் பெறுவதில் பிழை ஏற்பட்டது. தயவுசெய்து சிறிது நேரம் கழித்து மீண்டும் முயற்சிக்கவும்.'
              : 'Sorry, an error occurred while querying historical records. Please check if the backend server is running.',
          sources: [],
          places: [],
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto py-2">
      {/* Header */}
      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm space-y-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#C5A66A] text-[#172B40] flex items-center justify-center font-bold">
            <Bot className="w-5 h-5 text-[#172B40]" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-[#172B40]">
              {t('ask.title', 'Ask History AI')}
            </h2>
            <p className="text-xs sm:text-sm text-gray-500">
              {lang === 'ta'
                ? 'அரசு ஆவணங்கள் மற்றும் சான்றுகளின் அடிப்படையில் கேட்கப்படும் கேள்விகளுக்குப் பதில்கள்.'
                : 'Evidence-grounded historical Q&A with Gemini and primary database citations.'}
            </p>
          </div>
        </div>

        {/* Suggestion Chips */}
        <div className="pt-2">
          <span className="text-xs font-semibold text-gray-500 block mb-2">
            {lang === 'ta' ? 'மாதிரி வினாக்கள்:' : 'Suggested Questions:'}
          </span>
          <div className="flex flex-wrap gap-2">
            {suggestions.map((item, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSend(item.q)}
                disabled={loading}
                className="text-left px-3 py-1.5 rounded-lg bg-[#F7F4ED] hover:bg-[#C5A66A]/20 text-[#172B40] text-xs font-medium border border-gray-200 transition-colors"
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Chat Messages Container */}
      <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-4 sm:p-6 space-y-6 min-h-[380px]">
        {chatHistory.map((msg, index) => (
          <div
            key={index}
            className={`flex gap-3 sm:gap-4 ${
              msg.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {msg.role === 'assistant' && (
              <div className="w-8 h-8 rounded-lg bg-[#172B40] text-white flex items-center justify-center shrink-0 mt-1 shadow-xs">
                <Bot className="w-4 h-4 text-[#C5A66A]" />
              </div>
            )}

            <div
              className={`max-w-2xl rounded-2xl p-4 sm:p-5 text-sm leading-relaxed space-y-3 ${
                msg.role === 'user'
                  ? 'bg-[#172B40] text-white rounded-tr-none'
                  : 'bg-[#F7F4ED] text-[#172B40] border border-gray-200 rounded-tl-none'
              }`}
            >
              <div className="whitespace-pre-line font-normal text-xs sm:text-sm">
                {msg.text}
              </div>

              {/* Status pill for AI vs Database Grounding */}
              {msg.role === 'assistant' && !msg.isInitial && (
                <div className="pt-2 flex items-center gap-2 flex-wrap text-[11px] border-t border-gray-200/80">
                  {msg.aiGenerated ? (
                    <span className="inline-flex items-center gap-1 text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 font-semibold">
                      <Sparkles className="w-3 h-3 text-emerald-600" />
                      <span>{lang === 'ta' ? 'Gemini AI சான்றாய்வு பதில்' : 'Gemini AI Grounded Answer'}</span>
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-blue-800 bg-blue-50 px-2 py-0.5 rounded border border-blue-200 font-semibold">
                      <Database className="w-3 h-3 text-blue-600" />
                      <span>{lang === 'ta' ? 'நேரடி ஆவணத் தகவல் (Fallback)' : 'Database Archive Grounded Answer'}</span>
                    </span>
                  )}
                </div>
              )}

              {/* Sources citations attached to answer */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="pt-2 border-t border-gray-200 space-y-1.5">
                  <div className="text-[11px] font-bold text-gray-700 flex items-center gap-1">
                    <BookOpen className="w-3.5 h-3.5 text-[#C5A66A]" />
                    <span>{t('ask.sourcesUsed', 'Verified Archival Citations:')}</span>
                  </div>
                  <div className="space-y-1">
                    {msg.sources.map((src) => (
                      <div
                        key={src.id}
                        className="bg-white p-2.5 rounded-lg border border-gray-200 text-xs flex items-center justify-between gap-2"
                      >
                        <div>
                          <span className="font-semibold text-[#172B40]">
                            {lang === 'ta' && src.title_tamil ? src.title_tamil : src.title}
                          </span>
                          {src.document_identifier && (
                            <span className="ml-2 text-[10px] text-gray-500 font-mono">
                              ({src.document_identifier})
                            </span>
                          )}
                        </div>
                        {src.source_url && (
                          <a
                            href={src.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 inline-flex items-center gap-1 shrink-0 font-medium text-[11px]"
                          >
                            <span>{lang === 'ta' ? 'ஆதாரம்' : 'View Source'}</span>
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {msg.role === 'user' && (
              <div className="w-8 h-8 rounded-lg bg-[#C5A66A] text-[#172B40] flex items-center justify-center shrink-0 mt-1 shadow-xs">
                <User className="w-4 h-4 font-bold" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 items-center text-gray-500 text-xs pl-2">
            <div className="w-7 h-7 rounded-lg bg-[#172B40] text-white flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4 text-[#C5A66A] animate-pulse" />
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-[#C5A66A] animate-bounce"></div>
              <div className="w-2 h-2 rounded-full bg-[#C5A66A] animate-bounce [animation-delay:0.2s]"></div>
              <div className="w-2 h-2 rounded-full bg-[#C5A66A] animate-bounce [animation-delay:0.4s]"></div>
              <span className="ml-1 font-medium">
                {lang === 'ta' ? 'வரலாற்று ஆவணங்களை ஆய்வு செய்கிறது...' : 'Analyzing historical evidence...'}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Input Field */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="flex items-center gap-2 bg-white rounded-xl p-2 border border-gray-300 shadow-sm focus-within:border-[#C5A66A] focus-within:ring-2 focus-within:ring-[#C5A66A]/20 transition-all"
      >
        <input
          type="text"
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          placeholder={t('ask.placeholder', 'Ask a historical place question in Tamil or English...')}
          disabled={loading}
          className="w-full px-3 py-2 text-sm text-[#172B40] placeholder-gray-400 focus:outline-none bg-transparent"
        />
        <button
          type="submit"
          disabled={loading || !inputVal.trim()}
          className="bg-[#172B40] hover:bg-[#20364F] disabled:opacity-50 text-white font-semibold text-xs sm:text-sm px-5 py-2.5 rounded-lg flex items-center gap-1.5 transition-colors shadow-sm shrink-0"
        >
          <span>{t('ask.send', 'Ask')}</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
};

export default AskAI;
