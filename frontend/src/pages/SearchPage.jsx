import React, { useState, useEffect } from 'react';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import { useTranslation } from '../services/LanguageContext';
import { getPlaces, researchPlace } from '../services/api';
import { 
  Search, 
  MapPin, 
  ArrowRight, 
  Sparkles, 
  AlertCircle, 
  Clock, 
  ExternalLink, 
  Compass, 
  HelpCircle,
  RotateCcw,
  CheckCircle2,
  AlertTriangle,
  Filter,
  X
} from 'lucide-react';
import districtsDataRaw from '../data/districtsData.json';

export const SearchPage = () => {
  const { lang, t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const queryParam = searchParams.get('q') || '';
  const districtParam = searchParams.get('district') || '';

  const [inputVal, setInputVal] = useState(queryParam);
  const [localResults, setLocalResults] = useState([]);
  const [researchResult, setResearchResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [researching, setResearching] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  // Filter chips state
  const [evidenceFilter, setEvidenceFilter] = useState('all'); // 'all' | 'verified' | 'partially_verified' | 'unverified'
  const [districtFilter, setDistrictFilter] = useState(districtParam || 'all');

  const all38Districts = districtsDataRaw.districts || [];

  const popularDistricts = [
    { id: 'all', name_ta: 'அனைத்து மாவட்டங்கள் (38)', name_en: 'All 38 Districts' },
    ...all38Districts.map((d) => ({
      id: d.district_english,
      name_ta: d.district_tamil,
      name_en: d.district_english,
      no: d.no,
    })),
  ];

  // Match search query against 38 districts
  const matchedDistricts = React.useMemo(() => {
    const q = (inputVal || queryParam || '').trim().toLowerCase();
    if (!q || q.length < 2) return [];

    return all38Districts.filter((d) => {
      const eng = d.district_english.toLowerCase();
      const tam = d.district_tamil.toLowerCase();
      const formerEn = (d.former_administrative_name_history_en || d.former_administrative_name_history || '').toLowerCase();
      const formerTa = (d.former_administrative_name_history_ta || '').toLowerCase();
      const ancientEn = (d.ancient_or_historical_name_context_en || d.ancient_or_historical_name_context || '').toLowerCase();
      const ancientTa = (d.ancient_or_historical_name_context_ta || '').toLowerCase();
      const aliases = (d.search_aliases || []).map((a) => a.toLowerCase());

      return (
        eng === q ||
        tam === q ||
        aliases.includes(q) ||
        eng.includes(q) ||
        tam.includes(q) ||
        aliases.some((a) => a.includes(q)) ||
        formerEn.includes(q) ||
        formerTa.includes(q) ||
        ancientEn.includes(q) ||
        ancientTa.includes(q)
      );
    });
  }, [inputVal, queryParam, all38Districts]);

  const sampleQueries = [
    { label_ta: 'அரியலூர்', label_en: 'Ariyalur', q: 'Ariyalur' },
    { label_ta: 'திருவண்ணாமலை', label_en: 'Tiruvannamalai', q: 'Tiruvannamalai' },
    { label_ta: 'ஆரணி', label_en: 'Arani', q: 'Arani' },
    { label_ta: 'சென்னை', label_en: 'Chennai', q: 'Chennai' },
    { label_ta: 'மெட்ராஸ்', label_en: 'Madras', q: 'Madras' },
    { label_ta: 'மதுரை', label_en: 'Madurai', q: 'Madurai' },
    { label_ta: 'தஞ்சாவூர்', label_en: 'Thanjavur', q: 'Thanjavur' },
    { label_ta: 'கோயம்புத்தூர்', label_en: 'Coimbatore', q: 'Coimbatore' },
    { label_ta: 'நீலகிரி', label_en: 'Nilgiris', q: 'Nilgiris' },
  ];

  // Map known place IDs or names to curated images
  const getPlaceImage = (place) => {
    const name = (place.current_name || '').toLowerCase();
    if (name.includes('thanjavur')) return '/images/thanjavur.jpg';
    if (name.includes('tiruvannamalai')) return '/images/tiruvannamalai.jpg';
    if (name.includes('madurai')) return '/images/madurai.jpg';
    if (name.includes('mamallapuram') || name.includes('mahabalipuram')) return '/images/mamallapuram.jpg';
    return '/images/hero-temple.jpg';
  };

  const executeSearch = async (queryText, distFilter = null) => {
    const q = (queryText || '').trim();
    setLoading(true);
    setResearching(false);
    setHasSearched(true);
    setErrorMsg(null);
    setResearchResult(null);

    try {
      // 1. Fetch from SQLite database
      const localData = await getPlaces(q);
      setLocalResults(localData);

      // 2. If no local records found and a specific text query was typed:
      // Run the universal historical research pipeline
      if ((!localData || localData.length === 0) && q) {
        setResearching(true);
        const res = await researchPlace(q, distFilter !== 'all' ? distFilter : null, lang);
        setResearchResult(res);
      }
    } catch (err) {
      console.error('Search error:', err);
      setErrorMsg(
        lang === 'ta'
          ? 'வரலாற்றுத் தரவுகளைப் பெறுவதில் பிழை ஏற்பட்டது. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.'
          : 'Failed to retrieve historical research records. Please retry.'
      );
    } finally {
      setLoading(false);
      setResearching(false);
    }
  };

  useEffect(() => {
    // Run search on mount or when URL params change
    executeSearch(queryParam, districtParam);
    setInputVal(queryParam);
    if (districtParam) setDistrictFilter(districtParam);
  }, [queryParam, districtParam]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (inputVal.trim()) params.set('q', inputVal.trim());
    if (districtFilter && districtFilter !== 'all') params.set('district', districtFilter);
    setSearchParams(params);
    executeSearch(inputVal, districtFilter);
  };

  const handleClear = () => {
    setInputVal('');
    setDistrictFilter('all');
    setEvidenceFilter('all');
    setSearchParams({});
    executeSearch('');
  };

  // Filter local results by evidence chip and district
  const filteredResults = localResults.filter((p) => {
    // Evidence Filter
    if (evidenceFilter !== 'all') {
      const pStatus = p.evidence_status || 'verified';
      if (evidenceFilter !== pStatus) return false;
    }
    // District Filter
    if (districtFilter !== 'all') {
      const pDist = (p.district || '').toLowerCase();
      if (!pDist.includes(districtFilter.toLowerCase())) return false;
    }
    return true;
  });

  const getEvidenceStatusBadge = (status) => {
    switch (status) {
      case 'verified':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-900 border border-emerald-300">
            <CheckCircle2 className="w-3 h-3 text-emerald-700" />
            {lang === 'ta' ? 'சரிபார்க்கப்பட்டது' : 'Documented Fact'}
          </span>
        );
      case 'partially_verified':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-100 text-amber-900 border border-amber-300">
            <AlertTriangle className="w-3 h-3 text-amber-700" />
            {lang === 'ta' ? 'அறிஞர் கருதுகோள்' : 'Scholarly Hypothesis'}
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-rose-100 text-rose-900 border border-rose-300">
            <HelpCircle className="w-3 h-3 text-rose-700" />
            {lang === 'ta' ? 'வாய்மொழி மரபு' : 'Folk Tradition'}
          </span>
        );
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto py-2">
      {/* Search Header Banner */}
      <div className="bg-[#172B40] text-white rounded-2xl p-6 sm:p-8 border border-[#2A3E54] shadow-sm relative overflow-hidden">
        <div className="absolute right-0 top-0 w-72 h-72 bg-[#C5A66A]/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-4">
          <div className="flex items-center justify-between">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#C5A66A]/20 border border-[#C5A66A]/40 text-[#C5A66A] text-xs font-semibold">
              <Compass className="w-3.5 h-3.5" />
              <span>{lang === 'ta' ? 'வரலாற்று இடப்பெயர் தேடல்' : 'Place Name Research Explorer'}</span>
            </div>
            <span className="text-xs text-gray-400">
              {lang === 'ta' ? 'அரசிதழ் & ஆவணக் காப்பகத் தளம்' : 'SQLite Archival Source of Truth'}
            </span>
          </div>

          <form onSubmit={handleSubmit} className="space-y-3">
            <div className="flex flex-col sm:flex-row gap-2">
              <div className="relative flex-1">
                <Search className="w-5 h-5 text-gray-400 absolute left-3.5 top-3.5" />
                <input
                  type="text"
                  value={inputVal}
                  onChange={(e) => setInputVal(e.target.value)}
                  placeholder={
                    lang === 'ta'
                      ? 'தமிழ் அல்லது ஆங்கிலத்தில் ஊர்ப் பெயரைத் தேடுங்கள்... (எ.கா: அரியலூர், மதுரை)'
                      : 'Search place name in Tamil or English... (e.g. Ariyalur, Madurai)'
                  }
                  className="w-full pl-11 pr-10 py-3 bg-white text-[#172B40] rounded-xl text-sm font-medium placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#C5A66A] shadow-sm"
                />
                {inputVal && (
                  <button
                    type="button"
                    onClick={() => setInputVal('')}
                    className="absolute right-3 top-3.5 text-gray-400 hover:text-gray-600"
                    aria-label="Clear search"
                  >
                    <X className="w-4 h-4" />
                  </button>
                )}
              </div>

              {/* District Dropdown Selector */}
              <select
                value={districtFilter}
                onChange={(e) => setDistrictFilter(e.target.value)}
                className="py-3 px-3 bg-white text-[#172B40] rounded-xl text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-[#C5A66A] shadow-sm border-r-8 border-transparent"
              >
                {popularDistricts.map((d) => (
                  <option key={d.id} value={d.id}>
                    {lang === 'ta' ? d.name_ta : d.name_en}
                  </option>
                ))}
              </select>

              <button
                type="submit"
                className="bg-[#C5A66A] hover:bg-[#b8985c] text-[#172B40] font-extrabold text-sm px-6 py-3 rounded-xl transition-colors shadow-sm shrink-0 flex items-center justify-center gap-1.5"
              >
                <Search className="w-4 h-4" />
                <span>{lang === 'ta' ? 'தேடுக' : 'Search'}</span>
              </button>
            </div>
          </form>

          {/* Quick Suggestions Chips */}
          <div className="flex flex-wrap items-center gap-1.5 text-xs">
            <span className="text-[#C5A66A] font-medium mr-1">
              {lang === 'ta' ? 'பரிந்துரைகள்:' : 'Quick links:'}
            </span>
            {sampleQueries.map((item, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => {
                  setInputVal(item.q);
                  executeSearch(item.q, districtFilter);
                }}
                className="px-2.5 py-1 rounded-md bg-white/10 hover:bg-[#C5A66A] hover:text-[#172B40] text-gray-200 transition-colors text-xs font-medium"
              >
                {lang === 'ta' ? item.label_ta : item.label_en}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Filter Chips Bar */}
      <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2 text-xs font-bold text-[#172B40]">
          <Filter className="w-4 h-4 text-[#C5A66A]" />
          <span>{lang === 'ta' ? 'சான்றாதார வடிகட்டி:' : 'Evidence Filter:'}</span>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setEvidenceFilter('all')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
              evidenceFilter === 'all'
                ? 'bg-[#172B40] text-white shadow-sm'
                : 'bg-[#F7F4ED] text-[#172B40] hover:bg-[#eae5d7]'
            }`}
          >
            {lang === 'ta' ? 'அனைத்து சான்றுகளும்' : 'All Levels'}
          </button>
          <button
            onClick={() => setEvidenceFilter('verified')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1 ${
              evidenceFilter === 'verified'
                ? 'bg-emerald-700 text-white shadow-sm'
                : 'bg-emerald-50 text-emerald-800 hover:bg-emerald-100'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>{lang === 'ta' ? 'சரிபார்க்கப்பட்டது' : 'Documented Fact'}</span>
          </button>
          <button
            onClick={() => setEvidenceFilter('partially_verified')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1 ${
              evidenceFilter === 'partially_verified'
                ? 'bg-amber-700 text-white shadow-sm'
                : 'bg-amber-50 text-amber-800 hover:bg-amber-100'
            }`}
          >
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>{lang === 'ta' ? 'அறிஞர் கருதுகோள்' : 'Scholarly Hypothesis'}</span>
          </button>
          <button
            onClick={() => setEvidenceFilter('unverified')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1 ${
              evidenceFilter === 'unverified'
                ? 'bg-rose-700 text-white shadow-sm'
                : 'bg-rose-50 text-rose-800 hover:bg-rose-100'
            }`}
          >
            <HelpCircle className="w-3.5 h-3.5" />
            <span>{lang === 'ta' ? 'வாய்மொழி மரபு' : 'Folk Tradition'}</span>
          </button>
        </div>

        {(evidenceFilter !== 'all' || districtFilter !== 'all') && (
          <button
            onClick={handleClear}
            className="text-xs font-semibold text-rose-600 hover:text-rose-800 flex items-center gap-1"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>{lang === 'ta' ? 'வடிகட்டிகளை நீக்கு' : 'Reset Filters'}</span>
          </button>
        )}
      </div>

      {/* Loading Skeleton */}
      {loading && (
        <div className="bg-white rounded-2xl p-12 border border-gray-200 text-center space-y-4 shadow-sm">
          <div className="inline-block animate-spin w-8 h-8 border-3 border-[#172B40] border-t-transparent rounded-full" />
          <p className="text-sm font-semibold text-[#172B40]">
            {lang === 'ta' ? 'வரலாற்றுத் தரவுகளைத் தேடுகிறது...' : 'Searching historical place records...'}
          </p>
        </div>
      )}

      {/* Error Message */}
      {errorMsg && (
        <div className="bg-rose-50 border border-rose-200 rounded-xl p-4 text-rose-800 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Search Results List */}
      {!loading && (
        <div className="space-y-6">
          {/* Matched District Intelligence Spotlight Card */}
          {matchedDistricts.length === 1 && (
            <div className="bg-gradient-to-r from-[#172B40] to-[#0F1D2C] text-white rounded-3xl p-6 sm:p-7 border-2 border-[#C5A66A] shadow-xl space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="px-3 py-1 rounded-full bg-[#C5A66A] text-[#172B40] text-xs font-black shadow-sm">
                    {lang === 'ta' ? `மாவட்டம் #${matchedDistricts[0].no}` : `District #${matchedDistricts[0].no} of 38`}
                  </span>
                  <span className="text-xs text-gray-200 bg-white/10 px-2.5 py-0.5 rounded-md font-semibold border border-white/10">
                    {lang === 'ta' ? (matchedDistricts[0].region_ta || matchedDistricts[0].region) : (matchedDistricts[0].region_en || matchedDistricts[0].region)}
                  </span>
                  <span className="text-[11px] text-emerald-400 font-bold flex items-center gap-1 bg-emerald-950/60 px-2 py-0.5 rounded-md border border-emerald-800">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>{lang === 'ta' ? 'அதிகாரப்பூர்வ மாவட்டம்' : 'Verified District Record'}</span>
                  </span>
                </div>
                {matchedDistricts[0].official_district_portal && (
                  <a
                    href={matchedDistricts[0].official_district_portal}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-xs text-emerald-300 hover:text-emerald-200 font-bold bg-white/10 px-3 py-1 rounded-full border border-white/20 transition-colors"
                  >
                    <span>{t('district.officialWebsite', 'Official Website')}</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>

              <div className="space-y-1">
                <h3 className="text-2xl sm:text-3xl font-black text-white">
                  {lang === 'ta' ? matchedDistricts[0].district_tamil : matchedDistricts[0].district_english}
                </h3>
                <p className="text-xs sm:text-sm text-gray-200 leading-relaxed font-normal pt-1 max-w-4xl">
                  {lang === 'ta' ? (matchedDistricts[0].intro_ta || matchedDistricts[0].intro_en) : (matchedDistricts[0].intro_en || matchedDistricts[0].intro_ta)}
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1 text-xs">
                <div className="bg-white/5 p-3.5 rounded-2xl border border-white/10 space-y-1">
                  <span className="text-[#C5A66A] font-extrabold block">
                    {t('district.formerAdminHistory', 'Former Administrative History:')}
                  </span>
                  <p className="text-gray-200 text-xs leading-relaxed">
                    {lang === 'ta'
                      ? (matchedDistricts[0].former_administrative_name_history_ta || matchedDistricts[0].former_administrative_name_history)
                      : (matchedDistricts[0].former_administrative_name_history_en || matchedDistricts[0].former_administrative_name_history)}
                  </p>
                </div>
                <div className="bg-white/5 p-3.5 rounded-2xl border border-white/10 space-y-1">
                  <span className="text-[#C5A66A] font-extrabold block">
                    {t('district.ancientContext', 'Ancient / Historical Context:')}
                  </span>
                  <p className="text-gray-200 text-xs leading-relaxed">
                    {lang === 'ta'
                      ? (matchedDistricts[0].ancient_or_historical_name_context_ta || matchedDistricts[0].ancient_or_historical_name_context)
                      : (matchedDistricts[0].ancient_or_historical_name_context_en || matchedDistricts[0].ancient_or_historical_name_context)}
                  </p>
                </div>
              </div>

              <div className="pt-3 border-t border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="text-xs text-gray-300">
                  <span className="text-[#C5A66A] font-bold mr-1">
                    {t('district.changeAuthorityNote', 'G.O. / Authority:')}
                  </span>
                  <span>
                    {lang === 'ta'
                      ? (matchedDistricts[0].change_date_authority_verification_notes_ta || matchedDistricts[0].change_date_authority_verification_notes)
                      : (matchedDistricts[0].change_date_authority_verification_notes_en || matchedDistricts[0].change_date_authority_verification_notes)}
                  </span>
                </div>
                <Link
                  to={`/districts/${matchedDistricts[0].no}`}
                  className="px-6 py-2.5 bg-[#C5A66A] hover:bg-[#b8985c] text-[#172B40] font-black text-xs rounded-xl shadow-md transition-all flex items-center justify-center gap-2 shrink-0"
                >
                  <span>{lang === 'ta' ? 'முழு மாவட்ட நுண்ணறிவு விவரங்கள்' : 'Open Full District Dashboard'}</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          )}

          {/* Ambiguous Multi-district Match Disambiguation Banner */}
          {matchedDistricts.length > 1 && (
            <div className="bg-amber-50 border-2 border-amber-300 rounded-2xl p-5 text-amber-900 space-y-3 shadow-sm">
              <div className="flex items-center gap-2">
                <Compass className="w-5 h-5 text-amber-700 shrink-0" />
                <h4 className="font-extrabold text-sm text-amber-950">
                  {lang === 'ta'
                    ? `உங்கள் தேடலுக்கு ${matchedDistricts.length} மாவட்டங்கள் பொருந்துகின்றன — நீங்கள் தேடும் மாவட்டத்தைத் தேர்ந்தெடுக்கவும்:`
                    : `Multiple districts matched your query (${matchedDistricts.length}) — please select the intended district:`}
                </h4>
              </div>
              <div className="flex flex-wrap gap-2 pt-1">
                {matchedDistricts.map((d) => (
                  <Link
                    key={d.no}
                    to={`/districts/${d.no}`}
                    className="px-3.5 py-1.5 bg-white hover:bg-[#172B40] hover:text-[#C5A66A] text-[#172B40] font-bold text-xs rounded-xl border border-amber-300 transition-all flex items-center gap-1.5 shadow-sm"
                  >
                    <span>#{d.no} {lang === 'ta' ? d.district_tamil : d.district_english}</span>
                    <ArrowRight className="w-3.5 h-3.5 opacity-60" />
                  </Link>
                ))}
              </div>
            </div>
          )}

          <div className="flex items-center justify-between text-xs text-gray-500 font-semibold px-1 pt-2">
            <span>
              {lang === 'ta'
                ? `கிடைத்த இடங்கள்: ${filteredResults.length} இடங்கள்`
                : `Found ${filteredResults.length} matching places`}
            </span>
          </div>

          {filteredResults.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredResults.map((place) => (
                <div
                  key={place.id}
                  className="group bg-white rounded-2xl border border-gray-200 p-4 sm:p-5 shadow-sm hover:shadow-md hover:border-[#C5A66A] transition-all flex flex-col justify-between space-y-4"
                >
                  <div className="space-y-3">
                    {/* Top Row: Thumbnail + Title + Badge */}
                    <div className="flex items-start gap-3.5">
                      <img
                        src={getPlaceImage(place)}
                        alt={lang === 'ta' ? place.current_name_tamil || place.current_name : place.current_name}
                        className="w-16 h-16 rounded-xl object-cover shrink-0 border border-gray-200 shadow-sm"
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = '/images/hero-temple.jpg';
                        }}
                      />
                      <div className="flex-1 min-w-0">
                        <div className="flex flex-wrap items-center justify-between gap-1.5">
                          <h3 className="text-lg font-bold text-[#172B40] group-hover:text-[#C5A66A] transition-colors truncate">
                            {lang === 'ta'
                              ? (place.current_name_tamil || place.current_name)
                              : (place.current_name || place.current_name_tamil)}
                          </h3>
                          {getEvidenceStatusBadge(place.evidence_status)}
                        </div>

                        <div className="text-xs text-gray-500 font-medium">
                          {lang === 'ta'
                            ? (place.district_tamil || place.district)
                            : (place.district || place.district_tamil)}
                        </div>

                        <div className="text-[11px] font-semibold text-[#C5A66A] mt-0.5">
                          {lang === 'ta'
                            ? (place.category_tamil || place.category)
                            : (place.category || place.category_tamil)}
                        </div>
                      </div>
                    </div>

                    {/* Location Hierarchy Tag */}
                    <div className="flex flex-wrap items-center gap-1.5 text-[11px]">
                      <span className="px-2 py-0.5 rounded bg-[#172B40] text-white font-medium">
                        {lang === 'ta' ? 'தமிழ்நாடு' : 'Tamil Nadu'}
                      </span>
                      <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-800 font-semibold border border-blue-200 flex items-center gap-1">
                        <MapPin className="w-3 h-3" />
                        <span>{lang === 'ta' ? (place.district_tamil || place.district || '-') : (place.district || '-')}</span>
                      </span>
                      {place.taluk && (
                        <span className="px-2 py-0.5 rounded bg-gray-100 text-gray-700 font-medium border border-gray-200">
                          {place.taluk}
                        </span>
                      )}
                    </div>

                    {/* Short Description */}
                    <p className="text-xs text-gray-600 line-clamp-2 leading-relaxed">
                      {lang === 'ta'
                        ? (place.description_tamil || place.description)
                        : (place.description || place.description_tamil)}
                    </p>

                    {/* Historical Name Variants pill */}
                    {place.historical_names && place.historical_names.length > 0 && (
                      <div className="flex flex-wrap items-center gap-1 text-[11px] text-gray-500 pt-1">
                        <Clock className="w-3 h-3 text-[#C5A66A]" />
                        <span className="font-semibold text-gray-600">
                          {lang === 'ta' ? 'பழைய பெயர்கள்:' : 'Historical names:'}
                        </span>
                        {place.historical_names.slice(0, 3).map((hn, idx) => (
                          <span
                            key={idx}
                            className="bg-[#F7F4ED] px-1.5 py-0.5 rounded text-[#172B40] font-medium border border-gray-200"
                          >
                            {hn.name}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Card Bottom CTA */}
                  <div className="pt-3 border-t border-gray-100 flex items-center justify-between">
                    <Link
                      to={`/places/${place.id}`}
                      className="inline-flex items-center gap-1 text-xs font-bold text-[#172B40] group-hover:text-[#C5A66A] transition-colors"
                    >
                      <span>{lang === 'ta' ? 'முழு வரலாற்று விவரங்கள்' : 'View Place Details'}</span>
                      <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" />
                    </Link>

                    <Link
                      to={`/graph?place=${place.id}`}
                      className="text-xs text-gray-500 hover:text-[#172B40] font-medium"
                    >
                      {lang === 'ta' ? 'உறவு வரைபடம்' : 'Graph'}
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            /* Empty State */
            <div className="bg-white rounded-2xl p-10 border border-gray-200 text-center space-y-4 shadow-sm max-w-xl mx-auto my-6">
              <div className="w-12 h-12 rounded-full bg-[#F7F4ED] border border-[#C5A66A] flex items-center justify-center mx-auto text-[#172B40]">
                <HelpCircle className="w-6 h-6 text-[#C5A66A]" />
              </div>
              <h3 className="text-lg font-bold text-[#172B40]">
                {lang === 'ta'
                  ? 'பொருத்தமான இடங்கள் எதுவும் கிடைக்கவில்லை'
                  : 'No matching place records found'}
              </h3>
              <p className="text-xs text-gray-600 max-w-md mx-auto leading-relaxed">
                {lang === 'ta'
                  ? 'வேறு ஊர்ப் பெயரை உள்ளிட்டுத் தேடவும் அல்லது வடிகட்டிகளை மாற்றியமைக்கவும்.'
                  : 'Try searching for known historical towns like Ariyalur, Tiruvannamalai, Arani, Thanjavur, Chennai, or Madurai.'}
              </p>
              <button
                type="button"
                onClick={handleClear}
                className="px-4 py-2 bg-[#172B40] text-white text-xs font-bold rounded-lg hover:bg-[#20364F] transition-colors"
              >
                {lang === 'ta' ? 'அனைத்து இடங்களையும் காட்டுக' : 'Show All Places'}
              </button>
            </div>
          )}
        </div>
      )}

      {/* Live In-flight AI Deep Research Display */}
      {researching && (
        <div className="bg-[#172B40] text-white rounded-2xl p-6 border border-[#2A3E54] text-center space-y-3">
          <div className="inline-block animate-spin w-7 h-7 border-3 border-[#C5A66A] border-t-transparent rounded-full" />
          <h4 className="text-base font-bold text-white">
            {lang === 'ta'
              ? 'தமிழ்நாடு ஆவணக் காப்பகத் தரவுகளில் விரிவான ஆய்வு நடைபெறுகிறது...'
              : 'Conducting Archival Retrieval-Augmented Research...'}
          </h4>
          <p className="text-xs text-gray-300">
            {lang === 'ta'
              ? 'மாவட்ட அரசிதழ்கள் மற்றும் கல்வெட்டுப் பதிவுகளோடு ஒப்பிட்டு ஆய்வு அறிக்கை தயாரிக்கப்படுகிறது.'
              : 'Cross-referencing District Gazetteers and Epigraphia Indica.'}
          </p>
        </div>
      )}

      {researchResult && researchResult.report && (
        <div className="bg-white rounded-2xl p-6 border-2 border-[#C5A66A] shadow-lg space-y-4">
          <div className="flex items-center justify-between border-b border-gray-100 pb-3">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-[#C5A66A]" />
              <h3 className="text-lg font-extrabold text-[#172B40]">
                {lang === 'ta' ? 'சான்றாதார வரலாற்று ஆய்வு அறிக்கை' : 'Archival Research Report'}
              </h3>
            </div>
            <span className="text-xs font-bold px-2.5 py-1 bg-[#172B40] text-white rounded-md">
              {researchResult.query}
            </span>
          </div>

          <div className="prose prose-sm max-w-none text-[#172B40] text-xs sm:text-sm leading-relaxed whitespace-pre-line">
            {researchResult.report.raw_markdown || researchResult.raw_markdown}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchPage;
