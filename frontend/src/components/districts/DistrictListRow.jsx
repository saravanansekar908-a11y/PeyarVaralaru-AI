import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, History, Star } from 'lucide-react';
import { useTranslation } from '../../services/LanguageContext';

/**
 * DistrictListRow
 *
 * Compact list-row view for the district directory.
 * Renders as a horizontally scannable row with:
 * - Number / district names / region / historical snippet / CTA
 */
const DistrictListRow = ({ district }) => {
  const { lang, t } = useTranslation();
  const navigate = useNavigate();

  const no = district.no;
  const nameEn = district.district_english || '';
  const nameTa = district.district_tamil || '';
  const displayName = lang === 'ta' ? nameTa : nameEn;
  const subName = lang === 'ta' ? nameEn : nameTa;
  const regionLabel = lang === 'ta'
    ? (district.region_ta || district.region)
    : (district.region_en || district.region);

  const historicalCtx = lang === 'ta'
    ? district.ancient_or_historical_name_context_ta
    : district.ancient_or_historical_name_context_en;
  const ctxSnippet = (historicalCtx || '').slice(0, 100);

  const topSpeciality = district.specialities?.[0];
  const specName = topSpeciality
    ? (lang === 'ta' ? (topSpeciality.name_ta || topSpeciality.name) : (topSpeciality.name_en || topSpeciality.name))
    : null;

  const handleClick = () => {
    navigate(`/districts/${no}`);
    const mainEl = document.getElementById('main-content') || document.querySelector('main');
    if (mainEl) mainEl.scrollTo({ top: 0, behavior: 'smooth' });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <article
      role="button"
      tabIndex={0}
      onClick={handleClick}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && handleClick()}
      aria-label={`${displayName} ${lang === 'ta' ? 'மாவட்டம்' : 'district'}`}
      className="group w-full flex items-center gap-4 px-4 py-3.5 bg-white rounded-xl border border-gray-100
        hover:border-[#C5A66A] hover:shadow-md hover:bg-[#FDFBF7]
        transition-all duration-150 cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#C5A66A] focus:ring-offset-1"
    >
      {/* Number */}
      <span className="shrink-0 w-8 h-8 flex items-center justify-center rounded-lg bg-[#F7F4ED] text-[#172B40] text-xs font-black group-hover:bg-[#C5A66A] group-hover:text-[#172B40] transition-colors">
        {no}
      </span>

      {/* Names */}
      <div className="flex flex-col min-w-0 w-32 shrink-0">
        <span className="text-sm font-bold text-[#172B40] truncate leading-tight">{displayName}</span>
        <span className="text-[11px] text-gray-500 truncate">{subName}</span>
      </div>

      {/* Region chip */}
      <span className="hidden sm:inline-block shrink-0 text-[10px] font-semibold px-2.5 py-1 rounded-full bg-[#F7F4ED] text-[#172B40] border border-[#E8DFC6] truncate max-w-[120px]">
        {regionLabel}
      </span>

      {/* Historical snippet */}
      {ctxSnippet ? (
        <p className="hidden md:flex flex-1 items-start gap-1.5 text-xs text-gray-500 line-clamp-1 min-w-0">
          <History className="w-3 h-3 text-[#C5A66A] shrink-0 mt-0.5" />
          <span className="truncate">{ctxSnippet}{ctxSnippet.length >= 100 ? '…' : ''}</span>
        </p>
      ) : (
        <div className="hidden md:flex flex-1" />
      )}

      {/* Speciality highlight */}
      {specName && (
        <p className="hidden lg:flex items-start gap-1 text-[11px] text-gray-600 shrink-0 max-w-[200px] truncate">
          <Star className="w-3 h-3 text-amber-500 mt-0.5 shrink-0" />
          <span className="truncate">{specName}</span>
        </p>
      )}

      {/* CTA */}
      <div className="ml-auto shrink-0 flex items-center gap-1 text-[11px] font-bold text-gray-400 group-hover:text-[#C5A66A] transition-colors">
        <span className="hidden sm:inline">{t('district.viewProfile', 'View')}</span>
        <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
      </div>
    </article>
  );
};

export default DistrictListRow;
