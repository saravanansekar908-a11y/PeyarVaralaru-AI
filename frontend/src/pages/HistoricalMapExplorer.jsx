import React, { useState, useEffect, useMemo } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useTranslation } from '../services/LanguageContext';
import { 
  getHistoricalMaps, 
  getHistoricalMap, 
  getMapPeriods, 
  getMapPlaces, 
  getMapObservationCategories 
} from '../services/api';
import HistoricalMapWorkspace from '../components/maps/HistoricalMapWorkspace';
import StatusBadge from '../components/StatusBadge';
import { 
  Search, 
  Filter, 
  Layers, 
  SplitSquareVertical, 
  Columns, 
  FileSearch, 
  Compass, 
  ExternalLink, 
  Info, 
  CheckCircle2, 
  AlertCircle, 
  BookOpen, 
  MapPin, 
  Landmark, 
  Calendar, 
  Maximize2,
  ArrowRight,
  ShieldCheck,
  Building
} from 'lucide-react';

export const HistoricalMapExplorer = () => {
  const { lang, t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();

  // Data states
  const [maps, setMaps] = useState([]);
  const [selectedMap, setSelectedMap] = useState(null);
  const [selectedMapDetail, setSelectedMapDetail] = useState(null);
  const [periods, setPeriods] = useState([]);
  const [placesList, setPlacesList] = useState([]);
  const [categories, setCategories] = useState([]);
  
  // Loading & error
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState(null);

  // Filters & Search
  const initialQuery = searchParams.get('q') || searchParams.get('place') || '';
  const [searchQuery, setSearchQuery] = useState(initialQuery);
  const [selectedDistrict, setSelectedDistrict] = useState(searchParams.get('district') || 'all');
  const [selectedPeriod, setSelectedPeriod] = useState(searchParams.get('period') || 'all');
  const [georeferencedOnly, setGeoreferencedOnly] = useState(false);

  // Active Comparison Mode: 'side_by_side' | 'swipe' | 'transparency' | 'inspection'
  const [comparisonMode, setComparisonMode] = useState('side_by_side');

  // Change Detection Category filter
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Focused observation for map animation
  const [focusedObservation, setFocusedObservation] = useState(null);

  // Quick suggested places
  const recommendedPlaces = [
    { name: 'Tiruvannamalai', name_ta: 'திருவண்ணாமலை' },
    { name: 'Arani', name_ta: 'ஆரணி' },
    { name: 'Kalambur', name_ta: 'களம்பூர்' },
    { name: 'Chennai', name_ta: 'சென்னை' },
    { name: 'Coimbatore', name_ta: 'கோயம்புத்தூர்' },
    { name: 'Villupuram', name_ta: 'விழுப்புரம்' },
    { name: 'Thanjavur', name_ta: 'தஞ்சாவூர்' },
    { name: 'Madurai', name_ta: 'மதுரை' },
  ];

  // Load initial filter options (periods, places, categories)
  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const [periodsData, placesData, catData] = await Promise.all([
          getMapPeriods(),
          getMapPlaces(),
          getMapObservationCategories(),
        ]);
        setPeriods(periodsData || []);
        setPlacesList(placesData || []);
        setCategories(catData || []);
      } catch (err) {
        console.error('Failed to load map metadata options', err);
      }
    };
    fetchMetadata();
  }, []);

  // Fetch Maps list matching current filters
  useEffect(() => {
    const fetchMaps = async () => {
      setLoading(true);
      setError(null);
      try {
        const params = {};
        if (searchQuery.trim()) params.q = searchQuery.trim();
        if (selectedDistrict !== 'all') params.district = selectedDistrict;
        if (selectedPeriod !== 'all') params.period = selectedPeriod;
        if (georeferencedOnly) params.georeferencing_status = 'georeferenced';

        const data = await getHistoricalMaps(params);
        setMaps(data);

        // Auto-select map
        if (data.length > 0) {
          const mapIdParam = searchParams.get('id');
          const matched = mapIdParam ? data.find((m) => m.id === parseInt(mapIdParam)) : null;
          setSelectedMap(matched || data[0]);
        } else {
          setSelectedMap(null);
          setSelectedMapDetail(null);
        }
      } catch (err) {
        console.error('Error fetching historical maps', err);
        setError('Failed to load historical maps.');
      } finally {
        setLoading(false);
      }
    };

    fetchMaps();
  }, [searchQuery, selectedDistrict, selectedPeriod, georeferencedOnly, searchParams]);

  // Fetch full details & observations for the selected map
  useEffect(() => {
    if (!selectedMap) return;

    const fetchDetail = async () => {
      setDetailLoading(true);
      try {
        const detail = await getHistoricalMap(selectedMap.id);
        setSelectedMapDetail(detail);
      } catch (err) {
        console.error('Error fetching map details', err);
      } finally {
        setDetailLoading(false);
      }
    };

    fetchDetail();
  }, [selectedMap]);

  // Filter observations by selected category
  const filteredObservations = useMemo(() => {
    if (!selectedMapDetail?.observations) return [];
    if (selectedCategory === 'all') return selectedMapDetail.observations;
    return selectedMapDetail.observations.filter((obs) => obs.category === selectedCategory);
  }, [selectedMapDetail, selectedCategory]);

  // Distinct districts from places list
  const districtOptions = useMemo(() => {
    const dists = new Set();
    placesList.forEach((p) => {
      if (p.district) dists.add(p.district);
    });
    return Array.from(dists).sort();
  }, [placesList]);

  // Handle place pill selection
  const handleSelectPlace = (placeName) => {
    setSearchQuery(placeName);
    setSearchParams({ q: placeName });
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8 pb-16">
      {/* Page Header */}
      <div className="bg-[#172B40] text-white rounded-2xl p-6 sm:p-8 border border-[#2C3F55] shadow-lg relative overflow-hidden">
        {/* Subtle decorative background watermark */}
        <div className="absolute right-0 top-0 translate-x-8 -translate-y-8 w-64 h-64 opacity-5 pointer-events-none">
          <Compass className="w-full h-full text-white" />
        </div>

        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-[#C5A66A]/20 text-[#C5A66A] border border-[#C5A66A]/40 flex items-center gap-1.5">
              <Compass className="w-3.5 h-3.5" />
              {lang === 'ta' ? 'காப்பக வரைபட ஒப்பீட்டுத் தளம்' : 'Archival Cartography Platform'}
            </span>
            <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-[#1F3A57] text-gray-300 border border-[#2C3F55]">
              1710s – 1890s
            </span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-bold tracking-tight text-white font-serif">
            {t('maps.title', 'Historical Map Explorer')}
          </h1>

          <p className="text-sm sm:text-base text-gray-300 leading-relaxed">
            {t('maps.subtitle', "Explore Tamil Nadu's changing geography through historical evidence.")}
          </p>

          <p className="text-xs text-[#C5A66A]/90 font-medium">
            {t('maps.tagline', 'Authentic cartographic records from 1710s to 1890s cross-referenced with modern geospatial layers.')}
          </p>
        </div>
      </div>

      {/* Search & Filter Toolbar */}
      <div className="bg-white rounded-2xl p-5 border border-[#E2E8F0] shadow-sm space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-3">
          {/* Search Input */}
          <div className="md:col-span-5 relative">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={t('maps.searchPlaceholder', 'Search place in Tamil or English (e.g., Tiruvannamalai, Arani, Kalambur, Chennai)...')}
              className="w-full pl-10 pr-4 py-2.5 bg-[#F8FAFC] border border-[#CBD5E1] rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#C5A66A] focus:border-[#C5A66A] transition-all"
            />
            {searchQuery && (
              <button
                onClick={() => {
                  setSearchQuery('');
                  setSearchParams({});
                }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400 hover:text-gray-600 bg-gray-200 hover:bg-gray-300 rounded-full w-5 h-5 flex items-center justify-center"
              >
                ✕
              </button>
            )}
          </div>

          {/* District Filter */}
          <div className="md:col-span-3">
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              className="w-full px-3 py-2.5 bg-[#F8FAFC] border border-[#CBD5E1] rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#C5A66A] text-[#172B40]"
            >
              <option value="all">{t('maps.allDistricts', 'All Districts')}</option>
              {districtOptions.map((dist) => (
                <option key={dist} value={dist}>
                  {dist}
                </option>
              ))}
            </select>
          </div>

          {/* Period Filter */}
          <div className="md:col-span-2">
            <select
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
              className="w-full px-3 py-2.5 bg-[#F8FAFC] border border-[#CBD5E1] rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#C5A66A] text-[#172B40]"
            >
              <option value="all">{t('maps.allPeriods', 'All Periods')}</option>
              {periods.map((p, idx) => {
                const val = typeof p === 'string' ? p : (p?.period || `period-${idx}`);
                const label = typeof p === 'string' ? p : (lang === 'ta' ? (p?.period_tamil || p?.period) : p?.period);
                return (
                  <option key={val} value={val}>
                    {label}
                  </option>
                );
              })}
            </select>
          </div>

          {/* Georeferenced Only Checkbox */}
          <div className="md:col-span-2 flex items-center">
            <label className="flex items-center gap-2 cursor-pointer text-xs font-semibold text-[#172B40]">
              <input
                type="checkbox"
                checked={georeferencedOnly}
                onChange={(e) => setGeoreferencedOnly(e.target.checked)}
                className="rounded text-[#C5A66A] focus:ring-[#C5A66A] w-4 h-4 accent-[#C5A66A]"
              />
              <span>{t('maps.georeferencedOnly', 'Georeferenced Only')}</span>
            </label>
          </div>
        </div>

        {/* Quick Recommended Place Pills */}
        <div className="flex flex-wrap items-center gap-1.5 pt-2 border-t border-gray-100 text-xs">
          <span className="text-gray-500 font-medium mr-1 flex items-center gap-1">
            <MapPin className="w-3.5 h-3.5 text-[#C5A66A]" />
            {t('maps.recommendations', 'Suggested Places')}:
          </span>
          {recommendedPlaces.map((p) => (
            <button
              key={p.name}
              onClick={() => handleSelectPlace(p.name)}
              className={`px-2.5 py-1 rounded-lg border transition-all text-xs font-medium ${
                searchQuery.toLowerCase().includes(p.name.toLowerCase())
                  ? 'bg-[#172B40] text-white border-[#172B40]'
                  : 'bg-[#F8FAFC] text-gray-700 border-gray-200 hover:bg-gray-100 hover:border-gray-300'
              }`}
            >
              {lang === 'ta' ? p.name_ta : p.name}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content Area: Maps or Empty State */}
      {loading ? (
        <div className="bg-white rounded-2xl p-16 border border-gray-200 flex flex-col items-center justify-center text-center space-y-3">
          <div className="w-10 h-10 border-4 border-[#C5A66A] border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-semibold text-[#172B40]">
            {lang === 'ta' ? 'காப்பக வரைபடங்கள் ஏற்றப்படுகின்றன...' : 'Loading archival cartographic records...'}
          </p>
        </div>
      ) : maps.length === 0 ? (
        /* Empty State with Official Archival Portals */
        <div className="bg-white rounded-2xl p-8 sm:p-12 border border-[#E2E8F0] shadow-sm text-center max-w-2xl mx-auto space-y-6">
          <div className="w-16 h-16 mx-auto rounded-full bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-700">
            <FileSearch className="w-8 h-8" />
          </div>

          <div className="space-y-2">
            <h3 className="text-xl font-bold text-[#172B40]">
              {t('maps.noMapsFound', 'No Historical Maps Found in Catalog')}
            </h3>
            <p className="text-sm text-gray-600 leading-relaxed">
              {t(
                'maps.noMapsFoundDesc',
                'Our catalog strictly presents genuine, traceable cartography from official archival institutions. No verified map matches your search parameters.'
              )}
            </p>
          </div>

          <div className="pt-4 border-t border-gray-100 text-left space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-500">
              {t('maps.officialRepositories', 'Explore Official Archival Repositories')}:
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <a
                href="https://nationalarchives.nic.in"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between p-3 rounded-xl bg-[#F8FAFC] border border-gray-200 hover:border-[#C5A66A] hover:bg-[#FDF9F0] transition-colors font-medium text-gray-800"
              >
                <span>{t('maps.nationalArchives', 'National Archives of India (NAI)')}</span>
                <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
              </a>
              <a
                href="https://surveyofindia.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between p-3 rounded-xl bg-[#F8FAFC] border border-gray-200 hover:border-[#C5A66A] hover:bg-[#FDF9F0] transition-colors font-medium text-gray-800"
              >
                <span>{t('maps.surveyOfIndia', 'Survey of India Map Archive')}</span>
                <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
              </a>
              <a
                href="https://www.archives.tn.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between p-3 rounded-xl bg-[#F8FAFC] border border-gray-200 hover:border-[#C5A66A] hover:bg-[#FDF9F0] transition-colors font-medium text-gray-800"
              >
                <span>{t('maps.tnArchives', 'Tamil Nadu Archives & Historical Research')}</span>
                <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
              </a>
              <a
                href="https://www.archaeology.tn.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between p-3 rounded-xl bg-[#F8FAFC] border border-gray-200 hover:border-[#C5A66A] hover:bg-[#FDF9F0] transition-colors font-medium text-gray-800"
              >
                <span>{t('maps.tnArchaeology', 'Department of Archaeology, Tamil Nadu')}</span>
                <ExternalLink className="w-3.5 h-3.5 text-gray-400" />
              </a>
            </div>
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Map Catalog Selector & Comparison Mode Switcher */}
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            {/* Map Selection Pills/Selector */}
            <div className="flex items-center gap-2 overflow-x-auto pb-2 lg:pb-0 scrollbar-thin">
              <span className="text-xs font-bold text-gray-500 uppercase tracking-wider shrink-0">
                {maps.length} {lang === 'ta' ? 'வரைபடங்கள்' : 'Maps'}:
              </span>
              {maps.map((m) => {
                const isSelected = selectedMap?.id === m.id;
                return (
                  <button
                    key={m.id}
                    onClick={() => {
                      setSelectedMap(m);
                      setFocusedObservation(null);
                    }}
                    className={`px-3 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all border shrink-0 flex items-center gap-1.5 ${
                      isSelected
                        ? 'bg-[#172B40] text-white border-[#172B40] shadow-md'
                        : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'
                    }`}
                  >
                    <span>{lang === 'ta' ? (m.place_name_tamil || m.place_name) : m.place_name}</span>
                    <span className={`text-[10px] px-1.5 py-0.2 rounded-md ${
                      isSelected ? 'bg-[#C5A66A] text-[#172B40]' : 'bg-gray-100 text-gray-600'
                    }`}>
                      {m.year_start || m.historical_period}
                    </span>
                  </button>
                );
              })}
            </div>

            {/* Comparison Mode Switcher Tabs */}
            <div className="flex flex-wrap sm:inline-flex p-1 bg-white border border-[#CBD5E1] rounded-xl shadow-xs w-full sm:w-auto gap-1">
              <button
                onClick={() => setComparisonMode('side_by_side')}
                className={`flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-bold transition-all whitespace-nowrap ${
                  comparisonMode === 'side_by_side'
                    ? 'bg-[#172B40] text-white shadow-xs'
                    : 'text-gray-600 hover:text-[#172B40]'
                }`}
              >
                <Columns className="w-3.5 h-3.5 shrink-0" />
                <span>{t('maps.sideBySide', 'Side-by-Side')}</span>
              </button>

              <button
                onClick={() => setComparisonMode('swipe')}
                className={`flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-bold transition-all whitespace-nowrap ${
                  comparisonMode === 'swipe'
                    ? 'bg-[#172B40] text-white shadow-xs'
                    : 'text-gray-600 hover:text-[#172B40]'
                }`}
              >
                <SplitSquareVertical className="w-3.5 h-3.5 shrink-0" />
                <span>{t('maps.swipe', 'Swipe')}</span>
              </button>

              <button
                onClick={() => setComparisonMode('transparency')}
                className={`flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-bold transition-all whitespace-nowrap ${
                  comparisonMode === 'transparency'
                    ? 'bg-[#172B40] text-white shadow-xs'
                    : 'text-gray-600 hover:text-[#172B40]'
                }`}
              >
                <Layers className="w-3.5 h-3.5 shrink-0" />
                <span>{t('maps.transparency', 'Transparency')}</span>
              </button>

              <button
                onClick={() => setComparisonMode('inspection')}
                className={`flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-bold transition-all whitespace-nowrap ${
                  comparisonMode === 'inspection'
                    ? 'bg-[#172B40] text-white shadow-xs'
                    : 'text-gray-600 hover:text-[#172B40]'
                }`}
              >
                <Maximize2 className="w-3.5 h-3.5 shrink-0" />
                <span>{t('maps.inspection', 'Inspection')}</span>
              </button>
            </div>
          </div>

          {/* Interactive Map Comparison Workspace */}
          {selectedMap && (
            <HistoricalMapWorkspace
              mapData={selectedMap}
              observations={selectedMapDetail?.observations || []}
              mode={comparisonMode}
              focusedObservation={focusedObservation}
            />
          )}

          {/* Map Source Information & Metadata Card */}
          {selectedMap && (
            <div className="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-gray-100">
                <div className="flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-[#C5A66A]" />
                  <h3 className="font-bold text-base sm:text-lg text-[#172B40]">
                    {t('maps.sourceInfoTitle', 'Cartographic Source & Archival Provenance')}
                  </h3>
                </div>
                {selectedMap.source_url && (
                  <a
                    href={selectedMap.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-xs font-semibold text-[#172B40] hover:text-[#C5A66A] bg-gray-50 hover:bg-[#FDF9F0] border border-gray-200 px-3 py-1.5 rounded-xl transition-colors"
                  >
                    <span>{t('maps.viewHighRes', 'Open Archival Source')}</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
                <div className="p-3 bg-[#F8FAFC] rounded-xl border border-gray-100">
                  <div className="text-gray-500 font-medium mb-1">{t('maps.cartographer', 'Cartographer / Surveyor')}</div>
                  <div className="font-bold text-gray-800 text-sm">
                    {lang === 'ta' ? (selectedMap.creator_tamil || selectedMap.creator) : selectedMap.creator || 'Survey of India'}
                  </div>
                </div>

                <div className="p-3 bg-[#F8FAFC] rounded-xl border border-gray-100">
                  <div className="text-gray-500 font-medium mb-1">{t('maps.archivalRepository', 'Archival Repository')}</div>
                  <div className="font-bold text-gray-800 text-sm">{selectedMap.source_name}</div>
                </div>

                <div className="p-3 bg-[#F8FAFC] rounded-xl border border-gray-100">
                  <div className="text-gray-500 font-medium mb-1">{t('maps.yearRange', 'Publication Year')}</div>
                  <div className="font-bold text-gray-800 text-sm">
                    {selectedMap.year_start} {selectedMap.year_end && selectedMap.year_end !== selectedMap.year_start ? `– ${selectedMap.year_end}` : ''}
                  </div>
                </div>

                <div className="p-3 bg-[#F8FAFC] rounded-xl border border-gray-100">
                  <div className="text-gray-500 font-medium mb-1">{t('maps.license', 'Copyright / Usage')}</div>
                  <div className="font-bold text-emerald-800 text-sm">{selectedMap.license_info}</div>
                </div>
              </div>

              {/* Description & Cartographic Limitations */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 pt-2 text-xs">
                <div className="p-4 bg-[#F8FAFC] rounded-xl border border-gray-200">
                  <h4 className="font-bold text-gray-800 mb-1 flex items-center gap-1.5">
                    <Info className="w-4 h-4 text-blue-600" />
                    <span>{lang === 'ta' ? 'வரைபடக் குறிப்பு' : 'Archival Description'}</span>
                  </h4>
                  <p className="text-gray-600 leading-relaxed">
                    {lang === 'ta' ? (selectedMap.description_tamil || selectedMap.description) : selectedMap.description}
                  </p>
                </div>

                <div className="p-4 bg-amber-50/50 rounded-xl border border-amber-200/60">
                  <h4 className="font-bold text-amber-900 mb-1 flex items-center gap-1.5">
                    <AlertCircle className="w-4 h-4 text-amber-600" />
                    <span>{t('maps.limitations', 'Cartographic Limitations & Notes')}</span>
                  </h4>
                  <p className="text-amber-900/80 leading-relaxed">
                    {lang === 'ta' ? (selectedMap.limitations_tamil || selectedMap.limitations) : selectedMap.limitations}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Historical Change Detection & Archival Findings Panel */}
          {selectedMap && (
            <div className="bg-white rounded-2xl p-6 border border-[#E2E8F0] shadow-sm space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-gray-100">
                <div>
                  <h3 className="font-bold text-base sm:text-lg text-[#172B40] flex items-center gap-2">
                    <ShieldCheck className="w-5 h-5 text-emerald-600" />
                    <span>{t('maps.changesTitle', 'Historical Change Detection & Archival Findings')}</span>
                  </h3>
                  <p className="text-xs text-gray-500 mt-1">
                    {t(
                      'maps.changesSubtitle',
                      'Documented shifts in settlements, hydrology, roads, boundaries, and place names verified against archival maps and gazetteers.'
                    )}
                  </p>
                </div>
                <div className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 self-start sm:self-auto">
                  {selectedMapDetail?.observations?.length || 0} {t('maps.observationsCount', 'Verified Findings')}
                </div>
              </div>

              {/* Category Filter Tabs */}
              <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
                <button
                  onClick={() => setSelectedCategory('all')}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all border whitespace-nowrap ${
                    selectedCategory === 'all'
                      ? 'bg-[#172B40] text-white border-[#172B40]'
                      : 'bg-[#F8FAFC] text-gray-600 border-gray-200 hover:bg-gray-100'
                  }`}
                >
                  {t('maps.filterAll', 'All Changes')} ({selectedMapDetail?.observations?.length || 0})
                </button>

                {categories.map((cat) => {
                  const countForMap = selectedMapDetail?.observations?.filter((o) => o.category === cat.category).length || 0;
                  return (
                    <button
                      key={cat.category}
                      onClick={() => setSelectedCategory(cat.category)}
                      className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all border whitespace-nowrap ${
                        selectedCategory === cat.category
                          ? 'bg-[#172B40] text-white border-[#172B40]'
                          : 'bg-[#F8FAFC] text-gray-600 border-gray-200 hover:bg-gray-100'
                      }`}
                    >
                      <span>{lang === 'ta' ? cat.name_ta : cat.name_en}</span>
                      <span className="ml-1.5 text-[10px] opacity-75">({countForMap})</span>
                    </button>
                  );
                })}
              </div>

              {/* Findings Cards List */}
              {detailLoading ? (
                <div className="py-10 text-center text-sm text-gray-500">
                  {lang === 'ta' ? 'கண்டுபிடிப்புகள் ஏற்றப்படுகின்றன...' : 'Loading verified observations...'}
                </div>
              ) : filteredObservations.length === 0 ? (
                <div className="p-8 text-center bg-gray-50 rounded-xl border border-dashed border-gray-200 space-y-2">
                  <p className="text-sm font-medium text-gray-600">
                    {t('maps.noChangesFound', 'No recorded change observations in this category for this map.')}
                  </p>
                  <p className="text-xs text-gray-400">
                    {t('maps.unverifiableNote', 'Unable to verify this change from the available maps.')}
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {filteredObservations.map((obs) => {
                    const isFocused = focusedObservation?.id === obs.id;
                    return (
                      <div
                        key={obs.id}
                        className={`p-5 rounded-2xl border transition-all flex flex-col justify-between space-y-3 ${
                          isFocused
                            ? 'bg-[#FFFDF5] border-[#C5A66A] ring-2 ring-[#C5A66A]/30 shadow-md'
                            : 'bg-white border-[#E2E8F0] hover:border-gray-300 hover:shadow-xs'
                        }`}
                      >
                        <div className="space-y-2">
                          <div className="flex items-start justify-between gap-2">
                            <h4 className="font-bold text-sm sm:text-base text-[#172B40]">
                              {lang === 'ta' ? (obs.title_tamil || obs.title) : obs.title}
                            </h4>
                            <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-[#ECFDF5] text-[#065F46] border border-[#A7F3D0] shrink-0">
                              {t('maps.verifiedFinding', 'Verified Archival Finding')}
                            </span>
                          </div>

                          <div className="flex items-center gap-2 text-[11px] text-gray-500 font-medium">
                            <span>{obs.place_name}</span>
                            {obs.historical_year_ref && (
                              <>
                                <span>•</span>
                                <span className="text-[#C5A66A] font-bold">{obs.historical_year_ref}</span>
                              </>
                            )}
                          </div>

                          <div className="space-y-2 pt-2 text-xs">
                            <div className="p-3 bg-[#F8FAFC] rounded-xl border border-gray-100">
                              <span className="text-[10px] font-bold uppercase tracking-wider text-gray-500 block mb-0.5">
                                {t('maps.historicalRef', 'Historical Cartographic Evidence')}:
                              </span>
                              <p className="text-gray-700 leading-relaxed font-sans">
                                {lang === 'ta' ? (obs.observation_text_tamil || obs.observation_text) : obs.observation_text}
                              </p>
                            </div>

                            {obs.modern_comparison && (
                              <div className="p-3 bg-emerald-50/50 rounded-xl border border-emerald-100">
                                <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 block mb-0.5">
                                  {t('maps.modernRef', 'Modern Ground Reality Comparison')}:
                                </span>
                                <p className="text-emerald-900 leading-relaxed">
                                  {lang === 'ta' ? (obs.modern_comparison_tamil || obs.modern_comparison) : obs.modern_comparison}
                                </p>
                              </div>
                            )}
                          </div>
                        </div>

                        {/* Citation & Action Footer */}
                        <div className="pt-3 border-t border-gray-100 flex items-center justify-between gap-2 text-xs">
                          <span className="text-[11px] text-gray-400 truncate max-w-[220px]" title={obs.source_citation}>
                            {obs.source_citation}
                          </span>

                          {obs.coordinates_json && (
                            <button
                              onClick={() => {
                                setFocusedObservation(obs);
                                window.scrollTo({ top: 320, behavior: 'smooth' });
                              }}
                              className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold bg-[#172B40] text-white hover:bg-[#203D5B] transition-colors shrink-0"
                            >
                              <MapPin className="w-3.5 h-3.5 text-[#C5A66A]" />
                              <span>{t('maps.focusOnMap', 'Focus on Map')}</span>
                            </button>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default HistoricalMapExplorer;
