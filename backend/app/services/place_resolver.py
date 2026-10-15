"""
PeyarVaralaru AI — Place Resolver Service
Identifies places, normalizes names in Tamil and English,
detects administrative divisions, and manages disambiguation.
"""
import re
import unicodedata
import urllib.request
import urllib.parse
import json
from typing import Optional, List, Dict, Tuple, Any

# 38 Official Districts of Tamil Nadu (English <-> Tamil)
TN_DISTRICTS: Dict[str, str] = {
    "ariyalur": "அரியலூர்",
    "chengalpattu": "செங்கல்பட்டு",
    "chennai": "சென்னை",
    "coimbatore": "கோயம்புத்தூர்",
    "cuddalore": "கடலூர்",
    "dharmapuri": "தருமபுரி",
    "dindigul": "திண்டுக்கல்",
    "erode": "ஈரோடு",
    "kallakurichi": "கள்ளக்குறிச்சி",
    "kanchipuram": "காஞ்சிபுரம்",
    "kanyakumari": "கன்னியாகுமரி",
    "karur": "கரூர்",
    "krishnagiri": "கிருஷ்ணகிரி",
    "madurai": "மதுரை",
    "mayiladuthurai": "மயிலாடுதுறை",
    "nagapattinam": "நாகப்பட்டினம்",
    "namakkal": "நாமக்கல்",
    "nilgiris": "நீலகிரி",
    "perambalur": "பெரம்பலூர்",
    "pudukkottai": "புதுக்கோட்டை",
    "ramanathapuram": "ராமநாதபுரம்",
    "ranipet": "ராணிப்பேட்டை",
    "salem": "சேலம்",
    "sivagangai": "சிவகங்கை",
    "tenkasi": "தென்காசி",
    "thanjavur": "தஞ்சாவூர்",
    "theni": "தேனி",
    "thoothukudi": "தூத்துக்குடி",
    "tiruchirappalli": "திருச்சிராப்பள்ளி",
    "tirunelveli": "திருநெல்வேலி",
    "tirupathur": "திருப்பத்தூர்",
    "tiruppur": "திருப்பூர்",
    "tiruvallur": "திருவள்ளூர்",
    "tiruvannamalai": "திருவண்ணாமலை",
    "tiruvarur": "திருவாரூர்",
    "vellore": "வேலூர்",
    "viluppuram": "விழுப்புரம்",
    "virudhunagar": "விருதுநகர்",
}

# Reverse lookup for Tamil district names
TN_DISTRICTS_TA: Dict[str, str] = {
    v.lower(): k.capitalize() for k, v in TN_DISTRICTS.items()
}

