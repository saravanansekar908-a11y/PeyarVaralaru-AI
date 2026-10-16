import React, { useState, useMemo, useCallback } from 'react';
import { useParams, useNavigate, Link, useSearchParams } from 'react-router-dom';
import { useTranslation } from '../services/LanguageContext';
import districtsDataRaw from '../data/districtsData.json';
import {
  Landmark,
  MapPin,
  Clock,
  BookOpen,
  ExternalLink,
  Sparkles,
  ShieldCheck,
  AlertCircle,
  CheckCircle2,
  Compass,
  Globe2,
  Award,
  Utensils,
  Mountain,
  Factory,
  History,
  Building2,
  AlertTriangle,
  ChevronRight,
  ChevronLeft,
  ArrowLeft,
} from 'lucide-react';

// ── New smart navigation sub-components ──────────────────────────────────────
import DistrictBreadcrumb from '../components/districts/DistrictBreadcrumb';
import DistrictSearchBar from '../components/districts/DistrictSearchBar';
import DistrictAlphaNav from '../components/districts/DistrictAlphaNav';
import DistrictViewToolbar from '../components/districts/DistrictViewToolbar';
import DistrictGridCard from '../components/districts/DistrictGridCard';
import DistrictListRow from '../components/districts/DistrictListRow';

// ─────────────────────────────────────────────────────────────────────────────

