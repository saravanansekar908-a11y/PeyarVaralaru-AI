import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X, Loader2, History, MapPin, Landmark } from 'lucide-react';
import { useTranslation } from '../../services/LanguageContext';

import { API_BASE } from '../../services/api';

/**
 * DistrictSearchBar
 *
 * - Debounced search with backend suggestions via /api/districts/suggestions
 * - Grouped dropdown: Districts / Historical Names / Heritage Places
 * - Keyboard navigation (↑ ↓ Enter Escape)
 * - AbortController to cancel stale requests
 * - Falls back to local filtering gracefully when API unavailable
 */
const DistrictSearchBar = ({ value, onChange, onClear, onDistrictSelect }) => {
  const { lang, t } = useTranslation();
  const navigate = useNavigate();

  const [suggestions, setSuggestions] = useState(null); // null = closed
  const [loading, setLoading] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const inputRef = useRef(null);
  const dropdownRef = useRef(null);
  const abortRef = useRef(null);
  const debounceTimer = useRef(null);

  // Flatten suggestions for keyboard nav
  const flatSuggestions = suggestions
    ? [
        ...(suggestions.districts || []).map((s) => ({ ...s, _group: 'districts' })),
        ...(suggestions.historical_names || []).map((s) => ({ ...s, _group: 'historical_names' })),
        ...(suggestions.heritage_places || []).map((s) => ({ ...s, _group: 'heritage_places' })),
      ]
    : [];

  const fetchSuggestions = useCallback(async (q) => {
    if (!q || q.trim().length < 1) {
      setSuggestions(null);
      setLoading(false);
      return;
    }

    // Cancel previous request
    if (abortRef.current) {
      abortRef.current.abort();
    }
    abortRef.current = new AbortController();

    setLoading(true);
    try {
      const res = await fetch(
        `${API_BASE}/districts/suggestions?q=${encodeURIComponent(q.trim())}`,
        { signal: abortRef.current.signal }
      );
      if (!res.ok) throw new Error('API error');
      const data = await res.json();
      setSuggestions(data.suggestions || null);
      setActiveIndex(-1);
    } catch (err) {
      if (err.name !== 'AbortError') {
        // Silent fallback — local filtering in parent continues to work
        setSuggestions(null);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  // Debounce user input
  useEffect(() => {
    clearTimeout(debounceTimer.current);
    if (!value || value.trim().length === 0) {
      setSuggestions(null);
      setLoading(false);
      return;
    }
    debounceTimer.current = setTimeout(() => fetchSuggestions(value), 280);
    return () => clearTimeout(debounceTimer.current);
  }, [value, fetchSuggestions]);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => {
      if (
        dropdownRef.current && !dropdownRef.current.contains(e.target) &&
        inputRef.current && !inputRef.current.contains(e.target)
      ) {
        setSuggestions(null);
        setActiveIndex(-1);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handleKeyDown = (e) => {
    if (!flatSuggestions.length) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActiveIndex((i) => Math.min(i + 1, flatSuggestions.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (activeIndex >= 0 && flatSuggestions[activeIndex]) {
        selectSuggestion(flatSuggestions[activeIndex]);
      }
    } else if (e.key === 'Escape') {
      setSuggestions(null);
      setActiveIndex(-1);
      inputRef.current?.blur();
    }
  };

  const selectSuggestion = (item) => {
    setSuggestions(null);
    setActiveIndex(-1);
    // Navigate to the matching district
    if (item.district_no) {
      navigate(`/districts/${item.district_no}`);
      if (onDistrictSelect) onDistrictSelect(item.district_no);
      const mainEl = document.getElementById('main-content') || document.querySelector('main');
      if (mainEl) mainEl.scrollTo({ top: 0, behavior: 'smooth' });
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const groupMeta = {
    districts: {
      label_en: 'Districts',
      label_ta: 'மாவட்டங்கள்',
      icon: <MapPin className="w-3.5 h-3.5" />,
      color: 'text-[#172B40]',
    },
    historical_names: {
      label_en: 'Historical Names',
      label_ta: 'வரலாற்றுப் பெயர்கள்',
      icon: <History className="w-3.5 h-3.5" />,
      color: 'text-amber-700',
    },
    heritage_places: {
      label_en: 'Heritage & Specialities',
      label_ta: 'பாரம்பரியத் தலங்கள்',
      icon: <Landmark className="w-3.5 h-3.5" />,
      color: 'text-emerald-700',
    },
  };

  const hasResults = flatSuggestions.length > 0;
  const showDropdown =
    value && value.trim().length > 0 && (loading || suggestions !== null);

  let flatIdx = -1;

  return (
    <div className="relative w-full" role="combobox" aria-expanded={showDropdown} aria-haspopup="listbox">
      {/* Input */}
      <div className="relative">
        <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
        <input
          ref={inputRef}
          id="district-search-input"
          type="search"
          autoComplete="off"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => { if (value && value.trim()) fetchSuggestions(value); }}
          placeholder={t('district.searchPlaceholder', 'Search any of 38 districts… (e.g. Madurai, தஞ்சாவூர், Trichinopoly)')}
          aria-label={lang === 'ta' ? 'மாவட்டங்களைத் தேடுக' : 'Search districts'}
          aria-autocomplete="list"
          aria-controls="district-suggestion-list"
          className="w-full pl-10 pr-10 py-2.5 bg-white text-[#172B40] text-sm font-medium rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[#C5A66A] focus:border-[#C5A66A] placeholder-gray-400 transition-all shadow-sm"
        />
        <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1">
          {loading && <Loader2 className="w-3.5 h-3.5 text-[#C5A66A] animate-spin" />}
          {value && !loading && (
            <button
              type="button"
              onClick={() => { onClear(); setSuggestions(null); setActiveIndex(-1); }}
              aria-label={lang === 'ta' ? 'தேடலை அழிக்க' : 'Clear search'}
              className="text-gray-400 hover:text-gray-600 transition-colors p-0.5 rounded focus:outline-none focus:ring-1 focus:ring-[#C5A66A]"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>

      {/* Suggestion Dropdown */}
      {showDropdown && (
        <div
          ref={dropdownRef}
          id="district-suggestion-list"
          role="listbox"
          aria-label={lang === 'ta' ? 'தேடல் பரிந்துரைகள்' : 'Search suggestions'}
          className="absolute top-full left-0 right-0 mt-1.5 bg-white rounded-xl border border-gray-200 shadow-lg z-50 max-h-80 overflow-y-auto"
        >
          {loading && !hasResults && (
            <div className="px-4 py-3 text-xs text-gray-500 flex items-center gap-2">
              <Loader2 className="w-3.5 h-3.5 animate-spin text-[#C5A66A]" />
              <span>{lang === 'ta' ? 'தேடுகிறது…' : 'Searching…'}</span>
            </div>
          )}

          {!loading && suggestions && !hasResults && (
            <div className="px-4 py-3 text-xs text-gray-500">
              {lang === 'ta' ? 'பொருத்தமான மாவட்டம் கிடைக்கவில்லை.' : 'No matching districts found.'}
            </div>
          )}

          {['districts', 'historical_names', 'heritage_places'].map((group) => {
            const items = (suggestions || {})[group] || [];
            if (!items.length) return null;
            const meta = groupMeta[group];
            return (
              <div key={group}>
                {/* Group header */}
                <div className={`px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider flex items-center gap-1.5 bg-gray-50 border-b border-gray-100 ${meta.color}`}>
                  {meta.icon}
                  <span>{lang === 'ta' ? meta.label_ta : meta.label_en}</span>
                </div>
                {items.map((item) => {
                  flatIdx++;
                  const myIdx = flatIdx;
                  const isActive = myIdx === activeIndex;
                  const title = lang === 'ta' ? (item.title_ta || item.title) : item.title;
                  const subtitle = lang === 'ta' ? (item.subtitle_ta || item.subtitle) : item.subtitle;
                  return (
                    <button
                      key={`${group}-${item.district_no}-${item.title}`}
                      role="option"
                      aria-selected={isActive}
                      type="button"
                      onClick={() => selectSuggestion(item)}
                      onMouseEnter={() => setActiveIndex(myIdx)}
                      className={`w-full text-left px-4 py-2.5 flex items-start gap-3 transition-colors border-b border-gray-50 last:border-0 ${
                        isActive ? 'bg-[#F7F4ED]' : 'hover:bg-gray-50'
                      }`}
                    >
                      <div className="flex-1 min-w-0">
                        <span className="block text-sm font-semibold text-[#172B40] truncate">{title}</span>
                        {subtitle && (
                          <span className="block text-[11px] text-gray-500 truncate mt-0.5">{subtitle}</span>
                        )}
                      </div>
                      {item.type === 'historical_name' && (
                        <span className="shrink-0 text-[10px] px-1.5 py-0.5 rounded bg-amber-50 text-amber-700 border border-amber-200 font-semibold mt-0.5">
                          {lang === 'ta' ? 'வரலாற்று' : 'Historical'}
                        </span>
                      )}
                    </button>
                  );
                })}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default DistrictSearchBar;
