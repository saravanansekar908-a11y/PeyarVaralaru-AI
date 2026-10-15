import React from 'react';
import { useTranslation } from '../services/LanguageContext';
import { BookOpen, Globe2, Menu, X, Landmark } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

export const Navbar = ({ mobileMenuOpen, setMobileMenuOpen }) => {
  const { lang, setLang, t } = useTranslation();
  const location = useLocation();

  return (
    <header className="bg-[#172B40] text-white border-b border-[#2C3F55] sticky top-0 z-40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Title */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 rounded-md text-gray-300 hover:text-white hover:bg-[#20364F] focus:outline-none"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
            <Link to="/" className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-lg bg-[#C5A66A] flex items-center justify-center text-[#172B40] font-bold shadow-inner group-hover:bg-[#d6b980] transition-colors">
                <Landmark className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-lg font-bold tracking-wide text-white leading-tight">
                  {lang === 'ta' ? 'பெயர்வரலாறு AI' : 'PeyarVaralaru AI'}
                </h1>
                <p className="text-xs text-[#C5A66A] tracking-wider uppercase font-medium">
                  {lang === 'ta' ? 'வரலாற்று இடப்பெயர் ஆய்வு' : 'Historical Place Name Explorer'}
                </p>
              </div>
            </Link>
          </div>

          {/* Right Header actions: Language Selector */}
          <div className="flex items-center gap-3">
            <div className="inline-flex items-center bg-[#0F1D2C] p-1 rounded-lg border border-[#2C3F55]">
              <Globe2 className="w-4 h-4 text-[#C5A66A] ml-2 mr-1.5" />
              <button
                onClick={() => setLang('ta')}
                className={`px-3 py-1 rounded text-xs font-semibold transition-all ${
                  lang === 'ta'
                    ? 'bg-[#C5A66A] text-[#172B40] shadow-sm'
                    : 'text-gray-300 hover:text-white'
                }`}
              >
                தமிழ்
              </button>
              <button
                onClick={() => setLang('en')}
                className={`px-3 py-1 rounded text-xs font-semibold transition-all ${
                  lang === 'en'
                    ? 'bg-[#C5A66A] text-[#172B40] shadow-sm'
                    : 'text-gray-300 hover:text-white'
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