export const DistrictDashboard = () => {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { lang, t, localize } = useTranslation();

  const allDistricts = districtsDataRaw.districts || [];
  const officialSources = districtsDataRaw.official_sources || [];
  const researchGuidance = districtsDataRaw.research_guidance || [];

  // ── Selected district (detail view) ─────────────────────────────────────
  const selectedDistrict = useMemo(() => {
    const target = id || searchParams.get('select') || null;
    if (!target) return null;

    if (!isNaN(target)) {
      const matchNo = allDistricts.find((d) => String(d.no) === String(target));
      if (matchNo) return matchNo;
    }

    const cleanTarget = target.trim().toLowerCase();
    const matchName = allDistricts.find(
      (d) =>
        d.district_english.toLowerCase() === cleanTarget ||
        d.district_tamil.trim() === target.trim() ||
        (d.search_aliases && d.search_aliases.some((a) => a.toLowerCase() === cleanTarget))
    );
    if (matchName) return matchName;

    return allDistricts[0] || null;
  }, [id, searchParams, allDistricts]);

  // ── Directory filter/sort state ──────────────────────────────────────────
  const [districtQuery, setDistrictQuery] = useState('');
  const [selectedRegion, setSelectedRegion] = useState('all');
  const [activeLetter, setActiveLetter] = useState(null);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' | 'list'
  const [sortBy, setSortBy] = useState('number'); // 'number' | 'alpha' | 'region'

  const regions = [
    { id: 'all', label_ta: 'அனைத்து மண்டலங்கள்', label_en: 'All Regions' },
    { id: 'Northern', label_ta: 'வடக்கு மண்டலம்', label_en: 'Northern' },
    { id: 'Cauvery Delta', label_ta: 'காவிரி டெல்டா', label_en: 'Cauvery Delta' },
    { id: 'Kongu', label_ta: 'கொங்கு மண்டலம்', label_en: 'Kongu Nadu' },
    { id: 'Southern', label_ta: 'தெற்கு மண்டலம்', label_en: 'Southern Pandya' },
    { id: 'Western Ghats', label_ta: 'மேற்குத் தொடர்ச்சி மலை', label_en: 'Western Ghats' },
  ];

  // ── Filtered + sorted district list ─────────────────────────────────────
  const filteredDistricts = useMemo(() => {
    let result = allDistricts;

    // Region filter
    if (selectedRegion !== 'all') {
      result = result.filter((d) => {
        const regStr = `${d.region || ''} ${d.region_en || ''} ${d.region_ta || ''}`;
        return regStr.toLowerCase().includes(selectedRegion.toLowerCase());
      });
    }

    // Text search filter
    if (districtQuery.trim()) {
      const q = districtQuery.trim().toLowerCase();
      result = result.filter((d) => {
        const eng = d.district_english.toLowerCase();
        const tam = d.district_tamil.toLowerCase();
        const formerEn = (d.former_administrative_name_history_en || d.former_administrative_name_history || '').toLowerCase();
        const formerTa = (d.former_administrative_name_history_ta || '').toLowerCase();
        const ancientEn = (d.ancient_or_historical_name_context_en || d.ancient_or_historical_name_context || '').toLowerCase();
        const ancientTa = (d.ancient_or_historical_name_context_ta || '').toLowerCase();
        const aliases = (d.search_aliases || []).map((a) => a.toLowerCase());
        return (
          eng.includes(q) || tam.includes(q) || formerEn.includes(q) ||
          formerTa.includes(q) || ancientEn.includes(q) || ancientTa.includes(q) ||
          aliases.some((a) => a.includes(q))
        );
      });
    }

    // Bilingual letter filter (Tamil initial or English letter)
    if (activeLetter) {
      result = result.filter((d) => {
        const eng = (d.district_english || '')[0]?.toUpperCase();
        const tam = (d.district_tamil || '').trim()[0];
        return eng === activeLetter || tam === activeLetter;
      });
    }

    // Sort
    if (sortBy === 'alpha') {
      result = [...result].sort((a, b) =>
        a.district_english.localeCompare(b.district_english)
      );
    } else if (sortBy === 'region') {
      result = [...result].sort((a, b) =>
        (a.region || '').localeCompare(b.region || '')
      );
    } else {
      // Default: by district number
      result = [...result].sort((a, b) => a.no - b.no);
    }

    return result;
  }, [allDistricts, districtQuery, selectedRegion, activeLetter, sortBy]);

  const hasActiveFilters =
    districtQuery.trim().length > 0 ||
    selectedRegion !== 'all' ||
    activeLetter !== null;

  const handleClearAllFilters = useCallback(() => {
    setDistrictQuery('');
    setSelectedRegion('all');
    setActiveLetter(null);
  }, []);

  // ── Category icon helper (unchanged from original) ───────────────────────
  const getCategoryIcon = (category = '') => {
    const cat = category.toLowerCase();
    if (cat.includes('unesco') || cat.includes('architecture') || cat.includes('monument') || cat.includes('கட்டட'))
      return <Landmark className="w-4 h-4 text-[#C5A66A]" />;
    if (cat.includes('gi') || cat.includes('craft') || cat.includes('art') || cat.includes('textile') || cat.includes('கைவினை') || cat.includes('பட்டு'))
      return <Award className="w-4 h-4 text-emerald-600" />;
    if (cat.includes('culinary') || cat.includes('food') || cat.includes('sweet') || cat.includes('grape') || cat.includes('உணவு') || cat.includes('இனிப்பு'))
      return <Utensils className="w-4 h-4 text-amber-600" />;
    if (cat.includes('mountain') || cat.includes('hill') || cat.includes('waterfall') || cat.includes('ecology') || cat.includes('wildlife') || cat.includes('மலை') || cat.includes('அருவி'))
      return <Mountain className="w-4 h-4 text-sky-600" />;
    if (cat.includes('industrial') || cat.includes('engineering') || cat.includes('manufacturing') || cat.includes('தொழில்'))
      return <Factory className="w-4 h-4 text-purple-600" />;
    return <Sparkles className="w-4 h-4 text-[#C5A66A]" />;
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto py-2">

      {/* ── SMART NAVIGATION HEADER ─────────────────────────────────────────── */}
      <div className="flex flex-col gap-4 bg-white p-4 sm:p-5 rounded-2xl border border-gray-200 shadow-sm">

        {/* Row 1: Breadcrumb + Registry badge */}
        <div className="flex items-center justify-between gap-3 flex-wrap">
          <DistrictBreadcrumb selectedDistrict={selectedDistrict} />
          <span className="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 text-[10px] font-bold border border-emerald-200 shrink-0">
            {t('district.verifiedCount', '38 / 38 Verified')}
          </span>
        </div>

        {/* Row 2: Title */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#172B40] flex items-center justify-center text-[#C5A66A] shadow-inner shrink-0">
            <Compass className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] font-bold text-[#C5A66A] uppercase tracking-wider">
              {t('district.registryTitle', 'Official 38 Districts Registry')}
            </span>
            <h1 className="text-lg sm:text-xl font-extrabold text-[#172B40] leading-tight">
              {t('district.dashboardTitle', 'Tamil Nadu District Intelligence Dashboard')}
            </h1>
          </div>
        </div>

        {/* Row 3: Smart Search Bar */}
        <DistrictSearchBar
          value={districtQuery}
          onChange={setDistrictQuery}
          onClear={() => setDistrictQuery('')}
          onDistrictSelect={(no) => navigate(`/districts/${no}`)}
        />
      </div>

      {/* ── DISTRICT DETAIL VIEW (when selected) ────────────────────────────── */}
      {selectedDistrict && (
        <section className="space-y-6">
          {/* Navigation Bar: Back to All Districts & Prev/Next */}
          <div className="flex flex-wrap items-center justify-between gap-3 bg-white p-3 sm:p-4 rounded-2xl border border-gray-200 shadow-xs">
            <button
              type="button"
              onClick={() => {
                navigate('/districts');
                const mainEl = document.getElementById('main-content') || document.querySelector('main');
                if (mainEl) mainEl.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-[#172B40] hover:bg-[#20364F] text-white text-xs sm:text-sm font-bold shadow-sm transition-all group cursor-pointer"
            >
              <ArrowLeft className="w-4 h-4 transition-transform group-hover:-translate-x-1" />
              <span>{lang === 'ta' ? 'அனைத்து 38 மாவட்டங்களுக்கும் திரும்பு' : 'Back to All 38 Districts'}</span>
            </button>

            <div className="flex items-center gap-2">
              <button
                type="button"
                disabled={selectedDistrict.no <= 1}
                onClick={() => {
                  navigate(`/districts/${selectedDistrict.no - 1}`);
                  const mainEl = document.getElementById('main-content') || document.querySelector('main');
                  if (mainEl) mainEl.scrollTo({ top: 0, behavior: 'smooth' });
                }}
                className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg border border-gray-200 text-xs font-bold text-[#172B40] disabled:opacity-30 disabled:cursor-not-allowed hover:bg-[#F7F4ED] hover:border-[#C5A66A] transition-colors cursor-pointer"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
                <span>{lang === 'ta' ? 'முந்தைய' : 'Prev'}</span>
              </button>

              <span className="px-2.5 py-1 rounded-md bg-[#F7F4ED] text-xs font-black text-[#172B40] border border-gray-200">
                {selectedDistrict.no} / 38
              </span>

              <button
                type="button"
                disabled={selectedDistrict.no >= 38}
                onClick={() => {
                  navigate(`/districts/${selectedDistrict.no + 1}`);
                  const mainEl = document.getElementById('main-content') || document.querySelector('main');
                  if (mainEl) mainEl.scrollTo({ top: 0, behavior: 'smooth' });
                }}
                className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg border border-gray-200 text-xs font-bold text-[#172B40] disabled:opacity-30 disabled:cursor-not-allowed hover:bg-[#F7F4ED] hover:border-[#C5A66A] transition-colors cursor-pointer"
              >
                <span>{lang === 'ta' ? 'அடுத்தது' : 'Next'}</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* A. District Identity Header */}
          <div className="relative rounded-3xl overflow-hidden shadow-xl border border-[#2A3E54] bg-[#0F1D2C] text-white">
            <div
              className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-25 mix-blend-luminosity scale-105 transition-transform duration-700"
              style={{ backgroundImage: `url('${selectedDistrict.hero_image || '/images/hero-temple.jpg'}')` }}
            />
            <div className="absolute inset-0 bg-gradient-to-r from-[#0F1D2C] via-[#0F1D2C]/90 to-[#172B40]/80" />
            <div className="absolute right-0 top-0 w-96 h-96 bg-[#C5A66A]/10 rounded-full blur-3xl pointer-events-none" />

            <div className="relative z-10 p-6 sm:p-10 lg:p-12 space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                  <span className="px-3 py-1 rounded-full bg-[#C5A66A] text-[#172B40] text-xs font-extrabold shadow-sm">
                    {lang === 'ta' ? `மாவட்டம் ${selectedDistrict.no} / 38` : `District ${selectedDistrict.no} of 38`}
                  </span>
                  <span className="px-3 py-1 rounded-full bg-white/10 backdrop-blur-md text-gray-200 text-xs font-semibold border border-white/20">
                    {lang === 'ta' ? (selectedDistrict.region_ta || selectedDistrict.region) : (selectedDistrict.region_en || selectedDistrict.region)}
                  </span>
                </div>

                {selectedDistrict.official_district_portal && (
                  <a
                    href={selectedDistrict.official_district_portal}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-700/60 text-xs font-bold transition-colors"
                  >
                    <span>{t('district.officialWebsite', 'Official Website')}</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>

              <div className="space-y-2">
                <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight">
                  {lang === 'ta' ? selectedDistrict.district_tamil : selectedDistrict.district_english}
                </h2>
                <p className="text-sm sm:text-base text-gray-200/90 max-w-3xl leading-relaxed pt-1 font-normal">
                  {lang === 'ta'
                    ? (selectedDistrict.intro_ta || selectedDistrict.intro_en)
                    : (selectedDistrict.intro_en || selectedDistrict.intro_ta)}
                </p>
              </div>

              {selectedDistrict.search_aliases && selectedDistrict.search_aliases.length > 0 && (
                <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-white/10 text-xs">
                  <span className="text-[#C5A66A] font-semibold">
                    {t('district.searchAliases', 'Search Aliases & Variants:')}
                  </span>
                  {(() => {
                    const primary = selectedDistrict.search_aliases.filter((alias) => {
                      const isTamilScript = /[\u0B80-\u0BFF]/.test(alias);
                      return lang === 'ta' ? isTamilScript : !isTamilScript;
                    });
                    const toShow = primary.length > 0 ? primary : selectedDistrict.search_aliases.slice(0, 3);
                    return toShow.map((alias, idx) => (
                      <span
                        key={idx}
                        className="px-2.5 py-0.5 rounded-md bg-white/10 text-gray-200 text-[11px] font-medium border border-white/15"
                      >
                        {alias}
                      </span>
                    ));
                  })()}
                </div>
              )}
            </div>
          </div>

          {/* Quick-Glance Metadata Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2.5 sm:gap-3">
            <div className="p-3 sm:p-3.5 bg-white rounded-xl border border-gray-200 shadow-xs flex items-center gap-2.5 sm:gap-3 min-w-0">
              <div className="w-8 h-8 rounded-lg bg-[#F7F4ED] text-[#C5A66A] flex items-center justify-center shrink-0">
                <MapPin className="w-4 h-4" />
              </div>
              <div className="min-w-0 flex-1">
                <span className="text-[10px] text-gray-500 uppercase font-bold block">{t('district.district', 'District')}</span>
                <span className="text-xs font-extrabold text-[#172B40] truncate block">
                  {lang === 'ta' ? selectedDistrict.district_tamil : selectedDistrict.district_english}
                </span>
              </div>
            </div>

            <div className="p-3 sm:p-3.5 bg-white rounded-xl border border-gray-200 shadow-xs flex items-center gap-2.5 sm:gap-3 min-w-0">
              <div className="w-8 h-8 rounded-lg bg-[#F7F4ED] text-[#C5A66A] flex items-center justify-center shrink-0">
                <History className="w-4 h-4" />
              </div>
              <div className="min-w-0 flex-1">
                <span className="text-[10px] text-gray-500 uppercase font-bold block">{t('district.historicalName', 'Historical Name')}</span>
                <span className="text-xs font-bold text-[#172B40] truncate block">
                  {lang === 'ta' ? (selectedDistrict.ancient_or_historical_name_context_ta || selectedDistrict.district_tamil) : (selectedDistrict.ancient_or_historical_name_context_en || selectedDistrict.district_english)}
                </span>
              </div>
            </div>

            <div className="p-3 sm:p-3.5 bg-white rounded-xl border border-gray-200 shadow-xs flex items-center gap-2.5 sm:gap-3 min-w-0">
              <div className="w-8 h-8 rounded-lg bg-[#F7F4ED] text-[#C5A66A] flex items-center justify-center shrink-0">
                <Building2 className="w-4 h-4" />
              </div>
              <div className="min-w-0 flex-1">
                <span className="text-[10px] text-gray-500 uppercase font-bold block">{t('district.administrativeHistory', 'Administrative History')}</span>
                <span className="text-xs font-bold text-[#172B40] truncate block">
                  {lang === 'ta' ? (selectedDistrict.former_administrative_name_history_ta || 'பதிவு செய்யப்பட்டுள்ளது') : (selectedDistrict.former_administrative_name_history_en || 'Documented')}
                </span>
              </div>
            </div>

            <div className="p-3 sm:p-3.5 bg-white rounded-xl border border-gray-200 shadow-xs flex items-center gap-2.5 sm:gap-3 min-w-0 col-span-2 sm:col-span-1">
              <div className="w-8 h-8 rounded-lg bg-[#F7F4ED] text-[#C5A66A] flex items-center justify-center shrink-0">
                <Award className="w-4 h-4" />
              </div>
              <div className="min-w-0 flex-1">
                <span className="text-[10px] text-gray-500 uppercase font-bold block">{t('district.specialFeatures', 'Special Features')}</span>
                <span className="text-xs font-bold text-emerald-800 truncate block">
                  {selectedDistrict.specialities ? `${selectedDistrict.specialities.length} ${lang === 'ta' ? 'சிறப்புகள்' : 'Highlights'}` : '-'}
                </span>
              </div>
            </div>
          </div>

          {/* B & E. Historical Evolution & Administrative Context */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Timeline Column (Span 2) */}
            <div className="lg:col-span-2 bg-white rounded-2xl p-6 border border-gray-200 shadow-sm space-y-6">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <div className="flex items-center gap-2">
                  <Clock className="w-5 h-5 text-[#C5A66A]" />
                  <h3 className="text-base sm:text-lg font-bold text-[#172B40]">
                    {t('district.evolutionTitle', 'Historical Names & Administrative Evolution')}
                  </h3>
                </div>
                <span className="text-xs font-semibold text-gray-500 bg-[#F7F4ED] px-2.5 py-1 rounded-md border border-gray-200">
                  {t('district.gazetteerGrounded', 'Gazetteer Grounded')}
                </span>
              </div>

              <div className="space-y-6">
                {selectedDistrict.timeline && selectedDistrict.timeline.map((item, idx) => (
                  <div key={idx} className="relative pl-6 border-l-2 border-[#C5A66A] space-y-1.5">
                    <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-white border-2 border-[#C5A66A]" />
                    <div className="flex flex-wrap items-center justify-between gap-1">
                      <span className="text-xs font-extrabold text-[#172B40]">
                        {lang === 'ta' ? (item.title_ta || item.title) : (item.title_en || item.title)}
                      </span>
                      <span className="text-[11px] font-bold px-2 py-0.5 rounded bg-[#F7F4ED] text-[#C5A66A] border border-gray-200">
                        {lang === 'ta' ? (item.category_ta || item.category) : (item.category_en || item.category)}
                      </span>
                    </div>
                    <p className="text-xs sm:text-sm text-gray-700 leading-relaxed font-normal">
                      {lang === 'ta' ? (item.description_ta || item.description) : (item.description_en || item.description)}
                    </p>
                  </div>
                ))}
              </div>

              <div className="p-4 rounded-xl bg-[#F7F4ED] border border-[#E8D8B0] flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-[#C5A66A] shrink-0 mt-0.5" />
                <div className="space-y-1 text-xs text-gray-700 leading-relaxed">
                  <span className="font-bold text-[#172B40]">
                    {t('district.verificationPolicyTitle', 'Scholarly Verification Standard:')}
                  </span>
                  <p>
                    {t('district.verificationPolicyDesc', 'Former administrative district, colonial spelling variant, ancient settlement, and historical region are distinct categories.')}
                  </p>
                </div>
              </div>
            </div>

            {/* Official Record Summary Card */}
            <div className="bg-white rounded-2xl p-6 border border-gray-200 shadow-sm space-y-5 flex flex-col justify-between">
              <div className="space-y-4">
                <div className="flex items-center gap-2 border-b border-gray-100 pb-3">
                  <Building2 className="w-5 h-5 text-[#C5A66A]" />
                  <h3 className="text-base font-bold text-[#172B40]">
                    {t('district.metadataTitle', 'Official Record Metadata')}
                  </h3>
                </div>

                <div className="space-y-3.5 text-xs">
                  <div>
                    <span className="text-gray-500 font-medium block">
                      {t('district.formerAdminHistory', 'Former Administrative History:')}
                    </span>
                    <p className="font-semibold text-[#172B40] mt-0.5 leading-snug">
                      {lang === 'ta'
                        ? (selectedDistrict.former_administrative_name_history_ta || selectedDistrict.former_administrative_name_history)
                        : (selectedDistrict.former_administrative_name_history_en || selectedDistrict.former_administrative_name_history)}
                    </p>
                  </div>

                  <div>
                    <span className="text-gray-500 font-medium block">
                      {t('district.ancientContext', 'Ancient / Historical Context:')}
                    </span>
                    <p className="font-semibold text-[#172B40] mt-0.5 leading-snug">
                      {lang === 'ta'
                        ? (selectedDistrict.ancient_or_historical_name_context_ta || selectedDistrict.ancient_or_historical_name_context)
                        : (selectedDistrict.ancient_or_historical_name_context_en || selectedDistrict.ancient_or_historical_name_context)}
                    </p>
                  </div>

                  <div>
                    <span className="text-gray-500 font-medium block">
                      {t('district.changeAuthorityNote', 'Change Date / Verification Note:')}
                    </span>
                    <p className="font-semibold text-[#172B40] mt-0.5 leading-snug">
                      {lang === 'ta'
                        ? (selectedDistrict.change_date_authority_verification_notes_ta || selectedDistrict.change_date_authority_verification_notes)
                        : (selectedDistrict.change_date_authority_verification_notes_en || selectedDistrict.change_date_authority_verification_notes)}
                    </p>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-gray-100 space-y-2">
                <a
                  href={selectedDistrict.official_district_portal}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full py-2.5 px-4 bg-[#172B40] hover:bg-[#20364F] text-white rounded-xl text-xs font-bold transition-all shadow-sm flex items-center justify-center gap-2"
                >
                  <Globe2 className="w-4 h-4 text-[#C5A66A]" />
                  <span>{t('district.visitPortal', 'Visit Official District Portal')}</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>

                <Link
                  to={`/ask?district=${encodeURIComponent(selectedDistrict.district_english)}`}
                  className="w-full py-2 px-4 bg-[#F7F4ED] hover:bg-[#eae5d7] text-[#172B40] rounded-xl text-xs font-semibold transition-all border border-gray-200 flex items-center justify-center gap-1.5"
                >
                  <Sparkles className="w-3.5 h-3.5 text-[#C5A66A]" />
                  <span>{t('district.askAboutDistrict', 'Ask History AI about this District')}</span>
                </Link>
              </div>
            </div>
          </div>

          {/* C. District Specialities */}
          <div className="space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-200 pb-3">
              <div>
                <div className="inline-flex items-center gap-1 text-xs font-bold text-[#C5A66A] uppercase tracking-wider mb-1">
                  <Award className="w-4 h-4" />
                  <span>{t('district.specialityTitle', 'District Specialities')}</span>
                </div>
                <h3 className="text-xl sm:text-2xl font-extrabold text-[#172B40]">
                  {t('district.whatMakesSpecial', 'What Makes {name} Special?', {
                    name: lang === 'ta' ? selectedDistrict.district_tamil : selectedDistrict.district_english,
                  })}
                </h3>
                <p className="text-xs sm:text-sm text-gray-600">
                  {t('district.specialitySubtitle', 'Evidence-grounded highlights covering GI products, architectural landmarks, natural heritage, and local industries.')}
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {selectedDistrict.specialities && selectedDistrict.specialities.map((item, index) => (
                <div
                  key={index}
                  className="group bg-white rounded-2xl p-5 border border-gray-200 shadow-sm hover:shadow-md hover:border-[#C5A66A] transition-all flex flex-col justify-between space-y-4"
                >
                  <div className="space-y-2.5">
                    <div className="flex items-start justify-between gap-2">
                      <div className="w-9 h-9 rounded-xl bg-[#F7F4ED] border border-[#C5A66A]/30 flex items-center justify-center shrink-0">
                        {getCategoryIcon(item.category)}
                      </div>
                      <span className="px-2 py-0.5 rounded bg-gray-100 text-gray-700 text-[10px] font-semibold border border-gray-200 text-right truncate max-w-[180px]">
                        {lang === 'ta' ? (item.category_ta || item.category) : (item.category_en || item.category)}
                      </span>
                    </div>
                    <h4 className="font-bold text-base text-[#172B40] group-hover:text-[#C5A66A] transition-colors leading-snug">
                      {lang === 'ta' ? (item.name_ta || item.name) : (item.name_en || item.name)}
                    </h4>
                    <p className="text-xs text-gray-600 leading-relaxed font-normal">
                      {lang === 'ta' ? (item.explanation_ta || item.explanation) : (item.explanation_en || item.explanation)}
                    </p>
                  </div>

                  <div className="pt-3 border-t border-gray-100 space-y-2">
                    <div className="text-[11px] text-[#172B40] font-semibold flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                      <span>{lang === 'ta' ? (item.significance_ta || item.significance) : (item.significance_en || item.significance)}</span>
                    </div>
                    {item.source_url && (
                      <a
                        href={item.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-[11px] font-bold text-[#C5A66A] hover:underline"
                      >
                        <span>{t('district.referenceLink', 'Reference Link')}</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* D. Famous Places */}
          {selectedDistrict.famous_places && selectedDistrict.famous_places.length > 0 && (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-gray-200 pb-3">
                <div>
                  <h3 className="text-xl sm:text-2xl font-extrabold text-[#172B40]">
                    {t('district.famousPlacesTitle', 'Famous Places & Heritage Sites')}
                  </h3>
                  <p className="text-xs sm:text-sm text-gray-600">
                    {t('district.famousPlacesSubtitle', 'Notable historical sanctuaries, monuments, and ecological landmarks.')}
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                {selectedDistrict.famous_places.map((place, idx) => (
                  <div
                    key={idx}
                    className="bg-white rounded-2xl p-5 border border-gray-200 shadow-sm hover:shadow-md hover:border-[#C5A66A] transition-all flex flex-col justify-between space-y-3"
                  >
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] font-bold text-[#C5A66A] uppercase tracking-wider">
                          {lang === 'ta' ? (place.category_ta || place.category) : (place.category_en || place.category)}
                        </span>
                        <Landmark className="w-4 h-4 text-gray-400" />
                      </div>
                      <h4 className="font-bold text-base text-[#172B40]">
                        {lang === 'ta' ? (place.name_ta || place.name) : (place.name_en || place.name)}
                      </h4>
                      <p className="text-xs text-gray-600 leading-relaxed font-normal">
                        {lang === 'ta' ? (place.description_ta || place.description) : (place.description_en || place.description)}
                      </p>
                    </div>

                    {place.link && (
                      <div className="pt-2 border-t border-gray-100">
                        <a
                          href={place.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 text-xs font-bold text-[#172B40] hover:text-[#C5A66A] transition-colors"
                        >
                          <span>{t('district.exploreSite', 'Explore Site')}</span>
                          <ChevronRight className="w-3.5 h-3.5" />
                        </a>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>
      )}

      {/* ── INTERACTIVE DISTRICT DIRECTORY ─────────────────────────────────── */}
      <section className="space-y-5 pt-4 border-t border-gray-200">
        {/* Directory section header */}
        <div className="flex flex-col gap-1">
          <div className="inline-flex items-center gap-1.5 text-xs font-bold text-[#C5A66A] uppercase tracking-wider">
            <Compass className="w-4 h-4" />
            <span>{t('district.interactiveDirectory', 'Interactive District Directory')}</span>
          </div>
          <h2 className="text-xl sm:text-2xl font-extrabold text-[#172B40]">
            {t('district.directoryTitle', 'All 38 Districts of Tamil Nadu')}
          </h2>
          <p className="text-xs sm:text-sm text-gray-600">
            {t('district.directorySubtitle', 'Select any district to explore its complete heritage intelligence and archival records.')}
          </p>
        </div>

        {/* View Toolbar (grid/list toggle + sort + region chips) */}
        <DistrictViewToolbar
          viewMode={viewMode}
          onViewChange={setViewMode}
          sortBy={sortBy}
          onSortChange={setSortBy}
          regions={regions}
          selectedRegion={selectedRegion}
          onRegionChange={(id) => setSelectedRegion(id)}
          lang={lang}
        />

        {/* A–Z / Tamil Alpha Nav */}
        <DistrictAlphaNav
          districts={allDistricts}
          filteredCount={filteredDistricts.length}
          totalCount={allDistricts.length}
          activeLetter={activeLetter}
          onLetterClick={(letter) => {
            setActiveLetter(letter);
            if (id) {
              navigate('/districts');
            }
          }}
          hasActiveFilters={hasActiveFilters}
          onClearFilters={handleClearAllFilters}
        />

        {/* District Grid or List */}
        {filteredDistricts.length === 0 ? (
          <div className="bg-white rounded-2xl p-10 border border-gray-200 text-center space-y-3">
            <AlertCircle className="w-8 h-8 text-amber-500 mx-auto" />
            <h4 className="font-bold text-[#172B40]">
              {t('district.noResultsTitle', 'No matching districts')}
            </h4>
            <p className="text-xs text-gray-500">
              {t('district.noResultsDesc', 'Try a different search term, letter, or region filter.')}
            </p>
            <button
              onClick={handleClearAllFilters}
              className="mt-2 px-4 py-1.5 bg-[#172B40] text-white text-xs font-bold rounded-lg hover:bg-[#20364F] transition-colors"
            >
              {t('district.resetFilters', 'Reset Filters')}
            </button>
          </div>
        ) : viewMode === 'list' ? (
          <div className="flex flex-col gap-2">
            {filteredDistricts.map((d) => (
              <DistrictListRow key={d.no} district={d} />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {filteredDistricts.map((d) => (
              <DistrictGridCard key={d.no} district={d} />
            ))}
          </div>
        )}
      </section>

      {/* Official Sources & Research Guidance */}
      <section className="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-100 pb-3">
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-[#C5A66A]" />
            <h3 className="text-lg font-bold text-[#172B40]">
              {t('district.officialSourcesTitle', 'Official Sources & Research Guidance')}
            </h3>
          </div>
          <span className="text-xs text-gray-500">
            {t('district.fromWorksheets', 'Archived 38 District Sources')}
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-[#C5A66A] uppercase tracking-wider">
              {t('district.govtDirectories', 'Official Government Directories')}
            </h4>
            <div className="space-y-2.5">
              {officialSources.map((s, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-[#F7F4ED] border border-gray-200 text-xs space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-[#172B40]">{lang === 'ta' ? (s.source_ta || s.source) : (s.source_en || s.source)}</span>
                    {s.direct_url && (
                      <a
                        href={s.direct_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[#C5A66A] hover:underline flex items-center gap-1 font-semibold"
                      >
                        <span>{t('district.open', 'Open')}</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    )}
                  </div>
                  <p className="text-gray-600 text-[11px] leading-relaxed">
                    {lang === 'ta' ? (s.use_notes_ta || s.use_notes) : (s.use_notes_en || s.use_notes)}
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="space-y-3">
            <h4 className="text-xs font-bold text-[#C5A66A] uppercase tracking-wider">
              {t('district.researchDistinctions', 'Research Distinctions & Standards')}
            </h4>
            <div className="space-y-2.5">
              {researchGuidance.map((g, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-[#F7F4ED] border border-gray-200 text-xs space-y-1">
                  <div className="font-bold text-[#172B40] flex items-center gap-1.5">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                    <span>{lang === 'ta' ? (g.topic_ta || g.topic) : (g.topic_en || g.topic)}</span>
                  </div>
                  <p className="text-gray-600 text-[11px] leading-relaxed">
                    {lang === 'ta' ? (g.guidance_ta || g.guidance) : (g.guidance_en || g.guidance)}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default DistrictDashboard;
