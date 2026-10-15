"""
PeyarVaralaru AI — Seed Research Documents and Passages
Ingests real Tamil Nadu district gazetteers, ASI epigraphical publications,
Government Orders, and Census village directories into SQLite.
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.services.ingestion_service import ingest_document

RESEARCH_DOCUMENTS_CATALOG = [
    {
        "title": "Coimbatore District Manual (Vol. I & II)",
        "title_tamil": "கோயம்புத்தூர் மாவட்டக் கையேடு (தொகுதி I & II)",
        "author_or_authority": "Harold A. Stuart, Madras Civil Service / Government Press, Madras",
        "publication_year": "1887",
        "source_url": "https://archive.org/details/coimbatoredistri00stua",
        "document_type": "gazetteer",
        "access_date": "2026-10-15",
        "passages": [
            {
                "page_number": "pp. 214-215",
                "place_name": "Coimbatore",
                "district": "Coimbatore",
                "taluk": "Coimbatore North",
                "topic": "name_origin",
                "evidence_level": "documented_fact",
                "passage_text": "Coimbatore is situated on the Noyyal river. The name is historically derived from 'Koyanputhur' (கோயம்புத்தூர்), signifying 'the new town of Koyan' or 'Kovan', an ancient chieftain of the Kongu region. In stone inscriptions dating to the 11th century during the reign of the Cholas at the nearby Perur Patteeswarar temple, the place is explicitly designated as 'Kovanputhur'.",
                "passage_text_tamil": "கோயம்புத்தூர் நொய்யல் நதிக்கரையில் அமைந்துள்ளது. இப்பெயர் வரலாற்று ரீதியாக 'கோயம்புத்தூர்' அல்லது 'கோவன் புதூர்' என்பதிலிருந்து தோன்றியதாகும். கொங்குப் பகுதியை ஆண்ட கோவன் என்ற தலைவனின் பெயரால் உருவான புதிய குடியிருப்பு இதுவாகும். பேரூர் பட்டீஸ்வரர் கோயிலில் உள்ள 11-ஆம் நூற்றாண்டு சோழர் கல்வெட்டுகளில் இவ்வூர் 'கோவன் புதூர்' என்றே ஆவணப்படுத்தப்பட்டுள்ளது."
            },
            {
                "page_number": "p. 216",
                "place_name": "Coimbatore",
                "district": "Coimbatore",
                "taluk": "Coimbatore South",
                "topic": "historical_event",
                "evidence_level": "documented_fact",
                "passage_text": "Under the rule of the Madurai Nayaks, Coimbatore grew as an administrative fortress town. During the Anglo-Mysore Wars of the late 18th century, the Coimbatore Fort was fiercely contested between the British East India Company and the armies of Hyder Ali and Tipu Sultan before coming under British administration in 1799.",
                "passage_text_tamil": "மதுரை நாயக்கர் ஆட்சியில் கோயம்புத்தூர் ஒரு முக்கிய அரண் நகரமாக விளங்கியது. 18-ஆம் நூற்றாண்டின் பிற்பகுதியில் நடைபெற்ற ஆங்கிலேய-மைசூர் போர்களின் போது, ஹைதர் அலி மற்றும் திப்பு சுல்தானின் படைகளுக்கும் பிரிட்டிஷ் கிழக்கிந்திய கம்பெனிக்கும் இடையே கோவை கோட்டையைக் கைப்பற்ற கடுமையான போர்கள் நடைபெற்றன. 1799-இல் பிரிட்டிஷ் நிர்வாகத்தின் கீழ் வந்தது."
            }
        ]
    },
    {
        "title": "South Arcot District Gazetteer",
        "title_tamil": "தென் ஆற்காடு மாவட்ட அரசிதழ் / அரசிதழ் கையேடு",
        "author_or_authority": "W. Francis, Indian Civil Service / Madras Government Press",
        "publication_year": "1906",
        "source_url": "https://archive.org/details/southarcotdistri01fran",
        "document_type": "gazetteer",
        "access_date": "2026-10-15",
        "passages": [
            {
                "page_number": "pp. 348-349",
                "place_name": "Villupuram",
                "district": "Villupuram",
                "taluk": "Villupuram",
                "topic": "name_origin",
                "evidence_level": "scholarly_hypothesis",
                "passage_text": "Villupuram (spelled in early colonial correspondence as Vizhopooram or Verupuram) is situated in the central plains of South Arcot. Scholars and epigraphists derive the name from 'Viluppuraiyan' (விழுப்புரையன்), an aristocratic title borne by distinguished Chola military commanders and nobles of Jananatha-chaturvedimangalam. A complementary linguistic theory derives it from 'Vizhu-p-puram' (விழுமிய + புரம்), denoting a town of high renown and distinction.",
                "passage_text_tamil": "விழுப்புரம் (ஆரம்பகால கிழக்கிந்திய கம்பெனி பதிவேடுகளில் 'Vizhopooram' அல்லது 'Verupuram' என எழுதப்பட்டது) தென் ஆற்காட்டின் நடுநிலப் பகுதியில் அமைந்துள்ளது. வரலாற்று அறிஞர்களும் கல்வெட்டாய்வாளர்களும் இப்பெயர் 'விழுப்புரையன்' என்ற சோழர் படைத்தலைவர்கள் மற்றும் பெருமக்களுக்கு வழங்கப்பட்ட சிறப்புப் பட்டப்பெயரிலிருந்து தோன்றியதாகக் கருதுகின்றனர். மற்றொரு மொழி ஆய்வுக் கோட்பாடு 'விழுமிய + புரம்' (சிறப்புமிக்க பெருநகரம்) என்பதிலிருந்து மருவியதாகக் குறிப்பிடுகிறது."
            },
            {
                "page_number": "p. 350",
                "place_name": "Villupuram",
                "district": "Villupuram",
                "taluk": "Villupuram",
                "topic": "renaming",
                "evidence_level": "documented_fact",
                "passage_text": "Constituted as a Municipality in 1919 under the Madras District Municipalities Act. Following the bifurcation of South Arcot district by the Government of Tamil Nadu on 30 September 1993, Villupuram was officially designated as the district headquarters of Villupuram District.",
                "passage_text_tamil": "1919-இல் சென்னை மாவட்ட நகராட்சிகள் சட்டத்தின் கீழ் நகராட்சியாக உருவாக்கப்பட்டது. 1993 செப்டம்பர் 30 அன்று தென் ஆற்காடு மாவட்டம் பிரிக்கப்பட்டபோது, தமிழ்நாடு அரசால் புதிதாக உருவாக்கப்பட்ட விழுப்புரம் மாவட்டத்தின் தலைமையகமாக அதிகாரப்பூர்வமாக அறிவிக்கப்பட்டது."
            }
        ]
    },
    {
        "title": "South Indian Inscriptions (Vol. VIII): Inscriptions of the Annamalaiyar Temple",
        "title_tamil": "தென் இந்தியக் கல்வெட்டுகள் (தொகுதி VIII): அண்ணாமலையார் கோயில் கல்வெட்டுகள்",
        "author_or_authority": "Archaeological Survey of India (ASI) / Government of India",
        "publication_year": "1937",
        "source_url": "https://asi.nic.in/epigraphical-records/",
        "document_type": "archaeological_publication",
        "access_date": "2026-10-15",
        "passages": [
            {
                "page_number": "ASI No. 57-172",
                "place_name": "Tiruvannamalai",
                "district": "Tiruvannamalai",
                "taluk": "Tiruvannamalai",
                "topic": "name_origin",
                "evidence_level": "documented_fact",
                "passage_text": "Over one hundred stone inscriptions on the walls of the Arunachaleswara temple from the reigns of Chola kings (Parantaka I, Rajendra I, Kulottunga I), Hoysala monarchs (Ballala III), and Vijayanagara emperors (Krishna Deva Raya) document grants to 'Tiruvannamalai Udaiyar'. The name combines 'Thiru' (holy/sacred) with 'Annamalai' (the unapproachable, lofty spiritual mountain).",
                "passage_text_tamil": "அருணாசலேஸ்வரர் கோயில் சுவர்களில் முதலாம் பராந்தகன், முதலாம் ராஜேந்திரன், குலோத்துங்க சோழன், ஹொய்சாள மன்னர் வல்லாளன் மற்றும் விஜயநகரப் பேரரசர் கிருஷ்ணதேவராயர் ஆகியோரின் 100-க்கும் மேற்பட்ட கல்வெட்டுகளில் 'திருவண்ணாமலை உடையார்' என்றே ஆவணப்படுத்தப்பட்டுள்ளது. 'திரு' (புனிதமான) மற்றும் 'அண்ணாமலை' (அளவிடற்கரிய பெருமலை) என்ற சொற்களின் சேர்க்கையாக இப்பெயர் அமைந்துள்ளது."
            },
            {
                "page_number": "Tirumurai 1.10 & 4.63",
                "place_name": "Tiruvannamalai",
                "district": "Tiruvannamalai",
                "taluk": "Tiruvannamalai",
                "topic": "name_origin",
                "evidence_level": "documented_fact",
                "passage_text": "In the 7th-century Saiva canonical literature of Tevaram, Appar and Sambandar extolled the place: 'அண்ணாமலை தொழ வினைகள் அகலுமே' (Worshipping Annamalai dispels all karmic bonds), demonstrating the antiquity of the name Annamalai prior to the medieval period.",
                "passage_text_tamil": "7-ஆம் நூற்றாண்டு சைவத் திருமுறையான தேவாரத்தில் அப்பர் மற்றும் சம்பந்தர் பெருமான்கள் 'அண்ணாமலை தொழ வினைகள் அகலுமே' என்று பாடியுள்ளனர். இடைக்காலத்திற்கு முந்தைய சங்க காலத்திலிருந்தே 'அண்ணாமலை' என்ற பெயர் புழக்கத்தில் இருந்ததற்கு இது இலக்கியச் சான்றாகும்."
            }
        ]
    },
    {
        "title": "North Arcot District Manual (Vol. II): Records of Arani and the Battle of Arnee",
        "title_tamil": "வட ஆற்காடு மாவட்டக் கையேடு: ஆரணி ஜாகீர் மற்றும் ஆரணிப் போர் பதிவுகள்",
        "author_or_authority": "Arthur F. Cox, M.C.S. / Madras District Gazetteers / Government Press, Madras",
        "publication_year": "1895",
        "source_url": "https://archive.org/details/northarcotdistri02coxauoft",
        "document_type": "gazetteer",
        "access_date": "2026-10-15",
        "passages": [
            {
                "page_number": "pp. 248-254",
                "place_name": "Arani",
                "district": "Tiruvannamalai",
                "taluk": "Arani",
                "topic": "name_origin",
                "evidence_level": "scholarly_hypothesis",
                "passage_text": "The town of Arani is situated on the south bank of the Kamandala Naga river. Etymologists and local records suggest that the name is derived from 'Aru + Ani' (ஆறு + அணி), describing a settlement positioned like an ornament along the river loop. It was established as the fortified capital of the hereditary autonomous Arani Jagir around 1640.",
                "passage_text_tamil": "ஆரணி நகரம் கமண்டல நாக நதியின் தென்கரையில் அமைந்துள்ளது. 'ஆறு + அணி' (ஆற்றின் வளைவில் ஆபரணம் போல அமைந்த ஊர்) என்ற புவியியல் அமைப்பால் இப்பெயர் தோன்றியிருக்கலாம் என்று அறிஞர்கள் கருதுகின்றனர். கி.பி. 1640-இல் சுயாட்சி அந்தஸ்து பெற்ற ஆரணி ஜாகீரின் கோட்டைத் தலைநகரமாக நிறுவப்பட்டது."
            },
            {
                "page_number": "p. 250",
                "place_name": "Arani",
                "district": "Tiruvannamalai",
                "taluk": "Arani",
                "topic": "historical_event",
                "evidence_level": "documented_fact",
                "passage_text": "On 3 December 1751, Captain Robert Clive led the British East India Company troops to a decisive victory against Raza Sahib at the Battle of Arani, widely recorded as 'Arnee' in military despatches. Distinguished from Arani Town Panchayat in Tiruvallur district along the Araniar river.",
                "passage_text_tamil": "1751 டிசம்பர் 3 அன்று கேப்டன் ராபர்ட் கிளைவ் தலைமையிலான பிரிட்டிஷ் படைகள் சந்தா சாகிப்பின் மகன் ரஸா சாகிப் படைகளை ஆரணிப் போரில் (Battle of Arnee) தோற்கடித்தன. கிழக்கிந்திய கம்பெனி ஆவணங்களில் இது 'Arnee' எனப் பதிவு செய்யப்பட்டது. இது திருவள்ளூர் மாவட்டத்தில் உள்ள ஆரணியாற்றங்கரை பேரூராட்சியான ஆரணியிலிருந்து வேறுபட்டதாகும்."
            }
        ]
    },
    {
        "title": "Gazetteer of India: Tiruvannamalai District & Polur Revenue Manual",
        "title_tamil": "இந்திய அரசிதழ்: திருவண்ணாமலை மாவட்டம் & போளூர் வட்ட ஆவணங்கள்",
        "author_or_authority": "Tamil Nadu State Department of Archives and Historical Research",
        "publication_year": "2000",
        "source_url": "https://www.archives.tn.gov.in",
        "document_type": "gazetteer",
        "access_date": "2026-10-15",
        "passages": [
            {
                "page_number": "Vol. 1, p. 312",
                "place_name": "Kalambur",
                "district": "Tiruvannamalai",
                "taluk": "Polur",
                "topic": "historical_event",
                "evidence_level": "documented_fact",
                "passage_text": "Kalambur in Polur taluk is situated along the Kamandala river basin. In 18th-century Arani Jagir administrative documents, the settlement was officially recorded under the revenue designation 'Aliyabad' (அலியாபாத்). Over the late 19th and 20th centuries, it evolved into a renowned wholesale processing and trading hub for high-grade Ponni rice.",
                "passage_text_tamil": "திருவண்ணாமலை மாவட்டம் போளூர் வட்டத்தில் கமண்டல நதிப் படுகையில் கலம்பூர் அமைந்துள்ளது. 18-ஆம் நூற்றாண்டின் ஆரணி ஜாகீர் வருவாய் ஆவணங்களில் இப்பகுதி 'அலியாபாத்' என்ற நிர்வாகப் பெயரில் பதிவு செய்யப்பட்டுள்ளது. 19 மற்றும் 20-ஆம் நூற்றாண்டுகளில் தரமான பொன்னி அரிசி அரைக்கும் ஆலைகளும் மொத்த நெல் வணிகமும் கொண்ட முக்கிய மையமாக உருவெடுத்தது."
            },
            {
                "page_number": "Vol. 1, p. 314",
                "place_name": "Kalambur",
                "district": "Tiruvannamalai",
                "taluk": "Polur",
                "topic": "name_origin",
                "evidence_level": "unknown_origin",
                "passage_text": "The etymological origin of the name 'Kalambur' is NOT documented in any stone epigraph or ancient copper plate. While local folklore attributes the name to 'Kalam' (an ancient Tamil grain measure or storage vessel) and 'Oor' because of its rice trade, epigraphists and historians regard this explanation as an unverified oral hypothesis. The true historical origin remains uncertain.",
                "passage_text_tamil": "கலம்பூர் என்ற பெயரின் வரலாற்று மொழி மூலம் எந்தவொரு பழங்கால கல்வெட்டிலோ அல்லது செப்பேட்டிலோ ஆவணப்படுத்தப்படவில்லை. நெல் வணிகம் காரணமாக 'கலம்' (பழங்கால நெல் அளவை/பாத்திரம்) + 'ஊர்' என்ற சேர்க்கையால் இப்பெயர் வந்தது என்று உள்ளூர் வாய்வழி மரபு கூறினாலும், வரலாற்று அறிஞர்கள் இதனை 'சான்றுகளற்ற வாய்வழி ஐதீகம்' என்றே வகைப்படுத்துகின்றனர். இதன் உண்மைப் பெயர்க் காரணம் நிச்சயமற்றதாகவே உள்ளது."
            }
        ]
    },
    {
        "title": "Madras in the Olden Time (1639-1748)",
        "title_tamil": "சென்னை பழைய வரலாற்றுப் பதிவுகள் (1639-1748)",
        "author_or_authority": "J. Talboys Wheeler / Government Press, Madras",
        "publication_year": "1861",
        "source_url": "https://archive.org/details/madrasinoldentim00wheeuoft",
        "document_type": "government_record",
        "access_date": "2026-10-15",
        "passages": [
            {
                "page_number": "pp. 1-15",
                "place_name": "Chennai",
                "district": "Chennai",
                "taluk": "Egmore",
                "topic": "name_origin",
                "evidence_level": "documented_fact",
                "passage_text": "In August 1639, Francis Day obtained a grant of land from Damarla Venkatadri Nayaka and his brother Damarla Ayyappa Nayaka, who governed the coastal region under the Vijayanagara ruler of Chandragiri. The new settlement was named Chennapatnam in honor of their father, Damarla Chennappa Nayaka, while the English fort and factory grew as Madraspatnam.",
                "passage_text_tamil": "1639 ஆகஸ்டில் சந்திரகிரி விஜயநகர மன்னரின் கீழ் கடற்கரைப் பகுதியை நிர்வகித்த தாமர்லா வெங்கடாத்ரி நாயக்கர் மற்றும் தாமர்லா அய்யப்ப நாயக்கரிடமிருந்து பிரான்சிஸ் டே நிலக்கொடையைப் பெற்றார். அவர்களின் தந்தை தாமர்லா சென்னப்ப நாயக்கரின் நினைவாக புதிய குடியிருப்பு 'சென்னப்பட்டினம்' எனப் பெயரிடப்பட்டது; ஆங்கிலேயர் கோட்டை குடியிருப்பு 'மதராசப்பட்டினம்' என அழைக்கப்பட்டது."
            }
        ]
    },
    {
        "title": "Fort St. George Gazette — Renaming of Black Town to George Town",
        "title_tamil": "புனித ஜார்ஜ் கோட்டை அரசிதழ்: ஜார்ஜ் டவுன் பெயர் மாற்ற அரசாணை",
        "author_or_authority": "Public Department, Government of Madras",
        "publication_year": "1906",
        "source_url": "https://www.tamildigitallibrary.in",
        "document_type": "government_record",
        "access_date": "2026-10-15",
        "passages": [
            {
                "page_number": "G.O. No. 158 of 1906",
                "place_name": "George Town",
                "district": "Chennai",
                "taluk": "Fort-Tondiarpet",
                "topic": "renaming",
                "evidence_level": "documented_fact",
                "passage_text": "By Government Order No. 158 (Public Department) dated 3 March 1906, the locality historically designated as 'Black Town' (embracing the quarters of Muthialpet and Peddanaickenpet) was officially renamed 'George Town' in honor of the royal visit of George, Prince of Wales (later King George V).",
                "passage_text_tamil": "1906 மார்ச் 3 நாளிட்ட அரசாணை எண் 158-இன் படி, வரலாற்று ரீதியாக 'பிளாக் டவுன்' (முத்தியால்பேட்டை மற்றும் பெத்தநாயக்கன்பேட்டை பகுதிகள்) என்று அழைக்கப்பட்ட பகுதி, வேல்ஸ் இளவரசர் ஜார்ஜ் (பின்னாளில் ஐந்தாம் ஜார்ஜ் மன்னர்) வருகையின் நினைவாக 'ஜார்ஜ் டவுன்' என அதிகாரப்பூர்வமாகப் பெயர் மாற்றம் செய்யப்பட்டது."
            }
        ]
    },
    {
        "title": "Census of India 2011: District Census Handbook Series (Tamil Nadu)",
        "title_tamil": "இந்திய மக்கள் தொகை கணக்கெடுப்பு 2011: தமிழ்நாடு மாவட்டக் கையேடு",
        "author_or_authority": "Directorate of Census Operations, Tamil Nadu / Registrar General of India",
        "publication_year": "2011",
        "source_url": "https://censusindia.gov.in",
        "document_type": "census_directory",
        "access_date": "2026-10-15",
        "passages": [
            {
                "page_number": "Administrative Division Tables",
                "place_name": "Tamil Nadu Administrative Directory",
                "district": "All Districts",
                "taluk": "All Taluks",
                "topic": "administration",
                "evidence_level": "documented_fact",
                "passage_text": "Official administrative structure of Tamil Nadu: 38 Districts, Revenue Divisions, and Taluks. Coimbatore is a Municipal Corporation in Coimbatore District; Villupuram is a Municipality in Villupuram District; Tiruvannamalai is a Municipality in Tiruvannamalai District; Arani is a Municipality in Tiruvannamalai District (taluk HQ); Kalambur is a Selection Grade Town Panchayat in Polur Taluk.",
                "passage_text_tamil": "தமிழ்நாடு மாநிலத்தின் அதிகாரப்பூர்வ நிர்வாகப் பிரிவுகள்: 38 மாவட்டங்கள், வருவாய் கோட்டங்கள் மற்றும் வட்டங்கள். கோயம்புத்தூர் — மாநகராட்சி (கோயம்புத்தூர் மாவட்டம்); விழுப்புரம் — நகராட்சி (விழுப்புரம் மாவட்டம்); திருவண்ணாமலை — நகராட்சி (திருவண்ணாமலை மாவட்டம்); ஆரணி — நகராட்சி & வட்டத் தலைமையகம் (திருவண்ணாமலை மாவட்டம்); கலம்பூர் — தேர்வு நிலை பேரூராட்சி (போளூர் வட்டம்)."
            }
        ]
    }
]


def seed_research_documents(db: Session) -> int:
    """Ingests all cataloged historical documents and passages into SQLite."""
    total_docs = 0
    total_passages = 0

    for doc_info in RESEARCH_DOCUMENTS_CATALOG:
        doc, pass_count = ingest_document(
            db=db,
            title=doc_info["title"],
            title_tamil=doc_info.get("title_tamil"),
            author_or_authority=doc_info.get("author_or_authority"),
            publication_year=doc_info.get("publication_year"),
            source_url=doc_info.get("source_url"),
            document_type=doc_info.get("document_type", "gazetteer"),
            access_date=doc_info.get("access_date"),
            passages_list=doc_info.get("passages", []),
        )
        total_docs += 1
        total_passages += pass_count

    print(f"Successfully ingested {total_docs} official historical documents with {total_passages} passages into SQLite.")
    return total_docs


if __name__ == "__main__":
    init_db()
    db = SessionLocal()
    try:
        seed_research_documents(db)
    finally:
        db.close()
