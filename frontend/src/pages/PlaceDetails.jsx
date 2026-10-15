import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useTranslation } from '../services/LanguageContext';
import { getPlace, getPlaces } from '../services/api';
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
  FileText
} from 'lucide-react';

export const PlaceDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { lang, t } = useTranslation();

  const [place, setPlace] = useState(null);
  const [allPlaces, setAllPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
      try {
        const data = await getPlace(id || 1);
        setPlace(data);
      } catch (err) {
        console.error('Failed to load place details:', err);
        setError('Failed to load historical place profile.');
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [id]);

  const getEventTypeLabel = (type) => {
    const map = {
      official_renaming: lang === 'ta' ? 'அதிகாரப்பூர்வ பெயர் மாற்றம்' : 'Official Renaming',
      historical_variant: lang === 'ta' ? 'வரலாற்றுப் பெயர் பதிவு' : 'Historical Name Variant',
      transliteration: lang === 'ta' ? 'எழுத்துப்பெயர்ப்பு மாற்றம்' : 'Transliteration Variant',
      settlement_founded: lang === 'ta' ? 'குடியேற்றத் தொடக்கம்' : 'Settlement Founded',
      uncertain: lang === 'ta' ? 'ஐயத்திற்குரிய விளக்கம்' : 'Uncertain Interpretation',
    };
    return map[type] || type;
  };

  const getEventTypeBadgeClass = (type) => {
    switch (type) {
      case 'official_renaming':
        return 'bg-blue-50 text-blue-800 border-blue-200';
      case 'historical_variant':
        return 'bg-purple-50 text-purple-800 border-purple-200';
      case 'transliteration':
        return 'bg-slate-50 text-slate-800 border-slate-200';
      default:
        return 'bg-amber-50 text-amber-800 border-amber-200';
    }
  };

  if (loading) {
    return (
      <div className="text-center py-20 bg-white rounded-2xl border border-gray-200 text-gray-500">
        <div className="inline-block animate-spin w-7 h-7 border-2 border-[#172B40] border-t-transparent rounded-full mb-3"></div>
        <p className="text-sm">{t('common.loading', 'Loading historical place records...')}</p>
      </div>
    );
  }

  if (error || !place) {
    return (
      <div className="bg-white rounded-2xl p-10 border border-gray-200 text-center space-y-4 max-w-xl mx-auto my-10">
        <AlertCircle className="w-10 h-10 text-rose-500 mx-auto" />
        <h3 className="text-lg font-bold text-[#172B40]">
          {error || t('place.noDetails', 'Place record not found')}
        </h3>
        <button
          onClick={() => navigate('/search')}
          className="px-4 py-2 bg-[#172B40] text-white text-xs font-semibold rounded-lg hover:bg-[#20364F]"
        >
          {lang === 'ta' ? 'தேடல் பக்கத்திற்குச் செல்க' : 'Back to Search'}
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto py-2">
      {/* Top Bar with Place Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-4 rounded-xl border border-gray-200">
        <Link
          to="/search"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-gray-600 hover:text-[#172B40]"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>{lang === 'ta' ? 'அனைத்து இடங்கள்' : 'All Places'}</span>
        </Link>

        {/* Place Quick Selector */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0">
          <span className="text-xs font-medium text-gray-500 shrink-0">
            {lang === 'ta' ? 'இடத்தைத் தேர்வு செய்க:' : 'Select place:'}
          </span>
          <div className="flex gap-1.5">
            {allPlaces.map((p) => (
              <button
                key={p.id}
                onClick={() => navigate(`/places/${p.id}`)}
                className={`px-3 py-1 rounded-md text-xs font-medium transition-colors shrink-0 ${
                  String(p.id) === String(place.id)
                    ? 'bg-[#172B40] text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {lang === 'ta' && p.current_name_tamil ? p.current_name_tamil : p.current_name}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Place Header Card */}
      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <MapPin className="w-5 h-5 text-[#C5A66A]" />
              <h2 className="text-2xl sm:text-3xl font-extrabold text-[#172B40]">
                {lang === 'ta' && place.current_name_tamil
                  ? place.current_name_tamil
                  : place.current_name}
              </h2>
              <span className="text-sm font-medium text-gray-500">
                ({lang === 'ta' ? place.current_name : place.current_name_tamil})
              </span>
            </div>
            <p className="text-xs sm:text-sm text-gray-500 mt-1">
              {lang === 'ta' ? 'மாவட்டம்:' : 'District:'}{' '}
              <span className="font-semibold text-gray-700">{place.district || '-'}</span>
              {place.latitude && place.longitude && (
                <span className="ml-3 text-gray-400">
                  [{place.latitude.toFixed(4)}° N, {place.longitude.toFixed(4)}° E]
                </span>
              )}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <StatusBadge
              status={place.id === 1 || place.id === 2 ? 'verified' : 'partially_verified'}
              size="lg"
            />
            <Link
              to={`/graph?place=${place.id}`}
              className="px-3 py-1.5 rounded-lg border border-[#C5A66A] text-[#172B40] bg-[#C5A66A]/10 hover:bg-[#C5A66A]/20 text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <Network className="w-4 h-4 text-[#C5A66A]" />
              <span>{lang === 'ta' ? 'தொடர்பு வரைபடம்' : 'Relationship Graph'}</span>
            </Link>
          </div>
        </div>

        {/* Historical Names Box */}
        <div className="bg-[#F7F4ED] rounded-xl p-4 border border-[#E2E8F0]">
          <h4 className="text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
            {lang === 'ta' ? 'ஆவணப்படுத்தப்பட்ட வரலாற்றுப் பெயர்கள்' : 'Documented Historical Names & Variants'}
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
            {place.historical_names?.map((hn) => (
              <div
                key={hn.id}
                className="bg-white p-2.5 rounded-lg border border-gray-200 text-xs space-y-0.5 shadow-2xs"
              >
                <div className="font-bold text-[#172B40] text-sm">{hn.name}</div>
                <div className="text-[11px] text-gray-500 flex items-center justify-between">
                  <span>{hn.language || 'Historical Tamil / English'}</span>
                  <span className="px-1.5 py-0.2 rounded bg-gray-100 text-gray-600 font-medium">
                    {hn.name_type || 'Variant'}
                  </span>
                </div>
                {(hn.valid_from || hn.valid_to) && (
                  <div className="text-[10px] text-gray-400">
                    {hn.valid_from ? `${lang === 'ta' ? 'இருந்து:' : 'From:'} ${hn.valid_from}` : ''}{' '}
                    {hn.valid_to ? `${lang === 'ta' ? 'வரை:' : 'To:'} ${hn.valid_to}` : ''}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Narrative Description */}
        <p className="text-sm text-gray-700 leading-relaxed pt-1">
          {lang === 'ta' && place.description_tamil
            ? place.description_tamil
            : place.description}
        </p>
      </div>

      {/* Historical Timeline Section */}
      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm space-y-6">
        <div className="flex items-center justify-between border-b border-gray-100 pb-4">
          <div className="flex items-center gap-2">
            <Clock className="w-5 h-5 text-[#C5A66A]" />
            <h3 className="text-xl font-bold text-[#172B40]">
              {t('place.timeline', 'Historical Evolution Timeline')}
            </h3>
          </div>
          <span className="text-xs text-gray-500">
            {place.events?.length || 0} {lang === 'ta' ? 'நிகழ்வுகள் பதிவு செய்யப்பட்டுள்ளன' : 'documented events'}
          </span>
        </div>

        {place.events?.length === 0 ? (
          <p className="text-xs text-gray-500 text-center py-6">
            {t('place.noTimeline', 'No timeline events recorded yet.')}
          </p>
        ) : (
          <div className="relative pl-6 sm:pl-8 border-l-2 border-[#C5A66A]/40 space-y-8">
            {place.events?.map((evt, idx) => (
              <div key={evt.id} className="relative group">
                {/* Timeline node dot */}
                <div className="absolute -left-[31px] sm:-left-[39px] top-1.5 w-4 h-4 rounded-full bg-[#172B40] border-2 border-[#C5A66A] shadow-sm" />

                <div className="bg-[#F7F4ED] rounded-xl p-5 border border-gray-200 space-y-3">
                  {/* Event Header */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={`px-2.5 py-0.5 rounded text-xs font-bold border ${getEventTypeBadgeClass(evt.event_type)}`}>
                        {getEventTypeLabel(evt.event_type)}
                      </span>
                      <div className="flex items-center gap-1.5 text-xs font-semibold text-gray-700">
                        <Calendar className="w-3.5 h-3.5 text-[#C5A66A]" />
                        <span>
                          {evt.event_date ? evt.event_date : (lang === 'ta' ? 'தேதி ஆவணப்படுத்தப்படவில்லை' : 'Date unrecorded in primary archives')}
                        </span>
                        {evt.date_precision && (
                          <span className="text-[10px] text-gray-400">({evt.date_precision})</span>
                        )}
                      </div>
                    </div>

                    <StatusBadge status={evt.evidence_status} size="sm" />
                  </div>

                  {/* Event Description */}
                  <p className="text-xs sm:text-sm text-gray-800 leading-relaxed font-normal">
                    {lang === 'ta' && evt.description_tamil
                      ? evt.description_tamil
                      : evt.description}
                  </p>

                  {/* Supporting Sources citations */}
                  {evt.sources?.length > 0 && (
                    <div className="pt-2 border-t border-gray-200/80 space-y-2">
                      <div className="text-[11px] font-bold text-gray-600 flex items-center gap-1">
                        <BookOpen className="w-3.5 h-3.5 text-[#C5A66A]" />
                        <span>{lang === 'ta' ? 'ஆதார ஆவணங்கள் & மேற்கோள்கள்:' : 'Supporting Primary Sources:'}</span>
                      </div>

                      <div className="space-y-2">
                        {evt.sources.map((src) => (
                          <div
                            key={src.id}
                            className="bg-white p-3 rounded-lg border border-gray-200 text-xs space-y-1"
                          >
                            <div className="flex items-start justify-between gap-2">
                              <div>
                                <span className="font-bold text-[#172B40]">
                                  {lang === 'ta' && src.title_tamil ? src.title_tamil : src.title}
                                </span>
                                {src.document_identifier && (
                                  <span className="ml-2 px-1.5 py-0.2 bg-gray-100 text-gray-700 text-[10px] rounded font-mono">
                                    {src.document_identifier}
                                  </span>
                                )}
                              </div>
                              {src.source_url && (
                                <a
                                  href={src.source_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-xs text-blue-600 hover:text-blue-800 inline-flex items-center gap-0.5 shrink-0 font-medium"
                                >
                                  <span>{t('evidence.viewSource', 'Archive Link')}</span>
                                  <ExternalLink className="w-3 h-3" />
                                </a>
                              )}
                            </div>

                            <p className="text-[11px] text-gray-500">
                              {src.publisher}
                              {src.publication_date ? ` • ${src.publication_date}` : ''}
                              {src.page_number ? ` • ${lang === 'ta' ? 'பக்கம்' : 'p.'} ${src.page_number}` : ''}
                            </p>

                            {(src.evidence_excerpt || src.evidence_excerpt_tamil) && (
                              <blockquote className="border-l-2 border-[#C5A66A] pl-2 text-[11px] text-gray-600 italic bg-amber-50/40 py-1 rounded-r">
                                "{lang === 'ta' && src.evidence_excerpt_tamil ? src.evidence_excerpt_tamil : src.evidence_excerpt}"
                              </blockquote>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default PlaceDetails;
