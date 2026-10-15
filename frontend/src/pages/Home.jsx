import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useTranslation } from '../services/LanguageContext';
import { getPlaces } from '../services/api';
import StatusBadge from '../components/StatusBadge';
import { 
  Search, 
  Clock, 
  Bot, 
  Network, 
  BookOpen, 
  CheckCircle2, 
  AlertTriangle, 
  HelpCircle,
  ArrowRight,
  MapPin,
  Sparkles
} from 'lucide-react';

export const Home = () => {
  const { lang, t } = useTranslation();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const data = await getPlaces();
        setPlaces(data);
      } catch (err) {
        console.error('Failed to load places:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchPlaces();
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    } else {
      navigate('/search');
    }
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto py-2">
      {/* Hero Section */}
      <div className="bg-[#172B40] text-white rounded-2xl p-8 sm:p-10 shadow-lg border border-[#2A3E54] relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-96 bg-[#C5A66A]/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="max-w-2xl relative z-10 space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#C5A66A]/20 border border-[#C5A66A]/40 text-[#C5A66A] text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>
              {lang === 'ta'
                ? 'தமிழ்நாடு வரலாற்று இடப்பெயர் ஆய்வுத் தளம்'
                : 'Tamil Nadu Historical Place Names Explorer'}
            </span>
          </div>

          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
            {lang === 'ta'
              ? 'வரலாற்றில் நமது ஊர்ப் பெயர்களின் பரிணாமம்'
              : 'Discover How Tamil Nadu Place Names Evolved Through History'}
          </h2>

          <p className="text-sm sm:text-base text-gray-300 leading-relaxed">
            {lang === 'ta'
              ? 'பழைய வரைபடங்கள், கல்வெட்டுகள், அரசு ஆணைகள் மற்றும் வரலாற்று ஆவணங்கள் மூலம் ஊர்ப் பெயர்களின் மாற்றங்களைச் சான்றுகளுடன் ஆராயுங்கள்.'
              : 'Explore historical place names, official renamings, and spelling variants recorded in old maps, gazetteers, government orders, and inscriptions with verifiable citations.'}
          </p>

          {/* Prominent Search Field */}
          <form onSubmit={handleSearchSubmit} className="pt-2">
            <div className="flex items-center bg-white rounded-xl p-1.5 shadow-md border border-gray-200">
              <Search className="w-5 h-5 text-gray-400 ml-3 mr-2 shrink-0" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={
                  lang === 'ta'
                    ? 'ஊர்ப் பெயரைத் தேடுங்கள்... (எ.கா: Madras, மெட்ராஸ், சென்னை, George Town)'
                    : 'Search place name... (e.g., Madras, Black Town, Trichinopoly)'
                }
                className="w-full px-2 py-2 text-sm text-[#172B40] placeholder-gray-400 focus:outline-none"
              />
              <button
                type="submit"
                className="bg-[#C5A66A] hover:bg-[#b8985c] text-[#172B40] font-semibold text-sm px-5 py-2.5 rounded-lg transition-colors shadow-sm shrink-0"
              >
                {t('search.button', 'Search')}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Quick Navigation Cards */}
      <div>
        <h3 className="text-lg font-bold text-[#172B40] mb-4 flex items-center gap-2">
          <span className="w-2 h-5 bg-[#C5A66A] rounded-sm inline-block"></span>
          {t('home.quickLinks', 'Quick Links')}
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Link
            to="/search"
            className="p-5 bg-white rounded-xl border border-gray-200 hover:border-[#C5A66A] hover:shadow-md transition-all group"
          >
            <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
              <Search className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-[#172B40] text-sm group-hover:text-[#C5A66A] transition-colors">
              {t('nav.search', 'Smart Search')}
            </h4>
            <p className="text-xs text-gray-500 mt-1">
              {lang === 'ta'
                ? 'தமிழ் மற்றும் ஆங்கிலத்தில் வரலாற்றுப் பெயர்களைத் தேடுங்கள்.'
                : 'Fuzzy & exact historical name search in Tamil & English.'}
            </p>
          </Link>

          <Link
            to="/places/1"
            className="p-5 bg-white rounded-xl border border-gray-200 hover:border-[#C5A66A] hover:shadow-md transition-all group"
          >
            <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
              <Clock className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-[#172B40] text-sm group-hover:text-[#C5A66A] transition-colors">
              {t('nav.timeline', 'Historical Timeline')}
            </h4>
            <p className="text-xs text-gray-500 mt-1">
              {lang === 'ta'
                ? 'பெயர் மாற்றங்களின் காலவரிசை மற்றும் ஆவண ஆதாரங்கள்.'
                : 'Chronological timeline of renaming events & sources.'}
            </p>
          </Link>

          <Link
            to="/ask"
            className="p-5 bg-white rounded-xl border border-gray-200 hover:border-[#C5A66A] hover:shadow-md transition-all group"
          >
            <div className="w-10 h-10 rounded-lg bg-amber-50 text-amber-700 flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
              <Bot className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-[#172B40] text-sm group-hover:text-[#C5A66A] transition-colors">
              {t('nav.askAI', 'Ask History AI')}
            </h4>
            <p className="text-xs text-gray-500 mt-1">
              {lang === 'ta'
                ? 'சான்றாதாரங்களுடன் AI கேள்வி-பதில் உதவி.'
                : 'Evidence-grounded question answering with Gemini.'}
            </p>
          </Link>

          <Link
            to="/graph"
            className="p-5 bg-white rounded-xl border border-gray-200 hover:border-[#C5A66A] hover:shadow-md transition-all group"
          >
            <div className="w-10 h-10 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
              <Network className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-[#172B40] text-sm group-hover:text-[#C5A66A] transition-colors">
              {t('nav.graph', 'Relationship Graph')}
            </h4>
            <p className="text-xs text-gray-500 mt-1">
              {lang === 'ta'
                ? 'ஊர்கள், பெயர்கள், நிகழ்வுகளுக்கிடையேயான தொடர்பு வரைபடம்.'
                : 'Interactive graph visualization of historical connections.'}
            </p>
          </Link>
        </div>
      </div>

      {/* Featured Historical Places */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-[#172B40] flex items-center gap-2">
            <span className="w-2 h-5 bg-[#C5A66A] rounded-sm inline-block"></span>
            {t('home.featuredPlaces', 'Featured Historical Places')}
          </h3>
          <Link
            to="/search"
            className="text-xs font-semibold text-[#172B40] hover:text-[#C5A66A] flex items-center gap-1"
          >
            {lang === 'ta' ? 'அனைத்தையும் காண்க' : 'View all'}
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-10 bg-white rounded-xl border border-gray-200 text-gray-500 text-sm">
            {t('common.loading', 'Loading historical records...')}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {places.map((place) => (
              <div
                key={place.id}
                className="bg-white rounded-xl p-5 border border-gray-200 hover:border-[#C5A66A] shadow-sm hover:shadow-md transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <MapPin className="w-4 h-4 text-[#C5A66A]" />
                        <h4 className="font-bold text-base text-[#172B40]">
                          {lang === 'ta' && place.current_name_tamil
                            ? place.current_name_tamil
                            : place.current_name}
                        </h4>
                        <span className="text-xs text-gray-500">
                          ({lang === 'ta' ? place.current_name : place.current_name_tamil})
                        </span>
                      </div>
                      <p className="text-xs text-gray-500 mt-0.5">
                        {lang === 'ta' ? 'மாவட்டம்:' : 'District:'} {place.district || '-'}
                      </p>
                    </div>

                    <StatusBadge
                      status={
                        place.id === 1 || place.id === 2 ? 'verified' : 'partially_verified'
                      }
                    />
                  </div>

                  {/* Historical Names pill list */}
                  <div className="mt-3">
                    <span className="text-xs font-semibold text-gray-600">
                      {lang === 'ta' ? 'வரலாற்றுப் பெயர்கள்:' : 'Historical Variants:'}{' '}
                    </span>
                    <div className="inline-flex flex-wrap gap-1.5 mt-1">
                      {place.historical_names?.map((hn) => (
                        <span
                          key={hn.id}
                          className="px-2 py-0.5 bg-gray-100 text-[#172B40] text-xs rounded border border-gray-200 font-medium"
                        >
                          {hn.name}
                        </span>
                      ))}
                    </div>
                  </div>

                  <p className="text-xs text-gray-600 mt-2 line-clamp-2 leading-relaxed">
                    {lang === 'ta' && place.description_tamil
                      ? place.description_tamil
                      : place.description}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between">
                  <Link
                    to={`/places/${place.id}`}
                    className="text-xs font-semibold text-[#172B40] hover:text-[#C5A66A] flex items-center gap-1"
                  >
                    {t('place.timeline', 'Historical Timeline')}
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                  <Link
                    to={`/graph?place=${place.id}`}
                    className="text-xs font-medium text-gray-500 hover:text-[#172B40] flex items-center gap-1"
                  >
                    <Network className="w-3 h-3" />
                    {lang === 'ta' ? 'தொடர்பு வரைபடம்' : 'Graph'}
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Evidence Verification Standard Explanation */}
      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm">
        <div className="flex items-center gap-3 mb-3">
          <BookOpen className="w-5 h-5 text-[#C5A66A]" />
          <h3 className="text-base font-bold text-[#172B40]">
            {t('home.evidenceTitle', 'Evidence Verification Framework')}
          </h3>
        </div>
        <p className="text-xs sm:text-sm text-gray-600 leading-relaxed mb-6">
          {t(
            'home.evidenceDesc',
            'Our platform clearly distinguishes verified facts, historical spelling variants, and uncertain claims based on official government gazetteers, Tamil Nadu Archives records, and epigraphical evidence.'
          )}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-emerald-50/70 border border-emerald-200">
            <div className="flex items-center gap-2 text-emerald-800 font-bold text-sm mb-1">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>{lang === 'ta' ? 'சரிபார்க்கப்பட்டது' : 'Verified'}</span>
            </div>
            <p className="text-xs text-emerald-950 leading-relaxed">
              {lang === 'ta'
                ? 'அரசாணை எண், அரசிதழ் அல்லது அதிகாரப்பூர்வ ஆவணங்களால் உறுதிசெய்யப்பட்ட தகவல்கள்.'
                : 'Backed by confirmed Government Orders (G.O.), Gazetteers, or primary archival documents.'}
            </p>
          </div>

          <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200">
            <div className="flex items-center gap-2 text-amber-800 font-bold text-sm mb-1">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>{lang === 'ta' ? 'பகுதி சரிபார்க்கப்பட்டது' : 'Partially Verified'}</span>
            </div>
            <p className="text-xs text-amber-950 leading-relaxed">
              {lang === 'ta'
                ? 'ஆதார ஆவணங்கள் குறிப்பிடப்பட்டுள்ள போதிலும் மேலும் சரிபார்ப்பு தேவைப்படும் பதிவுகள்.'
                : 'Documented historical names and sources identified, but awaiting official gazetteer cross-verification.'}
            </p>
          </div>

          <div className="p-4 rounded-xl bg-rose-50/70 border border-rose-200">
            <div className="flex items-center gap-2 text-rose-800 font-bold text-sm mb-1">
              <HelpCircle className="w-4 h-4 text-rose-600" />
              <span>{lang === 'ta' ? 'சரிபார்க்கப்படாதது' : 'Unverified'}</span>
            </div>
            <p className="text-xs text-rose-950 leading-relaxed">
              {lang === 'ta'
                ? 'வாய்வழி வரலாறு அல்லது ஆரம்பக் குறிப்புகள்; ஆவணச் சான்றுகள் உறுதிப்படுத்தப்படவில்லை.'
                : 'Folk etymologies or preliminary claims requiring primary source discovery before verification.'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
