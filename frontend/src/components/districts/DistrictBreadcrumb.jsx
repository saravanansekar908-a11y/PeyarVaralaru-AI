import React from 'react';
import { Link } from 'react-router-dom';
import { ChevronRight, Home, Compass } from 'lucide-react';
import { useTranslation } from '../../services/LanguageContext';

/**
 * DistrictBreadcrumb — renders "Home → Districts" or "Home → Districts → {Name}"
 * based on whether a district is currently selected.
 */
const DistrictBreadcrumb = ({ selectedDistrict }) => {
  const { lang, t } = useTranslation();

  const districtName = selectedDistrict
    ? (lang === 'ta' ? selectedDistrict.district_tamil : selectedDistrict.district_english)
    : null;

  return (
    <nav aria-label={lang === 'ta' ? 'இருப்பிட வழி' : 'Breadcrumb'} className="flex items-center gap-1 text-xs text-gray-500 flex-wrap">
      <Link
        to="/"
        className="flex items-center gap-1 text-gray-500 hover:text-[#C5A66A] transition-colors font-medium"
      >
        <Home className="w-3 h-3" />
        <span>{t('nav.home', 'Home')}</span>
      </Link>

      <ChevronRight className="w-3 h-3 text-gray-400 shrink-0" />

      {districtName ? (
        <>
          <Link
            to="/districts"
            className="text-gray-500 hover:text-[#C5A66A] transition-colors font-medium flex items-center gap-1"
          >
            <Compass className="w-3 h-3" />
            <span>{t('nav.districts', '38 Districts')}</span>
          </Link>
          <ChevronRight className="w-3 h-3 text-gray-400 shrink-0" />
          <span className="text-[#172B40] font-semibold truncate max-w-[200px]">{districtName}</span>
        </>
      ) : (
        <span className="text-[#172B40] font-semibold flex items-center gap-1">
          <Compass className="w-3 h-3" />
          {t('nav.districts', '38 Districts')}
        </span>
      )}
    </nav>
  );
};

export default DistrictBreadcrumb;