# Well-known Tamil Nadu homonyms / ambiguous places
HOMONYMS_REGISTRY: Dict[str, List[Dict[str, Any]]] = {
    "arani": [
        {
            "canonical_name": "Arani",
            "canonical_name_tamil": "ஆரணி",
            "district": "Tiruvannamalai",
            "district_tamil": "திருவண்ணாமலை",
            "taluk": "Arani",
            "taluk_tamil": "ஆரணி",
            "category": "Municipality / Historic Fort Town",
            "category_tamil": "நகராட்சி / வரலாற்று கோட்டை நகரம்",
            "latitude": 12.67,
            "longitude": 79.28,
            "description": "Historic municipality on the Kamandala Naga river in Tiruvannamalai district, renowned for traditional silk weaving, Arani Fort, and the 1751 Battle of Arani.",
            "description_tamil": "திருவண்ணாமலை மாவட்டத்தில் கமண்டல நாக நதிக்கரையில் அமைந்துள்ள வரலாற்று சிறப்புமிக்க நகராட்சி. ஆரணிக் கோட்டை, 1751 ஆரணிப் போர் மற்றும் பட்டு நெசவுக்குப் புகழ்பெற்றது."
        },
        {
            "canonical_name": "Arani",
            "canonical_name_tamil": "ஆரணி",
            "district": "Tiruvallur",
            "district_tamil": "திருவள்ளூர்",
            "taluk": "Gummidipoondi",
            "taluk_tamil": "கும்மிடிப்பூண்டி",
            "category": "Town Panchayat / River Basin",
            "category_tamil": "பேரூராட்சி / நதிப் படுகை",
            "latitude": 13.33,
            "longitude": 80.08,
            "description": "Town panchayat situated in Tiruvallur district along the Arani River (Araniar), historic agricultural settlement near the northern boundary of Tamil Nadu.",
            "description_tamil": "திருவள்ளூர் மாவட்டத்தில் ஆரணி ஆற்றின் (ஆரணியாறு) கரையில் அமைந்துள்ள பேரூராட்சி. வட தமிழகத்தின் பழமையான விவசாயக் குடியிருப்பு."
        }
    ],
    "ஆரணி": [
        {
            "canonical_name": "Arani",
            "canonical_name_tamil": "ஆரணி",
            "district": "Tiruvannamalai",
            "district_tamil": "திருவண்ணாமலை",
            "taluk": "Arani",
            "taluk_tamil": "ஆரணி",
            "category": "Municipality / Historic Fort Town",
            "category_tamil": "நகராட்சி / வரலாற்று கோட்டை நகரம்",
            "latitude": 12.67,
            "longitude": 79.28,
            "description": "Historic municipality on the Kamandala Naga river in Tiruvannamalai district, renowned for traditional silk weaving, Arani Fort, and the 1751 Battle of Arani.",
            "description_tamil": "திருவண்ணாமலை மாவட்டத்தில் கமண்டல நாக நதிக்கரையில் அமைந்துள்ள வரலாற்று சிறப்புமிக்க நகராட்சி. ஆரணிக் கோட்டை, 1751 ஆரணிப் போர் மற்றும் பட்டு நெசவுக்குப் புகழ்பெற்றது."
        },
        {
            "canonical_name": "Arani",
            "canonical_name_tamil": "ஆரணி",
            "district": "Tiruvallur",
            "district_tamil": "திருவள்ளூர்",
            "taluk": "Gummidipoondi",
            "taluk_tamil": "கும்மிடிப்பூண்டி",
            "category": "Town Panchayat / River Basin",
            "category_tamil": "பேரூராட்சி / நதிப் படுகை",
            "latitude": 13.33,
            "longitude": 80.08,
            "description": "Town panchayat situated in Tiruvallur district along the Arani River (Araniar), historic agricultural settlement near the northern boundary of Tamil Nadu.",
            "description_tamil": "திருவள்ளூர் மாவட்டத்தில் ஆரணி ஆற்றின் (ஆரணியாறு) கரையில் அமைந்துள்ள பேரூராட்சி. வட தமிழகத்தின் பழமையான விவசாயக் குடியிருப்பு."
        }
    ],
    "alangulam": [
        {
            "canonical_name": "Alangulam",
            "canonical_name_tamil": "ஆலங்குளம்",
            "district": "Tenkasi",
            "district_tamil": "தென்காசி",
            "taluk": "Alangulam",
            "taluk_tamil": "ஆலங்குளம்",
            "category": "Taluk & Town Panchayat",
            "category_tamil": "வட்டம் & பேரூராட்சி",
            "latitude": 8.87,
            "longitude": 77.50,
            "description": "Taluk headquarters and town panchayat in Tenkasi district, historic agricultural centre in southern Tamil Nadu.",
            "description_tamil": "தென்காசி மாவட்டத்தின் வட்டத் தலைமையிடமும் பேரூராட்சியும் ஆகும். தென் தமிழகத்தின் முக்கியமான வேளாண் சந்தைப் பகுதி."
        },
        {
            "canonical_name": "Alangulam",
            "canonical_name_tamil": "ஆலங்குளம்",
            "district": "Virudhunagar",
            "district_tamil": "விருதுநகர்",
            "taluk": "Vembakottai",
            "taluk_tamil": "வெம்பக்கோட்டை",
            "category": "Town Panchayat / Industrial Town",
            "category_tamil": "பேரூராட்சி / தொழில் நகரம்",
            "latitude": 9.35,
            "longitude": 77.68,
            "description": "Town panchayat in Virudhunagar district, prominent for Tamil Nadu Cements Corporation (TANCEM) factory and limestone deposits.",
            "description_tamil": "விருதுநகர் மாவட்டத்தில் உள்ள பேரூராட்சி. தமிழ்நாடு சிமெண்ட்ஸ் நிறுவனம் (TANCEM) மற்றும் சுண்ணாம்புக்கல் படிவுகளுக்குப் பெயர் பெற்றது."
        }
    ],
    "ஆலங்குளம்": [
        {
            "canonical_name": "Alangulam",
            "canonical_name_tamil": "ஆலங்குளம்",
            "district": "Tenkasi",
            "district_tamil": "தென்காசி",
            "taluk": "Alangulam",
            "taluk_tamil": "ஆலங்குளம்",
            "category": "Taluk & Town Panchayat",
            "category_tamil": "வட்டம் & பேரூராட்சி",
            "latitude": 8.87,
            "longitude": 77.50,
            "description": "Taluk headquarters and town panchayat in Tenkasi district, historic agricultural centre in southern Tamil Nadu.",
            "description_tamil": "தென்காசி மாவட்டத்தின் வட்டத் தலைமையிடமும் பேரூராட்சியும் ஆகும். தென் தமிழகத்தின் முக்கியமான வேளாண் சந்தைப் பகுதி."
        },
        {
            "canonical_name": "Alangulam",
            "canonical_name_tamil": "ஆலங்குளம்",
            "district": "Virudhunagar",
            "district_tamil": "விருதுநகர்",
            "taluk": "Vembakottai",
            "taluk_tamil": "வெம்பக்கோட்டை",
            "category": "Town Panchayat / Industrial Town",
            "category_tamil": "பேரூராட்சி / தொழில் நகரம்",
            "latitude": 9.35,
            "longitude": 77.68,
            "description": "Town panchayat in Virudhunagar district, prominent for Tamil Nadu Cements Corporation (TANCEM) factory and limestone deposits.",
            "description_tamil": "விருதுநகர் மாவட்டத்தில் உள்ள பேரூராட்சி. தமிழ்நாடு சிமெண்ட்ஸ் நிறுவனம் (TANCEM) மற்றும் சுண்ணாம்புக்கல் படிவுகளுக்குப் பெயர் பெற்றது."
        }
    ],
    "sengundram": [
        {
            "canonical_name": "Sengundram (Red Hills)",
            "canonical_name_tamil": "செங்குன்றம் (ரெட் ஹில்ஸ்)",
            "district": "Tiruvallur",
            "district_tamil": "திருவள்ளூர்",
            "taluk": "Madhavaram / Ponneri",
            "taluk_tamil": "மாதவரம் / பொன்னேரி",
            "category": "Historic Catchment & Town",
            "category_tamil": "வரலாற்று நீர்த்தேக்கம் & நகரம்",
            "latitude": 13.19,
            "longitude": 80.19,
            "description": "Historic settlement and major reservoir lake supplying water to Chennai since the 1870s British colonial period, named after red laterite soil hills.",
            "description_tamil": "சிவப்பு சரளை மண் குன்றுகளின் காரணமாக செங்குன்றம் (ரெட் ஹில்ஸ்) எனப் பெயர் பெற்றது. 1870-களில் அமைக்கப்பட்ட வரலாற்று சிறப்புமிக்க சென்னை குடிநீர் ஏரி."
        },
        {
            "canonical_name": "Sengundram",
            "canonical_name_tamil": "செங்குன்றம்",
            "district": "Ranipet",
            "district_tamil": "ராணிப்பேட்டை",
            "taluk": "Walajah",
            "taluk_tamil": "வாலாஜா",
            "category": "Revenue Village",
            "category_tamil": "வருவாய் கிராமம்",
            "latitude": 12.98,
            "longitude": 79.35,
            "description": "Revenue village in Walajah taluk of Ranipet district.",
            "description_tamil": "ராணிப்பேட்டை மாவட்டம் வாலாஜா வட்டத்தில் உள்ள வருவாய் கிராமம்."
        }
    ],
    "செங்குன்றம்": [
        {
            "canonical_name": "Sengundram (Red Hills)",
            "canonical_name_tamil": "செங்குன்றம் (ரெட் ஹில்ஸ்)",
            "district": "Tiruvallur",
            "district_tamil": "திருவள்ளூர்",
            "taluk": "Madhavaram / Ponneri",
            "taluk_tamil": "மாதவரம் / பொன்னேரி",
            "category": "Historic Catchment & Town",
            "category_tamil": "வரலாற்று நீர்த்தேக்கம் & நகரம்",
            "latitude": 13.19,
            "longitude": 80.19,
            "description": "Historic settlement and major reservoir lake supplying water to Chennai since the 1870s British colonial period, named after red laterite soil hills.",
            "description_tamil": "சிவப்பு சரளை மண் குன்றுகளின் காரணமாக செங்குன்றம் (ரெட் ஹில்ஸ்) எனப் பெயர் பெற்றது. 1870-களில் அமைக்கப்பட்ட வரலாற்று சிறப்புமிக்க சென்னை குடிநீர் ஏரி."
        },
        {
            "canonical_name": "Sengundram",
            "canonical_name_tamil": "செங்குன்றம்",
            "district": "Ranipet",
            "district_tamil": "ராணிப்பேட்டை",
            "taluk": "Walajah",
            "taluk_tamil": "வாலாஜா",
            "category": "Revenue Village",
            "category_tamil": "வருவாய் கிராமம்",
            "latitude": 12.98,
            "longitude": 79.35,
            "description": "Revenue village in Walajah taluk of Ranipet district.",
            "description_tamil": "ராணிப்பேட்டை மாவட்டம் வாலாஜா வட்டத்தில் உள்ள வருவாய் கிராமம்."
        }
    ],
    "bhavani": [
        {
            "canonical_name": "Bhavani",
            "canonical_name_tamil": "பவானி",
            "district": "Erode",
            "district_tamil": "ஈரோடு",
            "taluk": "Bhavani",
            "taluk_tamil": "பவானி",
            "category": "Municipality / Pilgrimage Town",
            "category_tamil": "நகராட்சி / ஆன்மீக தலம்",
            "latitude": 11.45,
            "longitude": 77.68,
            "description": "Municipality at the sacred confluence of the Kaveri, Bhavani, and mythical Amutha rivers (Kooduthurai / Sangameswarar Temple). Renowned for carpet weaving.",
            "description_tamil": "காவிரி, பவானி மற்றும் அமிர்த நதிகள் சங்கமிக்கும் கூடுதுறை சங்கமேஸ்வரர் கோயில் அமைந்துள்ள புனித தலம். கம்பள நெசவுக்குப் பெயர் பெற்றது."
        },
        {
            "canonical_name": "Bhavani River",
            "canonical_name_tamil": "பவானி ஆறு",
            "district": "Erode / Coimbatore / Nilgiris",
            "district_tamil": "ஈரோடு / கோயம்புத்தூர் / நீலகிரி",
            "taluk": "Multiple",
            "taluk_tamil": "பல வட்டங்கள்",
            "category": "Perennial River",
            "category_tamil": "வற்றாத ஜீவ நதி",
            "latitude": 11.35,
            "longitude": 77.25,
            "description": "Major perennial tributary of the Kaveri river originating in the Silent Valley/Nilgiris hills.",
            "description_tamil": "நீலகிரி மற்றும் சைலண்ட் வேலி மலைகளில் தோன்றி காவிரியுடன் கலக்கும் முக்கியமான வற்றாத ஜீவ நதி."
        }
    ],
    "பவானி": [
        {
            "canonical_name": "Bhavani",
            "canonical_name_tamil": "பவானி",
            "district": "Erode",
            "district_tamil": "ஈரோடு",
            "taluk": "Bhavani",
            "taluk_tamil": "பவானி",
            "category": "Municipality / Pilgrimage Town",
            "category_tamil": "நகராட்சி / ஆன்மீக தலம்",
            "latitude": 11.45,
            "longitude": 77.68,
            "description": "Municipality at the sacred confluence of the Kaveri, Bhavani, and mythical Amutha rivers (Kooduthurai / Sangameswarar Temple). Renowned for carpet weaving.",
            "description_tamil": "காவிரி, பவானி மற்றும் அமிர்த நதிகள் சங்கமிக்கும் கூடுதுறை சங்கமேஸ்வரர் கோயில் அமைந்துள்ள புனித தலம். கம்பள நெசவுக்குப் பெயர் பெற்றது."
        },
        {
            "canonical_name": "Bhavani River",
            "canonical_name_tamil": "பவானி ஆறு",
            "district": "Erode / Coimbatore / Nilgiris",
            "district_tamil": "ஈரோடு / கோயம்புத்தூர் / நீலகிரி",
            "taluk": "Multiple",
            "taluk_tamil": "பல வட்டங்கள்",
            "category": "Perennial River",
            "category_tamil": "வற்றாத ஜீவ நதி",
            "latitude": 11.35,
            "longitude": 77.25,
            "description": "Major perennial tributary of the Kaveri river originating in the Silent Valley/Nilgiris hills.",
            "description_tamil": "நீலகிரி மற்றும் சைலண்ட் வேலி மலைகளில் தோன்றி காவிரியுடன் கலக்கும் முக்கியமான வற்றாத ஜீவ நதி."
        }
    ]
}

