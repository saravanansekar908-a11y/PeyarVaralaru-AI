import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, History, Star, MapPin } from 'lucide-react';
import { useTranslation } from '../../services/LanguageContext';

/**
 * DistrictGridCard
 *
 * Premium card for the grid view. Shows:
 * - District number badge
 * - District name (Tamil + English)
 * - Region label
 * - Historical context snippet (ancient/former admin name)
 * - One heritage highlight (first speciality name)
 * - CTA to navigate to district detail
 */
const DistrictGridCard = ({ district }) => {
  const { lang, t } = useTranslation();
  const navigate = useNavigate();

  const no = district.no;
  const nameEn = district.district_english || '';
  const nameTa = district.district_tamil || '';
  const displayName = lang === 'ta' ? nameTa : nameEn;
  const subName = lang === 'ta' ? nameEn : nameTa;

  const regionLabel = lang === 'ta' ? (district.region_ta || district.region) : (district.region_en || district.region);

  // Historical context (first 80 chars of ancient context)
  const historicalCtx = lang === 'ta'
    ? district.ancient_or_historical_name_context_ta
    : district.ancient_or_historical_name_context_en;
  const ctxSnippet = (historicalCtx || '').slice(0, 90);

  // Top speciality highlight
  const topSpeciality = district.specialities?.[0];
  const specName = topSpeciality
    ? (lang === 'ta' ? (topSpeciality.name_ta || topSpeciality.name) : (topSpeciality.name_en || topSpeciality.name))
    : null;

  // First famous place
  const topPlace = district.famous_places?.[0];

  const handleClick = () => {
    navigate(`/districts/${no}`);
    const mainEl = document.getElementById('main-content') || document.querySelector('main');
    if (mainEl) mainEl.scrollTo({ top: 0, behavior: 'smooth' });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Subtle per-region color accent
  const regionColor = getRegionColor(district.region);

  return (
    <article
      role="button"
      tabIndex={0}
      onClick={handleClick}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && handleClick()}
      aria-label={`${displayName} ${lang === 'ta' ? 'மாவட்டம் - விவரங்களைக் காண்க' : 'district - view details'}`}
      className="group relative bg-white border border-gray-100 rounded-2xl overflow-hidden cursor-pointer
        hover:border-[#C5A66A] hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0
        transition-all duration-200 ease-out focus:outline-none focus:ring-2 focus:ring-[#C5A66A] focus:ring-offset-1
        flex flex-col h-full"
    >
      {/* Color accent strip */}
      <div className={`h-1 w-full ${regionColor.strip}`} />

      <div className="flex flex-col flex-1 p-4 gap-3">
        {/* Header: number badge + region */}
        <div className="flex items-start justify-between gap-2">
          <span className={`inline-flex items-center justify-center w-7 h-7 rounded-lg text-xs font-black shrink-0 ${regionColor.badge}`}>
            {no}
          </span>
          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full truncate max-w-[140px] ${regionColor.region}`}>
            {regionLabel}
          </span>
        </div>

        {/* District names */}
        <div className="flex flex-col gap-0.5">
          <h3 className="text-base font-black text-[#172B40] leading-tight group-hover:text-[#0E1E2E] transition-colors">
            {displayName}
          </h3>
          <p className="text-xs text-gray-500 font-medium">{subName}</p>
        </div>

        {/* Historical snippet */}
        {ctxSnippet && (
          <div className="flex items-start gap-1.5">
            <History className="w-3 h-3 text-[#C5A66A] mt-0.5 shrink-0" />
            <p className="text-[11px] text-gray-600 leading-relaxed line-clamp-2">
              {ctxSnippet}{ctxSnippet.length >= 90 ? '…' : ''}
            </p>
          </div>
        )}

        {/* Heritage highlight */}
        {specName && (
          <div className="flex items-start gap-1.5">
            <Star className="w-3 h-3 text-amber-500 mt-0.5 shrink-0" />
            <p className="text-[11px] text-gray-700 font-medium leading-snug line-clamp-2">{specName}</p>
          </div>
        )}

        {/* Spacer */}
        <div className="flex-1" />

        {/* Footer CTA */}
        <div className="flex items-center justify-between pt-2 border-t border-gray-50">
          {topPlace && (
            <span className="flex items-center gap-1 text-[10px] text-gray-500 truncate">
              <MapPin className="w-3 h-3 shrink-0" />
              <span className="truncate">
                {lang === 'ta' ? (topPlace.name_ta || topPlace.name) : (topPlace.name_en || topPlace.name)}
              </span>
            </span>
          )}
          <span
            className="ml-auto inline-flex items-center gap-1 text-[11px] font-bold text-[#172B40] group-hover:text-[#C5A66A] transition-colors shrink-0"
          >
            {t('district.viewProfile', 'View')}
            <ArrowRight className="w-3 h-3 transition-transform group-hover:translate-x-0.5" />
          </span>
        </div>
      </div>
    </article>
  );
};

// Map a region string to a consistent color palette
function getRegionColor(region = '') {
  const r = region.toLowerCase();
  if (r.includes('north')) return {
    strip: 'bg-blue-400',
    badge: 'bg-blue-50 text-blue-700',
    region: 'bg-blue-50 text-blue-600',
  };
  if (r.includes('south')) return {
    strip: 'bg-emerald-400',
    badge: 'bg-emerald-50 text-emerald-700',
    region: 'bg-emerald-50 text-emerald-700',
  };
  if (r.includes('west')) return {
    strip: 'bg-purple-400',
    badge: 'bg-purple-50 text-purple-700',
    region: 'bg-purple-50 text-purple-700',
  };
  if (r.includes('cauvery') || r.includes('delta') || r.includes('central')) return {
    strip: 'bg-amber-400',
    badge: 'bg-amber-50 text-amber-800',
    region: 'bg-amber-50 text-amber-700',
  };
  if (r.includes('kongu')) return {
    strip: 'bg-orange-400',
    badge: 'bg-orange-50 text-orange-700',
    region: 'bg-orange-50 text-orange-700',
  };
  // default
  return {
    strip: 'bg-[#C5A66A]',
    badge: 'bg-[#F7F4ED] text-[#172B40]',
    region: 'bg-[#F7F4ED] text-[#172B40]',
  };
}

export default DistrictGridCard;
