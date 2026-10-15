import React, { useState, useEffect } from 'react';
import { useTranslation } from '../services/LanguageContext';
import { getAllSources, getDocuments, getDocumentPassages, ingestDocument } from '../services/api';
import { 
  BookOpen, 
  ExternalLink, 
  FileText, 
  ShieldCheck, 
  Calendar, 
  Building2, 
  Search, 
  Filter,
  PlusCircle,
  ChevronDown,
  ChevronUp,
  Bookmark,
  CheckCircle2,
  AlertTriangle,
  HelpCircle,
  X,
  Compass,
  ArrowRight
} from 'lucide-react';

export const SourcesPage = () => {
  const { lang, t } = useTranslation();
  
  // Research Documents state
  const [documents, setDocuments] = useState([]);
  const [selectedDocPassages, setSelectedDocPassages] = useState({});
  const [expandedDocId, setExpandedDocId] = useState(null);
  
  // Legacy Sources state
  const [sources, setSources] = useState([]);
  
  const [loading, setLoading] = useState(true);
  const [filterQuery, setFilterQuery] = useState('');
  const [selectedType, setSelectedType] = useState('all');
  
  // Modal for ingesting new document without retraining
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [ingestForm, setIngestForm] = useState({
    title: '',
    title_tamil: '',
    author_or_authority: '',
    publication_year: new Date().getFullYear(),
    document_type: 'district_gazetteer',
    source_url: '',
    raw_text: '',
    place_name: '',
    district: '',
    taluk: '',
    village: '',
    page_number: 1,
    evidence_level: 'documented_fact',
  });
  const [ingestSubmitting, setIngestSubmitting] = useState(false);
  const [ingestSuccess, setIngestSuccess] = useState(null);
  const [ingestError, setIngestError] = useState(null);

  const documentTypeFilters = [
    { id: 'all', name_ta: 'அனைத்து ஆவணங்களும்', name_en: 'All Sources' },
    { id: 'district_gazetteer', name_ta: 'மாவட்ட அரசிதழ்கள்', name_en: 'District Gazetteers' },
    { id: 'epigraphical_record', name_ta: 'கல்வெட்டு வெளியீடுகள்', name_en: 'Epigraphical Records' },
    { id: 'government_record', name_ta: 'அரசாணைகள் (G.O.)', name_en: 'Government Orders' },
    { id: 'census_directory', name_ta: 'நில அளவை & மக்கள் தொகை', name_en: 'Census & Village Directory' },
  ];

  const loadData = async () => {
    setLoading(true);
    try {
      const [docsData, sourcesData] = await Promise.all([
        getDocuments().catch(() => []),
        getAllSources().catch(() => []),
      ]);
      setDocuments(docsData || []);
      setSources(sourcesData || []);
    } catch (err) {
      console.error('Failed to load sources or documents:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const toggleExpandDoc = async (docId) => {
    if (expandedDocId === docId) {
      setExpandedDocId(null);
      return;
    }
    setExpandedDocId(docId);
    if (!selectedDocPassages[docId]) {
      try {
        const passages = await getDocumentPassages(docId);
        setSelectedDocPassages((prev) => ({ ...prev, [docId]: passages }));
      } catch (err) {
        console.error('Failed to load passages for doc:', docId, err);
      }
    }
  };

  const handleIngestSubmit = async (e) => {
    e.preventDefault();
    setIngestSubmitting(true);
    setIngestError(null);
    setIngestSuccess(null);

    try {
      const payload = {
        title: ingestForm.title,
        title_tamil: ingestForm.title_tamil || ingestForm.title,
        author_or_authority: ingestForm.author_or_authority,
        publication_year: parseInt(ingestForm.publication_year, 10) || null,
        document_type: ingestForm.document_type,
        source_url: ingestForm.source_url || null,
        raw_text: ingestForm.raw_text,
        passages: [
          {
            page_number: parseInt(ingestForm.page_number, 10) || 1,
            passage_text: ingestForm.raw_text,
            passage_text_tamil: ingestForm.raw_text,
            place_name: ingestForm.place_name || null,
            district: ingestForm.district || null,
            taluk: ingestForm.taluk || null,
            village: ingestForm.village || null,
            evidence_level: ingestForm.evidence_level,
          }
        ]
      };

      await ingestDocument(payload);
      setIngestSuccess(
        lang === 'ta' 
          ? 'ஆவணம் வெற்றிகரமாகச் சேர்க்கப்பட்டது! RAG தரவுதளத்தில் உடனடி பயன்பாட்டுக்கு வந்தது.' 
          : 'Document ingested successfully into RAG without model retraining!'
      );
      await loadData();
      setTimeout(() => {
        setIsModalOpen(false);
        setIngestSuccess(null);
      }, 1500);
    } catch (err) {
      setIngestError(err.response?.data?.detail || err.message || 'Failed to ingest document');
    } finally {
      setIngestSubmitting(false);
    }
  };

  const filteredDocuments = documents.filter((doc) => {
    // Type Filter
    if (selectedType !== 'all' && doc.document_type !== selectedType) {
      return false;
    }
    // Query Search
    const q = filterQuery.toLowerCase().trim();
    if (!q) return true;
    const title = (doc.title || '').toLowerCase();
    const titleTa = (doc.title_tamil || '').toLowerCase();
    const auth = (doc.author_or_authority || '').toLowerCase();
    const docType = (doc.document_type || '').toLowerCase();
    return title.includes(q) || titleTa.includes(q) || auth.includes(q) || docType.includes(q);
  });

  const getDocTypeBadge = (type) => {
    switch (type) {
      case 'district_gazetteer':
        return (
          <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-blue-100 text-blue-900 border border-blue-200">
            {lang === 'ta' ? 'மாவட்ட அரசிதழ்' : 'District Gazetteer'}
          </span>
        );
      case 'epigraphical_record':
        return (
          <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-purple-100 text-purple-900 border border-purple-200">
            {lang === 'ta' ? 'கல்வெட்டு அறிக்கை' : 'Epigraphy / Inscriptions'}
          </span>
        );
      case 'government_record':
        return (
          <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-900 border border-emerald-200">
            {lang === 'ta' ? 'அரசாணை (G.O.)' : 'Government Order'}
          </span>
        );
      default:
        return (
          <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-100 text-amber-900 border border-amber-200">
            {lang === 'ta' ? 'மக்கள் தொகை / நில அளவை' : 'Census / Survey'}
          </span>
        );
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto py-2">
      {/* Header Banner */}
      <div className="bg-[#172B40] text-white rounded-2xl p-6 sm:p-8 border border-[#2A3E54] shadow-sm relative overflow-hidden">
        <div className="absolute right-0 top-0 w-80 h-80 bg-[#C5A66A]/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#C5A66A]/20 border border-[#C5A66A]/40 text-[#C5A66A] text-xs font-semibold">
              <BookOpen className="w-3.5 h-3.5" />
              <span>{lang === 'ta' ? 'அரசிதழ் & கல்வெட்டு நூலகம்' : 'Archival Citations & Sources'}</span>
            </div>

            <button
              onClick={() => setIsModalOpen(true)}
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-[#C5A66A] hover:bg-[#b8985c] text-[#172B40] text-xs font-bold transition-all shadow-sm shrink-0"
            >
              <PlusCircle className="w-4 h-4" />
              <span>{lang === 'ta' ? 'புதிய ஆவணம் சேர்க்க' : 'Ingest New Document'}</span>
            </button>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {lang === 'ta'
              ? 'தமிழ்நாடு வரலாற்று மூல ஆவணங்கள் மற்றும் அரசிதழ்கள்'
              : 'Primary Historical Gazetteers, Inscriptions & G.O. Records'}
          </h1>
          <p className="text-xs sm:text-sm text-gray-300 max-w-2xl leading-relaxed">
            {lang === 'ta'
              ? 'இங்கு பட்டியலிடப்பட்டுள்ள அனைத்து ஆவணங்களும் தமிழ்நாடு ஆவணக் காப்பகம் மற்றும் இந்தியத் தொல்லியல் துறையின் அங்கீகரிக்கப்பட்ட வெளியீடுகளாகும். ஒவ்வொரு தகவலும் குறிப்பிட்ட பக்க எண்களுடன் மேற்கோள் காட்டப்பட்டுள்ளது.'
              : 'Official publications from the Archaeological Survey of India (ASI), Fort St. George Gazette, and District Manuals used as the ground truth for place name research.'}
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm space-y-3">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
            <input
              type="text"
              value={filterQuery}
              onChange={(e) => setFilterQuery(e.target.value)}
              placeholder={
                lang === 'ta'
                  ? 'ஆவணத்தின் தலைப்பு அல்லது ஆசிரியர் பெயரால் தேடுக...'
                  : 'Search by document title or issuing authority...'
              }
              className="w-full pl-9 pr-4 py-2 bg-[#F7F4ED] text-[#172B40] rounded-lg text-xs font-medium placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-[#C5A66A] border border-gray-200"
            />
          </div>
        </div>

        {/* Document Type Chips */}
        <div className="flex flex-wrap gap-2 pt-1">
          {documentTypeFilters.map((flt) => (
            <button
              key={flt.id}
              onClick={() => setSelectedType(flt.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                selectedType === flt.id
                  ? 'bg-[#172B40] text-white shadow-sm'
                  : 'bg-[#F7F4ED] text-[#172B40] hover:bg-[#eae5d8] border border-gray-200'
              }`}
            >
              {lang === 'ta' ? flt.name_ta : flt.name_en}
            </button>
          ))}
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="bg-white rounded-2xl p-12 border border-gray-200 text-center space-y-4 shadow-sm">
          <div className="inline-block animate-spin w-8 h-8 border-3 border-[#172B40] border-t-transparent rounded-full" />
          <p className="text-xs font-semibold text-gray-600">
            {lang === 'ta' ? 'ஆவணங்களை ஏற்றுகிறது...' : 'Loading archival citation records...'}
          </p>
        </div>
      )}

      {/* Citations List */}
      {!loading && (
        <div className="space-y-4">
          <div className="text-xs font-semibold text-gray-500 px-1">
            {lang === 'ta'
              ? `காட்டப்படும் ஆவணங்கள்: ${filteredDocuments.length}`
              : `Displaying ${filteredDocuments.length} primary source documents`}
          </div>

          <div className="space-y-4">
            {filteredDocuments.map((doc) => {
              const isExpanded = expandedDocId === doc.id;
              const docPassages = selectedDocPassages[doc.id] || [];

              return (
                <div
                  key={doc.id}
                  className="bg-white rounded-2xl border border-gray-200 p-5 shadow-sm hover:shadow-md transition-shadow space-y-3"
                >
                  <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                    <div className="space-y-1.5">
                      <div className="flex flex-wrap items-center gap-2">
                        {getDocTypeBadge(doc.document_type)}
                        <span className="text-xs font-bold text-gray-500 bg-[#F7F4ED] px-2 py-0.5 rounded border border-gray-200">
                          {doc.publication_year ? `${doc.publication_year}` : 'Historical'}
                        </span>
                      </div>

                      <h3 className="text-base sm:text-lg font-bold text-[#172B40]">
                        {lang === 'ta' ? (doc.title_tamil || doc.title) : (doc.title || doc.title_tamil)}
                      </h3>

                      <div className="text-xs text-gray-600 flex items-center gap-1.5 pt-0.5">
                        <Building2 className="w-3.5 h-3.5 text-[#C5A66A]" />
                        <span>
                          <strong className="text-[#172B40]">{lang === 'ta' ? 'வெளியீடு / அதிகாரி:' : 'Authority:'}</strong>{' '}
                          {doc.author_or_authority}
                        </span>
                      </div>
                    </div>

                    {/* Source URL External Link */}
                    {doc.source_url && (
                      <a
                        href={doc.source_url}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-[#F7F4ED] hover:bg-[#eae5d8] text-[#172B40] text-xs font-bold border border-gray-200 transition-colors shrink-0"
                      >
                        <span>{lang === 'ta' ? 'அசல் ஆவணம்' : 'Archival Link'}</span>
                        <ExternalLink className="w-3.5 h-3.5 text-[#C5A66A]" />
                      </a>
                    )}
                  </div>

                  {/* Passage Count & Toggle Button */}
                  <div className="pt-2 border-t border-gray-100 flex items-center justify-between">
                    <button
                      onClick={() => toggleExpandDoc(doc.id)}
                      className="inline-flex items-center gap-1.5 text-xs font-bold text-[#172B40] hover:text-[#C5A66A] transition-colors"
                    >
                      <Bookmark className="w-3.5 h-3.5 text-[#C5A66A]" />
                      <span>
                        {isExpanded
                          ? (lang === 'ta' ? 'பத்திகளை மறைக்க' : 'Hide Passages')
                          : (lang === 'ta' ? `ஆவணப் பத்திகளைக் காண்க (${doc.passages_count || 1})` : `View Extracted Passages (${doc.passages_count || 1})`)}
                      </span>
                      {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                    </button>

                    <span className="text-[11px] text-gray-400">
                      ID: #{doc.id}
                    </span>
                  </div>

                  {/* Expanded Passages Drawer */}
                  {isExpanded && (
                    <div className="pt-3 space-y-2 border-t border-gray-100">
                      {docPassages.length > 0 ? (
                        docPassages.map((p, pIdx) => (
                          <div
                            key={p.id || pIdx}
                            className="p-3.5 rounded-xl bg-[#F7F4ED] border border-gray-200 space-y-1.5 text-xs text-[#172B40]"
                          >
                            <div className="flex items-center justify-between font-bold text-gray-600 text-[11px]">
                              <span>{lang === 'ta' ? `பக்க எண்: ${p.page_number}` : `Page No: ${p.page_number}`}</span>
                              {p.place_name && (
                                <span className="bg-white px-2 py-0.5 rounded text-[#172B40] border border-gray-200">
                                  {p.place_name} {p.district ? `(${p.district})` : ''}
                                </span>
                              )}
                            </div>
                            <p className="leading-relaxed italic">
                              "{lang === 'ta' ? (p.passage_text_tamil || p.passage_text) : (p.passage_text || p.passage_text_tamil)}"
                            </p>
                          </div>
                        ))
                      ) : (
                        <p className="text-xs text-gray-500 italic p-2">
                          {lang === 'ta' ? 'பத்திகள் ஏற்றப்படுகின்றன...' : 'Loading passages...'}
                        </p>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Ingest Document Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-xl w-full p-6 sm:p-8 space-y-5 shadow-2xl border border-gray-200 my-8">
            <div className="flex items-center justify-between border-b border-gray-100 pb-3">
              <div className="flex items-center gap-2">
                <PlusCircle className="w-5 h-5 text-[#C5A66A]" />
                <h3 className="text-lg font-bold text-[#172B40]">
                  {lang === 'ta' ? 'புதிய வரலாற்று ஆவணம் சேர்த்தல்' : 'Ingest Archival Document'}
                </h3>
              </div>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-gray-400 hover:text-gray-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {ingestSuccess && (
              <div className="p-3 rounded-xl bg-emerald-50 text-emerald-800 text-xs font-semibold border border-emerald-200">
                {ingestSuccess}
              </div>
            )}

            {ingestError && (
              <div className="p-3 rounded-xl bg-rose-50 text-rose-800 text-xs font-semibold border border-rose-200">
                {ingestError}
              </div>
            )}

            <form onSubmit={handleIngestSubmit} className="space-y-3.5 text-xs">
              <div>
                <label className="block font-bold text-gray-700 mb-1">
                  {lang === 'ta' ? 'ஆவணத் தலைப்பு (Title)' : 'Document Title'} *
                </label>
                <input
                  type="text"
                  required
                  value={ingestForm.title}
                  onChange={(e) => setIngestForm({ ...ingestForm, title: e.target.value })}
                  placeholder={lang === 'ta' ? 'எ.கா: வட ஆற்காடு மாவட்டக் குறிப்பேடு' : 'e.g. Imperial Gazetteer of India: North Arcot'}
                  className="w-full px-3 py-2 bg-[#F7F4ED] rounded-lg border border-gray-300 focus:outline-none focus:ring-1 focus:ring-[#C5A66A]"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-gray-700 mb-1">
                    {lang === 'ta' ? 'ஆசிரியர் / நிர்வாக அமைப்பு' : 'Author / Authority'} *
                  </label>
                  <input
                    type="text"
                    required
                    value={ingestForm.author_or_authority}
                    onChange={(e) => setIngestForm({ ...ingestForm, author_or_authority: e.target.value })}
                    placeholder={lang === 'ta' ? 'எ.கா: இந்திய தொல்லியல் துறை' : 'e.g. Archaeological Survey of India'}
                    className="w-full px-3 py-2 bg-[#F7F4ED] rounded-lg border border-gray-300 focus:outline-none focus:ring-1 focus:ring-[#C5A66A]"
                  />
                </div>
                <div>
                  <label className="block font-bold text-gray-700 mb-1">
                    {lang === 'ta' ? 'வெளியீட்டு ஆண்டு' : 'Year'}
                  </label>
                  <input
                    type="number"
                    value={ingestForm.publication_year}
                    onChange={(e) => setIngestForm({ ...ingestForm, publication_year: e.target.value })}
                    className="w-full px-3 py-2 bg-[#F7F4ED] rounded-lg border border-gray-300 focus:outline-none focus:ring-1 focus:ring-[#C5A66A]"
                  />
                </div>
              </div>

              <div>
                <label className="block font-bold text-gray-700 mb-1">
                  {lang === 'ta' ? 'ஆவண வகை' : 'Document Type'}
                </label>
                <select
                  value={ingestForm.document_type}
                  onChange={(e) => setIngestForm({ ...ingestForm, document_type: e.target.value })}
                  className="w-full px-3 py-2 bg-[#F7F4ED] rounded-lg border border-gray-300 focus:outline-none focus:ring-1 focus:ring-[#C5A66A]"
                >
                  <option value="district_gazetteer">{lang === 'ta' ? 'மாவட்ட அரசிதழ்' : 'District Gazetteer'}</option>
                  <option value="epigraphical_record">{lang === 'ta' ? 'கல்வெட்டு அறிக்கை' : 'Epigraphical Record / Inscription'}</option>
                  <option value="government_record">{lang === 'ta' ? 'அரசாணை (G.O.)' : 'Government Order (G.O.)'}</option>
                  <option value="census_directory">{lang === 'ta' ? 'நில அளவை & மக்கள் தொகை' : 'Census Village Directory'}</option>
                </select>
              </div>

              <div>
                <label className="block font-bold text-gray-700 mb-1">
                  {lang === 'ta' ? 'அசல் ஆவண இணைப்பு URL' : 'Source URL'}
                </label>
                <input
                  type="url"
                  value={ingestForm.source_url}
                  onChange={(e) => setIngestForm({ ...ingestForm, source_url: e.target.value })}
                  placeholder="https://archive.org/details/..."
                  className="w-full px-3 py-2 bg-[#F7F4ED] rounded-lg border border-gray-300 focus:outline-none focus:ring-1 focus:ring-[#C5A66A]"
                />
              </div>

              <div>
                <label className="block font-bold text-gray-700 mb-1">
                  {lang === 'ta' ? 'எடுக்கப்பட்ட வரலாற்றுப் பத்தி' : 'Passage Text'} *
                </label>
                <textarea
                  rows={4}
                  required
                  value={ingestForm.raw_text}
                  onChange={(e) => setIngestForm({ ...ingestForm, raw_text: e.target.value })}
                  placeholder={lang === 'ta' ? 'வரலாற்று மேற்கோள் அல்லது கல்வெட்டு வரிகளை ஒட்டுக...' : 'Paste historical excerpt or inscription transcription...'}
                  className="w-full px-3 py-2 bg-[#F7F4ED] rounded-lg border border-gray-300 focus:outline-none focus:ring-1 focus:ring-[#C5A66A]"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg transition-colors"
                >
                  {lang === 'ta' ? 'ரத்து செய்க' : 'Cancel'}
                </button>
                <button
                  type="submit"
                  disabled={ingestSubmitting}
                  className="px-5 py-2 bg-[#172B40] hover:bg-[#20364F] text-white font-bold rounded-lg transition-colors flex items-center gap-1.5"
                >
                  {ingestSubmitting && <div className="animate-spin w-3 h-3 border-2 border-[#C5A66A] border-t-transparent rounded-full" />}
                  <span>{lang === 'ta' ? 'சேமிக்க' : 'Save & Ingest'}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default SourcesPage;
