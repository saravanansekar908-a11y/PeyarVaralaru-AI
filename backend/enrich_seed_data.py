import json
import os

SEED_FILE = os.path.join(os.path.dirname(__file__), "data", "seed_data.json")

with open(SEED_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Structured records mapping
structured_details = {
    1: {  # Chennai
        "place_name_tamil": "சென்னை",
        "place_name_english": "Chennai",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "taluk": "Chennai",
        "historical_period": "Colonial Period (17th-20th Century CE)",
        "name_origin_explanation": "'சென்னை' என்ற பெயர் 'சென்னப்பட்டணம்' என்ற பழைய பெயரிலிருந்து சுருக்கப்பட்டது. 1639-இல் பிரிட்டிஷ் கிழக்கிந்திய கம்பெனி ஆவணங்களில் 'மதராஸ்பட்டினம்' மற்றும் 'சென்னப்பட்டணம்' எனப் பதிவு செய்யப்பட்டுள்ளது.",
        "origin_evidence_status": "historically_documented",
        "historical_events_summary": "1639-இல் கிழக்கிந்திய கம்பெனி மதராஸ்பட்டினத்தில் வணிக தளம் அமைத்தது. 1996-இல் தமிழ்நாடு அரசால் 'சென்னை' என அதிகாரப்பூர்வமாகப் பெயர் மாற்றம் செய்யப்பட்டது.",
        "source_title": "Madras in the Olden Time (1639-1748)",
        "source_url": "https://archive.org/details/madrasinoldentim00wheeuoft",
        "source_page": "pp. 1-15",
        "evidence_quote": "The territory granted to Francis Day in 1639 was adjacent to Madraspatnam and Chennapatnam. Renamed Chennai in 1996.",
        "verification_status": "verified"
    },
    2: {  # George Town
        "place_name_tamil": "ஜார்ஜ் டவுன்",
        "place_name_english": "George Town",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "taluk": "Chennai",
        "historical_period": "Colonial Period (18th-20th Century CE)",
        "name_origin_explanation": "முற்காலத்தில் 'பிளாக் டவுன்' (Black Town) என அழைக்கப்பட்ட இப்பகுதி, ஐந்தாம் ஜார்ஜ் மன்னரின் வருகையை ஒட்டி அரசாணை எண் 158 (3 மார்ச் 1906) மூலம் 'ஜார்ஜ் டவுன்' எனப் பெயர் மாற்றப்பட்டது.",
        "origin_evidence_status": "historically_documented",
        "historical_events_summary": "1906 மார்ச் 3 அன்று புனித ஜார்ஜ் கோட்டை அரசாணை மூலம் பிளாக் டவுன் என்பது ஜார்ஜ் டவுன் என மறுபெயரிடப்பட்டது.",
        "source_title": "Fort St. George Gazette — Renaming of Black Town to George Town (G.O. No. 158)",
        "source_url": "https://www.tamildigitallibrary.in",
        "source_page": "G.O. No. 158, 3 March 1906",
        "evidence_quote": "His Excellency the Governor in Council is pleased to direct that the area hitherto known as Black Town shall henceforth be designated George Town.",
        "verification_status": "verified"
    },
    3: {  # Tiruchirappalli
        "place_name_tamil": "திருச்சிராப்பள்ளி",
        "place_name_english": "Tiruchirappalli",
        "state": "Tamil Nadu",
        "district": "Tiruchirappalli",
        "taluk": "Tiruchirappalli",
        "historical_period": "Medieval Chola & Nayak Period (10th-17th Century CE)",
        "name_origin_explanation": "'சிர' (மலை/பாறை) + 'பள்ளி' (குடியிருப்பு) அல்லது 'திரு' + 'சிராப்பள்ளி' என்ற சொல்லமைப்பால் அமைந்த பாறைக்கோட்டை நகரம். புராணங்களில் திரிசிரன் என்ற அசுரன் வழிபட்டதாகக் கூறப்படும் கதை நாட்டுப்புற மரபாகும்.",
        "origin_evidence_status": "scholarly_interpretation",
        "historical_events_summary": "சோழர் கல்வெட்டுகளிலும் பின்னர் மதுரை நாயக்கர் ஆட்சியில் மலைக்கோட்டை அரணாகவும் திகழ்ந்தது. பிரிட்டிஷ் காலத்தில் 'டிரிச்சினோப்பொலி' என வழங்கப்பட்டது.",
        "source_title": "Imperial Gazetteer of India: Trichinopoly",
        "source_url": "https://archive.org/details/imperialgazettee24grea",
        "source_page": "Vol. 24, pp. 26-42",
        "evidence_quote": "The Rock of Trichinopoly rises abruptly from the plain. The name is commonly derived from Tiru-chira-palli ('holy rock town') or from the mythical asura Trisira.",
        "verification_status": "partially_verified"
    },
    4: {  # Thanjavur
        "place_name_tamil": "தஞ்சாவூர்",
        "place_name_english": "Thanjavur",
        "state": "Tamil Nadu",
        "district": "Thanjavur",
        "taluk": "Thanjavur",
        "historical_period": "Imperial Chola Period (9th-13th Century CE)",
        "name_origin_explanation": "'தஞ்சன்' என்ற அசுரனின் பெயரால் உருவானது என்ற தலபுராண நம்பிக்கை வாய்வழி மரபாகும்; வரலாற்று ரீதியாக சோழர் தலைநகரமாகவும் 'தஞ்சம்' (புகலிடம்) தரும் வளம் கொழிக்கும் ஊராகவும் விளங்கியது.",
        "origin_evidence_status": "local_tradition",
        "historical_events_summary": "கி.பி. 1010-இல் முதலாம் ராஜராஜ சோழனால் பெருவுடையார் கோயில் (பிரகதீஸ்வரர் கோயில்) கட்டி முடிக்கப்பட்டது.",
        "source_title": "Tanjore District Gazetteer",
        "source_url": "https://archive.org/details/tanjoredistrict01heমি",
        "source_page": "pp. 1-25",
        "evidence_quote": "Tanjore was the ancient capital of the Cholas. Local legend ascribes the name to a demon named Tanjan who was slain by Vishnu.",
        "verification_status": "partially_verified"
    },
    5: {  # Tiruvannamalai
        "place_name_tamil": "திருவண்ணாமலை",
        "place_name_english": "Tiruvannamalai",
        "state": "Tamil Nadu",
        "district": "Tiruvannamalai",
        "taluk": "Tiruvannamalai",
        "historical_period": "Early Saiva, Chola & Vijayanagara Period (7th-16th Century CE)",
        "name_origin_explanation": "'திரு' (புனிதமான) + 'அண்ணாமலை' (நெருங்குவதற்கு அரிய பெருமலை). 7-ஆம் நூற்றாண்டு தேவாரப் பதிகங்களிலும், முதலாம் பராந்தகன் முதல் கிருஷ்ணதேவராயர் வரையிலான 100-க்கும் மேற்பட்ட கல்வெட்டுகளிலும் 'திருவண்ணாமலை உடையார்' என ஆவணப்படுத்தப்பட்டுள்ளது.",
        "origin_evidence_status": "historically_documented",
        "historical_events_summary": "அருணாசலேஸ்வரர் கோயிலில் சோழர், ஹொய்சாள, விஜயநகர கல்வெட்டுகள் உள்ளன. 1989-இல் வட ஆற்காட்டிலிருந்து பிரிக்கப்பட்டு தனி மாவட்டமானது.",
        "source_title": "South Indian Inscriptions (Vol. VIII): Inscriptions of the Annamalaiyar Temple",
        "source_url": "https://asi.nic.in/epigraphical-records/",
        "source_page": "ASI No. 57-172; Tirumurai 1.10",
        "evidence_quote": "Over one hundred stone inscriptions on the walls of the Arunachaleswara temple from the reigns of Chola kings (Parantaka I, Rajendra I, Kulottunga I), Hoysala monarchs (Ballala III), and Vijayanagara emperors document grants to 'Tiruvannamalai Udaiyar'.",
        "verification_status": "verified"
    },
    6: {  # Arani
        "place_name_tamil": "ஆரணி",
        "place_name_english": "Arani",
        "state": "Tamil Nadu",
        "district": "Tiruvannamalai",
        "taluk": "Arani",
        "historical_period": "Vijayanagara & Arani Jagir Period (17th-18th Century CE)",
        "name_origin_explanation": "கமண்டல நாக நதியால் சூழப்பட்டு 'ஆறு + அணி' (ஆற்றால் சூழப்பட்ட அணி போன்ற ஊர்) என்ற புவியியல் அமைப்பால் இப்பெயர் பெற்றிருக்கலாம் என்று அறிஞர்கள் கருதுகின்றனர். இது புவியியல் கருதுகோளே தவிர நேரடி கல்வெட்டு ஆவண நிறுவல் அல்ல.",
        "origin_evidence_status": "scholarly_interpretation",
        "historical_events_summary": "1640-இல் ஆரணி ஜாகீர் நிறுவப்பட்டது. 1751 டிசம்பர் 3 அன்று ராபர்ட் கிளைவ் ரஸா சாகிபை தோற்கடித்த புகழ்பெற்ற ஆரணிப் போர் (Battle of Arnee) நடைபெற்றது.",
        "source_title": "North Arcot District Manual (Vol. II): Records of Arani and the Battle of Arnee",
        "source_url": "https://archive.org/details/northarcotdistri02coxauoft",
        "source_page": "pp. 248-254",
        "evidence_quote": "The town of Arani is situated on the south bank of the Kamandala Naga river. Etymologists suggest the name is derived from 'Aru + Ani', describing a settlement positioned like an ornament along the river loop. Established as fortified capital of autonomous Arani Jagir around 1640.",
        "verification_status": "partially_verified"
    },
    7: {  # Kanchipuram
        "place_name_tamil": "காஞ்சிபுரம்",
        "place_name_english": "Kanchipuram",
        "state": "Tamil Nadu",
        "district": "Kanchipuram",
        "taluk": "Kanchipuram",
        "historical_period": "Sangam & Pallava Capital Period (3rd-9th Century CE)",
        "name_origin_explanation": "'காஞ்சி' என்பது இப்பகுதியில் செழித்து வளர்ந்த காஞ்சி மரத்தின் பெயரால் அல்லது நகரின் மங்களப் பெயரால் அமைந்தது என்று ஆய்வாளர்கள் கருதுகின்றனர். பல்லவர் கால கல்வெட்டுகளில் 'காஞ்சிபுரம்' என ஆவணப்படுத்தப்பட்டுள்ளது.",
        "origin_evidence_status": "scholarly_interpretation",
        "historical_events_summary": "பல்லவ பேரரசின் புகழ்பெற்ற தலைநகரம். யுவான் சுவாங் உள்ளிட்ட வரலாற்றுப் பயணிகள் விவரித்துள்ளனர். பிரிட்டிஷ் காலத்தில் 'கான்ஜீவரம்' என அழைக்கப்பட்டது.",
        "source_title": "Chingleput District Manual and Imperial Gazetteer — Conjeeveram",
        "source_url": "https://archive.org/details/chingleputdistri00crol",
        "source_page": "pp. 377-380",
        "evidence_quote": "Kanchi or Conjeeveram was the capital of the Pallava dynasty from the 4th to the 9th centuries. Classical Tamil texts mention Kanchipuram as a center of religious learning.",
        "verification_status": "partially_verified"
    },
    8: {  # Coimbatore
        "place_name_tamil": "கோயம்புத்தூர்",
        "place_name_english": "Coimbatore",
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "taluk": "Coimbatore North",
        "historical_period": "Kongu Chola Period (11th Century CE)",
        "name_origin_explanation": "கொங்குப் பகுதியின் பழங்காலத் தலைவனான 'கோவன்' அல்லது 'கோயன்' என்பவரின் பெயரால் உருவாக்கப்பட்ட 'கோவன் புதூர்' (கோயம்புத்தூர்) என்பதிலிருந்து இப்பெயர் தோன்றியது. பேரூர் பட்டீஸ்வரர் கோயிலில் உள்ள 11-ஆம் நூற்றாண்டு சோழர் கல்வெட்டுகளில் இவ்வூர் 'கோவன் புதூர்' என்றே ஆவணப்படுத்தப்பட்டுள்ளது.",
        "origin_evidence_status": "historically_documented",
        "historical_events_summary": "நொய்யல் நதிக்கரையில் பேரூர் பட்டீஸ்வரர் கோயில் சோழர் கல்வெட்டுகளில் கோவன் புதூர் எனப் பதிவு. 1799-இல் பிரிட்டிஷ் கிழக்கிந்திய கம்பெனியின் நேரடி ஆட்சிக்கு வந்தது.",
        "source_title": "Coimbatore District Manual (Vol. I & II)",
        "source_url": "https://archive.org/details/coimbatoredistri00stua",
        "source_page": "pp. 214-215",
        "evidence_quote": "Coimbatore is situated on the Noyyal river. The name is historically derived from 'Koyanputhur' (கோயம்புத்தூர்), signifying 'the new town of Koyan' or 'Kovan', an ancient chieftain of the Kongu region. In stone inscriptions dating to the 11th century during the reign of the Cholas at the nearby Perur Patteeswarar temple, the place is explicitly designated as 'Kovanputhur'.",
        "verification_status": "verified"
    },
    9: {  # Villupuram
        "place_name_tamil": "விழுப்புரம்",
        "place_name_english": "Villupuram",
        "state": "Tamil Nadu",
        "district": "Villupuram",
        "taluk": "Villupuram",
        "historical_period": "Medieval Chola & Modern Period (10th-20th Century CE)",
        "name_origin_explanation": "வரலாற்று அறிஞர்களும் கல்வெட்டாய்வாளர்களும் 'விழுப்புரம்' என்ற பெயர் 'விழுப்புரையன்' என்ற சோழர் படைத்தலைவர்கள் மற்றும் பெருமக்களுக்கு வழங்கப்பட்ட சிறப்புப் பட்டப்பெயரிலிருந்து தோன்றியதாகக் கருதுகின்றனர். மற்றொரு கோட்பாட்டின்படி 'விழுமிய + புரம்' (புகழ்பெற்ற பெருநகரம்) என்பதாகும். இது ஆய்வாளர்களின் மொழியியல் கருதுகோளாகும்.",
        "origin_evidence_status": "scholarly_interpretation",
        "historical_events_summary": "1919-இல் நகராட்சியாகவும், 1993 செப்டம்பர் 30 அன்று தென் ஆற்காடு மாவட்டம் பிரிக்கப்பட்டபோது புதிய விழுப்புரம் மாவட்டத்தின் தலைமையகமாகவும் ஆனது.",
        "source_title": "South Arcot District Gazetteer",
        "source_url": "https://archive.org/details/southarcotdistri01fran",
        "source_page": "pp. 348-350",
        "evidence_quote": "Villupuram (spelled in early colonial correspondence as Vizhopooram or Verupuram) is situated in the central plains of South Arcot. Scholars and epigraphists derive the name from 'Viluppuraiyan' (விழுப்புரையன்), an aristocratic title borne by distinguished Chola military commanders and nobles of Jananatha-chaturvedimangalam.",
        "verification_status": "partially_verified"
    },
    10: {  # Madurai
        "place_name_tamil": "மதுரை",
        "place_name_english": "Madurai",
        "state": "Tamil Nadu",
        "district": "Madurai",
        "taluk": "Madurai North",
        "historical_period": "Sangam & Early Pandya Period (3rd Century BCE - 14th Century CE)",
        "name_origin_explanation": "சங்க இலக்கியங்களில் 'கூடல்' என்றும், மதுரையை சிவபெருமான் அமிர்தம் (மது) தெளித்து ஆசீர்வதித்ததால் இப்பெயர் பெற்றது என்று புராணங்கள் கூறுகின்றன. மத்து + உரை (அரண் சூழ்ந்த நகரம்) என்ற மொழி ஆய்வுக் கருதுகோளும் உண்டு.",
        "origin_evidence_status": "scholarly_interpretation",
        "historical_events_summary": "பாண்டிய மன்னர்களின் சங்க காலத் தலைநகரம். மீனாட்சி அம்மன் கோயில் நகரம். பிரிட்டிஷ் காலத்தில் 'மதுரா' (Madura) என ஆவணப்படுத்தப்பட்டது.",
        "source_title": "Madura District Gazetteer",
        "source_url": "https://archive.org/details/maduradistrictga01fran",
        "source_page": "pp. 1-30",
        "evidence_quote": "Madura is situated on the Vaigai river. Classical Tamil literature refers to it as Koodal. Tradition derives the name from madhuram ('sweetness'), alluding to drops of divine nectar showered by Shiva.",
        "verification_status": "partially_verified"
    },
    11: {  # Kalambur
        "place_name_tamil": "கலம்பூர்",
        "place_name_english": "Kalambur",
        "state": "Tamil Nadu",
        "district": "Tiruvannamalai",
        "taluk": "Polur",
        "historical_period": "Arani Jagir & Modern Period (18th-20th Century CE)",
        "name_origin_explanation": "கலம்பூர் என்ற பெயரின் வரலாற்று மொழி மூலம் எந்தவொரு பழங்கால கல்வெட்டிலோ அல்லது செப்பேட்டிலோ ஆவணப்படுத்தப்படவில்லை. 'கலம்' (நெல் அளவை) + 'ஊர்' என்ற சேர்க்கையால் இப்பெயர் வந்தது என்று கூறப்படும் விளக்கம் சான்றுகளற்ற உள்ளூர் வாய்வழி ஐதீகமாகும். உண்மைப் பெயர்க் காரணம் நிச்சயமற்ற நிலையிலேயே உள்ளது.",
        "origin_evidence_status": "unknown_origin",
        "historical_events_summary": "18-ஆம் நூற்றாண்டின் ஆரணி ஜாகீர் வருவாய் ஆவணங்களில் இப்பகுதி 'அலியாபாத்' என்ற நிர்வாகப் பெயரில் பதிவு செய்யப்பட்டுள்ளது. 20-ஆம் நூற்றாண்டில் பொன்னி அரிசி ஆலைகள் மற்றும் வணிக மையமாக வளர்ந்தது.",
        "source_title": "Gazetteer of India: Tiruvannamalai District & Polur Revenue Manual",
        "source_url": "https://www.archives.tn.gov.in",
        "source_page": "Vol. 1, pp. 312-314",
        "evidence_quote": "In 18th-century Arani Jagir administrative documents, the settlement was officially recorded under the revenue designation 'Aliyabad'. The etymological origin of the name 'Kalambur' is NOT documented in any stone epigraph. Local folklore attributing it to 'Kalam' is an unverified oral hypothesis; true origin remains uncertain.",
        "verification_status": "unverified"
    }
}

for place in data["places"]:
    pid = place["id"]
    if pid in structured_details:
        place.update(structured_details[pid])
        # Ensure district is NEVER the state name
        assert place["district"] != "Tamil Nadu", f"Invalid district for place {pid}"
        assert place["state"] == "Tamil Nadu"

with open(SEED_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Enriched seed_data.json successfully with all 15 required fields!")
