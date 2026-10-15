import React, { useRef, useCallback } from 'react';
import { X } from 'lucide-react';
import { useTranslation } from '../../services/LanguageContext';

const ALPHA_EN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');

// Detect if text starts with a Tamil letter
const isTamilChar = (str = '') => /^[\u0B80-\u0BFF]/.test(str.trim());

/**
 * DistrictAlphaNav
 *
 * Renders an A–Z (English) alphabetical jump navigation bar.
 * When a letter is active, the parent filters the grid to districts
 * whose name starts with that letter.
 *
 * Also shows: result count, "Clear filters" pill when filters are active.
 */
const DistrictAlphaNav = ({
  districts,          // all 38 districts (unfiltered) — used to derive available letters
  filteredCount,      // how many districts currently visible
  totalCount,         // 38
  activeLetter,       // currently selected letter (null = all)
  onLetterClick,      // (letter | null) => void
  hasActiveFilters,   // bool — shows Clear pill
  onClearFilters,
}) => {
  const { lang, t } = useTranslation();
  const navRef = useRef(null);

  // Which letters have at least one district starting with them
  const availableLetters = new Set(
    (districts || []).map((d) => {
      const name = d.district_english || '';
      return name[0]?.toUpperCase();
    }).filter(Boolean)
  );

  const handleClick = useCallback((letter) => {
    onLetterClick(activeLetter === letter ? null : letter);
  }, [activeLetter, onLetterClick]);

  const countLabel = hasActiveFilters
    ? `${filteredCount} ${lang === 'ta' ? '/ 38 மாவட்டங்கள்' : `/ ${totalCount} districts`}`
    : `${totalCount} ${lang === 'ta' ? 'மாவட்டங்கள்' : 'districts'}`;

  return (
    <div className="flex flex-col gap-2">
      {/* Info row */}
      <div className="flex flex-wrap items-center justify-between gap-2">
        <span className="text-xs font-semibold text-gray-500">
          {countLabel}
        </span>
        {hasActiveFilters && (
          <button
            type="button"
            onClick={onClearFilters}
            className="inline-flex items-center gap-1 text-[11px] font-bold px-2.5 py-1 rounded-full bg-[#F7F4ED] border border-[#C5A66A] text-[#C5A66A] hover:bg-[#C5A66A] hover:text-[#172B40] transition-colors"
          >
            <X className="w-3 h-3" />
            <span>{t('district.clearFilters', 'Clear filters')}</span>
          </button>
        )}
      </div>

      {/* A–Z bar */}
      <nav
        ref={navRef}
        aria-label={lang === 'ta' ? 'எழுத்துவரிசை வழிசெலுத்தல்' : 'Alphabetical navigation'}
        className="flex flex-wrap gap-1"
      >
        {/* "All" reset pill */}
        <button
          type="button"
          onClick={() => onLetterClick(null)}
          aria-pressed={activeLetter === null}
          className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition-all focus:outline-none focus:ring-2 focus:ring-[#C5A66A] ${
            activeLetter === null
              ? 'bg-[#172B40] text-[#C5A66A] shadow-sm'
              : 'bg-white text-gray-600 border border-gray-200 hover:border-[#C5A66A] hover:text-[#172B40]'
          }`}
        >
          {lang === 'ta' ? 'அனைத்தும்' : 'All'}
        </button>

        {ALPHA_EN.map((letter) => {
          const available = availableLetters.has(letter);
          const isActive = activeLetter === letter;
          return (
            <button
              key={letter}
              type="button"
              onClick={() => available && handleClick(letter)}
              aria-pressed={isActive}
              aria-disabled={!available}
              disabled={!available}
              className={`w-7 h-7 rounded-lg text-[11px] font-bold transition-all focus:outline-none focus:ring-2 focus:ring-[#C5A66A] ${
                isActive
                  ? 'bg-[#C5A66A] text-[#172B40] shadow-sm'
                  : available
                  ? 'bg-white text-[#172B40] border border-gray-200 hover:border-[#C5A66A] hover:bg-[#F7F4ED]'
                  : 'bg-gray-50 text-gray-300 border border-gray-100 cursor-not-allowed'
              }`}
            >
              {letter}
            </button>
          );
        })}
      </nav>
    </div>
  );
};

export default DistrictAlphaNav;
