import React, { useRef, useCallback, useState } from 'react';
import { X, Globe2 } from 'lucide-react';
import { useTranslation } from '../../services/LanguageContext';

const ALPHA_EN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
const ALPHA_TA = ['அ', 'இ', 'ஈ', 'க', 'ச', 'த', 'ந', 'ப', 'ம', 'ர', 'வ'];

/**
 * DistrictAlphaNav
 *
 * Renders an alphabetical jump navigation bar.
 * - Supports Tamil initials ('அ', 'இ', 'க'...) in Tamil mode
 * - Supports English A–Z ('A', 'B', 'C'...) in English mode
 * - Allows 1-click script toggle (தமிழ் / A–Z)
 * - Result count + Clear filters pill
 */
const DistrictAlphaNav = ({
  districts,          // all 38 districts (unfiltered)
  filteredCount,      // how many districts currently visible
  totalCount,         // 38
  activeLetter,       // currently selected letter (null = all)
  onLetterClick,      // (letter | null) => void
  hasActiveFilters,   // bool — shows Clear pill
  onClearFilters,
}) => {
  const { lang, t } = useTranslation();
  const navRef = useRef(null);

  // Script mode: defaults to 'ta' if lang === 'ta', otherwise 'en'
  const [scriptMode, setScriptMode] = useState(lang === 'ta' ? 'ta' : 'en');

  // Sync scriptMode when language changes
  React.useEffect(() => {
    setScriptMode(lang === 'ta' ? 'ta' : 'en');
  }, [lang]);

  // Available English letters
  const availableEnLetters = new Set(
    (districts || []).map((d) => {
      const name = d.district_english || '';
      return name[0]?.toUpperCase();
    }).filter(Boolean)
  );

  // Available Tamil letters
  const availableTaLetters = new Set(
    (districts || []).map((d) => {
      const name = (d.district_tamil || '').trim();
      return name[0];
    }).filter(Boolean)
  );

  const handleClick = useCallback((letter) => {
    onLetterClick(activeLetter === letter ? null : letter);
  }, [activeLetter, onLetterClick]);

  const countLabel = hasActiveFilters
    ? `${filteredCount} ${lang === 'ta' ? '/ 38 மாவட்டங்கள்' : `/ ${totalCount} districts`}`
    : `${totalCount} ${lang === 'ta' ? 'மாவட்டங்கள்' : 'districts'}`;

  const currentAlphabet = scriptMode === 'ta' ? ALPHA_TA : ALPHA_EN;
  const currentAvailable = scriptMode === 'ta' ? availableTaLetters : availableEnLetters;

  return (
    <div className="flex flex-col gap-2.5 bg-white p-3.5 sm:p-4 rounded-xl border border-gray-200 shadow-xs">
      {/* Top row: Count, Script toggle, and Clear button */}
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold text-gray-700">
            {countLabel}
          </span>
          {/* Script toggle button */}
          <button
            type="button"
            onClick={() => {
              setScriptMode(scriptMode === 'ta' ? 'en' : 'ta');
              onLetterClick(null);
            }}
            className="inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded-md bg-gray-100 hover:bg-[#F7F4ED] text-[#172B40] border border-gray-200 transition-colors"
            title={scriptMode === 'ta' ? 'Switch to English A–Z' : 'தமிழ் எழுத்துகளுக்கு மாறுக'}
          >
            <Globe2 className="w-3 h-3 text-[#C5A66A]" />
            <span>{scriptMode === 'ta' ? 'A–Z ஆங்கிலம்' : 'தமிழ் எழுத்துகள்'}</span>
          </button>
        </div>

        {hasActiveFilters && (
          <button
            type="button"
            onClick={onClearFilters}
            className="inline-flex items-center gap-1 text-[11px] font-bold px-2.5 py-1 rounded-full bg-[#F7F4ED] border border-[#C5A66A] text-[#172B40] hover:bg-[#C5A66A] transition-colors"
          >
            <X className="w-3 h-3 text-[#C5A66A]" />
            <span>{t('district.clearFilters', 'Clear filters')}</span>
          </button>
        )}
      </div>

      {/* Letters navigation bar */}
      <nav
        ref={navRef}
        aria-label={lang === 'ta' ? 'எழுத்துவரிசை வழிசெலுத்தல்' : 'Alphabetical navigation'}
        className="flex flex-wrap items-center gap-1"
      >
        {/* "All" reset pill */}
        <button
          type="button"
          onClick={() => onLetterClick(null)}
          aria-pressed={activeLetter === null}
          className={`px-3 py-1 rounded-lg text-xs font-bold transition-all focus:outline-none focus:ring-2 focus:ring-[#C5A66A] ${
            activeLetter === null
              ? 'bg-[#172B40] text-[#C5A66A] shadow-sm'
              : 'bg-gray-50 text-gray-700 border border-gray-200 hover:border-[#C5A66A] hover:text-[#172B40]'
          }`}
        >
          {lang === 'ta' ? 'அனைத்தும்' : 'All'}
        </button>

        {currentAlphabet.map((letter) => {
          const available = currentAvailable.has(letter);
          const isActive = activeLetter === letter;
          return (
            <button
              key={letter}
              type="button"
              onClick={() => available && handleClick(letter)}
              aria-pressed={isActive}
              aria-disabled={!available}
              disabled={!available}
              className={`min-w-7 h-7 px-1.5 rounded-lg text-xs font-bold transition-all flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-[#C5A66A] ${
                isActive
                  ? 'bg-[#C5A66A] text-[#172B40] shadow-sm scale-105'
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
