import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { useTranslation } from '../services/LanguageContext';
import { getPlaces } from '../services/api';
import StatusBadge from '../components/StatusBadge';
import { Search, MapPin, ArrowRight, Sparkles, AlertCircle, Clock } from 'lucide-react';

export const SearchPage = () => {
  const { lang, t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const queryParam = searchParams.get('q') || '';

  const [inputVal, setInputVal] = useState(queryParam);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const sampleQueries = [
    { label: 'Madras', q: 'Madras' },
    { label: 'சென்னை', q: 'சென்னை' },
    { label: 'Black Town', q: 'Black Town' },
    { label: 'Trichinopoly', q: 'Trichinopoly' },
    { label: 'Tanjore', q: 'Tanjore' },
    { label: 'Chennapatnam', q: 'Chennapatnam' },
  ];

  const performSearch = async (q) => {
    setLoading(true);
    setHasSearched(true);
    try {
      const data = await getPlaces(q);
      setResults(data);
    } catch (err) {
      console.error('Search error:', err);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (queryParam) {
      setInputVal(queryParam);
      performSearch(queryParam);
    } else {
      performSearch('');
    }
  }, [queryParam]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputVal.trim()) {
      setSearchParams({ q: inputVal.trim() });
    } else {
      setSearchParams({});
    }
  };

  const handleChipClick = (q) => {
    setInputVal(q);
    setSearchParams({ q });
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto py-2">
      {/* Header & Search Bar */}
      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm">
        <div className="mb-4">
          <h2 className="text-2xl font-bold text-[#172B40]">
            {t('search.title', 'Smart Place Search')}
          </h2>
          <p className="text-xs sm:text-sm text-gray-500 mt-1">
            {lang === 'ta'
              ? 'தற்போதைய அல்லது பழைய பெயர்களை தமிழ் மற்றும் ஆங்கிலத்தில் தட்டச்சு செய்து தேடுங்கள்.'
              : 'Search historical or current place names in both Tamil and English (e.g., Madras, Black Town, திருச்சி).'}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          <div className="flex items-center bg-[#F7F4ED] rounded-xl p-1.5 border border-[#E2E8F0] focus-within:border-[#C5A66A] focus-within:ring-2 focus-within:ring-[#C5A66A]/20 transition-all">
            <Search className="w-5 h-5 text-gray-400 ml-3 mr-2 shrink-0" />
            <input
              type="text"
              value={inputVal}
              onChange={(e) => setInputVal(e.target.value)}
              placeholder={t('search.placeholder', 'Search in Tamil or English...')}
              className="w-full px-2 py-2.5 text-sm text-[#172B40] bg-transparent placeholder-gray-400 focus:outline-none"
            />
            <button
              type="submit"
              className="bg-[#172B40] hover:bg-[#20364F] text-white font-semibold text-sm px-6 py-2.5 rounded-lg transition-colors shadow-sm shrink-0"
            >
              {loading ? t('search.searching', 'Searching...') : t('search.button', 'Search')}
            </button>
          </div>

          {/* Quick Filter Chips */}
          <div className="flex items-center gap-2 flex-wrap pt-1">
            <span className="text-xs font-medium text-gray-500 flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5 text-[#C5A66A]" />
              {lang === 'ta' ? 'பரிந்துரைகள்:' : 'Quick suggestions:'}
            </span>
            {sampleQueries.map((item) => (
              <button
                key={item.q}
                type="button"
                onClick={() => handleChipClick(item.q)}
                className="px-2.5 py-1 text-xs font-medium rounded-full bg-gray-100 hover:bg-[#C5A66A]/20 hover:text-[#172B40] text-gray-700 transition-colors border border-gray-200"
              >
                {item.label}
              </button>
            ))}
          </div>
        </form>
      </div>

      {/* Results Section */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-[#172B40]">
            {t('search.results', 'Search Results')}{' '}
            <span className="text-xs font-normal text-gray-500">
              ({results.length} {lang === 'ta' ? 'பதிவுகள்' : 'records'})
            </span>
          </h3>
          {queryParam && (
            <button
              onClick={() => {
                setInputVal('');
                setSearchParams({});
              }}
              className="text-xs text-[#C5A66A] hover:underline font-medium"
            >
              {lang === 'ta' ? 'தேடலை நீக்கு' : 'Clear search'}
            </button>
          )}
        </div>

        {loading ? (
          <div className="text-center py-12 bg-white rounded-xl border border-gray-200 text-gray-500 text-sm">
            <div className="inline-block animate-spin w-6 h-6 border-2 border-[#172B40] border-t-transparent rounded-full mb-2"></div>
            <p>{t('search.searching', 'Searching database records...')}</p>
          </div>
        ) : results.length === 0 ? (
          <div className="bg-white rounded-2xl p-10 border border-gray-200 text-center space-y-3">
            <AlertCircle className="w-10 h-10 text-amber-500 mx-auto" />
            <h4 className="font-bold text-base text-[#172B40]">
              {t('search.noResults', 'No matching historical places found.')}
            </h4>
            <p className="text-xs text-gray-500 max-w-md mx-auto">
              {lang === 'ta'
                ? 'வேறொரு பெயரை உள்ளிட்டுப் பாருங்கள், அல்லது ஆங்கில எழுத்துக்களில் தேடவும்.'
                : 'Try searching with an alternative spelling or historical alias.'}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {results.map((place) => (
              <div
                key={place.id}
                className="bg-white rounded-xl p-6 border border-gray-200 hover:border-[#C5A66A] shadow-sm hover:shadow-md transition-all space-y-4"
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="flex items-start gap-3">
                    <div className="w-10 h-10 rounded-lg bg-[#F7F4ED] text-[#172B40] flex items-center justify-center shrink-0 border border-gray-200">
                      <MapPin className="w-5 h-5 text-[#C5A66A]" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <h4 className="text-lg font-bold text-[#172B40]">
                          {lang === 'ta' && place.current_name_tamil
                            ? place.current_name_tamil
                            : place.current_name}
                        </h4>
                        <span className="text-xs text-gray-500 font-medium">
                          ({lang === 'ta' ? place.current_name : place.current_name_tamil})
                        </span>
                        {place.match_reason && (
                          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-blue-50 text-blue-700 border border-blue-200">
                            {lang === 'ta' ? 'பொருத்தம்:' : 'Matched on:'} {place.match_reason}
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-gray-500 mt-0.5">
                        {lang === 'ta' ? 'மாவட்டம்:' : 'District:'} {place.district || '-'}
                      </p>
                    </div>
                  </div>

                  <StatusBadge
                    status={place.id === 1 || place.id === 2 ? 'verified' : 'partially_verified'}
                    size="sm"
                  />
                </div>

                {/* Historical Names List */}
                <div className="bg-[#F7F4ED] rounded-lg p-3 border border-gray-100 space-y-1">
                  <span className="text-xs font-semibold text-gray-700 block">
                    {lang === 'ta' ? 'பதிவான வரலாற்றுப் பெயர்கள்:' : 'Recorded Historical Names:'}
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {place.historical_names?.map((hn) => (
                      <span
                        key={hn.id}
                        className="inline-flex items-center px-2.5 py-1 rounded bg-white text-xs font-medium text-[#172B40] border border-gray-200 shadow-2xs"
                      >
                        <span className="font-semibold text-[#172B40]">{hn.name}</span>
                        {hn.name_type && (
                          <span className="ml-1 text-[10px] text-gray-400">
                            ({hn.name_type})
                          </span>
                        )}
                      </span>
                    ))}
                  </div>
                </div>

                <p className="text-xs sm:text-sm text-gray-600 leading-relaxed">
                  {lang === 'ta' && place.description_tamil
                    ? place.description_tamil
                    : place.description}
                </p>

                <div className="pt-2 flex items-center justify-between border-t border-gray-100">
                  <Link
                    to={`/places/${place.id}`}
                    className="inline-flex items-center gap-1.5 text-xs font-bold text-[#172B40] hover:text-[#C5A66A] transition-colors"
                  >
                    <Clock className="w-3.5 h-3.5" />
                    <span>{t('place.timeline', 'Explore Historical Timeline')}</span>
                    <ArrowRight className="w-3 h-3" />
                  </Link>

                  <Link
                    to={`/graph?place=${place.id}`}
                    className="text-xs font-medium text-gray-500 hover:text-[#172B40] transition-colors"
                  >
                    {lang === 'ta' ? 'தொடர்பு வரைபடம்' : 'View in Graph'} &rarr;
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPage;
