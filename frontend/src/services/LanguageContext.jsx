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

  // Nested translation helper with optional interpolation: t('district.whatMakesSpecial', '', { name: 'மதுரை' })
  const t = (keyPath, fallback = '', params = {}) => {
    if (!keyPath) return '';
    const keys = keyPath.split('.');
    let current = translations[lang];
    let found = true;

    for (const k of keys) {
      if (current && typeof current === 'object' && k in current) {
        current = current[k];
      } else {
        found = false;
        break;
      }
    }

    if (!found) {
      // Fallback to English, then to fallback string or key itself
      let alt = translations.en;
      let altFound = true;
      for (const ak of keys) {
        if (alt && typeof alt === 'object' && ak in alt) {
          alt = alt[ak];
        } else {
          altFound = false;
          break;
        }
      }
      if (altFound && typeof alt === 'string') {
        current = alt;
      } else {
        current = fallback || keyPath;
      }
    }

    let text = typeof current === 'string' ? current : (fallback || keyPath);

    // Replace {param} placeholders if any
    if (params && typeof params === 'object') {
      for (const [pk, pv] of Object.entries(params)) {
        text = text.replace(new RegExp(`\\{${pk}\\}`, 'g'), String(pv));
      }
    }

    return text;
  };

  // Helper to reliably retrieve language-appropriate text from data objects
  const localize = (obj, field, fallback = '') => {
    if (!obj) return fallback;
    if (lang === 'ta') {
      const val = obj[`${field}_ta`] || obj[`${field}_tamil`];
      if (val) return val;
      // If default field has Tamil script, use it
      const base = obj[field];
      if (typeof base === 'string' && /[\u0B80-\u0BFF]/.test(base)) return base;
      return fallback || base || '';
    } else {
      const val = obj[`${field}_en`] || obj[`${field}_english`];
      if (val) return val;
      // If default field does not have Tamil script, use it
      const base = obj[field];
      if (typeof base === 'string' && !/[\u0B80-\u0BFF]/.test(base)) return base;
      return fallback || base || '';
    }
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang, t, localize }}>
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

export default LanguageContext;
