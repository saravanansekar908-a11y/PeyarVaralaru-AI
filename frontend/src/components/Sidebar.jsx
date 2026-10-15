import React from 'react';
import { NavLink } from 'react-router-dom';
import { useTranslation } from '../services/LanguageContext';
import { 
  Home, 
  Search, 
  Clock, 
  BookOpen, 
  Bot, 
  Network, 
  ShieldCheck,
  ChevronRight 
} from 'lucide-react';

export const Sidebar = ({ mobileMenuOpen, setMobileMenuOpen }) => {
  const { lang, t } = useTranslation();

  const navItems = [
    {
      to: '/',
      label: t('nav.home', 'Home'),
      icon: Home,
      exact: true,
    },
    {
      to: '/search',
      label: t('nav.search', 'Smart Search'),
      icon: Search,
    },
    {
      to: '/places/1',
      label: t('nav.timeline', 'Place Timeline'),
      icon: Clock,
    },
    {
      to: '/sources',
      label: t('nav.sources', 'Evidence & Sources'),
      icon: BookOpen,
    },
    {
      to: '/ask',
      label: t('nav.askAI', 'Ask History AI'),
      icon: Bot,
    },
    {
      to: '/graph',
      label: t('nav.graph', 'Relationship Graph'),
      icon: Network,
    },
  ];

  const handleLinkClick = () => {
    if (setMobileMenuOpen) {
      setMobileMenuOpen(false);
    }
  };

  return (
    <>
      {/* Mobile backdrop */}
      {mobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar container */}
      <aside
        className={`fixed lg:static top-16 bottom-0 left-0 z-30 w-64 bg-[#172B40] text-gray-200 border-r border-[#243950] flex flex-col justify-between transition-transform duration-200 ease-in-out ${
          mobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="p-4 space-y-1">
          <div className="px-3 py-2 text-xs font-semibold text-[#C5A66A] uppercase tracking-wider">
            {lang === 'ta' ? 'ஆய்வுத் தளங்கள்' : 'Research Modules'}
          </div>

          <nav className="space-y-1.5">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.exact}
                  onClick={handleLinkClick}
                  className={({ isActive }) =>
                    `flex items-center justify-between px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-[#C5A66A] text-[#172B40] shadow-sm font-semibold'
                        : 'text-gray-300 hover:bg-[#20364F] hover:text-white'
                    }`
                  }
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-4 h-4 shrink-0" />
                    <span>{item.label}</span>
                  </div>
                  <ChevronRight className="w-3.5 h-3.5 opacity-60" />
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Footer verification badge / info */}
        <div className="p-4 border-t border-[#243950] bg-[#122233]">
          <div className="flex items-center gap-2 text-xs text-[#C5A66A] font-medium mb-1">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>{lang === 'ta' ? 'சான்றாதார அமைப்பு' : 'Evidence-Grounded'}</span>
          </div>
          <p className="text-[11px] text-gray-400 leading-relaxed">
            {lang === 'ta'
              ? 'தமிழ்நாடு ஆவணக் காப்பகம் மற்றும் அரசிதழ் சான்றுகள் அடிப்படையில் உருவாக்கப்பட்டது.'
              : 'Grounded in Tamil Nadu Archives & Government Gazetteers.'}
          </p>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
