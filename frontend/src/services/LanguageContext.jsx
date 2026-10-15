import React, { createContext, useContext, useState, useEffect } from 'react';
import enTranslations from '../locales/en.json';
import taTranslations from '../locales/ta.json';

const translations = {
  en: enTranslations,
  ta: taTranslations,
};

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  // Default to Tamil 'ta' if not stored in localStorage
  const [lang, setLangState] = useState(() => {
    const saved = localStorage.getItem('peyar_lang');
    return saved === 'en' ? 'en' : 'ta';
  });

  const setLang = (newLang) => {
    const valid = newLang === 'en' ? 'en' : 'ta';
    setLangState(valid);
    localStorage.setItem('peyar_lang', valid);
  };

  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  // Nested translation helper: t('home.searchPlaceholder')
  const t = (keyPath, fallback = '') => {
    if (!keyPath) return '';
    const keys = keyPath.split('.');
    let current = translations[lang];
    for (const k of keys) {
      if (current && typeof current === 'object' && k in current) {
        current = current[k];
      } else {
        // Fallback to English, then to fallback string or key itself
        let alt = translations.en;
        for (const ak of keys) {
          if (alt && typeof alt === 'object' && ak in alt) {
            alt = alt[ak];
          } else {
            return fallback || keyPath;
          }
        }
        return alt || fallback || keyPath;
      }
    }
    return typeof current === 'string' ? current : fallback || keyPath;
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useTranslation = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useTranslation must be used within a LanguageProvider');
  }
  return context;
};
