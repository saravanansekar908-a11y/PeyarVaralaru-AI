import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useTranslation } from '../services/LanguageContext';
import { getPlace, getPlaces, searchPassages, askAI } from '../services/api';
import StatusBadge from '../components/StatusBadge';
import { 
  MapPin, 
  Clock, 
  BookOpen, 
  ExternalLink, 
  Network, 
  Calendar, 
  CheckCircle2, 
  AlertCircle, 
  ArrowLeft,
  FileText,
  Bookmark,
  Building,
  HelpCircle,
  AlertTriangle,
  Bot,
  Sparkles,
  Send,
  Navigation,
  Globe2,
  Compass,
  ArrowRight,
  Map
} from 'lucide-react';

export const PlaceDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { lang, t } = useTranslation();

  const [place, setPlace] = useState(null);
  const [allPlaces, setAllPlaces] = useState([]);
  const [passages, setPassages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Active Tab: 'history' | 'meaning' | 'sources' | 'connections' | 'ai_insights'
  const [activeTab, setActiveTab] = useState('history');

  // AI Insights chat state scoped to this place
  const [customQuestion, setCustomQuestion] = useState('');
  const [aiAnswer, setAiAnswer] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);

  // Curated images for places
  const getPlaceHeroImage = (p) => {
    if (!p) return '/images/hero-temple.jpg';
    const name = (p.current_name || '').toLowerCase();
    if (name.includes('thanjavur')) return '/images/thanjavur.jpg';
    if (name.includes('tiruvannamalai')) return '/images/tiruvannamalai.jpg';
    if (name.includes('madurai')) return '/images/madurai.jpg';
    if (name.includes('mamallapuram') || name.includes('mahabalipuram')) return '/images/mamallapuram.jpg';
    return '/images/hero-temple.jpg';
  };

  useEffect(() => {
    const loadAll = async () => {
      try {
        const placesList = await getPlaces();
        setAllPlaces(placesList);
      } catch (err) {
        console.error('Failed to load places list:', err);
      }
    };
    loadAll();
  }, []);

  useEffect(() => {
    const fetchDetail = async () => {
      setLoading(true);
      setError(null);
      setAiAnswer(null);
      try {
        const data = await getPlace(id || 1);
        setPlace(data);

        // Fetch primary research passages from gazetteers and epigraphy
        if (data?.current_name) {
          const passData = await searchPassages(data.current_name, data.district).catch(() => []);
          setPassages(passData || []);
        }
      } catch (err) {
        console.error('Failed to load place details:', err);
        setError('Failed to load historical place profile.');
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [id]);

  const handleAskPlaceAI = async (queryText) => {
    const q = queryText || customQuestion;
    if (!q.trim() || !place) return;
    setAiLoading(true);
    setAiAnswer(null);
    try {
      const res = await askAI(q, lang, place.district);
      setAiAnswer(res);
    } catch (err) {
      console.error('AI ask error:', err);
    } finally {
      setAiLoading(false);
    }
  };

  const getEvidenceBadge = (status) => {
    switch (status) {
      case 'verified':
      case 'historically_documented':
      case 'documented_fact':
        return (
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-900 border border-emerald-300">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" />
            {lang === 'ta' ? 'சான்றாதார உண்மை' : 'Documented Fact'}
          </span>
        );
      case 'partially_verified':
      case 'scholarly_hypothesis':
      case 'scholarly_interpretation':
        return (
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-700" />
            {lang === 'ta' ? 'அறிஞர் கருதுகோள்' : 'Scholarly Hypothesis'}
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-900 border border-rose-300">
            <HelpCircle className="w-3.5 h-3.5 text-rose-700" />
            {lang === 'ta' ? 'வாய்மொழி மரபு' : 'Folk Tradition'}
          </span>
        );
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-2xl p-16 border border-gray-200 text-center space-y-4 max-w-xl mx-auto my-12 shadow-sm">
        <div className="inline-block animate-spin w-8 h-8 border-3 border-[#172B40] border-t-transparent rounded-full" />
        <p className="text-sm font-semibold text-[#172B40]">
          {lang === 'ta' ? 'வரலாற்று ஆவணங்களை ஏற்றுகிறது...' : 'Loading place records and archival citations...'}
        </p>
      </div>
    );
  }

  if (error || !place) {
    return (
      <div className="bg-white rounded-2xl p-10 border border-gray-200 text-center space-y-4 max-w-xl mx-auto my-10 shadow-sm">
        <AlertCircle className="w-10 h-10 text-rose-500 mx-auto" />
        <h3 className="text-lg font-bold text-[#172B40]">
          {error || (lang === 'ta' ? 'இட விவரங்கள் கிடைக்கவில்லை' : 'Place record not found')}
        </h3>
        <button
          onClick={() => navigate('/search')}
          className="px-4 py-2 bg-[#172B40] text-white text-xs font-bold rounded-lg hover:bg-[#20364F]"
        >
          {lang === 'ta' ? 'தேடல் பக்கத்திற்குச் செல்க' : 'Back to Search'}
        </button>
      </div>
    );
  }

  // Related places: places from same district or other popular places
  const relatedPlaces = allPlaces
    .filter((p) => p.id !== place.id)
    .slice(0, 3);

  return (
    <div className="space-y-6 max-w-5xl mx-auto py-2">
      {/* Top Bar with Navigation & Place Quick Switcher */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-3.5 rounded-xl border border-gray-200 shadow-sm">
        <Link
          to="/search"
          className="inline-flex items-center gap-1.5 text-xs font-bold text-[#172B40] hover:text-[#C5A66A] transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>{lang === 'ta' ? 'தேடல் முடிவுகளுக்குத் திரும்பு' : 'Back to Search Results'}</span>
        </Link>

        {/* Place Quick Selector */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0">
          <span className="text-xs font-medium text-gray-500 shrink-0">
            {lang === 'ta' ? 'வேறு இடம்:' : 'Switch place:'}
          </span>
          <div className="flex gap-1.5">
            {allPlaces.map((p) => (
              <button
                key={p.id}
                onClick={() => navigate(`/places/${p.id}`)}
                className={`px-2.5 py-1 rounded-md text-xs font-medium transition-colors shrink-0 ${
                  String(p.id) === String(place.id)
                    ? 'bg-[#172B40] text-white shadow-sm'
                    : 'bg-[#F7F4ED] text-[#172B40] hover:bg-[#eae5d7]'
                }`}
              >
                {lang === 'ta' && p.current_name_tamil ? p.current_name_tamil : p.current_name}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Hero Banner with Photographic Heritage Visual */}
      <div className="relative rounded-3xl overflow-hidden shadow-lg border border-[#2A3E54] min-h-[300px] flex items-end">
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: `url('${getPlaceHeroImage(place)}')` }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#0F1D2C] via-[#172B40]/70 to-black/30" />

        <div className="relative z-10 p-6 sm:p-8 w-full text-white space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div className="flex flex-wrap items-center gap-2">
              <span className="px-3 py-1 rounded-full bg-[#C5A66A] text-[#172B40] text-xs font-extrabold shadow-sm">
                {lang === 'ta' && place.category_tamil ? place.category_tamil : place.category}
              </span>
              {getEvidenceBadge(place.origin_evidence_status || place.evidence_status)}
            </div>

            <span className="text-xs font-semibold text-gray-300 bg-black/40 px-3 py-1 rounded-md backdrop-blur-sm">
              {place.historical_period || 'Ancient to Modern Era'}
            </span>
          </div>

          <div className="space-y-1">
            <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              {lang === 'ta' ? (place.current_name_tamil || place.current_name) : place.current_name}
            </h1>
            <p className="text-sm sm:text-base text-gray-200 font-medium">
              {lang === 'ta' ? (place.category_tamil || place.category) : place.category}
            </p>
          </div>

          {/* Location Hierarchy Tag Bar */}
          <div className="flex flex-wrap items-center gap-2 text-xs pt-1">
            <div className="flex items-center gap-1 bg-white/20 backdrop-blur-md px-3 py-1 rounded-md font-medium">
              <Compass className="w-3.5 h-3.5 text-[#C5A66A]" />
              <span>{lang === 'ta' ? 'மாநிலம்: தமிழ்நாடு' : 'State: Tamil Nadu'}</span>
            </div>
            <div className="flex items-center gap-1 bg-white/20 backdrop-blur-md px-3 py-1 rounded-md font-semibold">
              <MapPin className="w-3.5 h-3.5 text-[#C5A66A]" />
              <span>{lang === 'ta' ? 'மாவட்டம்:' : 'District:'} {lang === 'ta' ? (place.district_tamil || place.district || '-') : (place.district || '-')}</span>
            </div>
            {place.taluk && (
              <div className="bg-white/20 backdrop-blur-md px-3 py-1 rounded-md font-medium">
                <span>{lang === 'ta' ? 'வட்டம்:' : 'Taluk:'} {lang === 'ta' ? (place.taluk_tamil || place.taluk) : place.taluk}</span>
              </div>
            )}
            {place.village && (
              <div className="bg-white/20 backdrop-blur-md px-3 py-1 rounded-md font-medium">
                <span>{lang === 'ta' ? 'பழைய கிராமம்:' : 'Old Settlement:'} {lang === 'ta' ? (place.village_tamil || place.village) : place.village}</span>
              </div>
            )}
            <Link
              to={`/maps?place=${encodeURIComponent(place.current_name || '')}&district=${encodeURIComponent(place.district || '')}`}
              className="inline-flex items-center gap-1.5 bg-[#C5A66A] text-[#172B40] hover:bg-[#d6ba80] px-3 py-1 rounded-md font-bold text-xs shadow-sm transition-all ml-auto"
            >
              <Map className="w-3.5 h-3.5" />
              <span>{lang === 'ta' ? 'வரலாற்று வரைபடத்தில் பார்க்க' : 'View on Historical Map'}</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Tabs Navigation Bar */}
      <div className="bg-white rounded-xl border border-gray-200 p-1.5 shadow-sm flex flex-wrap gap-1">
        <button
          onClick={() => setActiveTab('history')}
          className={`flex-1 min-w-[110px] py-2.5 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
            activeTab === 'history'
              ? 'bg-[#172B40] text-[#C5A66A] shadow-sm'
              : 'text-[#172B40] hover:bg-gray-100'
          }`}
        >
          <Clock className="w-3.5 h-3.5" />
          <span>{lang === 'ta' ? 'வரலாறு' : 'History'}</span>
        </button>

        <button
          onClick={() => setActiveTab('meaning')}
          className={`flex-1 min-w-[110px] py-2.5 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
            activeTab === 'meaning'
              ? 'bg-[#172B40] text-[#C5A66A] shadow-sm'
              : 'text-[#172B40] hover:bg-gray-100'
          }`}
        >
          <BookOpen className="w-3.5 h-3.5" />
          <span>{lang === 'ta' ? 'பொருள் & தோற்றம்' : 'Meaning & Etymology'}</span>
        </button>

        <button
          onClick={() => setActiveTab('sources')}
          className={`flex-1 min-w-[110px] py-2.5 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
            activeTab === 'sources'
              ? 'bg-[#172B40] text-[#C5A66A] shadow-sm'
              : 'text-[#172B40] hover:bg-gray-100'
          }`}
        >
          <FileText className="w-3.5 h-3.5" />
          <span>{lang === 'ta' ? 'ஆதாரங்கள்' : 'Sources'}</span>
        </button>

        <button
          onClick={() => setActiveTab('connections')}
          className={`flex-1 min-w-[110px] py-2.5 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
            activeTab === 'connections'
              ? 'bg-[#172B40] text-[#C5A66A] shadow-sm'
              : 'text-[#172B40] hover:bg-gray-100'
          }`}
        >
          <Network className="w-3.5 h-3.5" />
          <span>{lang === 'ta' ? 'தொடர்புகள்' : 'Connections'}</span>
        </button>

        <button
          onClick={() => setActiveTab('ai_insights')}
          className={`flex-1 min-w-[110px] py-2.5 px-3 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
            activeTab === 'ai_insights'
              ? 'bg-[#172B40] text-[#C5A66A] shadow-sm'
              : 'text-[#172B40] hover:bg-gray-100'
          }`}
        >
          <Bot className="w-3.5 h-3.5" />
          <span>{lang === 'ta' ? 'AI நுண்ணறிவு' : 'AI Insights'}</span>
        </button>
      </div>

      {/* Tab 1: வரலாறு (History) */}
      {activeTab === 'history' && (
        <div className="space-y-6">
          {/* Historical Summary Card */}
          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-[#172B40] flex items-center gap-2">
              <Clock className="w-4 h-4 text-[#C5A66A]" />
              <span>{lang === 'ta' ? 'வரலாற்றுச் சுருக்கம்' : 'Historical Summary'}</span>
            </h3>
            <p className="text-xs sm:text-sm text-gray-700 leading-relaxed">
              {lang === 'ta' && place.description_tamil ? place.description_tamil : place.description}
            </p>
            {place.historical_events_summary && (
              <div className="p-3.5 rounded-xl bg-[#F7F4ED] border border-gray-200 text-xs text-[#172B40] leading-relaxed">
                <span className="font-bold text-[#C5A66A] block mb-1">
                  {lang === 'ta' ? 'முக்கிய வரலாற்று மைல்கற்கள்:' : 'Key Milestones:'}
                </span>
                {place.historical_events_summary}
              </div>
            )}
          </div>

          {/* Chronological Events Timeline */}
          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-[#172B40] flex items-center justify-between">
              <span className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-[#C5A66A]" />
                {lang === 'ta' ? 'ஆவணப்படுத்தப்பட்ட வரலாற்று நிகழ்வுகள்' : 'Documented Historical Timeline'}
              </span>
              <span className="text-xs text-gray-500 font-normal">
                {place.events ? place.events.length : 0} {lang === 'ta' ? 'நிகழ்வுகள்' : 'events'}
              </span>
            </h3>

            {place.events && place.events.length > 0 ? (
              <div className="relative border-l-2 border-[#C5A66A]/40 ml-3 pl-5 space-y-5">
                {place.events.map((evt, idx) => (
                  <div key={evt.id || idx} className="relative group">
                    <div className="absolute -left-[27px] top-1.5 w-3.5 h-3.5 rounded-full bg-[#172B40] border-2 border-[#C5A66A]" />
                    <div className="bg-[#F7F4ED] p-4 rounded-xl border border-gray-200 space-y-2">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <span className="text-xs font-bold text-[#172B40] bg-white px-2 py-0.5 rounded border border-gray-200">
                          {evt.event_date || (lang === 'ta' ? 'காலம் குறிப்பிடப்படவில்லை' : 'Undated')}
                        </span>
                        {getEvidenceBadge(evt.evidence_status)}
                      </div>
                      <p className="text-xs sm:text-sm text-gray-700 leading-relaxed font-medium">
                        {lang === 'ta' && evt.description_tamil ? evt.description_tamil : evt.description}
                      </p>
                      {evt.sources && evt.sources.length > 0 && (
                        <div className="text-[11px] text-gray-500 pt-1 flex items-center gap-1 italic">
                          <BookOpen className="w-3 h-3 text-[#C5A66A]" />
                          <span>{evt.sources[0].title}</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-gray-500 italic">
                {lang === 'ta' ? 'நிகழ்வுகள் ஆவணப்படுத்தப்படவில்லை.' : 'No timeline events recorded yet.'}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Tab 2: பொருள் & தோற்றம் (Meaning & Etymology) */}
      {activeTab === 'meaning' && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm space-y-5">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-gray-100 pb-3">
              <h3 className="text-base font-bold text-[#172B40] flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-[#C5A66A]" />
                <span>{lang === 'ta' ? 'பெயர்த் தோற்ற விளக்கம்' : 'Name Origin & Etymology'}</span>
              </h3>
              {getEvidenceBadge(place.origin_evidence_status || place.evidence_status)}
            </div>

            {/* Direct Structured Name Origin Explanation */}
            <div className="p-4 rounded-xl bg-[#F7F4ED] border border-gray-200 space-y-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-[#C5A66A]">
                {lang === 'ta' ? 'ஆவணப்படுத்தப்பட்ட விளக்கம்' : 'Documented Explanation'}
              </h4>
              <p className="text-xs sm:text-sm text-[#172B40] leading-relaxed font-medium">
                {place.name_origin_explanation || place.meaning_tamil || place.origin_tamil}
              </p>
            </div>

            {/* Inscriptional Evidence Quote */}
            {place.evidence_quote && (
              <div className="p-4 rounded-xl bg-blue-50/50 border border-blue-200 space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold text-blue-900">
                  <Bookmark className="w-3.5 h-3.5 text-blue-600" />
                  <span>{lang === 'ta' ? 'கல்வெட்டு / அரசிதழ் நேரடி மேற்கோள்:' : 'Direct Inscriptional / Archival Quote:'}</span>
                </div>
                <blockquote className="text-xs sm:text-sm text-blue-950 italic border-l-2 border-blue-400 pl-3 leading-relaxed">
                  "{place.evidence_quote}"
                </blockquote>
              </div>
            )}

            {/* Historical Names List */}
            {place.historical_names && place.historical_names.length > 0 && (
              <div className="space-y-2 pt-2">
                <h4 className="text-xs font-bold text-[#172B40] uppercase tracking-wider">
                  {lang === 'ta' ? 'வரலாற்றுப் பெயர்கள் மற்றும் எழுத்துப் பிழைகள்' : 'Historical Name Variants'}
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {place.historical_names.map((hn, idx) => (
                    <div
                      key={hn.id || idx}
                      className="p-3 rounded-xl bg-[#F7F4ED] border border-gray-200 flex items-center justify-between"
                    >
                      <div>
                        <div className="font-bold text-xs text-[#172B40]">{hn.name}</div>
                        <div className="text-[10px] text-gray-500 font-medium">
                          {hn.language} • {hn.name_type || 'Variant'}
                        </div>
                      </div>
                      {(hn.valid_from || hn.valid_to) && (
                        <span className="text-[10px] bg-white px-2 py-0.5 rounded border border-gray-200 text-gray-600 font-semibold">
                          {hn.valid_from || ''} - {hn.valid_to || ''}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tab 3: ஆதாரங்கள் (Sources & Documents) */}
      {activeTab === 'sources' && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-[#172B40] flex items-center gap-2">
              <FileText className="w-4 h-4 text-[#C5A66A]" />
              <span>{lang === 'ta' ? 'அதிகாரப்பூர்வ மூல ஆவணங்கள்' : 'Primary Research Sources & Gazetteers'}</span>
            </h3>

            {/* Direct primary source badge */}
            {place.source_title && (
              <div className="p-4 rounded-xl bg-[#F7F4ED] border border-gray-200 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-[#172B40]">{place.source_title}</span>
                  <span className="text-[11px] font-semibold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded">
                    {place.source_page || 'Archival Record'}
                  </span>
                </div>
                {place.source_url && (
                  <a
                    href={place.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-xs text-[#C5A66A] hover:underline font-semibold"
                  >
                    <span>{lang === 'ta' ? 'அசல் ஆவணத்தைக் காண்க' : 'Access Original Archive'}</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            )}

            {/* Ingested Passages List */}
            {passages && passages.length > 0 ? (
              <div className="space-y-3 pt-2">
                <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider">
                  {lang === 'ta' ? 'ஆவணப் பத்திகள் (Archival Passages)' : 'Extracted Research Passages'}
                </h4>
                {passages.map((p, idx) => (
                  <div key={p.id || idx} className="p-4 rounded-xl bg-white border border-gray-200 shadow-sm space-y-2">
                    <div className="flex flex-wrap items-center justify-between gap-1">
                      <span className="font-bold text-xs text-[#172B40]">{p.document_title}</span>
                      <span className="text-[10px] text-gray-500 font-medium">
                        {p.author_or_authority} ({p.publication_year}) • பக். {p.page_number}
                      </span>
                    </div>
                    <p className="text-xs text-gray-700 leading-relaxed italic bg-[#F7F4ED] p-3 rounded-lg border border-gray-100">
                      "{p.passage_text_tamil || p.passage_text}"
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-gray-500 italic">
                {lang === 'ta' ? 'மேலும் விரிவான பத்திகள் சேர்க்கப்பட்டு வருகின்றன.' : 'Passages catalogued in Tamil Nadu archives.'}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Tab 4: தொடர்புகள் (Connections & Graph) */}
      {activeTab === 'connections' && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-100 pb-3">
              <div>
                <h3 className="text-base font-bold text-[#172B40] flex items-center gap-2">
                  <Network className="w-4 h-4 text-[#C5A66A]" />
                  <span>{lang === 'ta' ? 'இடப்பெயர் தொடர்பு வரைபடம்' : 'Place Relationship Network'}</span>
                </h3>
                <p className="text-xs text-gray-500">
                  {lang === 'ta'
                    ? 'இடம், பழைய பெயர்கள், வரலாற்று நிகழ்வுகள் மற்றும் மூல ஆவணங்களுக்கிடையேயான தொடர்புகள்'
                    : 'Interactive graph connecting this place to its historical names, events, and citations.'}
                </p>
              </div>

              <Link
                to={`/graph?place=${place.id}`}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-[#172B40] text-white hover:bg-[#20364F] rounded-lg text-xs font-semibold transition-colors shrink-0"
              >
                <span>{lang === 'ta' ? 'முழு வரைபடப் பக்கம்' : 'Open Full Graph'}</span>
                <ExternalLink className="w-3.5 h-3.5 text-[#C5A66A]" />
              </Link>
            </div>

            {/* Quick Relationship Node Overview */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="bg-[#F7F4ED] p-4 rounded-xl border border-gray-200 space-y-1">
                <span className="text-[11px] font-bold text-[#C5A66A] uppercase tracking-wider">
                  {lang === 'ta' ? 'வரலாற்றுப் பெயர்கள்' : 'Historical Names'}
                </span>
                <div className="text-2xl font-extrabold text-[#172B40]">
                  {place.historical_names ? place.historical_names.length : 0}
                </div>
              </div>

              <div className="bg-[#F7F4ED] p-4 rounded-xl border border-gray-200 space-y-1">
                <span className="text-[11px] font-bold text-[#C5A66A] uppercase tracking-wider">
                  {lang === 'ta' ? 'வரலாற்று நிகழ்வுகள்' : 'Historical Events'}
                </span>
                <div className="text-2xl font-extrabold text-[#172B40]">
                  {place.events ? place.events.length : 0}
                </div>
              </div>

              <div className="bg-[#F7F4ED] p-4 rounded-xl border border-gray-200 space-y-1">
                <span className="text-[11px] font-bold text-[#C5A66A] uppercase tracking-wider">
                  {lang === 'ta' ? 'மூல ஆவணங்கள்' : 'Cited Sources'}
                </span>
                <div className="text-2xl font-extrabold text-[#172B40]">
                  {passages ? passages.length + 1 : 1}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 5: AI நுண்ணறிவு (AI Insights) */}
      {activeTab === 'ai_insights' && (
        <div className="space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm space-y-4">
            <div className="flex items-center gap-2 border-b border-gray-100 pb-3">
              <Sparkles className="w-5 h-5 text-[#C5A66A]" />
              <div>
                <h3 className="text-base font-bold text-[#172B40]">
                  {lang === 'ta' ? 'சான்றாதார AI வரலாற்று விளக்கம்' : 'Source-Grounded AI Analysis'}
                </h3>
                <p className="text-xs text-gray-500">
                  {lang === 'ta'
                    ? 'தமிழ்நாடு அரசிதழ்கள் மற்றும் கல்வெட்டு ஆதாரங்கள் அடிப்படையில் உருவாக்கப்பட்ட விளக்கம்'
                    : 'Grounded in SQLite archival records, clearly distinguishing facts from traditions.'}
                </p>
              </div>
            </div>

            {/* Suggested Scoped Questions */}
            <div className="space-y-2">
              <span className="text-xs font-bold text-gray-600">
                {lang === 'ta' ? 'பரிந்துரைக்கப்பட்ட கேள்விகள்:' : 'Suggested questions for this place:'}
              </span>
              <div className="flex flex-wrap gap-2">
                {[
                  `${place.current_name_tamil || place.current_name} பெயர்க் காரணம் என்ன?`,
                  `${place.current_name} பழைய பெயர்கள் மற்றும் கல்வெட்டு சான்றுகள் யாவை?`,
                  `${place.district} மாவட்ட அரசிதழ் என்ன கூறுகிறது?`
                ].map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleAskPlaceAI(q)}
                    className="px-3 py-1.5 rounded-lg bg-[#F7F4ED] hover:bg-[#eae5d8] text-[#172B40] text-xs font-semibold border border-gray-200 transition-colors text-left"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>

            {/* Custom Question Composer */}
            <div className="flex gap-2 pt-2">
              <input
                type="text"
                value={customQuestion}
                onChange={(e) => setCustomQuestion(e.target.value)}
                placeholder={
                  lang === 'ta'
                    ? `${place.current_name_tamil || place.current_name} குறித்து கேள்வி கேளுங்கள்...`
                    : `Ask anything about ${place.current_name}...`
                }
                className="flex-1 px-3 py-2 text-xs bg-white border border-gray-200 rounded-lg text-[#172B40] focus:outline-none focus:ring-1 focus:ring-[#C5A66A]"
              />
              <button
                onClick={() => handleAskPlaceAI()}
                disabled={aiLoading}
                className="px-4 py-2 bg-[#172B40] hover:bg-[#20364F] text-white text-xs font-bold rounded-lg transition-colors flex items-center gap-1.5 shrink-0"
              >
                {aiLoading ? (
                  <div className="animate-spin w-3.5 h-3.5 border-2 border-[#C5A66A] border-t-transparent rounded-full" />
                ) : (
                  <Send className="w-3.5 h-3.5 text-[#C5A66A]" />
                )}
                <span>{lang === 'ta' ? 'கேட்க' : 'Ask'}</span>
              </button>
            </div>

            {/* AI Answer Box */}
            {aiAnswer && (
              <div className="p-5 rounded-2xl bg-[#F7F4ED] border border-[#C5A66A] shadow-sm space-y-3 mt-4">
                <div className="flex items-center justify-between border-b border-gray-200/80 pb-2">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-[#172B40]">
                    <Bot className="w-4 h-4 text-[#C5A66A]" />
                    <span>{lang === 'ta' ? 'AI வரலாற்றுப் பதில்' : 'AI Grounded Response'}</span>
                  </div>
                  {getEvidenceBadge(aiAnswer.evidence_status || 'verified')}
                </div>
                <div className="text-xs sm:text-sm text-[#172B40] leading-relaxed whitespace-pre-line font-medium">
                  {aiAnswer.answer}
                </div>
                {aiAnswer.sources_used && aiAnswer.sources_used.length > 0 && (
                  <div className="pt-2 border-t border-gray-200/80 text-[11px] text-gray-600">
                    <span className="font-bold mr-1">{lang === 'ta' ? 'சான்றுகள்:' : 'Sources:'}</span>
                    {aiAnswer.sources_used.map((s, idx) => (
                      <span key={idx} className="mr-2 font-medium">
                        {s.title} ({s.publication_year || ''})
                      </span>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Map & Coordinates Card */}
      <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-[#172B40] flex items-center gap-2">
            <Navigation className="w-4 h-4 text-[#C5A66A]" />
            <span>{lang === 'ta' ? 'புவியியல் அமைவிடம் & வரைபடம்' : 'Geographic Location & Map'}</span>
          </h3>
          <span className="text-xs font-semibold text-gray-500 bg-[#F7F4ED] px-2.5 py-1 rounded border border-gray-200">
            {place.latitude || 13.0827}° N, {place.longitude || 80.2707}° E
          </span>
        </div>

        {/* Visual Map Representation */}
        <div className="relative h-48 bg-[#0F1D2C] rounded-xl overflow-hidden border border-[#2A3E54] flex items-center justify-center text-center p-4">
          <div className="absolute inset-0 opacity-20 bg-[radial-gradient(#C5A66A_1px,transparent_1px)] [background-size:16px_16px]" />
          <div className="relative z-10 space-y-2">
            <div className="w-10 h-10 rounded-full bg-[#C5A66A] text-[#172B40] flex items-center justify-center mx-auto shadow-lg animate-bounce">
              <MapPin className="w-5 h-5 font-bold" />
            </div>
            <div className="font-extrabold text-white text-sm">
              {lang === 'ta' ? (place.current_name_tamil || place.current_name) : place.current_name}
            </div>
            <div className="text-xs text-gray-300">
              {lang === 'ta' ? `${place.district_tamil || place.district || ''} மாவட்டம், தமிழ்நாடு` : `${place.district || ''} District, Tamil Nadu`}
            </div>
          </div>
        </div>
      </div>

      {/* Related Places */}
      {relatedPlaces.length > 0 && (
        <div className="space-y-4 pt-2">
          <h3 className="text-base font-bold text-[#172B40]">
            {lang === 'ta' ? 'தொடர்புடைய வரலாற்று இடங்கள்' : 'Related Historical Places'}
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {relatedPlaces.map((rp) => (
              <Link
                key={rp.id}
                to={`/places/${rp.id}`}
                className="bg-white p-4 rounded-xl border border-gray-200 hover:border-[#C5A66A] hover:shadow-md transition-all space-y-2 flex flex-col justify-between"
              >
                <div>
                  <div className="font-bold text-sm text-[#172B40]">
                    {lang === 'ta' ? (rp.current_name_tamil || rp.current_name) : rp.current_name}
                  </div>
                  <div className="text-xs text-[#C5A66A] font-semibold">
                    {lang === 'ta' ? (rp.district_tamil || rp.district) : rp.district}
                  </div>
                  <p className="text-xs text-gray-600 line-clamp-2 mt-1 leading-relaxed">
                    {lang === 'ta' ? (rp.description_tamil || rp.description) : rp.description}
                  </p>
                </div>
                <div className="pt-2 text-xs font-bold text-[#172B40] flex items-center gap-1">
                  <span>{lang === 'ta' ? 'விவரங்கள்' : 'Details'}</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PlaceDetails;
