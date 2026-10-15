import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useTranslation } from '../services/LanguageContext';
import { getPlaces } from '../services/api';
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
  Sparkles,
  ShieldCheck,
  Landmark,
  Compass,
  Scroll,
  Layers,
  ChevronRight
} from 'lucide-react';

export const Home = () => {
  const { lang, t } = useTranslation();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);

  // Suggested quick searches
  const suggestedSearches = [
    { label_ta: 'சென்னை', label_en: 'Chennai', q: 'சென்னை' },
    { label_ta: 'திருவண்ணாமலை', label_en: 'Tiruvannamalai', q: 'திருவண்ணாமலை' },
    { label_ta: 'ஆரணி', label_en: 'Arani', q: 'ஆரணி' },
    { label_ta: 'தஞ்சாவூர்', label_en: 'Thanjavur', q: 'தஞ்சாவூர்' },
    { label_ta: 'களம்பூர்', label_en: 'Kalambur', q: 'களம்பூர்' },
    { label_ta: 'மதுரை', label_en: 'Madurai', q: 'மதுரை' },
  ];

  // Core feature cards
  const featureCards = [
    {
      to: '/districts',
      icon: Compass,
      title_ta: '38 மாவட்டங்கள் நுண்ணறிவு',
      title_en: '38 Districts Intelligence',
      desc_ta: 'தமிழ்நாட்டின் 38 மாவட்டங்களின் அதிகாரப்பூர்வ வரலாறு, புவிசார் குறியீடுகள் (GI), தனித்துவச் சிறப்புகள் மற்றும் அரசுப் போர்டல்கள்.',
      desc_en: 'Explore all 38 Tamil Nadu districts with official gazetteers, GI tags, heritage landmarks, and government portals.'
    },
    {
      to: '/search',
      icon: Search,
      title_ta: 'இடப்பெயர் ஆய்வு',
      title_en: 'Etymological Origins',
      desc_ta: 'தமிழ்நாட்டின் கிராமங்கள், நகரங்கள் மற்றும் தெருக்களின் பெயர்த் தோற்றத்தை கல்வெட்டுச் சான்றுகளோடு ஆராயுங்கள்.',
      desc_en: 'Explore historical origins and documented root meanings of Tamil Nadu place names backed by inscriptional data.'
    },
    {
      to: '/sources',
      icon: BookOpen,
      title_ta: 'அரசிதழ்கள் & சான்றுகள்',
      title_en: 'Gazetteers & Archives',
      desc_ta: 'மாவட்ட அரசிதழ்கள், பழைய சென்னை மாகாண வரைபடங்கள் மற்றும் அரசு ஆணைகளை (G.O.) நேரடியாக வாசியுங்கள்.',
      desc_en: 'Browse official Imperial Gazetteers, Epigraphia Indica, Fort St. George G.O.s, and archival citations.'
    },
    {
      to: '/timeline',
      icon: Clock,
      title_ta: 'வரலாற்றுக் காலவரிசை',
      title_en: 'Historical Timeline',
      desc_ta: 'சங்க காலம், பல்லவர், சோழர், விஜயநகரர் மற்றும் காலனித்துவ ஆட்சிகளில் ஊர்ப் பெயர்களின் மாற்றங்களை காலவரிசையில் காண்க.',
      desc_en: 'Trace chronological transformations of settlements across Sangam, Chola, Nayak, and colonial periods.'
    },
    {
      to: '/ask',
      icon: Bot,
      title_ta: 'வரலாறு AI உரையாடல்',
      title_en: 'Ask History AI',
      desc_ta: 'தமிழ் ஆவணக் காப்பகத் தரவுகளின் அடிப்படையில் கேட்கப்படும் கேள்விகளுக்கு ஆதாரபூர்வ AI விளக்கங்களைப் பெறுங்கள்.',
      desc_en: 'Get source-grounded answers citing official publications, preventing fabricated claims.'
    }
  ];

  // Curated popular destinations with images
  const popularDestinations = [
    {
      id: 4,
      name_ta: 'தஞ்சாவூர்',
      name_en: 'Thanjavur',
      image: '/images/thanjavur.jpg',
      category_ta: 'சோழர் தலைநகரம் & உலகப் பாரம்பரியம்',
      category_en: 'Chola Capital & Heritage',
      district_ta: 'தஞ்சாவூர்',
      district_en: 'Thanjavur',
      period_ta: 'சோழர் பொற்காலம் (1010 கி.பி)',
      period_en: 'Imperial Chola (1010 CE)',
      evidence: 'partially_verified',
      desc_ta: 'ராஜராஜ சோழனால் கட்டப்பட்ட பெருவுடையார் கோயில் நகரம். சங்க காலம் முதல் ஆவணப்படுத்தப்பட்ட நெற்களஞ்சிய பூமி.',
      desc_en: 'Historic imperial capital of Chola emperors, home of the Brihadeeswarar Temple and Kaveri delta culture.'
    },
    {
      id: 5,
      name_ta: 'திருவண்ணாமலை',
      name_en: 'Tiruvannamalai',
      image: '/images/tiruvannamalai.jpg',
      category_ta: 'அருணாசலேஸ்வரர் ஆன்மீகத் தலம்',
      category_en: 'Temple City & District HQ',
      district_ta: 'திருவண்ணாமலை',
      district_en: 'Tiruvannamalai',
      period_ta: '7-ஆம் நூற்றாண்டு தேவாரம் முதல்',
      period_en: '7th Century Tevaram Epigraphy',
      evidence: 'verified',
      desc_ta: 'அண்ணாமலை மலையடிவாரத்தில் அமைந்த அக்னி தலம். சோழர், பாண்டிய, விஜயநகர மன்னர்களின் நூற்றுக்கும் மேற்பட்ட கல்வெட்டுகளைக் கொண்டது.',
      desc_en: 'Renowned temple city at the foothills of sacred Annamalai, with over 100 stone inscriptions recording endowments.'
    },
    {
      id: 10,
      name_ta: 'மதுரை',
      name_en: 'Madurai',
      image: '/images/madurai.jpg',
      category_ta: 'தூங்கா நகரம் & சங்க காலத் தலைநகர்',
      category_en: 'Pandya Capital & Cultural Seat',
      district_ta: 'மதுரை',
      district_en: 'Madurai',
      period_ta: 'சங்க காலம் (கி.மு 300 முதல்)',
      period_en: 'Sangam Era (300 BCE onwards)',
      evidence: 'verified',
      desc_ta: 'வைகை நதிக்கரையில் அமைந்துள்ள தமிழ்ச் சங்கங்களின் உறைவிடம். உலகப் புகழ்பெற்ற மீனாட்சி சுந்தரேஸ்வரர் திருக்கோயில் நகரம்.',
      desc_en: 'Ancient seat of the Tamil Sangam academies on the Vaigai river, celebrated in Sangam anthologies.'
    },
    {
      id: 7,
      name_ta: 'காஞ்சிபுரம்',
      name_en: 'Kanchipuram',
      image: '/images/mamallapuram.jpg',
      category_ta: 'பல்லவர் தலைநகரம் & பட்டு நகரம்',
      category_en: 'Pallava Capital & Temple City',
      district_ta: 'காஞ்சிபுரம்',
      district_en: 'Kanchipuram',
      period_ta: 'பல்லவர் காலம் (6-8-ஆம் நூற்றாண்டு)',
      period_en: 'Pallava Era (6th-8th Century CE)',
      evidence: 'verified',
      desc_ta: 'பல்லவ மன்னர்களின் தலைநகரமாகவும், கைலாசநாதர் மற்றும் ஏகாம்பரநாதர் வரலாற்றுச் சிறப்புமிக்க கோயில்களைக் கொண்ட புகழ்பெற்ற பட்டு நகரம்.',
      desc_en: 'Historic imperial capital of the Pallavas, celebrated for Kailasanathar temple inscriptions and traditional silk weaving.'
    },
    {
      id: 1,
      name_ta: 'சென்னை',
      name_en: 'Chennai',
      image: '/images/hero-temple.jpg',
      category_ta: 'தலைநகரம் & மதராசப்பட்டினம்',
      category_en: 'Capital City & Corporation',
      district_ta: 'சென்னை',
      district_en: 'Chennai',
      period_ta: '1639 கிழக்கிந்திய கம்பெனி முதல்',
      period_en: '1639 Colonial Era to 1996 G.O.',
      evidence: 'verified',
      desc_ta: '1639-இல் மதராசப்பட்டினம் என்ற வணிகத் தளமாகத் தொடங்கி, 1996-இல் "சென்னை" என மறுபெயரிடப்பட்ட தமிழ்நாட்டின் தலைநகரம்.',
      desc_en: 'Founded around Chennapatnam/Madraspatnam in 1639; renamed officially to Chennai in 1996 by Tamil Nadu Government.'
    },
    {
      id: 6,
      name_ta: 'ஆரணி',
      name_en: 'Arani',
      image: '/images/tiruvannamalai.jpg',
      category_ta: 'கமண்டல நாக நதிக்கரை கோட்டை நகரம்',
      category_en: 'Historic Fort & Silk Town',
      district_ta: 'திருவண்ணாமலை',
      district_en: 'Tiruvannamalai',
      period_ta: '1640 ஆரணி ஜாகீர் & 1751 போர்',
      period_en: '1640 Arani Jagir & Battle of Arnee',
      evidence: 'partially_verified',
      desc_ta: 'கமண்டல நாக நதியால் சூழப்பட்டு "ஆறு + அணி" எனப் பெயர் பெற்ற தன்னாட்சி ஜாகீர் கோட்டை நகரம். பாரம்பரிய பட்டு நெசவுக்குப் புகழ் பெற்றது.',
      desc_en: 'Historic town in Tiruvannamalai district along Kamandala Naga river; site of Clive’s historic Battle of Arnee in 1751.'
    }
  ];

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

  const getEvidenceStatusBadge = (status) => {
    switch (status) {
      case 'verified':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-100/90 text-emerald-900 border border-emerald-300">
            <CheckCircle2 className="w-3 h-3 text-emerald-700" />
            {lang === 'ta' ? 'சான்றாதார உண்மை' : 'Documented'}
          </span>
        );
      case 'partially_verified':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-100/90 text-amber-900 border border-amber-300">
            <AlertTriangle className="w-3 h-3 text-amber-700" />
            {lang === 'ta' ? 'அறிஞர் கருதுகோள்' : 'Scholarly'}
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-rose-100/90 text-rose-900 border border-rose-300">
            <HelpCircle className="w-3 h-3 text-rose-700" />
            {lang === 'ta' ? 'வாய்மொழி மரபு' : 'Folk Tradition'}
          </span>
        );
    }
  };

  return (
    <div className="space-y-12 max-w-6xl mx-auto py-2">
      {/* 1. Photographic Dark Hero Section */}
      <section className="relative rounded-3xl overflow-hidden shadow-2xl border border-[#2A3E54] min-h-[460px] sm:min-h-[500px] flex items-center">
        {/* Background Temple Image */}
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat transition-transform duration-700 hover:scale-105"
          style={{ backgroundImage: `url('/images/hero-temple.jpg')` }}
        />
        {/* Deep Navy/Black Gradient Overlay with Warm Gold Glow */}
        <div className="absolute inset-0 bg-gradient-to-r from-[#0F1D2C]/95 via-[#172B40]/85 to-[#0F1D2C]/80" />
        <div className="absolute right-0 top-0 w-96 h-96 bg-[#C5A66A]/15 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 p-6 sm:p-10 lg:p-12 max-w-3xl space-y-6">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#C5A66A]/20 border border-[#C5A66A]/40 text-[#C5A66A] text-xs font-semibold backdrop-blur-sm">
            <Sparkles className="w-3.5 h-3.5" />
            <span>
              {lang === 'ta'
                ? 'தமிழ்நாடு வரலாற்று இடப்பெயர் ஆய்வுத் தளம்'
                : 'Tamil Nadu Historical Place Names Explorer'}
            </span>
          </div>

          {/* Headline */}
          <div className="space-y-2">
            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-tight leading-tight">
              {lang === 'ta' ? (
                <>
                  தமிழ்நாட்டின் <span className="text-[#C5A66A]">வரலாற்று இடப்பெயர்கள்</span>
                </>
              ) : (
                <>
                  Explore How Tamil Nadu <span className="text-[#C5A66A]">Place Names Evolved</span>
                </>
              )}
            </h1>
            <p className="text-sm sm:text-base text-gray-200/90 leading-relaxed max-w-2xl font-normal">
              {lang === 'ta'
                ? 'பழைய மாவட்ட அரசிதழ்கள், கல்வெட்டுகள், செப்பேடுகள் மற்றும் அரசு ஆவணங்கள் மூலம் தமிழக ஊர்ப் பெயர்களின் பரிணாமத்தை சான்றுகளுடன் ஆராயுங்கள்.'
                : 'Discover historical renamings, linguistic derivations, and inscriptional evidence recorded across centuries of Tamil epigraphy and colonial archives.'}
            </p>
          </div>

          {/* Prominent Search Bar */}
          <form onSubmit={handleSearchSubmit} className="pt-2">
            <div className="flex flex-col sm:flex-row items-center bg-white rounded-2xl p-2 shadow-2xl border-2 border-[#C5A66A]/50 focus-within:border-[#C5A66A] transition-all gap-2">
              <div className="flex items-center w-full px-2">
                <Search className="w-5 h-5 text-[#C5A66A] mr-3 shrink-0" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder={
                    lang === 'ta'
                      ? 'ஊர்ப் பெயரைத் தேடுங்கள்... (எ.கா: திருவண்ணாமலை, ஆரணி, தஞ்சாவூர், சென்னை, மதுரை)'
                      : 'Search any Tamil Nadu place... (e.g. Tiruvannamalai, Arani, Thanjavur, Chennai)'
                  }
                  className="w-full py-2.5 text-sm sm:text-base text-[#172B40] placeholder-gray-400 focus:outline-none font-medium"
                />
              </div>
              <button
                type="submit"
                className="w-full sm:w-auto bg-[#C5A66A] hover:bg-[#b8985c] text-[#172B40] font-extrabold text-sm px-7 py-3 rounded-xl transition-all shadow-md shrink-0 flex items-center justify-center gap-2"
              >
                <span>{lang === 'ta' ? 'தேடுக' : 'Explore'}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </form>

          {/* Suggested Searches */}
          <div className="flex flex-wrap items-center gap-2 pt-1 text-xs text-gray-300">
            <span className="font-semibold text-[#C5A66A]">
              {lang === 'ta' ? 'பரிந்துரைக்கப்பட்டவை:' : 'Suggested searches:'}
            </span>
            {suggestedSearches.map((item, index) => (
              <button
                key={index}
                onClick={() => navigate(`/search?q=${encodeURIComponent(item.q)}`)}
                className="px-3 py-1 rounded-full bg-white/10 hover:bg-[#C5A66A] hover:text-[#172B40] text-gray-200 border border-white/20 transition-all font-medium text-xs backdrop-blur-sm"
              >
                {lang === 'ta' ? item.label_ta : item.label_en}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* 2. Feature Cards Grid */}
      <section className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-200 pb-3">
          <div>
            <h2 className="text-xl sm:text-2xl font-extrabold text-[#172B40]">
              {lang === 'ta' ? 'ஆய்வுத் திறன்கள்' : 'Research Capabilities'}
            </h2>
            <p className="text-xs sm:text-sm text-gray-600">
              {lang === 'ta'
                ? 'ஆவணப்படுத்தப்பட்ட உண்மைகள், கல்வெட்டுகள் மற்றும் வரலாற்றுத் தரவுகளின் தொகுப்பு'
                : 'Structured methodology grounded in verifiable epigraphy and official archival publications.'}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {featureCards.map((card, idx) => {
            const Icon = card.icon;
            return (
              <Link
                key={idx}
                to={card.to}
                className="group bg-white p-5 rounded-2xl border border-gray-200 shadow-sm hover:shadow-md hover:border-[#C5A66A] transition-all flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="w-11 h-11 rounded-xl bg-[#F7F4ED] border border-[#C5A66A]/30 flex items-center justify-center text-[#172B40] group-hover:bg-[#172B40] group-hover:text-[#C5A66A] transition-colors">
                    <Icon className="w-5 h-5" />
                  </div>
                  <h3 className="font-bold text-base text-[#172B40] group-hover:text-[#C5A66A] transition-colors">
                    {lang === 'ta' ? card.title_ta : card.title_en}
                  </h3>
                  <p className="text-xs text-gray-600 leading-relaxed">
                    {lang === 'ta' ? card.desc_ta : card.desc_en}
                  </p>
                </div>
                <div className="pt-4 flex items-center gap-1 text-xs font-bold text-[#172B40] group-hover:text-[#C5A66A] transition-colors">
                  <span>{lang === 'ta' ? 'ஆரம்பிக்க' : 'Explore'}</span>
                  <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* 3. Popular Destinations Grid */}
      <section className="space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-200 pb-3">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-bold text-[#C5A66A] uppercase tracking-wider mb-1">
              <Landmark className="w-4 h-4" />
              <span>{lang === 'ta' ? 'வரலாற்றுத் தளங்கள்' : 'Heritage Destinations'}</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-extrabold text-[#172B40]">
              {lang === 'ta' ? 'பிரபல வரலாற்று இடங்கள்' : 'Popular Historical Destinations'}
            </h2>
            <p className="text-xs sm:text-sm text-gray-600">
              {lang === 'ta'
                ? 'அதிகாரப்பூர்வ அரசிதழ்கள் மற்றும் கல்வெட்டுகளில் ஆவணப்படுத்தப்பட்ட முக்கிய ஊர்கள்'
                : 'Explore detailed research profiles with primary source citations and timeline events.'}
            </p>
          </div>
          <Link
            to="/search"
            className="inline-flex items-center gap-1 text-xs sm:text-sm font-bold text-[#172B40] hover:text-[#C5A66A] transition-colors shrink-0"
          >
            <span>{lang === 'ta' ? 'அனைத்து இடங்களையும் காண்க' : 'View all places'}</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {popularDestinations.map((place) => (
            <div
              key={place.id}
              className="group bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-lg hover:border-[#C5A66A] transition-all flex flex-col justify-between"
            >
              {/* Image with Category Badge */}
              <div className="relative h-48 overflow-hidden bg-gray-100">
                <img
                  src={place.image}
                  alt={place.name_en}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = '/images/hero-temple.jpg';
                  }}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
                
                {/* Evidence Status Badge on Image */}
                <div className="absolute top-3 right-3">
                  {getEvidenceStatusBadge(place.evidence)}
                </div>

                {/* Location Badge on Image */}
                <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between text-white">
                  <div className="flex items-center gap-1.5 text-xs font-semibold backdrop-blur-md bg-black/40 px-2.5 py-1 rounded-md">
                    <MapPin className="w-3.5 h-3.5 text-[#C5A66A]" />
                    <span>{lang === 'ta' ? place.district_ta : place.district_en}</span>
                  </div>
                  <span className="text-[11px] text-gray-200 bg-black/40 px-2 py-1 rounded-md font-medium">
                    {lang === 'ta' ? place.period_ta : place.period_en}
                  </span>
                </div>
              </div>

              {/* Card Body */}
              <div className="p-5 space-y-3 flex-1 flex flex-col justify-between">
                <div className="space-y-2">
                  <div className="flex items-baseline gap-2">
                    <h3 className="text-xl font-bold text-[#172B40] group-hover:text-[#C5A66A] transition-colors">
                      {lang === 'ta' ? place.name_ta : place.name_en}
                    </h3>
                  </div>

                  <div className="text-xs font-semibold text-[#C5A66A]">
                    {lang === 'ta' ? place.category_ta : place.category_en}
                  </div>

                  <p className="text-xs text-gray-600 line-clamp-3 leading-relaxed">
                    {lang === 'ta' ? place.desc_ta : place.desc_en}
                  </p>
                </div>

                {/* CTA Link */}
                <div className="pt-3 border-t border-gray-100 flex items-center justify-between">
                  <Link
                    to={`/places/${place.id}`}
                    className="inline-flex items-center gap-1 text-xs font-bold text-[#172B40] group-hover:text-[#C5A66A] transition-colors"
                  >
                    <span>{lang === 'ta' ? 'முழு ஆய்வு விவரங்கள்' : 'View full research'}</span>
                    <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" />
                  </Link>

                  <Link
                    to={`/graph?place=${place.id}`}
                    title={lang === 'ta' ? 'உறவு வரைபடம்' : 'Relationship Graph'}
                    className="p-1.5 rounded-md hover:bg-gray-100 text-gray-500 hover:text-[#172B40] transition-colors"
                  >
                    <Network className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 4. Methodology & Evidence Grounding Banner */}
      <section className="bg-white rounded-3xl p-6 sm:p-8 border border-gray-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2 max-w-xl">
          <div className="flex items-center gap-2 text-xs font-bold text-[#C5A66A] uppercase tracking-wider">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>{lang === 'ta' ? 'ஆவணச் சான்று உத்தரவாதம்' : 'Epigraphical & Archival Rigor'}</span>
          </div>
          <h3 className="text-lg sm:text-xl font-bold text-[#172B40]">
            {lang === 'ta'
              ? 'வரலாற்றுக் கற்பனைகள் இன்றி, உண்மை ஆவணங்கள் மட்டுமே'
              : 'Zero Historical Hallucination — Grounded in Documented Citations'}
          </h3>
          <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
            {lang === 'ta'
              ? 'தமிழ்நாடு ஆவணக் காப்பகம், தொல்லியல் துறை வெளியீடுகள் மற்றும் மத்திய அரசின் அரசிதழ்கள் அடிப்படையில் மட்டுமே ஆய்வு முடிவுகள் வழங்கப்படுகின்றன.'
              : 'Our retrieval pipeline cross-references District Gazetteers, Inscriptions of South India (ASI), and Tamil Nadu Government Orders before synthesizing explanations.'}
          </p>
        </div>
        <div className="flex flex-wrap gap-3 shrink-0">
          <Link
            to="/sources"
            className="px-5 py-2.5 rounded-xl bg-[#F7F4ED] text-[#172B40] hover:bg-[#eae4d5] text-xs font-bold border border-gray-300 transition-colors flex items-center gap-2"
          >
            <BookOpen className="w-4 h-4 text-[#C5A66A]" />
            <span>{lang === 'ta' ? 'அரசிதழ் மூலங்கள்' : 'View Source Archives'}</span>
          </Link>
          <Link
            to="/ask"
            className="px-5 py-2.5 rounded-xl bg-[#172B40] text-white hover:bg-[#20364F] text-xs font-bold transition-colors flex items-center gap-2 shadow-sm"
          >
            <Bot className="w-4 h-4 text-[#C5A66A]" />
            <span>{lang === 'ta' ? 'AI-யிடம் கேட்க' : 'Ask History AI'}</span>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