# Major known places registry for high accuracy resolution
KNOWN_PLACES_CATALOG: Dict[str, Dict[str, Any]] = {
    "chennai": {
        "canonical_name": "Chennai",
        "canonical_name_tamil": "சென்னை",
        "district": "Chennai",
        "district_tamil": "சென்னை",
        "taluk": "Chennai",
        "category": "Capital City & Corporation",
        "category_tamil": "தலைநகரம் & மாநகராட்சி",
        "latitude": 13.0827,
        "longitude": 80.2707,
    },
    "madras": {
        "canonical_name": "Chennai",
        "canonical_name_tamil": "சென்னை",
        "district": "Chennai",
        "district_tamil": "சென்னை",
        "taluk": "Chennai",
        "category": "Capital City & Corporation",
        "category_tamil": "தலைநகரம் & மாநகராட்சி",
        "latitude": 13.0827,
        "longitude": 80.2707,
    },
    "சென்னை": {
        "canonical_name": "Chennai",
        "canonical_name_tamil": "சென்னை",
        "district": "Chennai",
        "district_tamil": "சென்னை",
        "taluk": "Chennai",
        "category": "Capital City & Corporation",
        "category_tamil": "தலைநகரம் & மாநகராட்சி",
        "latitude": 13.0827,
        "longitude": 80.2707,
    },
    "மெட்ராஸ்": {
        "canonical_name": "Chennai",
        "canonical_name_tamil": "சென்னை",
        "district": "Chennai",
        "district_tamil": "சென்னை",
        "taluk": "Chennai",
        "category": "Capital City & Corporation",
        "category_tamil": "தலைநகரம் & மாநகராட்சி",
        "latitude": 13.0827,
        "longitude": 80.2707,
    },
    "tiruvannamalai": {
        "canonical_name": "Tiruvannamalai",
        "canonical_name_tamil": "திருவண்ணாமலை",
        "district": "Tiruvannamalai",
        "district_tamil": "திருவண்ணாமலை",
        "taluk": "Tiruvannamalai",
        "category": "District Headquarters & Temple City",
        "category_tamil": "மாவட்டத் தலைநகரம் & ஆன்மீக நகரம்",
        "latitude": 12.2253,
        "longitude": 79.0747,
    },
    "திருவண்ணாமலை": {
        "canonical_name": "Tiruvannamalai",
        "canonical_name_tamil": "திருவண்ணாமலை",
        "district": "Tiruvannamalai",
        "district_tamil": "திருவண்ணாமலை",
        "taluk": "Tiruvannamalai",
        "category": "District Headquarters & Temple City",
        "category_tamil": "மாவட்டத் தலைநகரம் & ஆன்மீக நகரம்",
        "latitude": 12.2253,
        "longitude": 79.0747,
    },
    "kalambur": {
        "canonical_name": "Kalambur",
        "canonical_name_tamil": "கலம்பூர்",
        "district": "Tiruvannamalai",
        "district_tamil": "திருவண்ணாமலை",
        "taluk": "Polur",
        "taluk_tamil": "போளூர்",
        "category": "Selection Grade Town Panchayat",
        "category_tamil": "தேர்வு நிலை பேரூராட்சி",
        "latitude": 12.54,
        "longitude": 79.16,
    },
    "கலம்பூர்": {
        "canonical_name": "Kalambur",
        "canonical_name_tamil": "கலம்பூர்",
        "district": "Tiruvannamalai",
        "district_tamil": "திருவண்ணாமலை",
        "taluk": "Polur",
        "taluk_tamil": "போளூர்",
        "category": "Selection Grade Town Panchayat",
        "category_tamil": "தேர்வு நிலை பேரூராட்சி",
        "latitude": 12.54,
        "longitude": 79.16,
    },
    "madurai": {
        "canonical_name": "Madurai",
        "canonical_name_tamil": "மதுரை",
        "district": "Madurai",
        "district_tamil": "மதுரை",
        "taluk": "Madurai North/South",
        "category": "City Municipal Corporation & Historic Capital",
        "category_tamil": "மாநகராட்சி & வரலாற்றுத் தலைநகரம்",
        "latitude": 9.9252,
        "longitude": 78.1198,
    },
    "மதுரை": {
        "canonical_name": "Madurai",
        "canonical_name_tamil": "மதுரை",
        "district": "Madurai",
        "district_tamil": "மதுரை",
        "taluk": "Madurai North/South",
        "category": "City Municipal Corporation & Historic Capital",
        "category_tamil": "மாநகராட்சி & வரலாற்றுத் தலைநகரம்",
        "latitude": 9.9252,
        "longitude": 78.1198,
    },
    "thanjavur": {
        "canonical_name": "Thanjavur",
        "canonical_name_tamil": "தஞ்சாவூர்",
        "district": "Thanjavur",
        "district_tamil": "தஞ்சாவூர்",
        "taluk": "Thanjavur",
        "category": "City Municipal Corporation & Chola Capital",
        "category_tamil": "மாநகராட்சி & சோழர் தலைநகரம்",
        "latitude": 10.787,
        "longitude": 79.1378,
    },
    "தஞ்சாவூர்": {
        "canonical_name": "Thanjavur",
        "canonical_name_tamil": "தஞ்சாவூர்",
        "district": "Thanjavur",
        "district_tamil": "தஞ்சாவூர்",
        "taluk": "Thanjavur",
        "category": "City Municipal Corporation & Chola Capital",
        "category_tamil": "மாநகராட்சி & சோழர் தலைநகரம்",
        "latitude": 10.787,
        "longitude": 79.1378,
    },
    "tiruchirappalli": {
        "canonical_name": "Tiruchirappalli",
        "canonical_name_tamil": "திருச்சிராப்பள்ளி",
        "district": "Tiruchirappalli",
        "district_tamil": "திருச்சிராப்பள்ளி",
        "taluk": "Tiruchirappalli",
        "category": "City Municipal Corporation & Rockfort City",
        "category_tamil": "மாநகராட்சி & மலைக்கோட்டை நகரம்",
        "latitude": 10.7905,
        "longitude": 78.7047,
    },
    "திருச்சிராப்பள்ளி": {
        "canonical_name": "Tiruchirappalli",
        "canonical_name_tamil": "திருச்சிராப்பள்ளி",
        "district": "Tiruchirappalli",
        "district_tamil": "திருச்சிராப்பள்ளி",
        "taluk": "Tiruchirappalli",
        "category": "City Municipal Corporation & Rockfort City",
        "category_tamil": "மாநகராட்சி & மலைக்கோட்டை நகரம்",
        "latitude": 10.7905,
        "longitude": 78.7047,
    },
    "kanchipuram": {
        "canonical_name": "Kanchipuram",
        "canonical_name_tamil": "காஞ்சிபுரம்",
        "district": "Kanchipuram",
        "district_tamil": "காஞ்சிபுரம்",
        "taluk": "Kanchipuram",
        "category": "City Municipal Corporation & Pallava Capital",
        "category_tamil": "மாநகராட்சி & பல்லவர் தலைநகரம்",
        "latitude": 12.8342,
        "longitude": 79.7036,
    },
    "காஞ்சிபுரம்": {
        "canonical_name": "Kanchipuram",
        "canonical_name_tamil": "காஞ்சிபுரம்",
        "district": "Kanchipuram",
        "district_tamil": "காஞ்சிபுரம்",
        "taluk": "Kanchipuram",
        "category": "City Municipal Corporation & Pallava Capital",
        "category_tamil": "மாநகராட்சி & பல்லவர் தலைநகரம்",
        "latitude": 12.8342,
        "longitude": 79.7036,
    },
    "coimbatore": {
        "canonical_name": "Coimbatore",
        "canonical_name_tamil": "கோயம்புத்தூர்",
        "district": "Coimbatore",
        "district_tamil": "கோயம்புத்தூர்",
        "taluk": "Coimbatore",
        "category": "City Municipal Corporation & Kongu Region Hub",
        "category_tamil": "மாநகராட்சி & கொங்கு மண்டல மையம்",
        "latitude": 11.0168,
        "longitude": 76.9558,
    },
    "கோயம்புத்தூர்": {
        "canonical_name": "Coimbatore",
        "canonical_name_tamil": "கோயம்புத்தூர்",
        "district": "Coimbatore",
        "district_tamil": "கோயம்புத்தூர்",
        "taluk": "Coimbatore",
        "category": "City Municipal Corporation & Kongu Region Hub",
        "category_tamil": "மாநகராட்சி & கொங்கு மண்டல மையம்",
        "latitude": 11.0168,
        "longitude": 76.9558,
    },
    "salem": {
        "canonical_name": "Salem",
        "canonical_name_tamil": "சேலம்",
        "district": "Salem",
        "district_tamil": "சேலம்",
        "taluk": "Salem",
        "category": "City Municipal Corporation",
        "category_tamil": "மாநகராட்சி",
        "latitude": 11.6643,
        "longitude": 78.1460,
    },
    "சேலம்": {
        "canonical_name": "Salem",
        "canonical_name_tamil": "சேலம்",
        "district": "Salem",
        "district_tamil": "சேலம்",
        "taluk": "Salem",
        "category": "City Municipal Corporation",
        "category_tamil": "மாநகராட்சி",
        "latitude": 11.6643,
        "longitude": 78.1460,
    },
    "villupuram": {
        "canonical_name": "Villupuram",
        "canonical_name_tamil": "விழுப்புரம்",
        "district": "Villupuram",
        "district_tamil": "விழுப்புரம்",
        "taluk": "Villupuram",
        "taluk_tamil": "விழுப்புரம்",
        "category": "District Headquarters & Municipality",
        "category_tamil": "மாவட்டத் தலைமையகம் & நகராட்சி",
        "latitude": 11.9401,
        "longitude": 79.4861,
    },
    "viluppuram": {
        "canonical_name": "Villupuram",
        "canonical_name_tamil": "விழுப்புரம்",
        "district": "Villupuram",
        "district_tamil": "விழுப்புரம்",
        "taluk": "Villupuram",
        "taluk_tamil": "விழுப்புரம்",
        "category": "District Headquarters & Municipality",
        "category_tamil": "மாவட்டத் தலைமையகம் & நகராட்சி",
        "latitude": 11.9401,
        "longitude": 79.4861,
    },
    "விழுப்புரம்": {
        "canonical_name": "Villupuram",
        "canonical_name_tamil": "விழுப்புரம்",
        "district": "Villupuram",
        "district_tamil": "விழுப்புரம்",
        "taluk": "Villupuram",
        "taluk_tamil": "விழுப்புரம்",
        "category": "District Headquarters & Municipality",
        "category_tamil": "மாவட்டத் தலைமையகம் & நகராட்சி",
        "latitude": 11.9401,
        "longitude": 79.4861,
    },
    "tirunelveli": {
        "canonical_name": "Tirunelveli",
        "canonical_name_tamil": "திருநெல்வேலி",
        "district": "Tirunelveli",
        "district_tamil": "திருநெல்வேலி",
        "taluk": "Tirunelveli",
        "category": "City Municipal Corporation & Historic Pandya Hub",
        "category_tamil": "மாநகராட்சி & வரலாற்று பாண்டிய மையம்",
        "latitude": 8.7139,
        "longitude": 77.7567,
    },
    "திருநெல்வேலி": {
        "canonical_name": "Tirunelveli",
        "canonical_name_tamil": "திருநெல்வேலி",
        "district": "Tirunelveli",
        "district_tamil": "திருநெல்வேலி",
        "taluk": "Tirunelveli",
        "category": "City Municipal Corporation & Historic Pandya Hub",
        "category_tamil": "மாநகராட்சி & வரலாற்று பாண்டிய மையம்",
        "latitude": 8.7139,
        "longitude": 77.7567,
    },
    "kaveri": {
        "canonical_name": "Kaveri River",
        "canonical_name_tamil": "காவிரி ஆறு",
        "district": "Kaveri Basin",
        "district_tamil": "காவிரி வடிநிலப் பகுதி",
        "taluk": "Multiple",
        "taluk_tamil": "பல வட்டங்கள்",
        "category": "Sacred Perennial River",
        "category_tamil": "புனித வற்றாத ஜீவ நதி",
        "latitude": 11.0,
        "longitude": 78.5,
    },
    "காவிரி": {
        "canonical_name": "Kaveri River",
        "canonical_name_tamil": "காவிரி ஆறு",
        "district": "Kaveri Basin",
        "district_tamil": "காவிரி வடிநிலப் பகுதி",
        "taluk": "Multiple",
        "taluk_tamil": "பல வட்டங்கள்",
        "category": "Sacred Perennial River",
        "category_tamil": "புனித வற்றாத ஜீவ நதி",
        "latitude": 11.0,
        "longitude": 78.5,
    }
}


