import React from 'react';
import { LayoutGrid, List, SlidersHorizontal } from 'lucide-react';
import { useTranslation } from '../../services/LanguageContext';

/**
 * DistrictViewToolbar
 *
 * Controls:
 * - Grid / List view toggle
 * - Sort selector (by number / alphabetical / region)
 * - Region filter chips (passed as props)
 */
const DistrictViewToolbar = ({
  viewMode,         // 'grid' | 'list'
  onViewChange,     // (mode) => void
  sortBy,           // 'number' | 'alpha' | 'region'
  onSortChange,     // (sort) => void
  regions,          // [{id, label_en, label_ta}]
  selectedRegion,   // string
  onRegionChange,   // (id) => void
  lang,
}) => {
  const { t } = useTranslation();

  const sortOptions = [
    { id: 'number', label_en: '# Number', label_ta: '# எண் வரிசை' },
    { id: 'alpha', label_en: 'A–Z Name', label_ta: 'அ–ஔ பெயர்' },
    { id: 'region', label_en: 'Region', label_ta: 'மண்டலம்' },
  ];

  return (
    <div className="flex flex-col gap-3">
      {/* Top row: view toggle + sort */}
      <div className="flex flex-wrap items-center justify-between gap-2.5 sm:gap-3">
        {/* View mode toggle */}
        <div
          className="inline-flex items-center bg-white border border-gray-200 rounded-xl p-1 gap-1 shadow-sm shrink-0"
          role="group"
          aria-label={lang === 'ta' ? 'காட்சி முறை' : 'View mode'}
        >
          <button
            type="button"
            onClick={() => onViewChange('grid')}
            aria-pressed={viewMode === 'grid'}
            title={lang === 'ta' ? 'கட்டக் காட்சி' : 'Grid view'}
            className={`p-1.5 rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-[#C5A66A] ${
              viewMode === 'grid'
                ? 'bg-[#172B40] text-[#C5A66A] shadow-sm'
                : 'text-gray-500 hover:text-[#172B40] hover:bg-gray-100'
            }`}
          >
            <LayoutGrid className="w-4 h-4" />
          </button>
          <button
            type="button"
            onClick={() => onViewChange('list')}
            aria-pressed={viewMode === 'list'}
            title={lang === 'ta' ? 'பட்டியல் காட்சி' : 'List view'}
            className={`p-1.5 rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-[#C5A66A] ${
              viewMode === 'list'
                ? 'bg-[#172B40] text-[#C5A66A] shadow-sm'
                : 'text-gray-500 hover:text-[#172B40] hover:bg-gray-100'
            }`}
          >
            <List className="w-4 h-4" />
          </button>
        </div>

        {/* Sort selector */}
        <div className="flex items-center gap-1.5 sm:gap-2 flex-wrap">
          <SlidersHorizontal className="w-3.5 h-3.5 text-gray-400 shrink-0 hidden xs:inline-block" />
          <div className="flex items-center gap-1 flex-wrap">
            {sortOptions.map((opt) => (
              <button
                key={opt.id}
                type="button"
                onClick={() => onSortChange(opt.id)}
                aria-pressed={sortBy === opt.id}
                className={`px-2 sm:px-2.5 py-1 rounded-lg text-[10px] sm:text-[11px] font-semibold transition-all focus:outline-none focus:ring-2 focus:ring-[#C5A66A] ${
                  sortBy === opt.id
                    ? 'bg-[#172B40] text-[#C5A66A]'
                    : 'bg-white text-gray-600 border border-gray-200 hover:border-[#C5A66A] hover:text-[#172B40]'
                }`}
              >
                {lang === 'ta' ? opt.label_ta : opt.label_en}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Region filter chips */}
      {regions && regions.length > 0 && (
        <div
          className="flex flex-wrap gap-1.5 overflow-x-auto pb-0.5"
          role="group"
          aria-label={lang === 'ta' ? 'மண்டல வடிகட்டி' : 'Region filter'}
        >
          {regions.map((reg) => (
            <button
              key={reg.id}
              type="button"
              onClick={() => onRegionChange(reg.id)}
              aria-pressed={selectedRegion === reg.id}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all shrink-0 focus:outline-none focus:ring-2 focus:ring-[#C5A66A] ${
                selectedRegion === reg.id
                  ? 'bg-[#172B40] text-[#C5A66A] shadow-sm'
                  : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200 hover:border-[#C5A66A]'
              }`}
            >
              {lang === 'ta' ? reg.label_ta : reg.label_en}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default DistrictViewToolbar;
