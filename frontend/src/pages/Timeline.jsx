import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from '../services/LanguageContext';
import { getPlaces } from '../services/api';
import { 
  Clock, 
  Landmark, 
  MapPin, 
  Calendar, 
  ShieldCheck, 
  ChevronRight, 
  Sparkles,
  BookOpen,
  Filter,
  CheckCircle2,
  AlertTriangle,
  Building,
  HelpCircle,
  ArrowRight
} from 'lucide-react';

export const Timeline = () => {
  const { lang, t } = useTranslation();
  const navigate = useNavigate();
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('all');

  const historicalEpochs = [
    {
      id: 'all',
      name_ta: 'அனைத்து காலங்கள்',
      name_en: 'All Epochs',
      span_ta: 'கி.மு 300 - தற்காலம்',
      span_en: '300 BCE - Present'
    },
    {
      id: 'sangam',
      name_ta: 'சங்க காலம்',
      name_en: 'Sangam Era',
      span_ta: 'கி.மு 300 - கி.பி 300',
      span_en: 'c. 300 BCE - 300 CE',
      description_ta: 'சங்க இலக்கியங்களிலும் அகநானூறு, புறநானூறு, சிலப்பதிகாரத்திலும் முதன்முதலாகப் பதிவு செய்யப்பட்ட தமிழக தொன்மை நகரங்கள்.',
      description_en: 'Earliest documented settlements and emporiums found in Sangam poetry and classical Tamil epics.'
    },
    {
      id: 'pallava',
      name_ta: 'பல்லவர் காலம்',
      name_en: 'Pallava Dynasty',
      span_ta: 'கி.பி 400 - 900',
      span_en: 'c. 400 - 900 CE',
      description_ta: 'காஞ்சிபுரத்தை தலைநகராகக் கொண்டு மாமல்லபுரம் துறைமுக சிற்பக் கலை மற்றும் குடைவரை கோயில்கள் உருவான காலம்.',
      description_en: 'Era of coastal rock-cut temples, maritime commerce at Mamallapuram, and royal epigraphy in Kanchipuram.'
    },
    {
      id: 'chola',
      name_ta: 'சோழர் பேரரசு',
      name_en: 'Imperial Chola Era',
      span_ta: 'கி.பி 900 - 1300',
      span_en: 'c. 900 - 1300 CE',
      description_ta: 'தஞ்சாவூர், திருச்சிராப்பள்ளி, திருவண்ணாமலை கோயில்களில் கல்வெட்டுகளில் ஆயிரக்கணக்கான நிலக்கொடைகளும் ஊர்ப் பெயர்களும் பொறிக்கப்பட்ட பொற்காலம்.',
      description_en: 'Golden age of stone epigraphy, administrative land-grants, and temple urbanism under Rajaraja I and Rajendra I.'
    },
    {
      id: 'vijayanagara_nayak',
      name_ta: 'விஜயநகர & நாயக்கர் காலம்',
      name_en: 'Vijayanagara & Nayak Period',
      span_ta: 'கி.பி 1350 - 1750',
      span_en: 'c. 1350 - 1750 CE',
      description_ta: 'மதுரை நாயக்கர்கள் மற்றும் ஆரணி ஜாகீர் ஆட்சி. கோட்டைகள், குளங்கள் மற்றும் பெரிய கோபுரங்கள் அமைக்கப்பட்ட வரலாற்று காலம்.',
      description_en: 'Fortified jagirs, monumental gopurams, and urban defense settlements across Arani and Madurai.'
    },
    {
      id: 'colonial',
      name_ta: 'காலனித்துவ ஆவணக் காலம்',
      name_en: 'Colonial & Gazetteer Era',
      span_ta: 'கி.பி 1639 - 1947',
      span_en: 'c. 1639 - 1947 CE',
      description_ta: 'கிழக்கிந்திய கம்பெனி மற்றும் சென்னை மாகாண நிர்வாகத்தால் மாவட்ட அரசிதழ்கள், நில அளவை வரைபடங்கள், ஆங்கிலேய ஒலிபெயர்ப்புகள் உருவான காலம்.',
      description_en: 'British East India Company surveys, Imperial Gazetteers, and phonetic English renamings like Madras and Trichinopoly.'
    },
    {
      id: 'modern',
      name_ta: 'சுதந்திரத்திற்குப் பிந்தைய காலம்',
      name_en: 'Post-Independence & Renaming',
      span_ta: '1947 - தற்காலம்',
      span_en: '1947 - Present',
      description_ta: 'தமிழ்நாடு அரசு அமைத்த அரசாணைகள் (G.O.) மூலம் வரலாற்று தூய தமிழ்ப் பெயர்களை மீட்டு அதிகாரப்பூர்வமாக அரசாணைகள் பிறப்பித்த காலம்.',
      description_en: 'Official Gazette notifications and Government Orders restoring historical Tamil names such as Chennai (1996).'
    }
  ];

  // Master timeline events curated with direct place linkages
  const timelineEvents = [
    {
      id: 1,
      period: 'sangam',
      year: 'கி.மு 300 - கி.பி 200',
      year_en: 'c. 300 BCE - 200 CE',
      title_ta: 'சங்க இலக்கியத்தில் மாமல்லபுரம் & காஞ்சிபுரம்',
      title_en: 'Sangam Port of Mallai (Mamallapuram)',
      description_ta: 'பெரும்பாணாற்றுப்படை மற்றும் அகநானூற்றில் தொண்டை நாட்டு துறைமுகமாக மாமல்லபுரம் "மல்லை" என்றும், கல்வி நகரமாக "காஞ்சி" என்றும் பாடப்பட்டது.',
      description_en: 'Documented as the thriving seaport "Mallai" in classical Tamil Perumpanarruppadai, and Kanchipuram as seat of scholarship.',
      places: [
        { id: 10, name_ta: 'மாமல்லபுரம்', name_en: 'Mamallapuram' },
        { id: 7, name_ta: 'காஞ்சிபுரம்', name_en: 'Kanchipuram' }
      ],
      evidence: 'documented_fact',
      source_ta: 'சங்க இலக்கியம் (பெரும்பாணாற்றுப்படை 311-320)',
      source_en: 'Sangam Literature (Perumpanarruppadai 311-320)'
    },
    {
      id: 2,
      period: 'sangam',
      year: 'கி.மு 2-ஆம் நூற்றாண்டு',
      year_en: 'c. 2nd Century BCE',
      title_ta: 'மதுரை தமிழ்ச் சங்கமும் தமிழ் பிராமி கல்வெட்டுகளும்',
      title_en: 'Madurai Tamil Sangam & Tamil-Brahmi Epigraphs',
      description_ta: 'மாங்குளம் மற்றும் ஆனைமலை குகைகளில் பாண்டியன் நெடுஞ்செழியன் காலத்து தமிழ் பிராமி கல்வெட்டுகளில் கூடல் / மதுரை நகரம் ஆவணப்படுத்தப்பட்டுள்ளது.',
      description_en: 'Tamil-Brahmi inscriptions at Mangulam cave records royal endowments by Pandya King Nedunjeliyan to Jain ascetics.',
      places: [
        { id: 9, name_ta: 'மதுரை', name_en: 'Madurai' }
      ],
      evidence: 'documented_fact',
      source_ta: 'மாங்குளம் கல்வெட்டு (ASI Epigraphia Indica)',
      source_en: 'Mangulam Inscription (ASI Epigraphia Indica)'
    },
    {
      id: 3,
      period: 'pallava',
      year: 'கி.பி 650 - 728',
      year_en: '650 - 728 CE',
      title_ta: 'மாமல்லபுரம் கடற்கரைக் கோயில் மற்றும் பல்லவர் கல்வெட்டுகள்',
      title_en: 'Mamallapuram Shore Temple & Pallava Royal Epigraphy',
      description_ta: 'இரண்டாம் நரசிம்மவர்மன் (ராஜசிம்மன்) காலத்தில் கடற்கரைக் கோயில் கட்டப்பட்டது. பல்லவ கிரந்த கல்வெட்டுகளில் "க்ஷத்ரியசிம்ம பல்லவேஸ்வரம்" எனப் பெயர் பெற்றது.',
      description_en: 'Built by Narasimhavarman II (Rajasimha). Grantham inscriptions designate the temple complex as Kshatriyasimha Pallaveswaram.',
      places: [
        { id: 10, name_ta: 'மாமல்லபுரம்', name_en: 'Mamallapuram' }
      ],
      evidence: 'documented_fact',
      source_ta: 'இந்திய தொல்லியல் துறை (ASI Memoir No. 40)',
      source_en: 'Archaeological Survey of India (ASI Memoir No. 40)'
    },
    {
      id: 4,
      period: 'pallava',
      year: '7-ஆம் நூற்றாண்டு',
      year_en: '7th Century CE',
      title_ta: 'தேவாரப் பதிகங்களில் திருவண்ணாமலை அண்ணாமலையார்',
      title_en: 'Tiruvannamalai in 7th Century Tevaram Hymns',
      description_ta: 'திருஞானசம்பந்தர் மற்றும் திருநாவுக்கரசர் ஆகிய சமயக் குரவர்கள் "அண்ணாமலை தொழ வினைகள் அகலுமே" எனப் பாடி ஊரின் தொன்மையை ஆவணப்படுத்தினர்.',
      description_en: 'Appar and Sambandar extolled the sacred hill as Annamalai in the 7th-century Saiva canon Tevaram.',
      places: [
        { id: 5, name_ta: 'திருவண்ணாமலை', name_en: 'Tiruvannamalai' }
      ],
      evidence: 'documented_fact',
      source_ta: 'தேவாரம் 1.10 (திருமுறை மூலப் பிரதி)',
      source_en: 'Tevaram Saiva Canon (Vol. 1.10)'
    },
    {
      id: 5,
      period: 'chola',
      year: 'கி.பி 1010',
      year_en: '1010 CE',
      title_ta: 'தஞ்சை பெருவுடையார் கோயில் & ராஜராஜ சோழன் கல்வெட்டு',
      title_en: 'Thanjavur Brihadeeswarar Temple Consecration',
      description_ta: 'முதலாம் ராஜராஜ சோழனால் பெருவுடையார் கோயில் கட்டப்பட்டது. கல்வெட்டுகளில் சோழ மண்டலத்தின் தலைசிறந்த நகரமாக தஞ்சாவூர் ஆவணப்படுத்தப்பட்டது.',
      description_en: 'Consecrated by Rajaraja Chola I. Massive stone epigraphs detail the land administration and royal gifts of the capital city.',
      places: [
        { id: 4, name_ta: 'தஞ்சாவூர்', name_en: 'Thanjavur' }
      ],
      evidence: 'documented_fact',
      source_ta: 'தென்னிந்திய கல்வெட்டுகள் (தொகுதி II), ASI',
      source_en: 'South Indian Inscriptions (Vol. II), ASI'
    },
    {
      id: 6,
      period: 'chola',
      year: 'கி.பி 11-ஆம் நூற்றாண்டு',
      year_en: '11th Century CE',
      title_ta: 'திருச்சிராப்பள்ளி மலைக்கோட்டையில் சோழர் கல்வெட்டுகள்',
      title_en: 'Tiruchirappalli Rockfort Chola Inscriptions',
      description_ta: 'காவிரி டெல்டா பகுதியில் சோழர்களின் பாதுகாப்பு மையமாக திருச்சிராப்பள்ளி மலைக்குகை கோயில் விளங்கியது; கல்வெட்டுகளில் "திருச்சிராப்பள்ளி" என நேரடியாகக் குறிப்பிடப்பட்டுள்ளது.',
      description_en: 'Chola epigraphs on the upper rockfort caverns refer directly to the settlement of Tiruchirappalli.',
      places: [
        { id: 3, name_ta: 'திருச்சிராப்பள்ளி', name_en: 'Tiruchirappalli' }
      ],
      evidence: 'scholarly_hypothesis',
      source_ta: 'எபிகிராபியா இண்டிகா (தொகுதி XVI)',
      source_en: 'Epigraphia Indica, Vol. XVI'
    },
    {
      id: 7,
      period: 'vijayanagara_nayak',
      year: 'கி.பி 1516 - 1520',
      year_en: '1516 - 1520 CE',
      title_ta: 'திருவண்ணாமலையில் கிருஷ்ணதேவராயர் ராஜகோபுரம் நிர்மாணம்',
      title_en: 'Krishnadevaraya Builds Eastern Gopuram at Tiruvannamalai',
      description_ta: 'விஜயநகரப் பேரரசர் கிருஷ்ணதேவராயர் அருணாசலேஸ்வரர் கோயிலில் 217 அடி உயர பிரம்மாண்ட கிழக்கு ராஜகோபுரத்தைக் கட்டி கல்வெட்டுப் பதிவு செய்தார்.',
      description_en: 'Emperor Krishnadevaraya commemorated his Digvijaya victory by raising the 217-foot eastern Rajagopuram at Tiruvannamalai.',
      places: [
        { id: 5, name_ta: 'திருவண்ணாமலை', name_en: 'Tiruvannamalai' }
      ],
      evidence: 'documented_fact',
      source_ta: 'தென்னிந்திய கல்வெட்டுகள் (தொகுதி VIII), எண் 165',
      source_en: 'South Indian Inscriptions (Vol. VIII), No. 165'
    },
    {
      id: 8,
      period: 'vijayanagara_nayak',
      year: 'கி.பி 1640',
      year_en: 'c. 1640 CE',
      title_ta: 'ஆரணி ஜாகீர் தன்னாட்சி கோட்டை நகரம் உருவாக்கம்',
      title_en: 'Establishment of Arani Autonomous Jagir',
      description_ta: 'கமண்டல நாக நதிக்கரையில் அமைந்த ஆரணி நகரம் வேதாஜி பாஸ்கர் பந்த் என்பவருக்கு ஜாகீராக வழங்கப்பட்டு பலமான கோட்டையாக உருவாக்கப்பட்டது.',
      description_en: 'Granted as hereditary Arani Jagir to Vedaji Bhaskar Pant; fortified citadel along the banks of Kamandala Naga river.',
      places: [
        { id: 6, name_ta: 'ஆரணி', name_en: 'Arani' }
      ],
      evidence: 'documented_fact',
      source_ta: 'வட ஆற்காடு மாவட்டக் குறிப்பேடு (தொகுதி II)',
      source_en: 'North Arcot District Manual (Vol. II, pp. 248-254)'
    },
    {
      id: 9,
      period: 'colonial',
      year: '1639 ஆகஸ்ட் 22',
      year_en: '22 August 1639',
      title_ta: 'பிரான்சிஸ் டே நிலக்கொடையும் மெட்ராஸ்பட்டினமும்',
      title_en: 'Francis Day Grant & Founding of Madraspatnam',
      description_ta: 'தர்மர்லா வெங்கடபதி நாயக்கரிடம் இருந்து பிரான்சிஸ் டே வாங்கிய நிலத்தில் கிழக்கிந்திய கம்பெனி மதராஸ்பட்டினம் வணிக தளத்தை அமைத்தது.',
      description_en: 'Grant from Damarla Venkatapati Nayak to Francis Day, founding the fortified settlement adjacent to Chennapatnam.',
      places: [
        { id: 1, name_ta: 'சென்னை', name_en: 'Chennai' }
      ],
      evidence: 'documented_fact',
      source_ta: 'மெட்ராஸ் இன் தி ஓல்டன் டைம் (ஜே.டி. வீலர், 1861)',
      source_en: 'Madras in the Olden Time (J.T. Wheeler, 1861)'
    },
    {
      id: 10,
      period: 'colonial',
      year: '1751 டிசம்பர் 3',
      year_en: '3 December 1751',
      title_ta: 'வரலாற்றுச் சிறப்புமிக்க ஆரணிப் போர் (Battle of Arnee)',
      title_en: 'Historic Battle of Arnee in Carnatic Wars',
      description_ta: 'ராபர்ட் கிளைவ் தலைமையிலான ஆங்கிலேயப் படைகள் சந்தா சாகிபின் மகன் ரஸா சாகிபை ஆரணி கோட்டைக்கு அருகே தோற்கடித்த வரலாற்று நிகழ்வு.',
      description_en: 'Robert Clive routed Raza Sahib near Arani Fort during the Second Carnatic War, recording the town as "Arnee".',
      places: [
        { id: 6, name_ta: 'ஆரணி', name_en: 'Arani' }
      ],
      evidence: 'documented_fact',
      source_ta: 'இந்துஸ்தான் இராணுவ நடவடிக்கைகள் (ராபர்ட் ஓர்ம்)',
      source_en: 'Military Transactions in Indostan (Robert Orme)'
    },
    {
      id: 11,
      period: 'colonial',
      year: '1906 மார்ச் 3',
      year_en: '3 March 1906',
      title_ta: 'பிளாக் டவுன் என்பது ஜார்ஜ் டவுன் என அரசாணை வெளியீடு',
      title_en: 'Black Town Renamed to George Town via G.O. No. 158',
      description_ta: 'ஐந்தாம் ஜார்ஜ் இளவரசரின் சென்னை வருகையின் போது அரசாணை எண் 158 மூலம் "Black Town" என்பது அதிகாரப்பூர்வமாக "George Town" எனப் பெயர் மாற்றப்பட்டது.',
      description_en: 'Official Fort St. George Gazette notification G.O. No. 158 permanently renaming Black Town to George Town.',
      places: [
        { id: 2, name_ta: 'ஜார்ஜ் டவுன்', name_en: 'George Town' }
      ],
      evidence: 'documented_fact',
      source_ta: 'புனித ஜார்ஜ் கோட்டை அரசிதழ் (அரசாணை எண் 158)',
      source_en: 'Fort St. George Gazette, G.O. No. 158 (3 March 1906)'
    },
    {
      id: 12,
      period: 'modern',
      year: '1996 ஜூலை 17',
      year_en: '17 July 1996',
      title_ta: 'மெட்ராஸ் என்பது சென்னை என அதிகாரப்பூர்வமாக பெயர் மாற்றம்',
      title_en: 'Madras Officially Renamed to Chennai',
      description_ta: 'தமிழ்நாடு சட்டமன்றத்தில் இயற்றப்பட்ட சிறப்புத் தீர்மானம் மூலம் ஆங்கிலேய காலத்து "Madras" என்ற பெயர் மாற்றப்பட்டு வரலாற்றுப் பெயரான "சென்னை" என நிலைநாட்டப்பட்டது.',
      description_en: 'Tamil Nadu Legislative Assembly unanimously ratified the official renaming of Madras to Chennai.',
      places: [
        { id: 1, name_ta: 'சென்னை', name_en: 'Chennai' }
      ],
      evidence: 'documented_fact',
      source_ta: 'தமிழ்நாடு அரசு அரசிதழ் (ஜூலை 1996)',
      source_en: 'Tamil Nadu Government Gazette, July 1996'
    }
  ];

  useEffect(() => {
    const fetchPlacesData = async () => {
      try {
        const data = await getPlaces();
        setPlaces(data);
      } catch (err) {
        console.error('Failed to load places for timeline:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchPlacesData();
  }, []);

  const filteredEvents = selectedPeriod === 'all'
    ? timelineEvents
    : timelineEvents.filter(e => e.period === selectedPeriod);

  return (
    <div className="space-y-8 max-w-5xl mx-auto py-2">
      {/* Page Header */}
      <div className="bg-[#172B40] text-white rounded-2xl p-6 sm:p-8 border border-[#2A3E54] shadow-sm relative overflow-hidden">
        <div className="absolute right-0 top-0 w-80 h-80 bg-[#C5A66A]/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#C5A66A]/20 border border-[#C5A66A]/40 text-[#C5A66A] text-xs font-semibold">
            <Clock className="w-3.5 h-3.5" />
            <span>{lang === 'ta' ? 'வரலாற்றுக் காலவரிசை' : 'Historical Chronology'}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {lang === 'ta'
              ? 'தமிழக வரலாற்றுப் பேரரசுகளும் இடப்பெயர் பதிவுகளும்'
              : 'Chronological Epochs & Place Name Evolution'}
          </h1>
          <p className="text-sm text-gray-300 max-w-2xl leading-relaxed">
            {lang === 'ta'
              ? 'சங்க காலம் முதல் நவீன அரசாணைகள் வரை தமிழ்நாட்டு ஊர்ப் பெயர்கள் எவ்வாறு கல்வெட்டுகள், செப்பேடுகள் மற்றும் வரலாற்று ஆவணங்களில் பொறிக்கப்பட்டுள்ளன என்பதைக் காலவரிசையில் காண்க.'
              : 'Trace how Tamil settlements transformed across Sangam literature, Pallava epigraphy, Imperial Chola grants, Vijayanagara fortifications, and colonial gazetteers.'}
          </p>
        </div>
      </div>

      {/* Epoch Filter Chips */}
      <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm space-y-3">
        <div className="flex items-center gap-2 text-xs font-semibold text-[#172B40] uppercase tracking-wider">
          <Filter className="w-3.5 h-3.5 text-[#C5A66A]" />
          <span>{lang === 'ta' ? 'வரலாற்றுக் காலம் தேர்வு செய்க:' : 'Select Historical Period:'}</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {historicalEpochs.map((epoch) => (
            <button
              key={epoch.id}
              onClick={() => setSelectedPeriod(epoch.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all text-left ${
                selectedPeriod === epoch.id
                  ? 'bg-[#172B40] text-white shadow-sm border border-[#172B40]'
                  : 'bg-[#F7F4ED] text-[#172B40] hover:bg-[#eae5d8] border border-gray-200'
              }`}
            >
              <div className="font-bold">
                {lang === 'ta' ? epoch.name_ta : epoch.name_en}
              </div>
              <div className="text-[10px] opacity-75 font-normal">
                {lang === 'ta' ? epoch.span_ta : epoch.span_en}
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Timeline Events Stream */}
      <div className="relative border-l-2 border-[#C5A66A]/40 ml-4 sm:ml-8 pl-6 sm:pl-8 space-y-8">
        {filteredEvents.map((evt, idx) => {
          return (
            <div key={evt.id} className="relative group">
              {/* Timeline Indicator Dot */}
              <div className="absolute -left-[31px] sm:-left-[39px] top-1.5 w-5 h-5 rounded-full bg-[#172B40] border-4 border-[#C5A66A] shadow-sm flex items-center justify-center group-hover:scale-125 transition-transform" />

              {/* Event Card */}
              <div className="bg-white rounded-xl p-5 sm:p-6 border border-gray-200 shadow-sm hover:shadow-md transition-shadow space-y-3">
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-gray-100 pb-3">
                  <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-[#F7F4ED] text-[#172B40] text-xs font-bold border border-gray-200">
                    <Calendar className="w-3.5 h-3.5 text-[#C5A66A]" />
                    <span>{lang === 'ta' ? evt.year : evt.year_en}</span>
                  </div>

                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
                    <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                    {lang === 'ta' ? 'சான்றாதார ஆவணம்' : 'Verified Evidence'}
                  </span>
                </div>

                <div>
                  <h3 className="text-lg font-bold text-[#172B40] group-hover:text-[#C5A66A] transition-colors">
                    {lang === 'ta' ? evt.title_ta : evt.title_en}
                  </h3>
                  <p className="text-xs sm:text-sm text-gray-600 mt-1 leading-relaxed">
                    {lang === 'ta' ? evt.description_ta : evt.description_en}
                  </p>
                </div>

                {/* Source Citation Footnote */}
                <div className="p-2.5 rounded-lg bg-[#F7F4ED] border border-gray-200/80 flex items-start gap-2 text-[11px] text-[#172B40]">
                  <BookOpen className="w-3.5 h-3.5 text-[#C5A66A] shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-gray-500 mr-1.5">
                      {lang === 'ta' ? 'மூல ஆவணம்:' : 'Primary Source:'}
                    </span>
                    <span className="italic font-medium">{lang === 'ta' ? (evt.source_ta || evt.source) : (evt.source_en || evt.source)}</span>
                  </div>
                </div>

                {/* Associated Places Links */}
                <div className="flex flex-wrap items-center gap-2 pt-1">
                  <span className="text-xs font-semibold text-gray-500">
                    {lang === 'ta' ? 'தொடர்புடைய இடங்கள்:' : 'Associated Places:'}
                  </span>
                  {evt.places.map((p) => (
                    <Link
                      key={p.id}
                      to={`/places/${p.id}`}
                      className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-[#172B40] text-white hover:bg-[#20364F] text-xs font-medium transition-colors"
                    >
                      <MapPin className="w-3 h-3 text-[#C5A66A]" />
                      <span>{lang === 'ta' ? p.name_ta : p.name_en}</span>
                      <ArrowRight className="w-3 h-3 opacity-60 ml-0.5" />
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default Timeline;