def normalize_query_text(text: str) -> str:
    """Normalize unicode NFC, strip extra spaces, lower-case."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[\t\r\n]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_place_query(raw_query: str) -> Tuple[str, Optional[str]]:
    """
    Strips conversational question wrappers and extracts:
    (extracted_place_name, optional_district_hint)
    e.g.:
    "What is the history of Arani?" -> ("Arani", None)
    "Why is Kalambur called Kalambur?" -> ("Kalambur", None)
    "How did Tiruvannamalai get its name?" -> ("Tiruvannamalai", None)
    "ஆரணி, திருவண்ணாமலை" -> ("ஆரணி", "திருவண்ணாமலை")
    "கலம்பூர் என்ற ஊரின் பெயர் காரணம் என்ன?" -> ("கலம்பூர்", None)
    """
    q = normalize_query_text(raw_query)

    # 1. Check for explicit comma/hyphen/parentheses district hint:
    # "Arani, Tiruvannamalai" or "Alangulam (Tenkasi)" or "ஆரணி - திருவண்ணாமலை"
    district_hint = None
    delim_match = re.split(r"[,|\-(/]\s*", q)
    if len(delim_match) >= 2:
        candidate_place = delim_match[0].strip()
        candidate_dist = delim_match[1].replace(")", "").strip()
        norm_dist = candidate_dist.lower()
        if norm_dist in TN_DISTRICTS or norm_dist in TN_DISTRICTS_TA:
            return candidate_place, candidate_dist
        for eng, tam in TN_DISTRICTS.items():
            if eng in norm_dist or tam in norm_dist:
                return candidate_place, eng

    # 2. Check for explicit district qualifier in natural sentence:
    # e.g. "திருவண்ணாமலை மாவட்ட ஆரணி" or "Tiruvannamalai district Arani"
    dist_prefix_match = re.search(r"([\w\u0B80-\u0BFF]+)\s+(?:மாவட்டம்|மாவட்ட|district)\s+([\w\u0B80-\u0BFF]+)", q, re.IGNORECASE)
    if dist_prefix_match:
        d_cand = dist_prefix_match.group(1).strip()
        p_cand = dist_prefix_match.group(2).strip()
        d_lower = d_cand.lower()
        if d_lower in TN_DISTRICTS or d_lower in TN_DISTRICTS_TA:
            return p_cand, d_cand

    # 3. Smart known-place extraction for conversational queries
    # Check if a known specific town / municipality / homonym is embedded in question
    known_targets = [
        ("arani", "ஆரணி"),
        ("kalambur", "கலம்பூர்"),
        ("tiruvannamalai", "திருவண்ணாமலை"),
        ("coimbatore", "கோயம்புத்தூர்"),
        ("villupuram", "விழுப்புரம்"),
        ("viluppuram", "விழுப்புரம்"),
        ("chennai", "சென்னை"),
        ("george town", "ஜார்ஜ் டவுன்"),
        ("black town", "பிளாக் டவுன்"),
        ("thanjavur", "தஞ்சாவூர்"),
        ("tiruchirappalli", "திருச்சிராப்பள்ளி"),
        ("madurai", "மதுரை"),
        ("kanchipuram", "காஞ்சிபுரம்")
    ]
    # Check if any target place is in q
    for eng_k, tam_k in known_targets:
        # Check Tamil token
        if tam_k in q:
            # Check if there is also a distinct district mentioned (e.g. திருவண்ணாமலை மாவட்ட ஆரணி)
            for d_eng, d_ta in TN_DISTRICTS.items():
                if d_ta != tam_k and (d_ta in q or d_eng in q.lower()):
                    district_hint = d_eng.capitalize()
                    break
            return tam_k, district_hint
        # Check English token
        pattern_eng = r'\b' + re.escape(eng_k) + r'\b'
        if re.search(pattern_eng, q, re.IGNORECASE):
            for d_eng, d_ta in TN_DISTRICTS.items():
                if d_eng != eng_k and (d_eng in q.lower() or d_ta in q):
                    district_hint = d_eng.capitalize()
                    break
            return eng_k.capitalize(), district_hint

    # 4. English question stripping regexes
    en_patterns = [
        r"^what\s+is\s+the\s+historical\s+origin\s+of\s+(.+)$",
        r"^what\s+is\s+the\s+history\s+of\s+(.+)$",
        r"^what\s+was\s+the\s+historical\s+name\s+of\s+(.+)$",
        r"^why\s+is\s+(.+?)\s+called\s+.+$",
        r"^why\s+is\s+(.+?)\s+named\s+.+$",
        r"^how\s+did\s+(.+?)\s+get\s+its\s+name\??$",
        r"^tell\s+me\s+about\s+(?:the\s+place\s+)?(.+)$",
        r"^history\s+of\s+(.+)$",
        r"^origin\s+of\s+(?:the\s+name\s+)?(.+)$",
        r"^where\s+is\s+(.+)$",
        r"^meaning\s+of\s+(?:the\s+name\s+)?(.+)$",
    ]
    for pat in en_patterns:
        m = re.match(pat, q, re.IGNORECASE)
        if m:
            clean = m.group(1).strip(" ?.,!\"'")
            return clean, district_hint

    # 5. Tamil question stripping regexes
    ta_patterns = [
        r"^(.+?)(?:\s+என்ற\s+)?(?:ஊரின்\s+|நகரத்தின்\s+|கிராமத்தின்\s+|இடத்தின்\s+)?(?:பெயரின்\s+)?(?:வரலாறு|தோற்றம்|பொருள்|காரணம்).+$",
        r"^(.+?)(?:\s+என்ற\s+)?(?:ஊரின்\s+|நகரத்தின்\s+|கிராமத்தின்\s+)?வரலாறு\s+(?:என்ன|பற்றி\s+கூறு)?\??$",
        r"^(.+?)(?:\s+என்ற\s+)?(?:ஊருக்கு\s+|இடத்திற்கு\s+)?பெயர்\s+(?:எப்படி\s+வந்தது|காரணம்\s+என்ன)\??$",
        r"^(.+?)(?:\s+என்ற\s+)?(?:ஊரின்\s+|இடத்தின்\s+)?பழைய\s+பெயர்\s+என்ன\??$",
        r"^(.+?)(?:\s+ஏன்\s+)?(?:அப்படி\s+)?அழைக்கப்படுகிறது\??$",
        r"^(.+?)(?:\s+பற்றிய\s+வரலாற்றுத்\s+தகவல்கள்)\??$",
        r"^(.+?)(?:\s+பெயர்\s+வரலாறு)\??$",
        r"^(.+?)(?:\s+என்ற\s+ஊர்)\??$",
    ]
    for pat in ta_patterns:
        m = re.match(pat, q)
        if m:
            clean = m.group(1).strip(" ?.,!\"'")
            return clean, district_hint

    # Clean residual punctuation
    cleaned = re.sub(r"[?!.,\"']+$", "", q).strip()
    return cleaned, district_hint


def resolve_place_with_external_geo(query: str) -> Optional[Dict[str, Any]]:
    """
    Resolve unknown place coordinates and administrative hierarchy
    using OpenStreetMap Nominatim or Wikipedia API within Tamil Nadu.
    Handles network errors safely with short timeout.
    """
    try:
        # 1. Search OpenStreetMap Nominatim restricted to Tamil Nadu, India
        encoded = urllib.parse.quote(f"{query}, Tamil Nadu, India")
        url = f"https://nominatim.openstreetmap.org/search?q={encoded}&format=json&addressdetails=1&limit=3"
        req = urllib.request.Request(url, headers={"User-Agent": "PeyarVaralaruPlaceResolver/1.0"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data and isinstance(data, list) and len(data) > 0:
                top = data[0]
                addr = top.get("address", {})
                state = addr.get("state", "")
                if "tamil nadu" in state.lower():
                    raw_dist = addr.get("state_district") or addr.get("county") or addr.get("city") or None
                    district = None
                    if raw_dist:
                        cleaned_d = raw_dist.replace("District", "").strip()
                        if cleaned_d.lower() in TN_DISTRICTS:
                            district = cleaned_d.title()
                    
                    cat = top.get("type", "Settlement")
                    lat = float(top.get("lat", 0.0))
                    lon = float(top.get("lon", 0.0))
                    name = top.get("name") or query
                    return {
                        "canonical_name": name,
                        "canonical_name_tamil": name,
                        "state": "Tamil Nadu",
                        "state_tamil": "தமிழ்நாடு",
                        "district": district,
                        "district_tamil": TN_DISTRICTS.get(district.lower(), None) if district else None,
                        "taluk": addr.get("county") or addr.get("municipality") or None,
                        "taluk_tamil": addr.get("county") or None,
                        "category": cat.capitalize(),
                        "category_tamil": "வருவாய் குடியிருப்பு / ஊர்",
                        "latitude": lat,
                        "longitude": lon,
                        "source": "osm_nominatim"
                    }
    except Exception:
        pass

    return None


def resolve_place(query: str, district_hint: Optional[str] = None) -> Dict[str, Any]:
    """
    Main place resolution engine:
    1. Extracts place name & district hint
    2. Checks for known homonyms and ambiguity
    3. Resolves known places catalogue
    4. Falls back to external geocoding if unknown
    5. Returns structured place identity with ambiguity flag
    """
    raw_place, parsed_dist = clean_place_query(query)
    effective_dist = district_hint or parsed_dist
    norm_place = normalize_query_text(raw_place).lower()

    # Check homonyms registry (e.g. Arani, Alangulam, Sengundram, Bhavani)
    if norm_place in HOMONYMS_REGISTRY:
        candidates = HOMONYMS_REGISTRY[norm_place]
        # If district hint was provided, see if it matches one candidate exactly
        if effective_dist:
            eff_norm = effective_dist.strip().lower()
            for cand in candidates:
                if (eff_norm in cand["district"].lower() or 
                    eff_norm in cand["district_tamil"].lower()):
                    return {
                        "status": "resolved",
                        "is_ambiguous": False,
                        "place": cand,
                        "candidates": []
                    }
        # If no district hint, it is ambiguous!
        return {
            "status": "ambiguous",
            "is_ambiguous": True,
            "place": candidates[0],  # default top candidate for fallback
            "candidates": candidates,
            "message_tamil": f"'{raw_place}' என்ற பெயரில் தமிழ்நாட்டில் ஒன்றுக்கும் மேற்பட்ட இடங்கள் உள்ளன. சரியான மாவட்டத்தைத் தேர்ந்தெடுக்கவும்.",
            "message_english": f"Multiple places named '{raw_place}' exist in Tamil Nadu. Please select the appropriate district."
        }

    # Check known places catalog
    if norm_place in KNOWN_PLACES_CATALOG:
        match = KNOWN_PLACES_CATALOG[norm_place]
        return {
            "status": "resolved",
            "is_ambiguous": False,
            "place": match,
            "candidates": []
        }

    # Try external geo resolution (Nominatim / Wikipedia)
    external_res = resolve_place_with_external_geo(raw_place)
    if external_res:
        return {
            "status": "resolved",
            "is_ambiguous": False,
            "place": external_res,
            "candidates": []
        }

    # Fallback for unrecognized place name — NEVER default district to state name!
    is_tamil_input = any('\u0b80' <= c <= '\u0bff' for c in raw_place)
    name_ta = raw_place if is_tamil_input else raw_place
    name_en = raw_place if not is_tamil_input else raw_place
    
    valid_dist = None
    if effective_dist:
        eff_clean = effective_dist.strip().lower()
        if eff_clean in TN_DISTRICTS:
            valid_dist = eff_clean.title()
        elif eff_clean in TN_DISTRICTS_TA:
            valid_dist = TN_DISTRICTS_TA[eff_clean]

    dist_ta = TN_DISTRICTS.get(valid_dist.lower(), None) if valid_dist else None

    generic_place = {
        "canonical_name": name_en,
        "canonical_name_tamil": name_ta,
        "state": "Tamil Nadu",
        "state_tamil": "தமிழ்நாடு",
        "district": valid_dist,
        "district_tamil": dist_ta,
        "taluk": None,
        "taluk_tamil": None,
        "category": "Unknown Locality",
        "category_tamil": "அடையாளம் காணப்படாத பகுதி",
        "latitude": None,
        "longitude": None,
        "is_custom": True,
        "is_unverified": True
    }

    return {
        "status": "unresolved" if not valid_dist else "partial",
        "is_ambiguous": False,
        "place": generic_place,
        "candidates": []
    }

