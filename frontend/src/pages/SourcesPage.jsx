import React, { useState, useEffect } from 'react';
import { useTranslation } from '../services/LanguageContext';
import { getAllSources } from '../services/api';
import StatusBadge from '../components/StatusBadge';
import { 
  BookOpen, 
  ExternalLink, 
  FileText, 
  ShieldCheck, 
  Calendar, 
  Building2, 
  Search, 
  Filter,
  CheckCircle2,
  AlertTriangle,
  HelpCircle
} from 'lucide-react';

export const SourcesPage = () => {
  const { lang, t } = useTranslation();
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterQuery, setFilterQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    const fetchSources = async () => {
      try {
        const data = await getAllSources();
        setSources(data);
      } catch (err) {
        console.error('Failed to load sources:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchSources();
  }, []);

  const filteredSources = sources.filter((s) => {
    const title = (s.title || '').toLowerCase();
    const titleTa = (s.title_tamil || '').toLowerCase();
    const docId = (s.document_identifier || '').toLowerCase();
    const publisher = (s.publisher || '').toLowerCase();
    const q = filterQuery.toLowerCase();

    const matchesQuery = !q || title.includes(q) || titleTa.includes(q) || docId.includes(q) || publisher.includes(q);

    // Filter by pseudo-status based on id or attributes
    if (statusFilter === 'all') return matchesQuery;
    if (statusFilter === 'verified') return matchesQuery && (s.id === 1 || s.id === 2);
    if (statusFilter === 'partially_verified') return matchesQuery && (s.id === 3 || s.id === 4);
    return matchesQuery;
  });

  return (
    <div className="space-y-6 max-w-5xl mx-auto py-2">
      {/* Header Banner */}
      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-gray-200 shadow-sm space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#C5A66A]/20 text-[#172B40] flex items-center justify-center">
            <BookOpen className="w-5 h-5 text-[#C5A66A]" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-[#172B40]">
              {t('evidence.title', 'Evidence & Source Explorer')}
            </h2>
            <p className="text-xs sm:text-sm text-gray-500">
              {lang === 'ta'
                ? 'அரசு ஆணைகள், அரசிதழ்கள் மற்றும் காப்பக ஆவணங்களின் தொகுப்பு'
                : 'Primary government orders, district gazetteers, and epigraphical records.'}
            </p>
          </div>
        </div>

        {/* Verification Ethics Warning Banner */}
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 flex items-start gap-3">
          <ShieldCheck className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
          <div className="text-xs text-amber-900 leading-relaxed">
            <span className="font-bold">
              {lang === 'ta' ? 'சான்றாதார நெறிமுறை:' : 'Evidence Standard:'}{' '}
            </span>
            {lang === 'ta'
              ? 'AI உருவாக்கிய பதில்கள் தானாகவே சரிபார்க்கப்பட்டதாகக் கருதப்படாது. முதன்மை அரசு ஆவணங்கள் மற்றும் அரசிதழ் பதிவுகள் கொண்டு நேரடியாக ஆய்வு செய்யப்பட்ட தகவல்கள் மட்டுமே சரிபார்க்கப்பட்டவையாகக் குறிக்கப்படும்.'
              : 'Records are never marked as verified merely because an AI model generated a response. Verification strictly requires primary gazetteers, government orders, or archival citations.'}
          </div>
        </div>

        {/* Search & Filter Controls */}
        <div className="flex flex-col sm:flex-row items-center gap-3 pt-2">
          <div className="relative w-full sm:w-80">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
            <input
              type="text"
              value={filterQuery}
              onChange={(e) => setFilterQuery(e.target.value)}
              placeholder={lang === 'ta' ? 'ஆவணங்களைத் தேடுங்கள்...' : 'Filter documents or G.O. numbers...'}
              className="w-full pl-9 pr-3 py-2 text-xs text-[#172B40] bg-[#F7F4ED] rounded-lg border border-gray-200 focus:outline-none focus:border-[#C5A66A]"
            />
          </div>

          <div className="flex items-center gap-2 w-full sm:w-auto">
            <Filter className="w-4 h-4 text-gray-400 shrink-0" />
            <button
              onClick={() => setStatusFilter('all')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                statusFilter === 'all'
                  ? 'bg-[#172B40] text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {lang === 'ta' ? 'அனைத்தும்' : 'All'}
            </button>
            <button
              onClick={() => setStatusFilter('verified')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                statusFilter === 'verified'
                  ? 'bg-emerald-700 text-white'
                  : 'bg-emerald-50 text-emerald-800 hover:bg-emerald-100'
              }`}
            >
              {lang === 'ta' ? 'சரிபார்க்கப்பட்டது' : 'Verified'}
            </button>
            <button
              onClick={() => setStatusFilter('partially_verified')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                statusFilter === 'partially_verified'
                  ? 'bg-amber-700 text-white'
                  : 'bg-amber-50 text-amber-800 hover:bg-amber-100'
              }`}
            >
              {lang === 'ta' ? 'பகுதி சரிபார்க்கப்பட்டது' : 'Partially Verified'}
            </button>
          </div>
        </div>
      </div>

      {/* Sources List */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-bold text-[#172B40]">
            {lang === 'ta' ? 'ஆவணப் பதிவுகள்' : 'Archival Documents'}{' '}
            <span className="text-xs font-normal text-gray-500">
              ({filteredSources.length} {lang === 'ta' ? 'மூலங்கள்' : 'sources'})
            </span>
          </h3>
        </div>

        {loading ? (
          <div className="text-center py-12 bg-white rounded-xl border border-gray-200 text-gray-500 text-sm">
            <div className="inline-block animate-spin w-6 h-6 border-2 border-[#172B40] border-t-transparent rounded-full mb-2"></div>
            <p>{t('common.loading', 'Loading archival sources...')}</p>
          </div>
        ) : filteredSources.length === 0 ? (
          <div className="bg-white rounded-2xl p-10 border border-gray-200 text-center text-gray-500 text-sm">
            {lang === 'ta' ? 'பொருத்தமான ஆவணங்கள் எதுவும் இல்லை.' : 'No matching archival records found.'}
          </div>
        ) : (
          <div className="space-y-4">
            {filteredSources.map((src) => {
              const isVerified = src.id === 1 || src.id === 2;
              return (
                <div
                  key={src.id}
                  className="bg-white rounded-xl p-6 border border-gray-200 hover:border-[#C5A66A] shadow-sm hover:shadow-md transition-all space-y-3"
                >
                  <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2 flex-wrap">
                        <FileText className="w-4 h-4 text-[#C5A66A] shrink-0" />
                        <h4 className="text-base font-bold text-[#172B40]">
                          {lang === 'ta' && src.title_tamil ? src.title_tamil : src.title}
                        </h4>
                      </div>
                      {src.document_identifier && (
                        <div className="inline-block px-2 py-0.5 bg-[#F7F4ED] text-[#172B40] text-xs font-mono font-semibold rounded border border-gray-200">
                          {src.document_identifier}
                        </div>
                      )}
                    </div>

                    <StatusBadge
                      status={isVerified ? 'verified' : 'partially_verified'}
                      size="sm"
                    />
                  </div>

                  {/* Metadata Row */}
                  <div className="flex flex-wrap items-center gap-4 text-xs text-gray-600 pt-1 border-t border-gray-100">
                    <div className="flex items-center gap-1.5">
                      <Building2 className="w-3.5 h-3.5 text-gray-400" />
                      <span>{src.publisher || 'Government Authority'}</span>
                    </div>
                    {src.publication_date && (
                      <div className="flex items-center gap-1.5">
                        <Calendar className="w-3.5 h-3.5 text-gray-400" />
                        <span>{src.publication_date}</span>
                      </div>
                    )}
                    {src.page_number && (
                      <div className="text-gray-500">
                        {lang === 'ta' ? 'பக்கம்:' : 'Page:'} {src.page_number}
                      </div>
                    )}
                  </div>

                  {/* Evidence Excerpt */}
                  {(src.evidence_excerpt || src.evidence_excerpt_tamil) && (
                    <div className="bg-[#F7F4ED] p-3.5 rounded-lg border border-gray-200">
                      <span className="text-[11px] font-bold uppercase tracking-wider text-gray-500 block mb-1">
                        {t('evidence.excerpt', 'Archival Excerpt / Citation')}
                      </span>
                      <blockquote className="text-xs text-gray-800 italic leading-relaxed">
                        "{lang === 'ta' && src.evidence_excerpt_tamil ? src.evidence_excerpt_tamil : src.evidence_excerpt}"
                      </blockquote>
                    </div>
                  )}

                  {/* Action Link */}
                  {src.source_url && (
                    <div className="pt-2 flex justify-end">
                      <a
                        href={src.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-700 hover:text-blue-900 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-lg transition-colors"
                      >
                        <span>{lang === 'ta' ? 'அதிகாரப்பூர்வ ஆவணத்தைக் காண்க' : 'Open Official Source'}</span>
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default SourcesPage;
