import React from 'react';
import { useTranslation } from '../services/LanguageContext';
import { Globe2, Menu, X, Landmark } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

export const Navbar = ({ mobileMenuOpen, setMobileMenuOpen }) => {
  const { lang, setLang, t } = useTranslation();
  const location = useLocation();

  return (
    <header className="bg-[#172B40] text-white border-b border-[#2C3F55] sticky top-0 z-40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Title */}
          <div className="flex items-center gap-2.5 sm:gap-3 min-w-0">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 rounded-lg text-gray-300 hover:text-white hover:bg-[#20364F] focus:outline-none focus:ring-2 focus:ring-[#C5A66A] shrink-0"
              aria-label={lang === 'ta' ? 'பட்டி திறக்க' : 'Toggle navigation menu'}
            >
              {mobileMenuOpen ? <X className="w-5 h-5 sm:w-6 sm:h-6" /> : <Menu className="w-5 h-5 sm:w-6 sm:h-6" />}
            </button>
            <Link to="/" className="flex items-center gap-2 sm:gap-3 group min-w-0">
              <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-lg bg-[#C5A66A] flex items-center justify-center text-[#172B40] font-bold shadow-inner group-hover:bg-[#d6b980] transition-colors shrink-0">
                <Landmark className="w-5 h-5 sm:w-6 sm:h-6" />
              </div>
              <div className="min-w-0">
                <h1 className="text-sm sm:text-base md:text-lg font-bold tracking-wide text-white leading-tight truncate">
                  {lang === 'ta' ? 'பெயர்வரலாறு AI' : 'PeyarVaralaru AI'}
                </h1>
                <p className="text-[10px] sm:text-xs text-[#C5A66A] tracking-wider uppercase font-medium truncate hidden xs:block">
                  {lang === 'ta' ? 'வரலாற்று இடப்பெயர் ஆய்வு' : 'Historical Place Name Explorer'}
                </p>
              </div>
            </Link>
          </div>

          {/* Large Screen Quick Navigation Links (Sidebar serves as primary navigation on desktop) */}
          <nav className="hidden 2xl:flex items-center gap-1">
            <Link
              to="/"
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                location.pathname === '/'
                  ? 'bg-[#20364F] text-[#C5A66A]'
                  : 'text-gray-300 hover:text-white hover:bg-[#20364F]/50'
              }`}
            >
              {t('nav.home', 'Home')}
            </Link>
            <Link
              to="/districts"
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                location.pathname.startsWith('/districts')
                  ? 'bg-[#20364F] text-[#C5A66A]'
                  : 'text-gray-300 hover:text-white hover:bg-[#20364F]/50'
              }`}
            >
              {lang === 'ta' ? 'மாவட்டங்கள் (38)' : '38 Districts'}
            </Link>
            <Link
              to="/search"
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                location.pathname.startsWith('/search')
                  ? 'bg-[#20364F] text-[#C5A66A]'
                  : 'text-gray-300 hover:text-white hover:bg-[#20364F]/50'
              }`}
            >
              {t('nav.search', 'Search')}
            </Link>
            <Link
              to="/timeline"
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                location.pathname === '/timeline'
                  ? 'bg-[#20364F] text-[#C5A66A]'
                  : 'text-gray-300 hover:text-white hover:bg-[#20364F]/50'
              }`}
            >
              {lang === 'ta' ? 'காலவரிசை' : 'Timeline'}
            </Link>
            <Link
              to="/maps"
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                location.pathname.startsWith('/maps')
                  ? 'bg-[#20364F] text-[#C5A66A]'
                  : 'text-gray-300 hover:text-white hover:bg-[#20364F]/50'
              }`}
            >
              {lang === 'ta' ? 'வரலாற்று வரைபடங்கள்' : 'Historical Maps'}
            </Link>
            <Link
              to="/sources"
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                location.pathname === '/sources'
                  ? 'bg-[#20364F] text-[#C5A66A]'
                  : 'text-gray-300 hover:text-white hover:bg-[#20364F]/50'
              }`}
            >
              {t('nav.sources', 'Sources')}
            </Link>
            <Link
              to="/ask"
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                location.pathname === '/ask'
                  ? 'bg-[#20364F] text-[#C5A66A]'
                  : 'text-gray-300 hover:text-white hover:bg-[#20364F]/50'
              }`}
            >
              {t('nav.askAI', 'Ask AI')}
            </Link>
            <Link
              to="/graph"
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                location.pathname === '/graph'
                  ? 'bg-[#20364F] text-[#C5A66A]'
                  : 'text-gray-300 hover:text-white hover:bg-[#20364F]/50'
              }`}
            >
              {t('nav.graph', 'Graph')}
            </Link>
          </nav>

          {/* Right Header actions: Language Selector */}
          <div className="flex items-center gap-1.5 sm:gap-3 shrink-0">
            <div 
              className="inline-flex items-center bg-[#0F1D2C] p-0.5 sm:p-1 rounded-xl border border-[#2C3F55] shadow-inner"
              role="group"
              aria-label={lang === 'ta' ? 'மொழி தேர்வு' : 'Language selection'}
            >
              <Globe2 className="w-3.5 h-3.5 text-[#C5A66A] ml-1.5 mr-1 shrink-0 hidden sm:inline-block" />
              <button
                type="button"
                onClick={() => setLang('ta')}
                aria-pressed={lang === 'ta'}
                className={`px-2 sm:px-3 py-1 rounded-lg text-[11px] sm:text-xs font-bold transition-all focus:outline-none focus:ring-2 focus:ring-[#C5A66A] ${
                  lang === 'ta'
                    ? 'bg-[#C5A66A] text-[#172B40] shadow-sm font-extrabold'
                    : 'text-gray-300 hover:text-white hover:bg-[#20364F]/60'
                }`}
              >
                தமிழ்
              </button>
              <button
                type="button"
                onClick={() => setLang('en')}
                aria-pressed={lang === 'en'}
                className={`px-2 sm:px-3 py-1 rounded-lg text-[11px] sm:text-xs font-bold transition-all focus:outline-none focus:ring-2 focus:ring-[#C5A66A] ${
                  lang === 'en'
                    ? 'bg-[#C5A66A] text-[#172B40] shadow-sm font-extrabold'
                    : 'text-gray-300 hover:text-white hover:bg-[#20364F]/60'
                }`}
              >
                English
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
