import React from 'react';
import { CheckCircle2, AlertTriangle, HelpCircle } from 'lucide-react';
import { useTranslation } from '../services/LanguageContext';

export const StatusBadge = ({ status, size = 'sm' }) => {
  const { lang, t } = useTranslation();

  const normalized = (status || 'unverified').toLowerCase().replace(' ', '_');

  const configs = {
    verified: {
      label: lang === 'ta' ? 'சரிபார்க்கப்பட்டது' : 'Verified',
      bgClass: 'bg-emerald-50 text-emerald-800 border-emerald-300',
      icon: CheckCircle2,
    },
    partially_verified: {
      label: lang === 'ta' ? 'பகுதி சரிபார்க்கப்பட்டது' : 'Partially Verified',
      bgClass: 'bg-amber-50 text-amber-800 border-amber-300',
      icon: AlertTriangle,
    },
    unverified: {
      label: lang === 'ta' ? 'சரிபார்க்கப்படாதது' : 'Unverified',
      bgClass: 'bg-rose-50 text-rose-800 border-rose-300',
      icon: HelpCircle,
    },
  };

  const current = configs[normalized] || configs.unverified;
  const Icon = current.icon;
  const sizeClasses = size === 'lg' ? 'px-3 py-1.5 text-sm gap-1.5' : 'px-2 py-0.5 text-xs gap-1';

  return (
    <span className={`inline-flex items-center font-medium rounded-full border ${current.bgClass} ${sizeClasses}`}>
      <Icon className={size === 'lg' ? 'w-4 h-4' : 'w-3 h-3'} />
      <span>{current.label}</span>
    </span>
  );
};

export default StatusBadge;
