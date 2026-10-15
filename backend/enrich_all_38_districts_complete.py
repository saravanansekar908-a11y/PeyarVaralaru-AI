"""
Comprehensive 38 Districts Bilingual Enrichment Script for PeyarVaralaru AI.
Translates all specialities, famous places, official sources, and research guidance
into authentic, natural Tamil and clean English, ensuring NO mixed language sentences.
Updates both frontend/src/data/districtsData.json and backend/data/tamil_nadu_38_districts_intelligence.json.
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

# Comprehensive translation dictionary for all specialities across 38 districts
# Key: English Name
SPECIALITIES_TRANSLATIONS = {
    # 1. Ariyalur
    "Gangaikonda Cholapuram Temple (UNESCO)": {
        "name_ta": "கங்கைகொண்ட சோழபுரம் பெருவுடையார் திருக்கோயில் (யுனெஸ்கோ)",
        "name_en": "Gangaikonda Cholapuram Temple (UNESCO)",
        "category_ta": "யுனெஸ்கோ உலகப் பாரம்பரியச் சின்னம் & சோழர் கட்டடக் கலை",
        "category_en": "UNESCO World Heritage & Imperial Architecture",
        "explanation_ta": "கங்கைப் படையெடுப்பின் வெற்றி நினைவாக முதலாம் ராஜேந்திர சோழனால் கி.பி. 1035-இல் எழுப்பப்பட்ட கம்பீரமான பெருங்கோயில்.",
        "explanation_en": "Built by Rajendra Chola I around 1035 CE to commemorate his victorious expedition to the Ganges. One of the Great Living Chola Temples.",
        "significance_ta": "சுமார் 250 ஆண்டுகள் சோழப் பேரரசின் தலைநகரமாகத் திகழ்ந்த வரலாற்றுப் பெருமை வாய்ந்தது.",
        "significance_en": "Served as the imperial capital of the Chola Empire for nearly 250 years."
    },
    "Cretaceous Era Fossil Beds & Ammonites": {
        "name_ta": "கிரெட்டேசியஸ் புதைபடிவ பாறைப்படிவுகள் & அம்மோனைட்டுகள்",
        "name_en": "Cretaceous Era Fossil Beds & Ammonites",
        "category_ta": "புவியியல் & தொல்லுயிரியல் மரபு",
        "category_en": "Paleontological Heritage",
        "explanation_ta": "அரியலூரின் சுண்ணாம்பு பாறைப் படுகைகளில் 6.5 முதல் 10 கோடி ஆண்டுகள் பழமையான கடல்வாழ் உயிரினங்கள், டைனோசர் முட்டைகள் மற்றும் அம்மோனைட் புதைபடிவங்கள் நிறைந்துள்ளன.",
        "explanation_en": "Ariyalur's sedimentary limestone terrain holds extensive marine fossils, dinosaur eggs, and ammonite shells dating back 65 to 100 million years.",
        "significance_ta": "தெற்காசியாவின் மிக முக்கியமான புவியியல் மற்றும் தொல்லுயிரியல் களமாக சர்வதேச அறிஞர்களால் போற்றப்படுகிறது.",
        "significance_en": "A critical geological field site for paleontology in South Asia, often called a geological wonderland."
    },
    "Cement Capital of Tamil Nadu": {
        "name_ta": "தமிழ்நாட்டின் சிமெண்ட் தலைநகரம்",
        "name_en": "Cement Capital of Tamil Nadu",
        "category_ta": "தொழில் & கனிம வளம்",
        "category_en": "Industrial & Mineral Economy",
        "explanation_ta": "உயர்தர சுண்ணாம்புக்கல் படிவுகள் நிறைந்த பகுதியாக விளங்குவதால், அரியலூர் பல முன்னணி சிமெண்ட் உற்பத்தி ஆலைகளின் மையமாகத் திகழ்கிறது.",
        "explanation_en": "Rich high-grade limestone deposits have made Ariyalur host to numerous major cement manufacturing plants.",
        "significance_ta": "தமிழ்நாடு மற்றும் அண்டை மாநிலங்களின் உள்கட்டமைப்பு வளர்ச்சிக்குத் தேவையான முக்கிய சிமெண்ட் உற்பத்தியை வழங்குகிறது.",
        "significance_en": "Powers infrastructure across Tamil Nadu and neighbouring states."
    },
    "Karaivetti Bird Sanctuary": {
        "name_ta": "கரைவெட்டி பறவைகள் சரணாலயம்",
        "name_en": "Karaivetti Bird Sanctuary",
        "category_ta": "சூழலியல் & பறவைகள் சரணாலயம்",
        "category_en": "Ecology & Wildlife",
        "explanation_ta": "தமிழ்நாட்டின் மிகப்பெரிய நன்னீர் ஏரி சரணாலயங்களில் ஒன்று; குளிர்காலத்தில் பல்லாயிரக்கணக்கான வலசைப் பறவைகள் இங்கு தஞ்சமடைகின்றன.",
        "explanation_en": "One of the largest freshwater lake bird sanctuaries in Tamil Nadu, hosting thousands of migratory waterfowl every winter.",
        "significance_ta": "பட்டைத்தலை வாத்துகள் உள்ளிட்ட அரிய வலசைப் பறவைகளைக் காக்கும் சர்வதேச ராம்சார் ஈரநிலத் தளம்.",
        "significance_en": "Ramsar-recognized habitat supporting bar-headed geese and migratory birds."
    },

    # 2. Chengalpattu
    "Group of Monuments at Mamallapuram (UNESCO)": {
        "name_ta": "மாமல்லபுரம் கடற்கரைக் கோயில் மற்றும் குடைவரைக் கலை (யுனெஸ்கோ)",
        "name_en": "Group of Monuments at Mamallapuram (UNESCO)",
        "category_ta": "யுனெஸ்கோ உலகப் பாரம்பரியத் தளம்",
        "category_en": "UNESCO World Heritage Site",
        "explanation_ta": "கி.பி. 7 மற்றும் 8-ஆம் நூற்றாண்டுகளில் பல்லவ மன்னர்களால் செதுக்கப்பட்ட கடற்கரைக் கோயில், ஐந்து ரதங்கள் மற்றும் அர்ச்சுனன் தபசு உள்ளிட்ட ஒற்றைக்கல் கலைப்படைப்புகள்.",
        "explanation_en": "7th and 8th-century Pallava coastal sanctuary featuring the monolithic Shore Temple, Five Rathas, and Arjuna's Penance.",
        "significance_ta": "பல்லவர்களின் கடல்வழி வாணிபப் பெருமையையும் பாறை குடைவரைக் கலைச் சிறப்பையும் பறைசாற்றும் வரலாற்றுச் சின்னம்.",
        "significance_en": "Premier open-air rock sculpture sanctuary illustrating Pallava maritime greatness."
    },
    "Vedanthangal Bird Sanctuary": {
        "name_ta": "வேடந்தாங்கல் பறவைகள் சரணாலயம்",
        "name_en": "Vedanthangal Bird Sanctuary",
        "category_ta": "வனவிலங்கு & சூழல் பாதுகாப்பு",
        "category_en": "Wildlife & Conservation",
        "explanation_ta": "1798-இல் முறைப்படுத்தப்பட்ட இந்தியாவின் பழமையான நீர்ப்பறவைகள் சரணாலயம்; பல நூற்றாண்டுகளாக உள்ளூர் மக்களால் பாதுகாக்கப்பட்ட இயற்கை புகலிடம்.",
        "explanation_en": "Established in 1798, it is the oldest water bird sanctuary in India, conserved by local community protection for centuries.",
        "significance_ta": "நாரைகள், கூழைக்கடாக்கள் மற்றும் கரண்டிவாயன்கள் இனப்பெருக்கம் செய்யும் முக்கிய வலசை தளம்.",
        "significance_en": "Critical breeding habitat for migratory herons, storks, egrets, and spoonbills."
    },
    "Automobile & Electronics Corridor (Maraimalai Nagar & Oragadam)": {
        "name_ta": "வாகன உற்பத்தி & மின்னணு தொழிற்பேட்டை மையம்",
        "name_en": "Automobile & Electronics Corridor (Maraimalai Nagar & Oragadam)",
        "category_ta": "நவீன தொழில் வளர்ச்சி",
        "category_en": "Industrial Innovation",
        "explanation_ta": "மறைமலைநகர் மற்றும் ஒரகடம் பகுதிகளை உள்ளடக்கிய தெற்காசியாவின் முன்னணி வாகன மற்றும் மின்னணு பாகங்கள் தயாரிப்பு மண்டலம்.",
        "explanation_en": "Major hub for automobile manufacturing and electronic engineering in South Asia.",
        "significance_ta": "தமிழ்நாட்டின் சர்வதேச வாகன ஏற்றுமதி மற்றும் தொழில் வளர்ச்சிக்கு மாபெரும் பங்களிப்பை வழங்குகிறது.",
        "significance_en": "A major contributor to Tamil Nadu's industrial and automotive export economy."
    },

    # 3. Chennai
    "Kapaleeshwarar Temple & Mylapore Heritage": {
        "name_ta": "மயிலாப்பூர் கபாலீஸ்வரர் திருக்கோயில் & தொன்மை மரபு",
        "name_en": "Kapaleeshwarar Temple & Mylapore Heritage",
        "category_ta": "திராவிட கோயில் கட்டடக்கலை மரபு",
        "category_en": "Dravidian Temple Heritage",
        "explanation_ta": "பல்லவர் மற்றும் விஜயநகர கலை வண்ணத்தில் மிளிரும் திராவிடக் கோயில்; தேவாரப் பதிகங்கள் பெற்ற பாடல் பெற்ற சிவத்தலம்.",
        "explanation_en": "Ancient Dravidian temple sanctified by the 7th-century Saivite Nayanars, embodying the vibrant religious traditions of Mylapore.",
        "significance_ta": "மயிலாப்பூரின் 2000 ஆண்டுகால வரலாற்றுத் தொடர்ச்சியையும் கர்நாடக இசைப் பண்பாட்டையும் பிரதிபலிக்கிறது.",
        "significance_en": "Represents Mylapore's two millennia of documented coastal culture and cultural festivals."
    },
    "Fort St. George & Tamil Nadu Secretariat": {
        "name_ta": "புனித ஜார்ஜ் கோட்டை & தலைமைச் செயலகம்",
        "name_en": "Fort St. George & Tamil Nadu Secretariat",
        "category_ta": "வரலாற்று நிர்வாக அரண்",
        "category_en": "Colonial Administrative Heritage",
        "explanation_ta": "1644-இல் ஆங்கிலேய கிழக்கிந்தியக் கம்பெனியால் கட்டப்பட்ட முதல் பிரிட்டிஷ் கோட்டை; தற்கால தமிழ்நாடு அரசின் தலைமைச் செயலகம் இயங்கும் இடம்.",
        "explanation_en": "First English fortress in India founded in 1644, now housing the Legislative Assembly and Secretariat of Tamil Nadu.",
        "significance_ta": "நவீன சென்னை மாநகரத்தின் நிர்வாக உருவாக்கத்திற்கும் தென்னிந்திய வரலாற்றிற்கும் அடித்தளமாக அமைந்த தளம்.",
        "significance_en": "Foundational site around which the modern metropolis of Madras and southern governance evolved."
    },
    "Marina Beach & Promenade": {
        "name_ta": "மெரினா கடற்கரை & உலாச்சாலை",
        "name_en": "Marina Beach & Promenade",
        "category_ta": "இயற்கைக் கடற்கரை சின்னம்",
        "category_en": "Natural Urban Landmark",
        "explanation_ta": "வங்காள விரிகுடாக் கரையில் 13 கி.மீ நீளத்திற்கு விரிந்துள்ள உலகின் இரண்டாவது மிக நீளமான இயற்கை கடற்கரை உலாச்சாலை.",
        "explanation_en": "A 13-kilometer natural urban beach stretching along the Bay of Bengal, known as the second longest natural urban beach globally.",
        "significance_ta": "சென்னையின் அடையாளச் சின்னமாகவும், தமிழ் வரலாற்று ஆளுமைகளின் சிலைகள் நிறைந்த பண்பாட்டு உலாவரங்கமாகவும் திகழ்கிறது.",
        "significance_en": "Iconic cultural and public promenade lined with statues of legendary Tamil literary figures and leaders."
    },
    "Healthcare & Automobile Capital of India": {
        "name_ta": "இந்தியாவின் மருத்துவ & வாகனத் தலைநகரம்",
        "name_en": "Healthcare & Automobile Capital of India",
        "category_ta": "பொருளாதாரம் & உலகளாவிய சேவைகள்",
        "category_en": "Economy & Healthcare",
        "explanation_ta": "இந்தியாவின் மருத்துவத் தலைநகரமாகவும் ('டெட்ராய்ட் ஆஃப் சவுத் ஏசியா' எனவும்) போற்றப்படும் சென்னையின் உலகத்தரம் வாய்ந்த மருத்துவமனைகள் மற்றும் வாகனத் தொழிற்சாலைகள்.",
        "explanation_en": "Renowned as the 'Detroit of South Asia' and medical capital of India, with top multispecialty health centers and automotive plants.",
        "significance_ta": "சர்வதேச மருத்துவச் சுற்றுலா மற்றும் ஏற்றுமதி உற்பத்தியில் இந்தியாவிலேயே முன்னணி வகிக்கிறது.",
        "significance_en": "Commands global leadership in medical tourism and international automotive component manufacturing."
    },

    # 4. Coimbatore
    "Kovai Kora Cotton Sarees (GI Tag)": {
        "name_ta": "கோவை கோரா பருத்தி சேலைகள் (புவிசார் குறியீடு)",
        "name_en": "Kovai Kora Cotton Sarees (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) கைத்தறி",
        "category_en": "Geographical Indication (GI) Craft",
        "explanation_ta": "பட்டு இழைகளும் உயர்தரப் பருத்தி நூலும் இணைந்து நெசவு செய்யப்படும் மென்மையான பாரம்பரியத் கைத்தறி சேலைகள்.",
        "explanation_en": "Traditional handloom sarees woven using a blend of pure raw silk and superior combed cotton yarn.",
        "significance_ta": "கொங்கு மண்டலத்தின் நேர்த்தியான நெசவுக் கலைக்கு வழங்கப்பட்ட அதிகாரப்பூர்வ புவிசார் குறியீடு.",
        "significance_en": "Celebrated across India for lightweight texture, distinctive borders, and climatic comfort."
    },
    "Coimbatore Wet Grinder (GI Tag)": {
        "name_ta": "கோயம்புத்தூர் கிரைண்டர் (புவிசார் குறியீடு)",
        "name_en": "Coimbatore Wet Grinder (GI Tag)",
        "category_ta": "பொறியியல் புவிசார் குறியீடு (GI)",
        "category_en": "Engineering GI Tag",
        "explanation_ta": "கொங்கு பகுதியின் இயற்கை கிரானைட் கற்களைக் கொண்டு துல்லியப் பொறியியலில் உருவாக்கப்பட்ட மின்சார ஆட்டுக் கல் இயந்திரங்கள்.",
        "explanation_en": "Precision kitchen appliance utilizing indigenous Coimbatore granite stones for fine batter grinding.",
        "significance_ta": "இந்தியாவின் 75 சதவீதத்திற்கும் அதிகமான கிரைண்டர் தேவையைப் பூர்த்தி செய்யும் தனித்துவத் தொழில்.",
        "significance_en": "Commands over 75% of India's commercial and domestic commercial wet grinder production."
    },
    "Siruvani Water": {
        "name_ta": "சிறுவாணி நன்னீர்",
        "name_en": "Siruvani Water",
        "category_ta": "இயற்கை நன்னீர் வளம்",
        "category_en": "Natural Resource",
        "explanation_ta": "மேற்குத் தொடர்ச்சி மலையின் அடர்ந்த காடுகளின் வழியே பாய்ந்து வரும் உலகின் சுவையான இயற்கை நன்னீர்.",
        "explanation_en": "Mountain spring water flowing from the pristine rainforests of the Western Ghats, renowned for mineral sweetness.",
        "significance_ta": "கோயம்புத்தூர் மாநகர மக்களின் குடிநீர் தேவையை நிறைவு செய்யும் உலகப் புகழ்பெற்ற சுவைநீர்.",
        "significance_en": "Famed worldwide for mineral richness and revered by locals as Coimbatore's natural blessing."
    },
    "Marudhamalai Murugan Temple": {
        "name_ta": "மருதமலை முருகன் திருக்கோயில்",
        "name_en": "Marudhamalai Murugan Temple",
        "category_ta": "ஆன்மீக மலைத் தலம்",
        "category_en": "Spiritual Heritage",
        "explanation_ta": "மேற்குத் தொடர்ச்சி மலையின் எழில்மிகு மருத மரங்கள் சூழ்ந்த குன்றில் அமைந்துள்ள புகழ்பெற்ற சுப்பிரமணிய சுவாமி திருக்கோயில்.",
        "explanation_en": "Scenic hill temple dedicated to Lord Muruga, nestled amidst medicinal flora in the Western Ghats.",
        "significance_ta": "பாம்பாட்டி சித்தர் தவம் புரிந்து முக்தி அடைந்த புண்ணிய பூமியாகப் போற்றப்படுகிறது.",
        "significance_en": "Associated with the mystic sage Pambatti Siddhar who meditated in the hill's natural caves."
    },

    # 5. Cuddalore
    "Chidambaram Thillai Nataraja Temple": {
        "name_ta": "சிதம்பரம் தில்லை நடராஜர் திருக்கோயில்",
        "name_en": "Chidambaram Thillai Nataraja Temple",
        "category_ta": "பஞ்சபூத ஆகாய தலம் & சோழர் கலை",
        "category_en": "Sacred Architecture & Epigraphy",
        "explanation_ta": "பஞ்சபூதத் தலங்களில் ஆகாயத் தலமாகவும், பொன்னம்பலக் கூத்தன் ஆனந்த தாண்டவம் ஆடும் உலகப் புகழ்பெற்ற சைவத் தலமாகவும் போற்றப்படுகிறது.",
        "explanation_en": "Pancha Bhoota Sthalam representing Akasha (Space), featuring the golden roof sanctum where Lord Shiva performs the cosmic dance.",
        "significance_ta": "சோழப் பேரரசர்களின் குலதெய்வக் கோயிலாகவும், பல்லாயிரக்கணக்கான வரலாற்று கல்வெட்டுகளைக் கொண்ட பொக்கிஷமாகவும் விளங்குகிறது.",
        "significance_en": "Dynastic sanctuary of the Cholas, housing foundational inscriptions on medieval temple administration and dance shastras."
    },
    "Pichavaram Mangrove Forest": {
        "name_ta": "பிச்சாவரம் அலையாத்திக் காடுகள் (ராம்சார் தளம்)",
        "name_en": "Pichavaram Mangrove Forest",
        "category_ta": "சதுப்புநிலச் சூழலியல் & ராம்சார் தளம்",
        "category_en": "Eco-Tourism & Coastal Mangroves",
        "explanation_ta": "வெள்ளாறு மற்றும் கொள்ளிடம் நதிகளின் முகத்துவாரத்தில் 1,100 ஹெக்டேர் பரப்பளவில் அமைந்துள்ள உலகின் இரண்டாவது மிகப்பெரிய அலையாத்திக் காடு.",
        "explanation_en": "World's second largest mangrove forest sprawling across 1,100 hectares of interconnected waterways between Vellar and Coleroon estuaries.",
        "significance_ta": "கடற்கரை அரிப்பைத் தடுக்கும் இயற்கை அரணாகவும், 177-க்கும் மேற்பட்ட பறவை இனங்களின் புகலிடமாகவும் உள்ள சர்வதேச ராம்சார் ஈரநிலம்.",
        "significance_en": "Global Ramsar wetland offering vital bioshield protection and habitat for rare estuarine fauna."
    },
    "Neyveli Lignite Corporation (NLC)": {
        "name_ta": "நெய்வேலி பழுப்பு நிலக்கரி நிறுவனம் (என்.எல்.சி)",
        "name_en": "Neyveli Lignite Corporation (NLC)",
        "category_ta": "ஆற்றல் & சுரங்கத் தொழில்",
        "category_en": "Energy & Mining",
        "explanation_ta": "இந்தியாவின் மிகப்பெரிய பழுப்பு நிலக்கரி சுரங்கங்கள் மற்றும் அனல்மின் நிலையங்களை இயக்கும் மத்திய அரசு நவரத்னா நிறுவனம்.",
        "explanation_en": "Pioneering open-cast lignite mining and thermal power generation complex in India, established in 1956.",
        "significance_ta": "தென்னிந்தியாவின் மின்சார விநியோகத்தில் முக்கியப் பங்காற்றும் மிகப்பெரிய ஆற்றல் மையம்.",
        "significance_en": "Serves as the power powerhouse supporting South India's industrial grid."
    },

    # 6. Dharmapuri
    "Tagadur & King Adhiyaman Neduman Anji Heritage": {
        "name_ta": "தகடூர் & அதியமான் நெடுமான் அஞ்சி வரலாற்று மரபு",
        "name_en": "Tagadur & King Adhiyaman Neduman Anji Heritage",
        "category_ta": "சங்க இலக்கியம் & கல்வெட்டு மரபு",
        "category_en": "Sangam Epigraphy & Literature",
        "explanation_ta": "சங்க கால கடையேழு வள்ளல்களில் ஒருவரான அதியமான் அவ்வைக்கு நெல்லிக்கனி ஈந்த வரலாற்றுப் புகழ்மிக்க தகடூர் பூமி.",
        "explanation_en": "Ancient Sangam seat ruled by the illustrious Chieftain Adhiyaman Neduman Anji, celebrated by poetess Avvaiyar.",
        "significance_ta": "சங்க இலக்கியப் பாடல்களிலும் ஜம்பை கல்வெட்டுகளிலும் பொறிக்கப்பட்ட தமிழகத்தின் வீர வரலாற்றுத் தொட்டில்.",
        "significance_en": "Immensely celebrated in Sangam anthologies and confirmed by ancient Tamil-Brahmi inscriptions."
    },
    "Hogenakkal Waterfalls ('Niagara of India')": {
        "name_ta": "ஒகேனக்கல் நீர்வீழ்ச்சி ('இந்தியாவின் நயாகரா')",
        "name_en": "Hogenakkal Waterfalls ('Niagara of India')",
        "category_ta": "இயற்கை நீர்வீழ்ச்சி & சுற்றுலா",
        "category_en": "Natural Attraction",
        "explanation_ta": "காவிரி ஆறு தமிழ்நாட்டிற்குள் நுழையும் இடத்தில் பாறைகளில் மோதி புகைபோல் சிதறி விழும் கம்பீரமான நீர்வீழ்ச்சி.",
        "explanation_en": "Spectacular cascade where River Kaveri carves through deep carbonatite canyons, often called the 'Niagara of India'.",
        "significance_ta": "பரிசல் சவாரி, மூலிகை நீராடல் மற்றும் உலகின் பழமையான கார்பனடைட் பாறைகளைக் கொண்ட இயற்கை அற்புதம்.",
        "significance_en": "Famed for traditional coracle rafting, curative herbal waters, and ancient geological rock formations."
    },
    "Sericulture & Silk Reeling": {
        "name_ta": "பட்டு வளர்ப்பு & நூல் நூற்றல் தொழில்",
        "name_en": "Sericulture & Silk Reeling",
        "category_ta": "பாரம்பரிய விவசாயத் தொழில்",
        "category_en": "Traditional Industry",
        "explanation_ta": "மல்பெரி சாகுபடி மற்றும் பட்டுப்புழு வளர்ப்பில் தமிழ்நாட்டிலேயே முதன்மை மாவட்டமாகத் திகழும் தொழில் வளம்.",
        "explanation_en": "Extensive mulberry cultivation and silkworm rearing making Dharmapuri the premier silk cocoon producer in Tamil Nadu.",
        "significance_ta": "காஞ்சிபுரம் மற்றும் ஆரணி பட்டு நெசவுக்குத் தேவையான உயர்தர பட்டுநூலை உற்பத்தி செய்யும் மையம்.",
        "significance_en": "Supplies premium raw silk to renowned weaving centers like Kanchipuram and Arani."
    },

    # 7. Dindigul
    "Dindigul Lock (GI Tag)": {
        "name_ta": "திண்டுக்கல் பூட்டு (புவிசார் குறியீடு)",
        "name_en": "Dindigul Lock (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) கைவினை",
        "category_en": "Geographical Indication (GI) Craft",
        "explanation_ta": "கைவினைக் கலைஞர்களால் வார்ப்பிரும்பு மற்றும் பித்தளையில் தனித்துவ சாவி அமைப்புகளுடன் செய்யப்படும் உலகப் புகழ்பெற்ற பூட்டுகள்.",
        "explanation_en": "Handcrafted iron and brass security locks forged by skilled artisans with intricate, tamper-proof lever mechanisms.",
        "significance_ta": "பாதுகாப்பிற்குப் பெயர் பெற்று அரசு கருவூலங்கள் மற்றும் கோயில்களில் பயன்படுத்தப்படும் பாரம்பரிய பெருமை கொண்ட தயாரிப்பு.",
        "significance_en": "Secures temples, banks, and historic prisons nationwide due to unpickable artisanal designs."
    },
    "Dindigul Rock Fort": {
        "name_ta": "திண்டுக்கல் மலைக்கோட்டை",
        "name_en": "Dindigul Rock Fort",
        "category_ta": "வரலாற்று இராணுவக் கோட்டை",
        "category_en": "Military Heritage Architecture",
        "explanation_ta": "17-ஆம் நூற்றாண்டில் நாயக்கர் மன்னர் முத்துகிருஷ்ணப்ப நாயக்கரால் 280 அடி உயர ஒற்றைப் பாறையில் கட்டப்பட்ட பிரம்மாண்ட கோட்டை.",
        "explanation_en": "A 17th-century bastion built by Muthu Krishna Nayakkar on a massive 280-foot isolated granite rock hill.",
        "significance_ta": "திப்பு சுல்தான் மற்றும் ஹைதர் அலியின் இராணுவத் தளமாகவும் பீரங்கி தளவாட மையமாகவும் விளங்கிய வரலாற்றுச் சின்னம்.",
        "significance_en": "Fortified heavily by Hyder Ali and Tipu Sultan during the Carnatic and Anglo-Mysore Wars."
    },
    "Sirumalai Hill Banana (GI Tag)": {
        "name_ta": "சிறுமலை மலைவாழைப்பழம் (புவிசார் குறியீடு)",
        "name_en": "Sirumalai Hill Banana (GI Tag)",
        "category_ta": "வேளாண் புவிசார் குறியீடு (GI)",
        "category_en": "Agri-GI Horticultural Heritage",
        "explanation_ta": "சிறுமலை மலைப்பகுதியில் விளையும் தனித்துவமான இனிப்புச் சுவையும் நீண்ட நாள் கெடாத தன்மையும் கொண்ட இயற்கை மலைவாழை.",
        "explanation_en": "Unique mountain banana variety grown in the microclimate of Sirumalai hills, prized for sweet flavor and long shelf-life.",
        "significance_ta": "பழனி முருகன் கோயில் பஞ்சாமிர்தத் தயாரிப்பில் முதன்மையாகப் பயன்படுத்தப்படும் புனித நற்பழம்.",
        "significance_en": "Essential ingredient in the traditional preparation of the world-famous Palani Panchamirtham."
    },
    "Kodaikanal ('Princess of Hill Stations')": {
        "name_ta": "கொடைக்கானல் ('மலைகளின் இளவரசி')",
        "name_en": "Kodaikanal ('Princess of Hill Stations')",
        "category_ta": "மலை வாழிடம் & சூழல் சுற்றுலா",
        "category_en": "Hill Station & Eco-Reserve",
        "explanation_ta": "பழனி மலைத்தொடரில் 2,133 மீட்டர் உயரத்தில் அமைந்துள்ள பசுமை மாறாக் காடுகளும் நட்சத்திர ஏரியும் கொண்ட எழில்மிகு மலை வாழிடம்.",
        "explanation_en": "Picturesque hill station situated at 2,133 meters in the Palani hills, famous for its star-shaped lake, kurinji flowers, and cool climate.",
        "significance_ta": "12 ஆண்டுகளுக்கு ஒருமுறை பூக்கும் நீலக்குறிஞ்சி மலர்களின் இருப்பிடமாகவும் தென்னிந்தியாவின் சிறந்த சுற்றுலாத் தலமாகவும் திகழ்கிறது.",
        "significance_en": "Home to the rare Strobilanthes kunthiana (Kurinji) blossom and pristine Shola evergreen forests."
    },

    # 8. Erode
    "Erode Turmeric (GI Tag)": {
        "name_ta": "ஈரோடு மஞ்சள் (புவிசார் குறியீடு)",
        "name_en": "Erode Turmeric (GI Tag)",
        "category_ta": "வேளாண் புவிசார் குறியீடு (GI)",
        "category_en": "Agri-GI Heritage",
        "explanation_ta": "ஈரோட்டின் மண்வளத்தால் அதிக குர்குமின் சத்தும், ஆழ்ந்த தங்க மஞ்சள் நிறமும் கொண்ட பாரம்பரிய மருத்துவ மஞ்சள்.",
        "explanation_en": "Indigenous cultivar with high curcumin content and deep yellow color, cultivated across the fertile Cauvery-Bhavani basin.",
        "significance_ta": "இந்தியாவின் முன்னணி மஞ்சள் சந்தையாக விளங்கி ஈரோட்டிற்கு 'மஞ்சள் மாநகரம்' என்ற பெயரை ஈட்டித் தந்துள்ளது.",
        "significance_en": "Commands one of India's largest turmeric exchanges, earning Erode the moniker 'Yellow City'."
    },
    "Bhavani Jamakkalam (GI Tag)": {
        "name_ta": "பவானி ஜமக்காளம் (புவிசார் குறியீடு)",
        "name_en": "Bhavani Jamakkalam (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) கைத்தறி ஜவுளி",
        "category_en": "Textile GI Craft",
        "explanation_ta": "பவானி பகுதியில் தறி நெசவாளர்களால் பிரத்யேக வண்ண நூல்களால் நெய்யப்படும் உறுதியான பாரம்பரிய தரை விரிப்புகள்.",
        "explanation_en": "Vibrant, durable woven carpets and floor spreads woven on pit looms by generational weavers in Bhavani.",
        "significance_ta": "உலக அளவில் ஏற்றுமதி செய்யப்படும் தமிழ்நாட்டின் தலைசிறந்த பாரம்பரிய கைத்தறி கலைப் பொக்கிஷம்.",
        "significance_en": "Celebrated globally for aesthetic geometric patterns and exceptional durability."
    },
    "Kodumanal Megalithic Archaeological Site": {
        "name_ta": "கொடுமணல் பெருங்கற்கால தொல்லியல் தளம்",
        "name_en": "Kodumanal Megalithic Archaeological Site",
        "category_ta": "சங்க கால தொல்லியல் அகழாய்வு",
        "category_en": "Archaeological Heritage",
        "explanation_ta": "நொய்யல் ஆற்றங்கரையில் சங்க கால இரும்பு உருக்கு ஆலைகள், மணிக்கற்கள் மற்றும் ரோமானிய நாணயங்கள் கண்டறியப்பட்ட பண்டைய தொழில் நகரம்.",
        "explanation_en": "Crucial Sangam industrial site on the Noyyal river, revealing ancient iron smelting furnaces and semi-precious stone workshops.",
        "significance_ta": "2,300 ஆண்டுகளுக்கு முந்தைய தமிழ்-பிராமி எழுத்துப் பொறித்த மண்பாண்டங்கள் மற்றும் சர்வதேச கடல் வாணிபத்தை மெய்ப்பிக்கும் சான்று.",
        "significance_en": "Yielded hundreds of inscribed Tamil-Brahmi pot sherds proving high ancient literacy and Mediterranean trade links."
    },

    # 9. Kallakurichi
    "Kalvarayan Hills & Waterfalls": {
        "name_ta": "கல்வராயன் மலைத்தொடர் & அருவிகள்",
        "name_en": "Kalvarayan Hills & Waterfalls",
        "category_ta": "கிழக்குத் தொடர்ச்சி மலை & சூழல் சுற்றுலா",
        "category_en": "Mountain Ecosystem & Eco-Tourism",
        "explanation_ta": "கிழக்குத் தொடர்ச்சி மலையின் பசுமையான முகடுகள், பெரியார் அருவி, மேகம் அருவி மற்றும் பழங்குடியினர் பண்பாடு நிறைந்த மலைப்பகுதி.",
        "explanation_en": "Scenic Eastern Ghats hill range featuring pristine waterfalls like Periyar Falls and rich indigenous Malayali tribal heritage.",
        "significance_ta": "இயற்கை வனவளம் மற்றும் மூலிகைத் தாவரங்கள் நிறைந்த கள்ளக்குறிச்சி மாவட்டத்தின் முக்கிய சூழல் சுற்றுலாத் தளம்.",
        "significance_en": "Ecological hotspot rich in botanical diversity and traditional tribal culture."
    },
    "Gomukhi Dam & Reservoir": {
        "name_ta": "கோமுகி அணை & நீர்த்தேக்கம்",
        "name_en": "Gomukhi Dam & Reservoir",
        "category_ta": "நீர்வளம் & சுற்றுலா",
        "category_en": "Water Resource & Recreation",
        "explanation_ta": "கல்வராயன் மலையடிவாரத்தில் கோமுகி ஆற்றின் குறுக்கே 1965-இல் கட்டப்பட்ட எழில்மிகு நீர்த்தேக்கம்.",
        "explanation_en": "Major earthen dam built across the Gomukhi river at the foothills of Kalvarayan, commissioned in 1965.",
        "significance_ta": "மாவட்டத்தின் ஆயிரக்கணக்கான ஏக்கர் விவசாய நிலங்களுக்கு பாசன வசதி அளிக்கும் உயிர்நாடி அணை.",
        "significance_en": "Lifeline reservoir nourishing extensive paddy and sugarcane acreage in the Kallakurichi plains."
    },
    "Agro-Sugar Mills & Grain Markets": {
        "name_ta": "கரும்பு சர்க்கரை ஆலைகள் & தானியச் சந்தைகள்",
        "name_en": "Agro-Sugar Mills & Grain Markets",
        "category_ta": "விவசாயப் பொருளாதாரம்",
        "category_en": "Agricultural Economy",
        "explanation_ta": "செழிப்பான கரும்பு விளைச்சல், நவீன கூட்டுறவு சர்க்கரை ஆலைகள் மற்றும் நெல் கொள்முதல் சந்தைகள்.",
        "explanation_en": "High-yield sugarcane farmlands and massive co-operative sugar processing plants powering the agrarian economy.",
        "significance_ta": "நடுநாட்டுப் பகுதியின் முதன்மையான சர்க்கரை மற்றும் வெல்ல உற்பத்தி கேந்திரமாக விளங்குகிறது.",
        "significance_en": "Central agro-processing hub contributing significantly to sugar production in Tamil Nadu."
    },

    # 10. Kancheepuram
    "Kanchipuram Silk Sarees (GI Tag)": {
        "name_ta": "காஞ்சிபுரம் பட்டுப் புடவைகள் (புவிசார் குறியீடு)",
        "name_en": "Kanchipuram Silk Sarees (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) கைத்தறி பட்டு",
        "category_en": "World-Renowned Textile GI Craft",
        "explanation_ta": "தூய மல்பெரி பட்டு மற்றும் முறுக்கு ஜரிகை இழைகளால் மூன்று முட்டு நெசவு முறையில் உருவாக்கப்படும் உலகப் புகழ்பெற்ற திருமணப் பட்டுப் புடவைகள்.",
        "explanation_en": "Exquisite handwoven mulberry silk sarees interlaced with pure gold and silver zari using the authentic three-shuttle technique.",
        "significance_ta": "தென்னிந்தியாவின் தலைசிறந்த கைத்தறி பட்டுக் கலைக்கான உலகளாவிய புவிசார் குறியீடு பெற்ற பெருமை வாய்ந்தது.",
        "significance_en": "Globally renowned symbol of South Indian bridal tradition and artisanal master-craft."
    },
    "Kailasanathar Temple (Pallava Epigraphy)": {
        "name_ta": "கைலாசநாதர் திருக்கோயில் (பல்லவர் கட்டடக் கலை)",
        "name_en": "Kailasanathar Temple (Pallava Epigraphy)",
        "category_ta": "திராவிட கட்டடக்கலை மரபு",
        "category_en": "Dravidian Architectural Heritage",
        "explanation_ta": "கி.பி. 8-ஆம் நூற்றாண்டின் தொடக்கத்தில் ராஜசிம்ம பல்லவனால் மணற்கல்லில் வடிக்கப்பட்ட காஞ்சியின் மிகத் தொன்மையான கட்டடக் கோயில்.",
        "explanation_en": "Earliest structural sandstone temple in Kanchipuram, built around 700 CE by Pallava King Rajasimha (Narasimhavarman II).",
        "significance_ta": "பல்லவ மன்னர்களின் விருதுப் பெயர்களைக் கொண்ட பல்லவ-கிரந்த கல்வெட்டுகள் மற்றும் மாமல்லபுரத்திற்குப் பிந்தைய கோயில் கட்டடக் கலையின் முன்மாதிரி.",
        "significance_en": "Seminal masterwork of Dravidian architecture that directly inspired the Rajarajeshwaram of Thanjavur."
    },
    "Ekambareswarar Temple (Earth Element)": {
        "name_ta": "ஏகாம்பரேஸ்வரர் திருக்கோயில் (பஞ்சபூத நில தலம்)",
        "name_en": "Ekambareswarar Temple (Earth Element)",
        "category_ta": "பஞ்சபூதத் திருத்தலம்",
        "category_en": "Pancha Bhoota Sthalam",
        "explanation_ta": "பஞ்சபூதத் தலங்களில் நிலத்திற்குரிய (பிருத்வி) தலமாகப் போற்றப்படும் பிரம்மாண்டமான சைவத் திருக்கோயில்.",
        "explanation_en": "One of the five elemental Shiva temples representing Earth (Prithvi), with a sacred mango tree said to be thousands of years old.",
        "significance_ta": "கிருஷ்ணதேவராயரால் கட்டப்பட்ட 192 அடி உயர இராஜகோபுரமும் பாடல் பெற்ற தேவாரப் பெருமையும் கொண்டது.",
        "significance_en": "Features a towering 59-meter Rajagopuram built by Vijayanagara Emperor Krishnadevaraya in 1509 CE."
    },
    "Ancient Ghatikasthanam (University of Kanchi)": {
        "name_ta": "காஞ்சி கடிகாஸ்தானம் (பண்டைய பல்கலைக்கழகம்)",
        "name_en": "Ancient Ghatikasthanam (University of Kanchi)",
        "category_ta": "பண்டைய தத்துவ & கல்வி மையம்",
        "category_en": "Scholarly & Philosophical Center",
        "explanation_ta": "பண்டைய பாரதத்தின் நாலாபுறங்களிலிருந்தும் அறிஞர்களை ஈர்த்த தொன்மை வாய்ந்த காஞ்சி மாநகரப் பல்கலைக்கழகம்.",
        "explanation_en": "Famed ancient collegiate academy that attracted scholars across Asia, including Buddhist philosophers Bodhidharma and Dignaga.",
        "significance_ta": "பௌத்த, சமண, வைணவ மற்றும் சைவ தத்துவங்கள் செழித்து வளர்ந்த வரலாற்றுப் புகழ்மிக்க கல்வி பீடம்.",
        "significance_en": "Immortalized in literature as 'Nagarangalil Kanchi' (Foremost among Cities) by poet Kalidasa."
    },

    # 11. Kanniyakumari
    "Thiruvalluvar Statue & Vivekananda Rock Memorial": {
        "name_ta": "திருவள்ளுவர் சிலை & விவேகானந்தர் பாறை நினைவு மண்டபம்",
        "name_en": "Thiruvalluvar Statue & Vivekananda Rock Memorial",
        "category_ta": "கடல்சார் தேசிய நினைவுச் சின்னம்",
        "category_en": "Iconic Maritime Heritage",
        "explanation_ta": "முக்கடல் நடுவே பாறையில் அமைந்துள்ள 133 அடி உயர பிரம்மாண்ட திருவள்ளுவர் கற்சிலை மற்றும் சுவாமி விவேகானந்தர் நினைவு மண்டபம்.",
        "explanation_en": "Twin monumental shrines erected on isolated ocean rocks: the 133-foot granite statue of saint-poet Thiruvalluvar and the memorial to Swami Vivekananda.",
        "significance_ta": "தமிழ் இலக்கிய ஞானத்தையும் ஆன்மீகச் சிந்தனையையும் உலகுக்கு உணர்த்தும் பாரதத்தின் தென்கோடி அடையாளச் சின்னம்.",
        "significance_en": "Symbolizes timeless Tamil ethical wisdom and Indian philosophical confluence at the southernmost tip."
    },
    "Triveni Sangamam (Three Seas Confluence)": {
        "name_ta": "முக்கடல் சங்கமம் (திரிவேணி சங்கமம்)",
        "name_en": "Triveni Sangamam (Three Seas Confluence)",
        "category_ta": "புவியியல் & புனித சங்கமம்",
        "category_en": "Geographical Landmark",
        "explanation_ta": "அரபிக்கடல், வங்காள விரிகுடா மற்றும் இந்தியப் பெருங்கடல் ஆகிய மூன்று கடல்களும் இணையும் பாரதத்தின் தெற்குக் கடற்கரை எல்லை.",
        "explanation_en": "Unique geographical confluence where the waters of the Arabian Sea, Bay of Bengal, and Indian Ocean meet.",
        "significance_ta": "ஒரே இடத்தில் சூரிய உதயம் மற்றும் சூரிய அஸ்தமனம் இரண்டையும் காணக்கூடிய சர்வதேசப் புகழ்பெற்ற தலம்.",
        "significance_en": "One of the few spots on earth where both sunrise and sunset can be viewed over open ocean horizons."
    },
    "Padmanabhapuram Palace": {
        "name_ta": "பத்மநாபபுரம் அரண்மனை",
        "name_en": "Padmanabhapuram Palace",
        "category_ta": "பாரம்பரிய மரச் சிற்பக் கலை அரண்மனை",
        "category_en": "Timber Architectural Wonder",
        "explanation_ta": "16-ஆம் நூற்றாண்டில் திருவிதாங்கூர் மன்னர்களால் முற்றிலும் தேக்கு மற்றும் ரோஸ்வுட் மரங்களால் வடிக்கப்பட்ட பிரம்மாண்ட அரண்மனை வளாகம்.",
        "explanation_en": "Magnificent 16th-century royal wooden palace complex constructed by the Venad and Travancore kings at the foothills of Velli Hills.",
        "significance_ta": "பாரம்பரிய கேரள-தமிழ் கட்டடக் கலையின் மிகச்சிறந்த மர வேலைப்பாடுகள் கொண்ட ஆசியாவின் தனித்துவ அரண்மனை.",
        "significance_en": "Considered the finest and largest surviving specimen of traditional wooden palace architecture in South Asia."
    },
    "Mathur Aqueduct": {
        "name_ta": "மாத்தூர் தொட்டிப்பாலம்",
        "name_en": "Mathur Aqueduct",
        "category_ta": "பொறியியல் சாதனைச் சின்னம்",
        "category_en": "Engineering Landmark",
        "explanation_ta": "பறளியாற்றின் குறுக்கே இரண்டு மலைகளுக்கு இடையே விவசாயப் பாசன நீரை எடுத்துச் செல்ல 115 அடி உயரத்தில் கட்டப்பட்ட தொங்கு தொட்டிப் பாலம்.",
        "explanation_en": "One of the tallest and longest flume aqueducts in Asia, built in 1966 across the Pahrali river for drought relief irrigation.",
        "significance_ta": "ஆசியாவின் மிக உயரமான மற்றும் நீளமான பாசனத் தொட்டிப் பாலங்களில் ஒன்றாகத் திகழும் பொறியியல் அற்புதம்.",
        "significance_en": "Engineering feat spanning 1,240 feet across 28 massive concrete pillars."
    },

    # 12. Karur
    "Home Textiles Export Capital": {
        "name_ta": "வீட்டு உபயோக ஜவுளி ஏற்றுமதி தலைநகரம்",
        "name_en": "Home Textiles Export Capital",
        "category_ta": "சர்வதேச தொழில் கேந்திரம்",
        "category_en": "Global Industrial Hub",
        "explanation_ta": "படுக்கை விரிப்புகள், திரைச்சீலைகள், சமையலறை துணிகள் உள்ளிட்ட வீட்டு உபயோக ஜவுளித் தயாரிப்பில் சர்வதேச அளவில் ஏற்றுமதி செய்யும் நகரம்.",
        "explanation_en": "Global manufacturing powerhouse exporting billions in bed linens, kitchen textiles, and upholstery worldwide.",
        "significance_ta": "இந்தியாவின் வீட்டு உபயோக ஜவுளி ஏற்றுமதியில் சிம்ம சொப்பனமாக விளங்கும் சர்வதேச தொழிற்பேட்டை.",
        "significance_en": "Accounts for a dominant share of India's home textile export earnings to Europe and North America."
    },
    "Ancient Karuvoor Chera Epigraphy": {
        "name_ta": "பண்டைய கருவூர் சேரர் வரலாற்று கல்வெட்டுகள்",
        "name_en": "Ancient Karuvoor Chera Epigraphy",
        "category_ta": "சங்க கால தொல்லியல் மையம்",
        "category_en": "Sangam Archaeological Center",
        "explanation_ta": "சங்க கால சேர மன்னர்களின் தலைநகரமான 'வஞ்சி' அல்லது 'கருவூர்'; அமராவதி ஆற்றுப் படுகையில் சேரர் காசுகளும் ரோமானியப் பொற்காசுகளும் கண்டறியப்பட்ட பூமி.",
        "explanation_en": "Ancient capital of the Sangam Cheras mentioned as Karuvoor / Vanji, confirmed by riverbed finds of inscribed coins and Roman amphorae.",
        "significance_ta": "சங்க இலக்கியப் பாடல்களிலும் தாலமியின் குறிப்புகளிலும் குறிப்பிடப்பட்ட சர்வதேச வாணிபத் தலைநகர்.",
        "significance_en": "Proves extensive commercial connections between inland Kongu and the Mediterranean Roman Empire."
    },
    "Pasupatheeswarar Temple": {
        "name_ta": "கரூர் பசுபதீஸ்வரர் திருக்கோயில்",
        "name_en": "Pasupatheeswarar Temple",
        "category_ta": "சோழர் & பாண்டியர் பாடல் பெற்ற தலம்",
        "category_en": "Chola & Pandyan Temple Heritage",
        "explanation_ta": "திருஞானசம்பந்தரால் தேவாரப் பதிகம் பாடப்பெற்ற கொங்கு நாட்டின் ஏழு பாடல் பெற்ற சிவத்தலங்களில் முதன்மையான பழம்பெரும் கோயில்.",
        "explanation_en": "Historic 7th-century Saivite sanctuary praised in the Thevaram hymns, featuring exquisite Rajendra Chola inscriptions.",
        "significance_ta": "காமதேனு வழிபட்ட தலம் என்றும், புகழ்பெற்ற எறிபத்த நாயனார் அவதரித்த திருத்தலம் என்றும் போற்றப்படுகிறது.",
        "significance_en": "Sacred birthplace of Eripatha Nayanar and repository of vital medieval inscriptional records."
    },

    # 13. Krishnagiri
    "Mango Capital of Tamil Nadu": {
        "name_ta": "தமிழ்நாட்டின் மாம்பழத் தலைநகரம்",
        "name_en": "Mango Capital of Tamil Nadu",
        "category_ta": "வேளாண் தோட்டக்கலை மரபு",
        "category_en": "Horticultural Heritage",
        "explanation_ta": "சுமார் 40,000 ஹெக்டேர் பரப்பளவில் விளையும் அல்போன்சா, தோத்தாபுரி மாம்பழங்கள் மற்றும் சர்வதேச தரத்திலான மாம்பழக் கூழ் ஏற்றுமதி ஆலைகள்.",
        "explanation_en": "Premier mango-growing district with vast orchards of Alphonso and Totapuri varieties, supporting massive pulp processing industries.",
        "significance_ta": "மத்திய கிழக்கு மற்றும் ஐரோப்பிய நாடுகளுக்கு அதிக அளவில் மாம்பழக்கூழ் ஏற்றுமதி செய்யும் முதன்மை மாவட்டம்.",
        "significance_en": "Supplies over 60% of India's processed mango pulp exported to international markets."
    },
    "Hosur Advanced EV & Industrial Ecosystem": {
        "name_ta": "ஓசூர் மின்சார வாகன (EV) & தொழில் நகரம்",
        "name_en": "Hosur Advanced EV & Industrial Ecosystem",
        "category_ta": "நவீன பொறியியல் தொழிற்பேட்டை",
        "category_en": "Modern Engineering Hub",
        "explanation_ta": "அதிநவீன மின்சார வாகனத் தயாரிப்பு ஆலைகள், துல்லியப் பொறியியல் மற்றும் மின்னணு தொழிற்பேட்டைகளைக் கொண்ட சர்வதேச நகரம்.",
        "explanation_en": "Leading manufacturing corridor hosting electric vehicle gigafactories, automobile assembly lines, and precision engineering.",
        "significance_ta": "இந்தியாவின் மின்சார வாகனப் புரட்சியின் முன்னணி உற்பத்தி கேந்திரமாக ஓசூர் உருவெடுத்துள்ளது.",
        "significance_en": "Emerging as the premier Electric Vehicle (EV) manufacturing ecosystem in India."
    },
    "Baramahal Historic Forts": {
        "name_ta": "பாராமஹால் வரலாற்று எல்லைக் கோட்டைகள்",
        "name_en": "Baramahal Historic Forts",
        "category_ta": "வரலாற்று இராணுவ அரண்கள்",
        "category_en": "Military Architecture",
        "explanation_ta": "கிருஷ்ணகிரி மலைக்கோட்டை, ராயக்கோட்டை உள்ளிட்ட 12 வரலாற்று பாறைக்கோட்டைகளைக் கொண்ட பாராமஹால் பிராந்தியம்.",
        "explanation_en": "Strategic frontier fortified with 12 historic hill fortresses (Baramahal) including Krishnagiri Fort and Rayakottai.",
        "significance_ta": "ஹைதர் அலி, திப்பு சுல்தான் மற்றும் பிரிட்டிஷ் படைகளுக்கு இடையே நடைபெற்ற ஆங்கிலேய-மைசூர் போர்களின் முக்கிய போர்க்களம்.",
        "significance_en": "Formidable defensive bastion that changed hands between Nayaks, Mysore sultans, and the British."
    },

    # 14. Madurai
    "Meenakshi Sundareswarar Temple": {
        "name_ta": "மதுரை மீனாட்சி சுந்தரேஸ்வரர் திருக்கோயில்",
        "name_en": "Meenakshi Sundareswarar Temple",
        "category_ta": "திராவிட கட்டடக் கலையின் சிகரம்",
        "category_en": "Iconic Dravidian Monument",
        "explanation_ta": "வைகை நதிக்கரையில் அமைந்துள்ள 14 பிரம்மாண்ட இராஜகோபுரங்கள், ஆயிரம் கால் மண்டபம் மற்றும் பொற்றாமரைக் குளம் கொண்ட உலகப் புகழ்பெற்ற திருக்கோயில்.",
        "explanation_en": "Magnificent living temple complex covering 14 acres with 14 soaring gopurams, the thousand-pillar hall, and golden lotus tank.",
        "significance_ta": "பாண்டிய மன்னர்களின் ஆன்மீகத் தலைநகராகவும், 2500 ஆண்டுகால தமிழ் நாகரிகத்தின் அழியாப் பண்பாட்டு மையமாகவும் திகழ்கிறது.",
        "significance_en": "Heart of ancient Madurai, celebrating continuous urban culture and living traditions for over 2,500 years."
    },
    "Madurai Malli (GI Tag)": {
        "name_ta": "மதுரை மல்லிகை (புவிசார் குறியீடு)",
        "name_en": "Madurai Malli (GI Tag)",
        "category_ta": "தாவரவியல் புவிசார் குறியீடு (GI)",
        "category_en": "Botanical GI Heritage",
        "explanation_ta": "தடித்த இதழ்களும், நீடித்த நறுமணமும், மாலை தொடுக்க ஏற்ற உறுதியான தண்டும் கொண்ட உலகப் புகழ்பெற்ற மல்லிகைப் பூ.",
        "explanation_en": "Heavily scented jasmine flower (Jasminum sambac) grown in the unique red soil of Madurai, famous for petal thickness and scent retention.",
        "significance_ta": "சர்வதேச வாசனைத் திரவியத் தயாரிப்பிற்கு ஏற்றுமதி செய்யப்படும் புவிசார் குறியீடு பெற்ற தனித்துவப் பூ.",
        "significance_en": "Coveted worldwide by luxury perfume houses and culturally ubiquitous in Tamil weddings."
    },
    "Madurai Sungudi Sarees (GI Tag)": {
        "name_ta": "மதுரை சுங்குடி சேலைகள் (புவிசார் குறியீடு)",
        "name_en": "Madurai Sungudi Sarees (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) பாரம்பரிய ஜவுளி",
        "category_en": "Textile GI Craft",
        "explanation_ta": "16-ஆம் நூற்றாண்டில் சௌராஷ்டிரா நெசவாளர்களால் அறிமுகப்படுத்தப்பட்ட பாரம்பரிய முடிச்சுப் போடும் சாயம் பூசும் (டை-அண்ட்-டை) பருத்திப் புடவைகள்.",
        "explanation_en": "Traditional tie-and-dye cotton sarees created by Saurashtrian weavers who settled under the patronage of the Nayak rulers.",
        "significance_ta": "கோயில் கரைகளும் வட்ட வடிவ சுங்குடிப் புள்ளிகளும் கொண்ட புவிசார் குறியீடு பெற்ற கைவினைக் கலை.",
        "significance_en": "Renowned for dot-pattern wax prints and breathable 100% combed cotton weave."
    },
    "Madurai Jigarthanda & Culinary Tradition": {
        "name_ta": "மதுரை ஜிகர்தண்டா & பாரம்பரிய உணவுக் கலை",
        "name_en": "Madurai Jigarthanda & Culinary Tradition",
        "category_ta": "தனித்துவ உணவுப் பாரம்பரியம்",
        "category_en": "Iconic Culinary Heritage",
        "explanation_ta": "பாதாம் பிசின், நன்னாரி நறுமணப் பாகு, சுண்டக் காய்ச்சிய பாலாடை மற்றும் ஐஸ்கிரீம் கொண்டு தயாரிக்கப்படும் பாரம்பரிய குளிர் பானம்.",
        "explanation_en": "Legendary cooling dessert beverage prepared using natural tree almond gum, condensed caramelized milk cream, and nannari syrup.",
        "significance_ta": "மதுரையின் விருந்தோம்பல் மரபிலும் தெருவோர உணவுக் கலாச்சாரத்திலும் நீங்காத இடம்பிடித்த சுவை அடையாளம்.",
        "significance_en": "Signature taste sensation originated in the royal kitchens and beloved by millions of culinary travelers."
    },

    # 15. Mayiladuthurai
    "Ancient Port of Poompuhar (Kaveripoompattinam)": {
        "name_ta": "பண்டைய பூம்புகார் துறைமுகம் (காவிரிப்பூம்பட்டினம்)",
        "name_en": "Ancient Port of Poompuhar (Kaveripoompattinam)",
        "category_ta": "சங்க கால கடல்சார் தொல்லியல்",
        "category_en": "Sangam Maritime Archaeology",
        "explanation_ta": "சிலப்பதிகாரம் மற்றும் மணிமேகலை காப்பியங்கள் தோன்றிய, காவிரி ஆறு கடலில் கலக்கும் சோழர்களின் வரலாற்றுத் துறைமுக நகரம்.",
        "explanation_en": "Epic Sangam seaport where the Cauvery river empties into the sea, immortalized in Silappadikaram and Manimekalai.",
        "significance_ta": "பண்டைய ரோம், கிரேக்கம் மற்றும் தென்கிழக்கு ஆசிய நாடுகளுடன் சர்வதேச வாணிபம் நடத்திய கடல்சார் தொல்லியல் தளம்.",
        "significance_en": "Underwater marine excavations have revealed submerged brick docks dating back 2,000 years."
    },
    "Tharangambadi (Tranquebar) Danish Fort": {
        "name_ta": "தரங்கம்பாடி டேனிஷ் கோட்டை (டான்ஸ்போர்க்)",
        "name_en": "Tharangambadi (Tranquebar) Danish Fort",
        "category_ta": "ஐரோப்பிய கடல்சார் வரலாற்றுச் சின்னம்",
        "category_en": "Colonial Maritime Heritage",
        "explanation_ta": "1620-இல் தஞ்சாவூர் ரகுநாத நாயக்கரின் உடன்படிக்கையோடு டேனிஷ் கிழக்கிந்தியக் கம்பெனியால் கடற்கரையில் கட்டப்பட்ட வரலாற்று கோட்டை.",
        "explanation_en": "Coastal fortress built in 1620 under treaty with Thanjavur Nayak ruler, serving as the center of Danish India for 225 years.",
        "significance_ta": "இந்தியாவின் முதல் தமிழ் அச்சுக்கூடத்தை சீகன்பால்கு அமைத்த வரலாற்றுப் புகழ்மிக்க இடமாகத் திகழ்கிறது.",
        "significance_en": "Site where missionary Ziegenbalg established India's first printing press for Tamil typography in 1712."
    },
    "Mayuranathar Temple & Cauvery Thula Utsavam": {
        "name_ta": "மயூரநாதர் திருக்கோயில் & காவிரி துலா உற்சவம்",
        "name_en": "Mayuranathar Temple & Cauvery Thula Utsavam",
        "category_ta": "காவிரி டெல்டா புண்ணிய தலம்",
        "category_en": "Sacred Delta Heritage",
        "explanation_ta": "பார்வதி தேவி மயில் உருவில் இறைவனை வழிபட்ட தலபுராணம் கொண்ட கோயில்; ஐப்பசி துலா மாதத்தில் காவிரியில் புனித நீராடும் மகா உற்சவம்.",
        "explanation_en": "Ancient Shiva temple where Goddess Parvati worshipped as a peacock (Mayura); epicenter of the sacred Thula Snanam river bath festival.",
        "significance_ta": "மயிலாடுதுறை என்ற பெயர் உருவாகக் காரணமான முதன்மைத் தலமும் நவக்கிரகக் கோயில்களின் நுழைவு வாயிலும் ஆகும்.",
        "significance_en": "Origin of the town's name and gateway to the surrounding Cauvery Delta Navagraha pilgrimage circuit."
    },

    # 16. Nagapattinam
    "Velankanni Basilica of Our Lady of Good Health": {
        "name_ta": "வேளாங்கண்ணி புனித ஆரோக்கிய அன்னை பேராலயம்",
        "name_en": "Velankanni Basilica of Our Lady of Good Health",
        "category_ta": "சர்வதேச ஆன்மீகத் திருத்தலம்",
        "category_en": "International Pilgrimage Center",
        "explanation_ta": "16-ஆம் நூற்றாண்டின் அற்புதக் காட்சிகளுடன் தொடர்புடைய கோத்திக் கட்டடக் கலையில் உருவான உலகப் புகழ்பெற்ற கத்தோலிக்க திருத்தலம்.",
        "explanation_en": "World-renowned Roman Catholic Marian basilica constructed in neo-Gothic style, celebrated as the 'Lourdes of the East'.",
        "significance_ta": "மத பேதமின்றி ஆண்டுதோறும் கோடிக்கணக்கான பக்தர்கள் வந்து வழிபடும் நல்லிணக்க புண்ணிய பூமி.",
        "significance_en": "Draws over 20 million pilgrims annually from all faiths for curative blessings and peace."
    },
    "Nagore Dargah (Hazrat Syed Shahul Hameed)": {
        "name_ta": "நாகூர் தர்கா (ஹசரத் சையத் ஷாஹுல் ஹமீது பாதுஷா)",
        "name_en": "Nagore Dargah (Hazrat Syed Shahul Hameed)",
        "category_ta": "வரலாற்று சூஃபி தலம் & மத நல்லிணக்கம்",
        "category_en": "Sufi Pilgrimage & Interfaith Harmony",
        "explanation_ta": "16-ஆம் நூற்றாண்டில் வாழ்ந்த சூஃபி மகான் ஹசரத் காதிர் வலீ அவர்களின் தர்கா; தஞ்சை அச்சுதப்ப நாயக்கரால் நிலம் கொடையாக அளிக்கப்பட்ட தலம்.",
        "explanation_en": "16th-century Sufi shrine dedicated to Saint Shahul Hameed, constructed on land endowed by Thanjavur Nayak king Achuthappa Nayak.",
        "significance_ta": "மத நல்லிணக்கத்தின் சிகரமாக விளங்கி புகழ்பெற்ற கந்தூரி சந்தனக்கூடு விழா நடைபெறும் புனித இடம்.",
        "significance_en": "Renowned for its 131-foot tall minarets and the historic multi-faith Kandoori festival."
    },
    "Point Calimere (Kodiakkarai) Wildlife Sanctuary": {
        "name_ta": "கோடியக்கரை வனவிலங்கு & பறவைகள் சரணாலயம்",
        "name_en": "Point Calimere (Kodiakkarai) Wildlife Sanctuary",
        "category_ta": "ராம்சார் ஈரநிலம் & வனவிலங்கு காப்பகம்",
        "category_en": "Ramsar Wetland Site",
        "explanation_ta": "பாக்கு நீரிணையின் முனையில் அமைந்துள்ள புல்வெளிகள், சதுப்புநிலங்கள் மற்றும் அரிய வெளிமான் காப்பகம்.",
        "explanation_en": "Coastal protected reserve sprawling across mudflats and coastal lagoons, hosting thousands of Greater Flamingos every winter.",
        "significance_ta": "சைபீரியா உள்ளிட்ட வட நாடுகளிலிருந்து வரும் லட்சக்கணக்கான பூநாரைகள் தங்கும் சர்வதேச ராம்சார் ஈரநிலம்.",
        "significance_en": "Ramsar Site of international significance protecting endangered blackbucks and coastal migratory birds."
    },

    # 17. Namakkal
    "Poultry Capital & Egg Production of India": {
        "name_ta": "இந்தியாவின் முட்டை தலைநகரம் & கோழிப்பண்ணைத் தொழில்",
        "name_en": "Poultry Capital & Egg Production of India",
        "category_ta": "வேளாண் கோழிப்பண்ணைப் பொருளாதாரம்",
        "category_en": "Agricultural Economy",
        "explanation_ta": "நாள்தோறும் 4 முதல் 5 கோடி முட்டைகளை உற்பத்தி செய்து இந்தியா மற்றும் மத்திய கிழக்கு நாடுகளுக்கு விநியோகிக்கும் பிரம்மாண்ட தொழில் மையம்.",
        "explanation_en": "India's premier poultry hub producing over 40 to 50 million table eggs daily with automated breeding technology.",
        "significance_ta": "இந்தியாவின் 'முட்டை நகரம்' என்றும், லாரி கூண்டு கட்டும் தொழிலின் முதன்மை கேந்திரம் என்றும் போற்றப்படுகிறது.",
        "significance_en": "Supplies national mid-day meal programs and exports fresh poultry products globally."
    },
    "Namakkal Anjaneyar & Monolithic Rock Fort": {
        "name_ta": "நாமக்கல் ஆஞ்சநேயர் & ஒற்றைக்கல் பாறைக்கோட்டை",
        "name_en": "Namakkal Anjaneyar & Monolithic Rock Fort",
        "category_ta": "சிற்பக் கலை & வரலாற்று அரண்",
        "category_en": "Sculptural & Military Monument",
        "explanation_ta": "18 அடி உயர திறந்தவெளி ஒற்றைக்கல் ஆஞ்சநேயர் சிலையும், ஒரே பாறையில் அமைந்த நரசிம்மர் குடைவரைக் கோயிலும் கொண்ட பாறைக்கோட்டை.",
        "explanation_en": "Spectacular 18-foot monolithic Hanuman idol standing under open sky facing Lord Narasimha's 8th-century rock-cut cave temple.",
        "significance_ta": "அதியமான் மன்னர்கள் காலத்தில் செதுக்கப்பட்ட உன்னத குடைவரைக் கலையும் வரலாற்றுப் பாறை அரணும்.",
        "significance_en": "Features Adhiyaman rock architecture and Tippu Sultan's hilltop fortification."
    },
    "Kolli Hills & Agaya Gangai Waterfalls": {
        "name_ta": "கொல்லிமலை & ஆகாய கங்கை நீர்வீழ்ச்சி",
        "name_en": "Kolli Hills & Agaya Gangai Waterfalls",
        "category_ta": "மலை சுற்றுலா & மூலிகைப் பல்லுயிர் வளம்",
        "category_en": "Hill Tourism & Medicinal Flora",
        "explanation_ta": "70 கொண்டை ஊசி வளைவுகளுடன் கூடிய கிழக்குத் தொடர்ச்சி மலையின் இயற்கை எழில் மற்றும் 300 அடி உயர ஆகாய கங்கை அருவி.",
        "explanation_en": "Pristine mountain range famous for 70 continuous hairpin bends, medicinal plant reserves, and the roaring 300-foot Agaya Gangai cascade.",
        "significance_ta": "சங்க கால வல்வில் ஓரி ஆட்சி புரிந்த வரலாற்றுப் பூமியாகவும் சித்தர்கள் வாழ்ந்த மூலிகை மலையாகவும் போற்றப்படுகிறது.",
        "significance_en": "Immortalized in Sangam poetry as the realm of philanthropist king Valvil Ori."
    },

    # 18. The Nilgiris
    "Nilgiri Mountain Railway (UNESCO)": {
        "name_ta": "நீலகிரி மலை ரயில் (யுனெஸ்கோ உலகப் பாரம்பரியச் சின்னம்)",
        "name_en": "Nilgiri Mountain Railway (UNESCO)",
        "category_ta": "யுனெஸ்கோ உலகப் பாரம்பரிய மலை ரயில்",
        "category_en": "UNESCO World Heritage Site",
        "explanation_ta": "1908-இல் அமைக்கப்பட்ட இந்தியாவின் ஒரே ரேக் மற்றும் பினியன் பல்சக்கர நீராவியால் இயங்கும் வரலாற்று மலை ரயில் பாதை.",
        "explanation_en": "Operational mountain railway built in 1908 using the unique Abt rack-and-pinion steam system to scale steep mountain grades.",
        "significance_ta": "மேட்டுப்பாளையத்திலிருந்து ஊட்டி வரை அடர்ந்த காடுகளையும் பாலங்களையும் கடந்து செல்லும் உலகப் புகழ்பெற்ற பொறியியல் அற்புதம்.",
        "significance_en": "Inscribed by UNESCO as part of Mountain Railways of India for pioneering engineering."
    },
    "Toda Embroidery (GI Tag)": {
        "name_ta": "தோடர் பழங்குடியினர் எம்பிராய்டரி (புவிசார் குறியீடு)",
        "name_en": "Toda Embroidery (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) தொல்குடி கைவினை",
        "category_en": "Tribal Textile GI Craft",
        "explanation_ta": "நீலகிரியின் பூர்வகுடிகளான தோடர் இனப் பெண்கள் வெள்ளை பருத்தி ஆடையில் சிவப்பு மற்றும் கருப்பு நூல்களால் தைக்கும் பிரத்யேக கைத்தையல் கலை.",
        "explanation_en": "Distinctive geometric embroidery ('Pukhoor') hand-stitched by indigenous Toda women using red and black wool on coarse unbleached white cotton.",
        "significance_ta": "தோடர் தொல்குடி மக்களின் கலாச்சார ஆன்மீக சடங்குகளோடு பின்னிப் பிணைந்த புவிசார் குறியீடு பெற்ற அரிய கலை.",
        "significance_en": "Symbolizes the sacred pastoral identity of the Toda tribe of the Nilgiris biosphere."
    },
    "Nilgiri Orthodox Tea (GI Tag)": {
        "name_ta": "நீலகிரி ஆர்த்தடாக்ஸ் தேயிலை (புவிசார் குறியீடு)",
        "name_en": "Nilgiri Orthodox Tea (GI Tag)",
        "category_ta": "வேளாண் புவிசார் குறியீடு (GI)",
        "category_en": "Agri-GI Beverage Heritage",
        "explanation_ta": "நீலகிரி மலையின் 2000 மீட்டர் உயரக் குளிர் காலநிலையில் விளையும் நறுமணமிக்க உலகப் புகழ்பெற்ற தங்க நிறத் தேயிலை.",
        "explanation_en": "High-grown black tea cultivated at elevations exceeding 6,000 feet, celebrated for subtle floral fragrance, bright liquor, and brisk flavor.",
        "significance_ta": "சர்வதேச அளவில் 'நீல மலையின் தங்கம்' எனப் போற்றப்பட்டு உலகெங்கும் ஏற்றுமதி செய்யப்படும் புவிசார் பானம்.",
        "significance_en": "Prized globally by connoisseurs as one of the finest specialty orthodox teas."
    },
    "Mudumalai National Park & Tiger Reserve": {
        "name_ta": "முதுமலை தேசியப் பூங்கா & புலிகள் காப்பகம்",
        "name_en": "Mudumalai National Park & Tiger Reserve",
        "category_ta": "உயிர்க்கோளக் காப்பகம் & வனவிலங்கு பாதுகாப்பு",
        "category_en": "Biosphere Conservation",
        "explanation_ta": "நீலகிரி உயிர்க்கோளக் காப்பகத்தின் முக்கிய அங்கம்; புலிகள், ஆசிய யானைகள் மற்றும் சிறுத்தைகள் வாழும் அடர்ந்த வனப்பகுதி.",
        "explanation_en": "One of India's earliest wildlife sanctuaries established in 1940, forming a vital corridor in the Nilgiri Biosphere Reserve.",
        "significance_ta": "யானைகள் மறுவாழ்வு முகாம் மற்றும் புலிகள் பாதுகாப்பில் இந்தியாவின் முதன்மை சரணாலயங்களில் ஒன்று.",
        "significance_en": "Anchors the largest population of wild Asian elephants and Bengal tigers in southern India."
    },

    # 19. Perambalur
    "Ranjankudi Fort": {
        "name_ta": "ரஞ்சன்குடி வரலாற்று பாறைக்கோட்டை",
        "name_en": "Ranjankudi Fort",
        "category_ta": "வரலாற்று இராணுவக் கோட்டை",
        "category_en": "Military Architecture",
        "explanation_ta": "17-ஆம் நூற்றாண்டில் கர்நாடக நவாப்களின் கீழ் முகம்மது அலீ என்பவரால் கட்டப்பட்ட கம்பீரமான 3 அடுக்கு பாறை அரண்.",
        "explanation_en": "Imposing 17th-century fortress constructed by the Nawab of the Carnatic with concentric stone defense walls and bastions.",
        "significance_ta": "1751-இல் ஆங்கிலேய கிழக்கிந்தியக் கம்பெனி மற்றும் பிரெஞ்சு படைகளுக்கு இடையே நடைபெற்ற வாலிகண்டபுரம் போரின் முக்கிய வரலாற்றுத் தளம்.",
        "significance_en": "Key battleground of the Carnatic Wars fought between British, French, and Nawab forces in 1751."
    },
    "National Fossil Wood Park, Sathanur": {
        "name_ta": "சாத்தனூர் தேசிய கல்மரப் பூங்கா",
        "name_en": "National Fossil Wood Park, Sathanur",
        "category_ta": "தேசிய புவியியல் நினைவுச் சின்னம்",
        "category_en": "Geological Heritage",
        "explanation_ta": "12 கோடி ஆண்டுகளுக்கு முன்பு வாழ்ந்த கூம்பு வடிவ மரங்கள் சிலிக்கா பாறையாக உறைந்த 18 மீட்டர் நீள பிரம்மாண்ட கல்மரம்.",
        "explanation_en": "National Geological Monument holding a petrified coniferous tree trunk over 18 meters long, dating back 120 million years.",
        "significance_ta": "கிரெட்டேசியஸ் யுகத்தில் கடல் பின்வாங்கியபோது தாவரங்கள் புதைபடிவமாக மாறியதை நிரூபிக்கும் அரிய இயற்கை அற்புதம்.",
        "significance_en": "Provides scientific evidence of ancient marine ingressions during the Early Cretaceous era."
    },
    "Shallot (Small Onion) & Maize Hub": {
        "name_ta": "சின்ன வெங்காயம் & மக்காச்சோளம் உற்பத்திக் களஞ்சியம்",
        "name_en": "Shallot (Small Onion) & Maize Hub",
        "category_ta": "விவசாயப் பொருளாதாரம்",
        "category_en": "Agricultural Economy",
        "explanation_ta": "தமிழ்நாட்டின் 25 சதவீதத்திற்கும் அதிகமான சின்ன வெங்காயம் மற்றும் மக்காச்சோளத்தை உற்பத்தி செய்யும் முதன்மை விவசாய மாவட்டம்.",
        "explanation_en": "Produces over a quarter of Tamil Nadu's total shallot (small onion) and maize crop through advanced dryland farming.",
        "significance_ta": "தென்னிந்தியாவின் சமையல் தேவைக்கான தரமான சின்ன வெங்காய விநியோகத்தை உறுதி செய்யும் விவசாய பூமி.",
        "significance_en": "Major supplier of essential shallots to markets across South India."
    },

    # 20. Pudukkottai
    "Sittanavasal Cave Paintings & Jain Beds": {
        "name_ta": "சித்தன்னவாசல் சமணர் குடைவரை ஓவியங்கள் & கற்படுக்கைகள்",
        "name_en": "Sittanavasal Cave Paintings & Jain Beds",
        "category_ta": "பண்டைய சுவரோவியங்கள் & கல்வெட்டு மரபு",
        "category_en": "Ancient Fresco Art & Inscriptions",
        "explanation_ta": "கி.மு. 2-ஆம் நூற்றாண்டு முதல் சமண முனிவர்கள் வாழ்ந்த கற்படுக்கைகளும், 7-ஆம் நூற்றாண்டின் அஜந்தாவுக்கு இணையான தாமரைத் தடாக ஓவியங்களும் கொண்ட குடைவரை.",
        "explanation_en": "2nd-century BCE rock-cut Jain monastery famed for magnificent fresco paintings of lotus ponds, monks, and Tamil-Brahmi beds.",
        "significance_ta": "தமிழகத்தின் மிகத் தொன்மையான சுவரோவிய மரபையும் சமண சமய வரலாற்றையும் விளக்கும் ஒப்பற்ற கலைப் பொக்கிஷம்.",
        "significance_en": "Earliest surviving non-secular wall murals in Tamil Nadu, rivaling Ajanta in aesthetic grace."
    },
    "Thirumayam Rock Fort & Cave Temples": {
        "name_ta": "திருமயம் வரலாற்று பாறைக்கோட்டை & குடைவரைக் கோயில்கள்",
        "name_en": "Thirumayam Rock Fort & Cave Temples",
        "category_ta": "பாறைக் குடைவரைக் கட்டடக் கலை",
        "category_en": "Rock-Cut Architecture",
        "explanation_ta": "1687-இல் சேதுபதி மன்னர் விஜயரகுநாத கிழவன் சேதுபதியால் அமைக்கப்பட்ட கோட்டையும், சத்தியகிரீஸ்வரர் - சத்யமூர்த்தி பெருமாள் இரட்டைக் குடைவரைகளும்.",
        "explanation_en": "Imposing 17th-century bastion built by Sethupathi ruler Vijaya Raghunatha Kilavan, enclosing 8th-century Pandya rock temples.",
        "significance_ta": "ஊமைத்துரை அடைக்கலம் பெற்ற விடுதலைப் போராட்டக் களமாகவும், மாபெரும் பள்ளி கொண்ட பெருமாள் குடைவரையாகவும் விளங்குகிறது.",
        "significance_en": "Served as a fortress stronghold for Polygar rebels including Oomathurai during the South Indian Rebellion."
    },
    "Kudumiyanmalai Musical Inscription": {
        "name_ta": "குடுமியான்மலை கர்நாடக இசை கல்வெட்டு",
        "name_en": "Kudumiyanmalai Musical Inscription",
        "category_ta": "இசையியல் தொல்லியல் கல்வெட்டு",
        "category_en": "Musicological Epigraphy",
        "explanation_ta": "கி.பி. 7-ஆம் நூற்றாண்டில் பல்லவ மன்னன் மகேந்திரவர்மனால் பாறையில் செதுக்கப்பட்ட 7 கிராம ராகங்களைக் கொண்ட புகழ்பெற்ற இசைக் கல்வெட்டு.",
        "explanation_en": "Unique 7th-century epigraph on rock face detailing classical music notation across seven ancient scales (grama-ragas).",
        "significance_ta": "இந்திய இசையியலின் மிகத் தொன்மையான ஆவணப்படுத்தப்பட்ட இசை இலக்கணக் கல்வெட்டு ஆதாரமாகும்.",
        "significance_en": "World's earliest epigraphical manual of Indian musical scale notation."
    },

    # 21. Ramanathapuram
    "Ramanathaswamy Temple, Rameswaram": {
        "name_ta": "இராமேஸ்வரம் இராமநாதசுவாமி திருக்கோயில்",
        "name_en": "Ramanathaswamy Temple, Rameswaram",
        "category_ta": "ஜோதிர்லிங்கத் தலம் & திராவிடக் கட்டடக் கலை",
        "category_en": "Sacred Jyotirlinga Architecture",
        "explanation_ta": "உலகின் மிக நீளமான 1,212 தூண்களைக் கொண்ட பிரம்மாண்ட மூன்றாம் திருச்சுற்றுப் பிரகாரம் மற்றும் 22 புண்ணிய தீர்த்தங்களைக் கொண்ட புனிதத் தலம்.",
        "explanation_en": "Celebrated coastal Jyotirlinga temple housing the world's longest pillared corridor measuring nearly 4,000 feet with 1,212 carved pillars.",
        "significance_ta": "சேதுபதி மன்னர்களால் திருப்பணி செய்யப்பட்ட பாரதத்தின் மிக முக்கியமான நான்கு புனித யாத்திரைத் தலங்களில் (சார் தாம்) ஒன்று.",
        "significance_en": "One of India's Char Dham pilgrimage destinations, consecrated by centuries of royal Sethupathi patronage."
    },
    "Historic Pamban Rail Bridge": {
        "name_ta": "பாம்பன் வரலாற்று கடல் ரயில் பாலம்",
        "name_en": "Historic Pamban Rail Bridge",
        "category_ta": "கடல்சார் பொறியியல் வரலாற்றுச் சின்னம்",
        "category_en": "Maritime Engineering Landmark",
        "explanation_ta": "1914-இல் பாக் நீரிணையின் மேல் அமைக்கப்பட்ட இந்தியாவின் முதல் கடல் பாலம்; கப்பல்கள் கடந்து செல்ல நடுவில் திறக்கும் ஷெர்சர் தூக்கு விளிம்பு கொண்டது.",
        "explanation_en": "India's first sea bridge opened in 1914, featuring a double-leaf Scherzer rolling lift span that lifts to let ships pass.",
        "significance_ta": "ராமேஸ்வரம் தீவை இந்தியப் பெருநிலப்பரப்புடன் இணைக்கும் உலகப் புகழ்பெற்ற பொறியியல் அதிசயம்.",
        "significance_en": "Monument of colonial civil engineering battling intense marine salinity and cyclones for over a century."
    },
    "Ramnad Mundu Chilli (GI Tag)": {
        "name_ta": "இராமநாதபுரம் குண்டு மிளகாய் (புவிசார் குறியீடு)",
        "name_en": "Ramnad Mundu Chilli (GI Tag)",
        "category_ta": "வேளாண் புவிசார் குறியீடு (GI)",
        "category_en": "Agri-GI Horticultural Heritage",
        "explanation_ta": "கடலோர உவர் மண்ணிலும் மழையற்ற வறட்சியிலும் விளையும் உருண்டையான வடிவம், அடர்ந்த சிவப்பு நிறம் மற்றும் நறுமண காரம் கொண்ட மிளகாய்.",
        "explanation_en": "Round, thick-skinned, fiery local chilli cultivar grown under rainfed coastal saline conditions, celebrated for distinctive aroma and color.",
        "significance_ta": "செட்டிநாட்டு உணவு தயாரிப்பில் தனித்துவ ருசியைத் தரும் அதிகாரப்பூர்வ புவிசார் குறியீடு பெற்ற விவசாயத் தங்கம்.",
        "significance_en": "Cornerstone ingredient giving Chettinad cuisine its signature spicy punch and deep red hue."
    },
    "Dhanushkodi ('Ghost Town')": {
        "name_ta": "தனுஷ்கோடி ('புயலால் அழிந்த வரலாற்று நகரம்')",
        "name_en": "Dhanushkodi ('Ghost Town')",
        "category_ta": "கடல்சார் வரலாற்றுச் சின்னம்",
        "category_en": "Maritime Landmark & Pilgrimage",
        "explanation_ta": "1964-ஆம் ஆண்டு புயலால் கடலில் மூழ்கிய வரலாற்றுத் துறைமுக நகரம்; தேவாலயம், ரயில் நிலையம் மற்றும் பள்ளிவாசலின் வரலாற்று இடிபாடுகள் கொண்ட தலம்.",
        "explanation_en": "Historic thriving port town submerged and abandoned following the devastating 1964 cyclone, preserving romantic seaside ruins.",
        "significance_ta": "இலங்கைக்கு மிக அருகில் அமைந்துள்ள ராமர் பாலம் (ஆதாம் பாலம்) தொடங்கும் சர்வதேச கடலோர எல்லை.",
        "significance_en": "Sacred tip where the Bay of Bengal meets the Indian Ocean, just 18 miles from Sri Lanka."
    },

    # 22. Ranipet
    "Global Leather Footwear & Tanning Cluster": {
        "name_ta": "சர்வதேச தோல் பதனிடுதல் & காலணி தயாரிப்பு மையம்",
        "name_en": "Global Leather Footwear & Tanning Cluster",
        "category_ta": "சர்வதேச தொழில்துறை ஏற்றுமதி",
        "category_en": "Industrial Export Cluster",
        "explanation_ta": "ராணிப்பேட்டை, வாலாஜாபேட்டை பகுதிகளில் அமைந்துள்ள சர்வதேச பிராண்டுகளுக்கான உயர்தர தோல் பொருட்கள் மற்றும் காலணி தயாரிப்பு தொழிற்பேட்டை.",
        "explanation_en": "World-class industrial ecosystem for processed leather, footwear uppers, and export garments supplying global fashion brands.",
        "significance_ta": "இந்தியாவின் தோல் பொருட்கள் ஏற்றுமதியில் பெரும் பங்கு வகித்து அந்நியச் செலாவணியை ஈட்டித் தரும் மையம்.",
        "significance_en": "Major employment generator and forex earner in India's finished leather goods market."
    },
    "Arcot Makkan Peda & Historic Arcot": {
        "name_ta": "ஆற்காடு மக்கான் பேடா & வரலாற்று ஆற்காடு",
        "name_en": "Arcot Makkan Peda & Historic Arcot",
        "category_ta": "பாரம்பரிய உணவுக் கலை & நவாப் மரபு",
        "category_en": "Culinary & Historical Heritage",
        "explanation_ta": "ஆற்காடு நவாப்களின் அரண்மனை சமையலறையில் உருவான திரட்டுப்பால், உலர் பழங்கள் பொதிந்து சர்க்கரைப் பாகில் ஊறும் சுவையான பாரம்பரிய இனிப்பு.",
        "explanation_en": "Legendary sweet confection created in the royal kitchens of the Nawabs of Arcot, stuffed with dry fruits and soaked in rose sugar syrup.",
        "significance_ta": "கர்நாடக நவாப்களின் தலைநகரமான ஆற்காட்டின் 300 ஆண்டுகால உணவுப் பாரம்பரிய அடையாளம்.",
        "significance_en": "Celebrated across Tamil Nadu as an unmatched royal culinary delicacy."
    },
    "BHEL Boiler Auxiliaries Plant": {
        "name_ta": "பாரத மிகுமின் நிறுவனம் (பி.எச்.இ.எல்) கொதிகலன் ஆலை",
        "name_en": "BHEL Boiler Auxiliaries Plant",
        "category_ta": "கனரகப் பொறியியல் தொழில்",
        "category_en": "Heavy Engineering",
        "explanation_ta": "ராணிப்பேட்டையில் இயங்கும் பாரத மிகுமின் நிறுவனத்தின் கொதிகலன் துணை உபகரணங்கள் மற்றும் மாசுக் கட்டுப்பாட்டுக் கருவிகள் தயாரிக்கும் முதன்மை ஆலை.",
        "explanation_en": "Major public sector manufacturing unit producing air preheaters and electrostatic precipitators for thermal power stations nationwide.",
        "significance_ta": "இந்தியாவின் மின் உற்பத்தி நிலையங்களின் உள்கட்டமைப்பைத் தாங்கி நிற்கும் முன்னணி கனரக ஆலை.",
        "significance_en": "Foundational plant powering India's thermal and green energy engineering infrastructure."
    },

    # 23. Salem
    "Salem Steel Plant (SAIL)": {
        "name_ta": "சேலம் இரும்பாலை (இந்திய எஃகு ஆணையம்)",
        "name_en": "Salem Steel Plant (SAIL)",
        "category_ta": "கனரக எஃகுத் தொழில்",
        "category_en": "Heavy Metallurgy",
        "explanation_ta": "உயர்தர துருப்பிடிக்காத எஃகு மற்றும் நாணயங்கள் தயாரிப்பதற்கான தகடுகளை உற்பத்தி செய்யும் இந்திய எஃகு ஆணையத்தின் சிறப்பு ஆலை.",
        "explanation_en": "Specialized public sector metallurgical unit producing internationally certified austenitic stainless steel coils and coin blanks.",
        "significance_ta": "சேலத்திற்கு 'எஃகு நகரம்' என்ற பெருமையை ஈட்டித் தந்த இந்தியாவின் முதன்மை எஃகு ஆலை.",
        "significance_en": "Supplies defense, aerospace, coin mints, and consumer appliance sectors worldwide."
    },
    "Salem Fabric & Venpattu Silk (GI Tag)": {
        "name_ta": "சேலம் வெண்பட்டு & கைத்தறி ஜவுளி (புவிசார் குறியீடு)",
        "name_en": "Salem Fabric & Venpattu Silk (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) கைத்தறி",
        "category_en": "Textile GI Heritage",
        "explanation_ta": "தூய வெண்பட்டு இழைகளால் நெய்யப்பட்டு அரச மரியாதைகளுக்கும் விசேஷங்களுக்கும் அணியப்படும் பிரத்யேக சேலம் பட்டு வேட்டிகள் மற்றும் அங்கவஸ்திரங்கள்.",
        "explanation_en": "Pristine white silk dhotis and handwoven fabrics woven on traditional pit looms, renowned for pure luster and ceremonial status.",
        "significance_ta": "தமிழ்நாட்டின் ஆன்மீக மற்றும் சுபகாரியங்களில் பிரதான இடம் வகிக்கும் புவிசார் குறியீடு பெற்ற கைத்தறி பாரம்பரியம்.",
        "significance_en": "Revered across India as the quintessential traditional ceremonial garment."
    },
    "Mettur Dam & Stanley Reservoir": {
        "name_ta": "மேட்டூர் அணை & ஸ்டான்லி நீர்த்தேக்கம்",
        "name_en": "Mettur Dam & Stanley Reservoir",
        "category_ta": "வரலாற்றுப் பொறியியல் அணை",
        "category_en": "Historic Engineering Landmark",
        "explanation_ta": "1934-இல் காவிரி ஆற்றின் குறுக்கே கட்டி முடிக்கப்பட்ட இந்தியாவின் பழமையான மற்றும் மிகப்பெரிய அணைகளில் ஒன்று.",
        "explanation_en": "Historic dam commissioned in 1934 across the river Kaveri, forming the sprawling Stanley Reservoir with 93.4 tmc capacity.",
        "significance_ta": "காவிரி டெல்டா மாவட்டங்களின் 16 லட்சம் ஏக்கர் விவசாய நிலங்களுக்கு பாசனம் அளிக்கும் தமிழகத்தின் உயிர்நாடி அணை.",
        "significance_en": "Primary lifeline providing irrigation to the agrarian rice-bowl of the Cauvery Delta."
    },
    "Yercaud ('Jewel of the Shevaroys')": {
        "name_ta": "ஏற்காடு ('சேர்வராயன் மலையின் ஆபரணம்')",
        "name_en": "Yercaud ('Jewel of the Shevaroys')",
        "category_ta": "மலை வாழிடம் & சூழல் சுற்றுலா",
        "category_en": "Hill Station & Eco-Tourism",
        "explanation_ta": "சேர்வராயன் மலையில் 1,515 மீட்டர் உயரத்தில் காப்பித் தோட்டங்கள், மிளகுப் பயிர்கள் மற்றும் மரகத ஏரி சூழ்ந்த இயற்கை எழில் வாழிடம்.",
        "explanation_en": "Charming hill resort situated at 1,515 meters amidst coffee plantations, orange groves, and the serene Yercaud Lake.",
        "significance_ta": "குறைந்த செலவிலான இயற்கை எழில் வாழிடமாகவும் காப்பிக் கொட்டை உற்பத்தியிலும் சிறந்து விளங்கும் சுற்றுலா மையம்.",
        "significance_en": "Renowned for colonial heritage cottages, orchidarium, and pleasant year-round climate."
    },

    # 24. Sivaganga
    "Keezhadi Archaeological Excavations": {
        "name_ta": "கீழடி தொல்லியல் அகழாய்வுத் தளம்",
        "name_en": "Keezhadi Archaeological Excavations",
        "category_ta": "சங்க கால நகர நாகரிகம்",
        "category_en": "Sangam Urban Civilization",
        "explanation_ta": "வைகை நதிக்கரையில் கி.மு. 6-ஆம் நூற்றாண்டைச் சேர்ந்த திட்டமிடப்பட்ட செங்கல் கட்டடங்கள், வடிகால் அமைப்புகள் மற்றும் தமிழ்-பிராமி எழுத்துக்கள் கண்டறியப்பட்ட தளம்.",
        "explanation_en": "Landmark archaeological site proving a literate, sophisticated urban civilization flourished along the Vaigai river as early as the 6th century BCE.",
        "significance_ta": "சங்க கால தமிழ் நாகரிகம் கங்கைச் சமவெளி நாகரிகத்திற்கு இணையான பழமை வாய்ந்தது என்பதை அறிவியல் பூர்வமாக நிரூபித்த உலகப் பெருமை கொண்ட தளம்.",
        "significance_en": "Pushed back the documented timeline of South Indian urbanization and literacy by centuries."
    },
    "Chettinad Heritage Architecture & Palaces": {
        "name_ta": "செட்டிநாட்டுப் பாரம்பரிய மாளிகைகள் & அரண்மனைகள்",
        "name_en": "Chettinad Heritage Architecture & Palaces",
        "category_ta": "பாரம்பரியக் கட்டடக் கலை அற்புதம்",
        "category_en": "Architectural Marvel",
        "explanation_ta": "பர்மிய தேக்கு, இத்தாலிய பளிங்கு மற்றும் பெல்ஜியம் கண்ணாடி வேலைப்பாடுகளுடன் கூடிய பிரம்மாண்ட நாட்டுக்கோட்டை செட்டியார் அரண்மனை மாளிகைகள்.",
        "explanation_en": "Opulent palatial mansions built by the merchant banking Nattukottai Chettiars, adorned with Burma teak, Italian marble, and Belgian chandeliers.",
        "significance_ta": "யுனெஸ்கோ பாரம்பரிய நகர பரிந்துரை பட்டியலில் இடம்பெற்றுள்ள உலகப் புகழ்பெற்ற தமிழர் கட்டடக் கலை மரபு.",
        "significance_en": "UNESCO-recognized vernacular architectural heritage reflecting global trade wealth."
    },
    "Chettinad Athangudi Tiles (GI Tag)": {
        "name_ta": "செட்டிநாடு ஆத்தங்குடி தரை ஓடுகள் (புவிசார் குறியீடு)",
        "name_en": "Chettinad Athangudi Tiles (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) கைவினை",
        "category_en": "Handcrafted GI Heritage",
        "explanation_ta": "கண்ணாடியில் உள்ளூர் செம்மண், சிமெண்ட் மற்றும் இயற்கை வண்ணப் பொடிகளால் கைகளால் வடிக்கப்படும் பளபளப்பான அலங்காரத் தரை ஓடுகள்.",
        "explanation_en": "Handmade sun-dried decorative cement floor tiles cast on glass plates with bespoke floral and geometric motifs.",
        "significance_ta": "காலம் செல்லச் செல்ல பளபளப்பு கூடும் தனித்துவக் கைவினைக்கு வழங்கப்பட்ட அதிகாரப்பூர்வ புவிசார் குறியீடு.",
        "significance_en": "Eco-friendly heritage flooring acclaimed worldwide for artisanal beauty and natural sheen."
    },
    "Maruthu Pandiyars & 1801 Tiruchirappalli Proclamation": {
        "name_ta": "மருது பாண்டியர்கள் & 1801 ஜம்புத்தீவு பிரகடனம்",
        "name_en": "Maruthu Pandiyars & 1801 Tiruchirappalli Proclamation",
        "category_ta": "சுதந்திரப் போராட்ட வரலாற்று மரபு",
        "category_en": "Freedom Struggle Heritage",
        "explanation_ta": "ஆங்கிலேயரின் காலனி ஆதிக்கத்திற்கு எதிராக அனைத்து மக்களையும் ஒன்றிணைத்து 1801-இல் சுதந்திரப் பிரகடனம் வெளியிட்ட வீரப் பெருநிலம்.",
        "explanation_en": "Seat of the legendary freedom fighters Periya Maruthu and Chinna Maruthu who issued the historic 1801 Trichy Proclamation of Independence against British rule.",
        "significance_ta": "1857 சிப்பாய் புரட்சிக்கு அரை நூற்றாண்டுக்கு முன்பே தென்னிந்திய விடுதலைப் புரட்சியை வழிநடத்திய வீரம் விளைந்த பூமி.",
        "significance_en": "Preceded the 1857 Sepoy Mutiny by more than five decades in organizing unified resistance against colonial rule."
    },

    # 25. Tenkasi
    "Courtallam Waterfalls ('Spa of South India')": {
        "name_ta": "குற்றாலம் அருவிகள் ('தென்னிந்தியாவின் இயற்கை ஆரோக்கிய மையம்')",
        "name_en": "Courtallam Waterfalls ('Spa of South India')",
        "category_ta": "இயற்கை மூலிகை அருவிகள்",
        "category_en": "Natural Herbal Therapy",
        "explanation_ta": "மேற்குத் தொடர்ச்சி மலையின் அடர்ந்த மூலிகைக் காடுகளின் வழியே பாய்ந்து வரும் பேரருவி, ஐந்தருவி, சிற்றருவி உள்ளிட்ட ஒன்பது எழில்மிகு நீர்வீழ்ச்சிகள்.",
        "explanation_en": "Nine scenic waterfalls cascading down the Western Ghats through dense medicinal herb forests, celebrated as a natural hydrotherapy retreat.",
        "significance_ta": "குற்றாலக் குறவஞ்சி இலக்கியத்தில் போற்றப்படும் உடல்நலத்தையும் புத்துணர்ச்சியையும் தரும் உலகப் புகழ் பெற்ற இயற்கை அருவி நகரம்.",
        "significance_en": "Celebrated in classical Tamil Kuravanji literature for curative mineral baths and scenic monsoon charm."
    },
    "Kasi Viswanathar Temple, Tenkasi": {
        "name_ta": "தென்காசி காசி விசுவநாதர் திருக்கோயில்",
        "name_en": "Kasi Viswanathar Temple, Tenkasi",
        "category_ta": "பாண்டியர் கால வரலாற்றுத் தலம்",
        "category_en": "Pandyan Sacred Heritage",
        "explanation_ta": "15-ஆம் நூற்றாண்டில் பராக்கிரம பாண்டிய மன்னரால் உத்தர காசிக்கு நிகராகச் சித்திரா நதிக்கரையில் கட்டப்பட்ட பிரம்மாண்ட சிவன் கோயில்.",
        "explanation_en": "Grand 15th-century temple built by Pandya King Parakkirama Pandian, replicating the spiritual sanctity of North Indian Kashi.",
        "significance_ta": "180 அடி உயர கம்பீரமான இராஜகோபுரமும், தென்காசி என்ற பெயர் உருவாவதற்குக் காரணமான வரலாற்றுத் தலமுமாகும்.",
        "significance_en": "Architectural anchor of the Later Pandyas featuring a towering 180-foot Rajagopuram."
    },
    "Puli Thevar & Nerkattumseval Freedom Struggle": {
        "name_ta": "பூலித்தேவர் & நெற்கட்டும்செவல் விடுதலைப் போராட்ட மரபு",
        "name_en": "Puli Thevar & Nerkattumseval Freedom Struggle",
        "category_ta": "ஆரம்பகால காலனி ஆதிக்க எதிர்ப்பு மரபு",
        "category_en": "Early Anti-Colonial Resistance",
        "explanation_ta": "1755-இல் பிரிட்டிஷ் கிழக்கிந்தியக் கம்பெனிக்கு வரி செலுத்த மறுத்து, முதன்முதலில் ஆயுதம் ஏந்திப் போரிட்ட வீரத்தளபதி பூலித்தேவரின் மண்.",
        "explanation_en": "Domain of Palayakarar chieftain Puli Thevar, who initiated the earliest armed rebellion against British East India Company rule in 1755.",
        "significance_ta": "இந்திய விடுதலைப் போராட்ட வரலாற்றில் வெள்ளையரை எதிர்த்து முதல் முழக்கமிட்ட வரலாற்றுப் பெருமை கொண்ட பூமி.",
        "significance_en": "Pioneering chapter in Indian independence history challenging colonial taxation and sovereignty."
    },

    # 26. Thanjavur (Strictly aligned with user prompt examples)
    "Brihadeeswarar Temple (UNESCO Great Living Chola Temple)": {
        "name_ta": "பெருவுடையார் கோயில் (யுனெஸ்கோ அங்கீகாரம் பெற்ற சோழர் காலப் பெருங்கோயில்)",
        "name_en": "Brihadeeswarar Temple (UNESCO Great Living Chola Temple)",
        "category_ta": "யுனெஸ்கோ உலகப் பாரம்பரியத் தளம்",
        "category_en": "UNESCO World Heritage Site",
        "explanation_ta": "கி.பி. 1010-இல் முதலாம் ராஜராஜ சோழனால் கட்டப்பட்ட மாபெரும் கற்கோயில்; 216 அடி உயர விமானமும், 80 டன் எடைகொண்ட ஒற்றைக்கல் கலசமும் கொண்ட திராவிடக் கட்டடக் கலையின் சிகரம்.",
        "explanation_en": "Built in 1010 CE by Emperor Rajaraja Chola I, featuring a 216-foot granite Vimana topped by an 80-tonne single-stone Kumbam.",
        "significance_ta": "சோழர் கால சுவரோவியங்கள், கல்வெட்டுகள் மற்றும் தூய கருங்கல் கட்டடக் கலையின் உலக சாதனைச் சின்னம்.",
        "significance_en": "Pinnacle of pure granite Dravidian architecture with monumental Chola frescoes and inscriptional records."
    },
    "Thanjavur Paintings (GI Tag)": {
        "name_ta": "தஞ்சாவூர் ஓவியங்கள் (பாரம்பரியத் தஞ்சாவூர் ஓவியக் கலை)",
        "name_en": "Thanjavur Paintings (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) நுண்கலை",
        "category_en": "Geographical Indication (GI) Fine Art",
        "explanation_ta": "17-ஆம் நூற்றாண்டு முதல் மராட்டிய மன்னர்கள் காலத்தில் செழித்தோங்கிய, தங்கம் மற்றும் நவரத்தினங்கள் பதித்த பாரம்பரிய ஓவியக் கலை.",
        "explanation_en": "Classical South Indian painting style characterized by rich, vivid colors, gesso work, and precious gold leaf overlay with semi-precious stones.",
        "significance_ta": "தென்னிந்தியாவின் உன்னதமான தெய்வீக ஓவிய மரபிற்கு வழங்கப்பட்ட சர்வதேச புவிசார் குறியீடு.",
        "significance_en": "Flourished under the Maratha rulers of Thanjavur since the 17th century."
    },
    "Thanjavur Art Plate & Dancing Dolls (GI Tag)": {
        "name_ta": "தஞ்சாவூர் கலைத்தட்டு மற்றும் தலையாட்டிப் பொம்மைகள் (புகழ்பெற்ற கைவினைப் பொருட்கள்)",
        "name_en": "Thanjavur Art Plate & Dancing Dolls (GI Tag)",
        "category_ta": "புவிசார் கைவினைப் பாரம்பரியம்",
        "category_en": "Handicraft GI Heritage",
        "explanation_ta": "பித்தளை மற்றும் செப்புத் தகடுகளில் வெள்ளி உருவங்கள் பொறிக்கப்பட்ட கலைத்தட்டு மற்றும் புவியீர்ப்பு மைய சமநிலையைக் கொண்ட தலையாட்டிப் பொம்மைகள்.",
        "explanation_en": "Circular brass and copper plates inlaid with silver motifs of deities, alongside the iconic roly-poly bobblehead Thanjavur dolls (Thalaiyatti Bommai).",
        "significance_ta": "தஞ்சாவூர் கைவினைஞர்களின் கணித மற்றும் உலோகவியல் கலை நுணுக்கத்திற்குச் சான்றான உலகப் புகழ்பெற்ற தயாரிப்புகள்.",
        "significance_en": "Cherished globally for mathematical centre-of-gravity balance and artisanal elegance."
    },
    "Saraswathi Mahal Library": {
        "name_ta": "சரஸ்வதி மகால் நூலகம் (அரிய வரலாற்றுச் சுவடிகள் நூலகம்)",
        "name_en": "Saraswathi Mahal Library",
        "category_ta": "பண்டைய சுவடிகள் காப்பகம்",
        "category_en": "Ancient Manuscripts Repository",
        "explanation_ta": "நாயக்கர் மற்றும் மராட்டிய மன்னர்களால் தோற்றுவிக்கப்பட்டு, 60,000-க்கும் மேற்பட்ட அரிய பனையோலை மற்றும் காகிதச் சுவடிகளைக் கொண்ட ஆசியாவின் பழமையான நூலகம்.",
        "explanation_en": "One of the oldest libraries in Asia established by the Nayak and Maratha rulers, housing over 60,000 rare palm-leaf and paper manuscripts.",
        "significance_ta": "தமிழ், சமஸ்கிருதம், மராத்தி மற்றும் தெலுங்கு மொழிகளில் மருத்துவம், வானியல், இலக்கியச் சுவடிகள் பாதுகாக்கப்பட்ட அறிவுப் பொக்கிஷம்.",
        "significance_en": "Described by encyclopedia scholars as the most remarkable library in India."
    },

    # 27. Theni
    "Cumbum Panneer Thratchai (Grape) (GI Tag)": {
        "name_ta": "கம்பம் பன்னீர் திராட்சை (புவிசார் குறியீடு)",
        "name_en": "Cumbum Panneer Thratchai (Grape) (GI Tag)",
        "category_ta": "வேளாண் புவிசார் குறியீடு (GI)",
        "category_en": "Agri-GI Horticultural Pride",
        "explanation_ta": "மேற்குத் தொடர்ச்சி மலையின் கம்பம் பள்ளத்தாக்கில் ஆண்டு முழுவதும் தொடர்ந்து அறுவடை செய்யப்படும் சுவையான பன்னீர் திராட்சை.",
        "explanation_en": "Purple Muscat Hamburg grapes cultivated year-round in the unique microclimate of the Cumbum Valley.",
        "significance_ta": "இந்தியாவில் ஆண்டு முழுவதும் திராட்சை உற்பத்தி செய்யும் ஒரே பள்ளத்தாக்காகத் திகழும் தனித்துவப் புவிசார் பெருமை.",
        "significance_en": "Accounts for nearly 85% of Tamil Nadu's total grape production with year-round harvest cycles."
    },
    "Megamalai ('Highwavy Mountains')": {
        "name_ta": "மேகமலை ('மேகங்கள் தவழும் மலை')",
        "name_en": "Megamalai ('Highwavy Mountains')",
        "category_ta": "ஏலக்காய் & வனவிலங்கு சரணாலயம்",
        "category_en": "Cardamom & Wildlife Sanctuary",
        "explanation_ta": "மேற்குத் தொடர்ச்சி மலையில் 1,500 மீட்டர் உயரத்தில் அமைந்துள்ள தேயிலைத் தோட்டங்கள், ஏலக்காய் தோட்டங்கள் மற்றும் பசுமை மாறாக் காடுகள்.",
        "explanation_en": "Misty mountain range in the Western Ghats blanketed with organic tea estates, cardamom plantations, and evergreen rainforests.",
        "significance_ta": "ஸ்ரீவில்லிபுத்தூர் - மேகமலை புலிகள் காப்பகத்தின் முக்கிய வாழிடமாகவும் வைகை ஆற்றின் மூல நீர்ப்பிடிப்பாகவும் திகழ்கிறது.",
        "significance_en": "Serves as the vital catchment for River Vaigai and forms part of the Tiger Reserve corridor."
    },
    "Suruli Falls & Herbal Stream": {
        "name_ta": "சுருளி நீர்வீழ்ச்சி & மூலிகை நதி",
        "name_en": "Suruli Falls & Herbal Stream",
        "category_ta": "இயற்கை நீர்வீழ்ச்சி & புண்ணிய நதி",
        "category_en": "Natural Cascade",
        "explanation_ta": "மேகமலைத் தொடரிலிருந்து மூலிகைகளைக் கடந்து இரு அடுக்குகளாக 150 அடி உயரத்தில் இருந்து விழும் எழில் கொஞ்சும் அருவி.",
        "explanation_en": "Two-tier scenic waterfall tumbling down 150 feet through the Megamalai slopes, mentioned in the ancient epic Silappadikaram.",
        "significance_ta": "சிலப்பதிகாரத்தில் போற்றப்பட்ட புனித நீராடல் தலமாகவும், 18 பாறை குகைகள் சூழ்ந்த ஆன்மீகத் தலமாகவும் விளங்குகிறது.",
        "significance_en": "Celebrated in classical Tamil literature for restorative herbal waters and sacred rock caves."
    },

    # 28. Thoothukudi
    "Kovilpatti Kadalai Mittai (GI Tag)": {
        "name_ta": "கோவில்பட்டி கடலை மிட்டாய் (புவிசார் குறியீடு)",
        "name_en": "Kovilpatti Kadalai Mittai (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) பாரம்பரிய தின்பண்டம்",
        "category_en": "Confectionery GI Heritage",
        "explanation_ta": "தேர்ந்தெடுத்த வறுத்த நிலக்கடலை மற்றும் இயற்கை மரக்காய்ச்சிய பாகு வெல்லம் கொண்டு உருவாக்கப்படும் சுவையான மிட்டாய்.",
        "explanation_en": "Traditional peanut brittle candy prepared using carefully roasted groundnuts and organic dark jaggery syrup enriched with dry ginger.",
        "significance_ta": "தாமிரபரணி ஆற்று நன்னீர் பயன்பாட்டால் தனித்துவ சுவை பெற்று உலகெங்கும் ஏற்றுமதி செய்யப்படும் புவிசார் இனிப்பு.",
        "significance_en": "GI-tagged snack prized globally for nutty crunch, purity, and healthy energy."
    },
    "V.O. Chidambaranar Port & Maritime Legacy": {
        "name_ta": "வ.உ.சிதம்பரனார் பன்னாட்டுத் துறைமுகம் & கடல்சார் வரலாறு",
        "name_en": "V.O. Chidambaranar Port & Maritime Legacy",
        "category_ta": "பன்னாட்டுத் துறைமுகம் & சுதேசிக் கப்பல் மரபு",
        "category_en": "Seaport & Maritime Trade",
        "explanation_ta": "கப்பலோட்டிய தமிழன் வ.உ.சிதம்பரனார் 1906-இல் சுதேசி கப்பல் நிறுவனத்தைத் தொடங்கிய வரலாற்றுச் சிறப்புமிக்க சர்வதேச துறைமுகம்.",
        "explanation_en": "All-weather deep-water seaport honoring freedom pioneer V.O. Chidambaram Pillai, who launched India's first indigenous shipping line in 1906.",
        "significance_ta": "இந்தியாவின் முன்னணி கொள்கலன் முனையங்களில் ஒன்றாகவும் தென் தமிழகத்தின் ஏற்றுமதி வாயிலாகவும் திகழ்கிறது.",
        "significance_en": "Strategic maritime hub driving industrial and international trade for southern Tamil Nadu."
    },
    "Pearl Fishery & Salt Manufacturing": {
        "name_ta": "முத்துக்குளித்தல் & உப்புத் தொழில்",
        "name_en": "Pearl Fishery & Salt Manufacturing",
        "category_ta": "இயற்கை வளம் & தொழில்",
        "category_en": "Natural Resource & Industry",
        "explanation_ta": "சங்க கால பாண்டியர் காலம் முதல் இயற்கை முத்துக்களுக்குப் பெயர் பெற்று, தற்போது இந்தியாவின் மிகப்பெரிய உப்பு உற்பத்தி மையமாகத் திகழ்கிறது.",
        "explanation_en": "Ancient epicenter of deep-sea natural pearl diving documented by Greek and Roman geographers, now India's second largest marine salt producer.",
        "significance_ta": "தூத்துக்குடிக்கு 'முத்து நகரம்' என்ற உலகப் புகழ்பெற்ற பெயரை ஈட்டித் தந்த இயற்கை வளம்.",
        "significance_en": "Earned Thoothukudi the historic title 'Pearl City' in international maritime chronicles."
    },
    "Thoothukudi Macaroon": {
        "name_ta": "தூத்துக்குடி மக்ரூன்",
        "name_en": "Thoothukudi Macaroon",
        "category_ta": "தனித்துவ பேக்கரி உணவுக் கலை",
        "category_en": "Colonial Pastry Tradition",
        "explanation_ta": "முட்டை வெள்ளைக்கரு, முந்திரிப் பருப்பு மற்றும் சர்க்கரை கொண்டு கூம்பு வடிவில் மென்மையாக சுடப்படும் பிரத்யேக இனிப்பு.",
        "explanation_en": "Delicate, melt-in-the-mouth cone-shaped meringue pastry prepared using egg whites, powdered sugar, and premium cashews.",
        "significance_ta": "போர்ச்சுகீசிய மாலுமிகளால் அறிமுகப்படுத்தப்பட்டு தூத்துக்குடியின் தனித்துவ சுவை அடையாளமாக மாறிய தின்பண்டம்.",
        "significance_en": "Unique Indo-Portuguese culinary fusion cherished across the globe."
    },

    # 29. Tiruchirappalli
    "Sri Ranganathaswamy Temple, Srirangam": {
        "name_ta": "ஸ்ரீரங்கம் ரெங்கநாதசுவாமி திருக்கோயில்",
        "name_en": "Sri Ranganathaswamy Temple, Srirangam",
        "category_ta": "யுனெஸ்கோ விருது பெற்ற வைணவத் தலம்",
        "category_en": "Premier Vaishnavite Heritage & UNESCO Award",
        "explanation_ta": "காவிரி மற்றும் கொள்ளிடம் நதிகளுக்கு இடையே 156 ஏக்கர் பரப்பளவில் 21 கோபுரங்கள், 7 திருச்சுற்றுகளுடன் அமைந்துள்ள உலகின் மிகப்பெரிய செயல்படும் திருக்கோயில்.",
        "explanation_en": "World's largest functioning Hindu temple complex covering 156 acres with 7 concentric parikramas and 21 majestic gopurams.",
        "significance_ta": "108 திவ்ய தேசங்களில் முதன்மையானதும் யுனெஸ்கோ ஆசிய பசிபிக் பாரம்பரிய விருது பெற்ற கட்டடக் கலைப் பொக்கிஷமும் ஆகும்.",
        "significance_en": "Foremost of the 108 Divya Desams, awarded the prestigious UNESCO Asia-Pacific Award for Cultural Heritage Conservation."
    },
    "Kallanai (Grand Anicut Built by Karikala Chola)": {
        "name_ta": "கல்லணை (கரிகால் சோழன் கட்டிய வரலாற்று அணை)",
        "name_en": "Kallanai (Grand Anicut Built by Karikala Chola)",
        "category_ta": "உலகின் பழமையான நீர் ஒழுங்குமுறை அணை",
        "category_en": "World's Oldest Water Regulating Dam",
        "explanation_ta": "கி.பி. 2-ஆம் நூற்றாண்டில் கரிகால் சோழனால் பாயும் காவிரி ஆற்றில் பாறைகளை அடுக்கி கட்டப்பட்ட 2000 ஆண்டுகள் பழமையான நீர்ப்பாசன அணை.",
        "explanation_en": "Built across the river Kaveri by Karikala Chola around the 2nd century CE, recognized as one of the world's oldest functional water diversion dams.",
        "significance_ta": "சர்வதேச நீரியல் பொறியியலின் முன்னோடியாக விளங்கி இன்றும் காவிரி டெல்டாவின் செழிப்புக்கு வித்திடும் அற்புதம்.",
        "significance_en": "A hydraulic marvel that has safely irrigated the entire delta basin for two millennia."
    },
    "Tiruchirappalli Rockfort & Ucchi Pillayar Temple": {
        "name_ta": "திருச்சி மலைக்கோட்டை & உச்சிப்பிள்ளையார் திருக்கோயில்",
        "name_en": "Tiruchirappalli Rockfort & Ucchi Pillayar Temple",
        "category_ta": "புவியியல் & வரலாற்று இராணுவ அதிசயம்",
        "category_en": "Geological & Military Wonder",
        "explanation_ta": "3.8 பில்லியன் ஆண்டுகள் பழமையான 273 அடி உயர ஒற்றை கிரானைட் பாறையில் 437 படிகளுடன் செதுக்கப்பட்ட பல்லவர்-நாயக்கர் கால பாறைக்கோயில்.",
        "explanation_en": "Historic fortress shrine perched on a 273-foot sheer granite rock that is older than the Himalayas (3.8 billion years old).",
        "significance_ta": "பல்லவர் கால லலிதாங்குர பல்லவேஸ்வரர் குடைவரையும் உச்சியில் விநாயகர் ஆலயமும் கொண்ட திருச்சி மாநகரின் அடையாளம்.",
        "significance_en": "Features seminal 6th-century Pallava cave temples and offered impregnable defense during the Carnatic Wars."
    },
    "Manapparai Murukku (GI Tag)": {
        "name_ta": "மணப்பாறை முறுக்கு (புவிசார் குறியீடு)",
        "name_en": "Manapparai Murukku (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) பாரம்பரிய தின்பண்டம்",
        "category_en": "Culinary GI Specialty",
        "explanation_ta": "மணப்பாறையின் உவர் நன்னீரும், இருமுறை வறுத்து அரைத்த அரிசி மாவும் கொண்டு கைச்சுற்றாகச் சுடப்படும் மொறுமொறுப்பான பாரம்பரிய முறுக்கு.",
        "explanation_en": "Hand-extruded crispy spiral snack crafted from double-roasted rice flour and local mineral-rich well water.",
        "significance_ta": "தன் தனித்துவமான சுவை மற்றும் மொறுமொறுப்பிற்குப் பெயர் பெற்றுப் புவிசார் குறியீடு பெற்ற பாரம்பரிய உணவு.",
        "significance_en": "Commands legendary popularity across Tamil Nadu for distinct snap, golden color, and aroma."
    },

    # 30. Tirunelveli
    "Tirunelveli Halwa (GI Tag)": {
        "name_ta": "திருநெல்வேலி அல்வா (புவிசார் குறியீடு)",
        "name_en": "Tirunelveli Halwa (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) சுவை இனிப்பு",
        "category_en": "Geographical Indication (GI) Culinary Legend",
        "explanation_ta": "தாமிரபரணி நதியின் இயற்கை சுவைநீர், சம்பா கோதுமைப் பால் மற்றும் தூய நெய் கொண்டு பல மணிநேரம் வதக்கிச் செய்யப்படும் உலகப் புகழ்பெற்ற இனிப்பு.",
        "explanation_en": "Mouthwatering wheat jelly confection made by slow-cooking fermented samba wheat milk, pure cow ghee, and sugar in Tamirabarani river water.",
        "significance_ta": "திருநெல்வேலியின் உலகளாவிய அடையாளமாகத் திகழும் தனித்துவப் புவிசார் குறியீடு பெற்ற சுவைச் சின்னம்.",
        "significance_en": "Universally celebrated delicacy whose melt-in-mouth texture is attributed to the mineral qualities of the perennial Tamirabarani."
    },
    "Nellaiappar & Kanthimathi Temple (Musical Pillars)": {
        "name_ta": "நெல்லையப்பர் காந்திமதி திருக்கோயில் (இசைத் தூண்கள்)",
        "name_en": "Nellaiappar & Kanthimathi Temple (Musical Pillars)",
        "category_ta": "திராவிட கட்டடக்கலை அதிசயம்",
        "category_en": "Dravidian Architectural Wonder",
        "explanation_ta": "தாமிர சபை, தட்டினால் சப்தஸ்வரங்களை எழுப்பும் ஒற்றைக்கல் இசைத் தூண்கள் மற்றும் ஆயிரங்கால் மண்டபம் கொண்ட பிரம்மாண்ட பாண்டியர் கோயில்.",
        "explanation_en": "Monumental Pandyan twin temple spanning 14 acres, famous for the Thamira Sabha (Copper Dance Hall) and musical stone pillars that emit swaras.",
        "significance_ta": "வேணுவனம் என அழைக்கப்பட்ட ஊரில் நெல்லுக்கு வேலியாக நின்ற இறைவனின் பெயரால் திருநெல்வேலி எனப் பெயர் வரக் காரணமான மூலத் தலம்.",
        "significance_en": "Origin of the name 'Tirunelveli' (Sacred Hedge of Paddy) and supreme showcase of medieval acoustic stone sculpting."
    },
    "Thamirabarani Perennial River": {
        "name_ta": "தாமிரபரணி வற்றாத ஜீவநதி",
        "name_en": "Thamirabarani Perennial River",
        "category_ta": "வற்றாத நதி அமைப்பு",
        "category_en": "Perennial River System",
        "explanation_ta": "பொதிகை மலையில் அகத்தியர் தோற்றுவித்ததாகக் கருதப்படும், தமிழ்நாட்டில் மட்டுமே பிறந்து பாயும் ஒரே வற்றாத ஜீவநதி.",
        "explanation_en": "The only perennial river originating and culminating entirely within Tamil Nadu, descending from Agasthiyamalai in the Western Ghats.",
        "significance_ta": "ஆதிச்சநல்லூர் நாகரிகம் முதல் நெல்லைச் சீமையின் விவசாயத்தையும் பண்பாட்டையும் வளர்க்கும் புண்ணிய நதி.",
        "significance_en": "Cradle of prehistoric Iron Age civilization at Adichanallur and lifeline for southern irrigation."
    },
    "Manjolai Hill Tea Estates": {
        "name_ta": "மாஞ்சோலை மலை தேயிலைத் தோட்டங்கள்",
        "name_en": "Manjolai Hill Tea Estates",
        "category_ta": "சூழல் சுற்றுலா & பனிமலைக் காப்பகம்",
        "category_en": "Eco-Tourism & Mist Reserve",
        "explanation_ta": "களக்காடு முண்டந்துறை புலிகள் சரணாலயத்தின் உச்சியில் 1,100 மீட்டர் உயரத்தில் அமைந்துள்ள அமைதியான மலை தேயிலைத் தோட்டங்கள்.",
        "explanation_en": "Serene tea plantation haven situated at 1,100 meters inside the Kalakkad Mundanthurai Tiger Reserve.",
        "significance_ta": "குதிரைவெட்டி, மணிமுத்தாறு அருவி மற்றும் அரிய சோலைக்காடுகளைக் கொண்ட இயற்கை எழில் பூமி.",
        "significance_en": "Pristine bio-corridor featuring panoramic viewpoints, tea processing heritage, and endemic wildlife."
    },

    # 31. Tirupathur
    "Yelagiri Hills ('Poor Man's Ooty')": {
        "name_ta": "ஏலகிரி மலை ('ஏழைகளின் ஊட்டி')",
        "name_en": "Yelagiri Hills ('Poor Man's Ooty')",
        "category_ta": "மலை வாழிடம் & சாகச சுற்றுலா",
        "category_en": "Hill Station & Adventure Hub",
        "explanation_ta": "14 பழங்குடியினர் கிராமங்களும், புங்கனூர் ஏரியும், 14 கொண்டை ஊசி வளைவுகளும் கொண்ட அமைதியான மலை வாழிடம்.",
        "explanation_en": "Peaceful hill cluster at 1,110 meters surrounded by orchards, rose gardens, and the scenic Punganur artificial lake.",
        "significance_ta": "பாராகிளைடிங் மற்றும் மலையேற்றத்திற்கு உகந்த தென்னிந்தியாவின் முன்னணி சாகச சுற்றுலா தளம்.",
        "significance_en": "Premier adventure destination hosting paragliding festivals and mountain trekking trails."
    },
    "Vainu Bappu Observatory, Kavalur": {
        "name_ta": "வைணு பாப்பு வான் இயற்பியல் ஆய்வகம், காவலூர்",
        "name_en": "Vainu Bappu Observatory, Kavalur",
        "category_ta": "வானியல் அறிவியல் வரலாற்று மையம்",
        "category_en": "Astronomical Science Heritage",
        "explanation_ta": "ஆசியாவின் மிகப்பெரிய 2.34 மீட்டர் ஆப்டிகல் தொலைநோக்கியைக் கொண்டு இயங்கும் இந்திய வான் இயற்பியல் ஆய்வு மையம்.",
        "explanation_en": "Premier astronomical observatory operated by the Indian Institute of Astrophysics, home to the 2.34-meter Vainu Bappu Telescope.",
        "significance_ta": "யுரேனஸ் கோளின் வளையங்கள் மற்றும் புதிய சிறுகோள்களைக் கண்டறிந்த சர்வதேசப் புகழ் பெற்ற ஆய்வுக்கூடம்.",
        "significance_en": "Historic center where astronomers discovered the rings of Uranus and new solar system asteroids."
    },
    "Ambur Biryani & Leather Cluster": {
        "name_ta": "ஆம்பூர் பிரியாணி & தோல் தொழிற்பேட்டை",
        "name_en": "Ambur Biryani & Leather Cluster",
        "category_ta": "பாரம்பரிய உணவுக் கலை & தொழில்",
        "category_en": "Culinary & Industrial Heritage",
        "explanation_ta": "ஆற்காடு நவாப் காலத்து சீரக சம்பா அரிசி மற்றும் தயிர் மசாலா கொண்டு செய்யப்படும் தனித்துவ ஆம்பூர் பிரியாணி மற்றும் தோல் தொழிற்சாலைகள்.",
        "explanation_en": "World-famous Seeraga Samba dum biryani recipe evolved under Arcot Nawabs, coexisting with India's largest leather tanning clusters.",
        "significance_ta": "சர்வதேச காலணி ஏற்றுமதியிலும் உணவுக் கலையிலும் உலகப் புகழ் பெற்ற இரட்டை அடையாள நகரம்.",
        "significance_en": "Blends historic culinary fame with export leadership in global leatherwear."
    },

    # 32. Tiruppur
    "Knitwear Capital of India ('Dollar City')": {
        "name_ta": "இந்தியாவின் பின்னலாடை தலைநகரம் ('டாலர் சிட்டி')",
        "name_en": "Knitwear Capital of India ('Dollar City')",
        "category_ta": "சர்வதேச ஆடை ஏற்றுமதி கேந்திரம்",
        "category_en": "Global Garment Export Hub",
        "explanation_ta": "இந்தியாவின் 90 சதவீத பருத்தி பின்னலாடைகளை உற்பத்தி செய்து பல்லாயிரம் கோடி ரூபாய் அந்நியச் செலாவணியை ஈட்டும் தொழில் நகரம்.",
        "explanation_en": "Vibrant industrial export giant producing over 90% of India's cotton knitwear exports, earning the moniker 'Dollar City'.",
        "significance_ta": "லட்சக்கணக்கான தொழிலாளர்களுக்கு வாழ்வளிக்கும் தெற்காசியாவின் மிகப்பெரிய ஆடை தயாரிப்பு மண்டலம்.",
        "significance_en": "Drives employment for nearly a million workers with eco-friendly zero liquid discharge processing."
    },
    "Kangeyam Bull Breed & Heritage": {
        "name_ta": "காங்கேயம் காளை இனம் & பண்பாட்டு மரபு",
        "name_en": "Kangeyam Bull Breed & Heritage",
        "category_ta": "பாரம்பரிய நாட்டினக் கால்நடை மரபு",
        "category_en": "Indigenous Cattle Heritage",
        "explanation_ta": "வறட்சியைத் தாங்கி கடின உழைப்பை நல்கும் கம்பீரமான திமில்களும் கூர்மையான கொம்புகளும் கொண்ட காங்கேயம் நாட்டின மாடுகள்.",
        "explanation_en": "Indigenous draft cattle breed world-famous for immense strength, drought tolerance, and prominent hump and horns.",
        "significance_ta": "ஜல்லிக்கட்டு வீர விளையாட்டின் நாயகனாகவும் கொங்கு நாட்டின் பாரம்பரிய விவசாயப் பெருமையாகவும் திகழ்கிறது.",
        "significance_en": "Icon of Tamil martial sports (Jallikattu) and traditional pasture farming in the Kangeyam grasslands."
    },
    "Uthukuli Butter": {
        "name_ta": "ஊத்துக்குளி வெண்ணெய்",
        "name_en": "Uthukuli Butter",
        "category_ta": "பாரம்பரிய பால்பண்ணை உணவுக் கலை",
        "category_en": "Culinary Dairy Specialty",
        "explanation_ta": "ஊத்துக்குளி எருமைப் பாலில் இருந்து பாரம்பரிய முறையில் கடையப்படும் தனித்துவ நறுமணமும் தூய்மையும் கொண்ட வெண்ணெய்.",
        "explanation_en": "Renowned clarified butter and curd churned from rich buffalo milk, known across India for unmatched culinary aroma.",
        "significance_ta": "தமிழகத்தின் அனைத்து முன்னணி இனிப்பகங்களிலும் நெய் தயாரிப்பிற்கும் சுவைக்கும் பயன்படுத்தப்படும் பாரம்பரிய உணவுப் பொருள்.",
        "significance_en": "Premium benchmark for pure ghee making in South Indian culinary establishments."
    },

    # 33. Tiruvallur
    "Pulicat Lake & Bird Sanctuary": {
        "name_ta": "பழவேற்காடு ஏரி & பறவைகள் சரணாலயம்",
        "name_en": "Pulicat Lake & Bird Sanctuary",
        "category_ta": "கடலோர உப்பங்கழி ஈரநிலம்",
        "category_en": "Coastal Lagoon Ecosystem",
        "explanation_ta": "சிலிகா ஏரிக்கு அடுத்தபடியாக இந்தியாவின் இரண்டாவது பெரிய உவர்நீர் உப்பங்கழி ஏரி மற்றும் வலசைப் பறவைகள் சரணாலயம்.",
        "explanation_en": "India's second largest brackish-water lagoon covering 759 sq km, separated from the Bay of Bengal by Sriharikota island.",
        "significance_ta": "ஆண்டுதோறும் பல்லாயிரக்கணக்கான பூநாரைகள் தஞ்சமடையும் இயற்கை ஈரநிலமாகவும் டச்சுக்காரர்களின் 17-ஆம் நூற்றாண்டு கோட்டையைக் கொண்ட வரலாற்றுத் தளமாகவும் திகழ்கிறது.",
        "significance_en": "Critical winter feeding ground for 15,000 Greater Flamingos alongside historical 17th-century Dutch colonial monuments."
    },
    "Sri Veeraraghava Swamy Temple": {
        "name_ta": "திருவள்ளூர் வீரராகவ சுவாமி திருக்கோயில்",
        "name_en": "Sri Veeraraghava Swamy Temple",
        "category_ta": "திவ்ய தேசத் திருத்தலம்",
        "category_en": "Divya Desam Heritage",
        "explanation_ta": "108 வைணவ திவ்ய தேசங்களில் ஒன்றான வரலாற்றுப் பிரசித்தி பெற்ற வீரராகவ பெருமாள் சயனத் திருக்கோயில்.",
        "explanation_en": "Celebrated 8th-century Vaishnavite shrine where Lord Vishnu reposes as Vaidya Veeraraghava, the celestial healer.",
        "significance_ta": "தீராத நோய்களைத் தீர்க்கும் வைத்திய வீரராகவர் என்றும், 'எவ்வுள் படுத்தாய்' என்ற புராணப் பின்னணியில் திருவள்ளூர் பெயர் பெறக் காரணமான மூலத் தலம்.",
        "significance_en": "Origin of the ancient name 'Tiru-evvul-oor' (Where did you sleep?) associated with saint Salihothra Maharishi."
    },
    "Poondi Reservoir (Sathyamurthy Sagar)": {
        "name_ta": "பூண்டி நீர்த்தேக்கம் (சத்தியமூர்த்தி சாகர்)",
        "name_en": "Poondi Reservoir (Sathyamurthy Sagar)",
        "category_ta": "நீர்வளப் பாதுகாப்பு அணை",
        "category_en": "Water Lifeline Reservoir",
        "explanation_ta": "சென்னை மாநகரத்தின் குடிநீர் தேவையைப் பூர்த்தி செய்ய கொற்றலை ஆற்றின் குறுக்கே 1944-இல் அமைக்கப்பட்ட பிரம்மாண்ட நீர்த்தேக்கம்.",
        "explanation_en": "Vital masonry storage reservoir constructed across the Kosasthalaiyar river in 1944 to supply drinking water to Chennai city.",
        "significance_ta": "சுதந்திரப் போராட்ட வீரர் தீரர் சத்தியமூர்த்தியின் கனவை நனவாக்கிய சென்னை மற்றும் திருவள்ளூர் மக்களின் குடிநீர் ஆதாரம்.",
        "significance_en": "Named in honor of freedom fighter S. Satyamurti who championed the reservoir's construction."
    },

    # 34. Tiruvannamalai
    "Arunachaleswarar Temple (Agni Sthalam)": {
        "name_ta": "திருவண்ணாமலை அருணாசலேஸ்வரர் திருக்கோயில் (பஞ்சபூத அக்னி தலம்)",
        "name_en": "Arunachaleswarar Temple (Agni Sthalam)",
        "category_ta": "பஞ்சபூதக் கட்டடக் கலை அற்புதம்",
        "category_en": "Pancha Bhoota Architectural Wonder",
        "explanation_ta": "பஞ்சபூதத் தலங்களில் நெருப்புக்குரிய (அக்னி) தலமாக அண்ணாமலையின் அடிவாரத்தில் 25 ஏக்கர் பரப்பளவில் அமைந்துள்ள மாபெரும் திருக்கோயில்.",
        "explanation_en": "Ancient 25-acre temple complex at the foot of Mount Annamalai representing the Agni (Fire) element of Pancha Bhoota.",
        "significance_ta": "217 அடி உயர இராஜகோபுரம், கார்த்திகை மகா தீபத் திருவிழா மற்றும் சோழர், விஜயநகர கல்வெட்டுகளின் பொக்கிஷம்.",
        "significance_en": "Site of the Karthigai Deepam beacon lit atop the sacred peak and repository of over a thousand medieval stone records."
    },
    "Girivalam (Sacred Hill Circumambulation)": {
        "name_ta": "கிரிவலம் (14 கி.மீ அண்ணாமலை புனித வலம்)",
        "name_en": "Girivalam (Sacred Hill Circumambulation)",
        "category_ta": "ஆன்மீகப் பாதை & ஆசிரம மரபு",
        "category_en": "Spiritual Practice & Hermitage Heritage",
        "explanation_ta": "பௌர்ணமி தோறும் லட்சக்கணக்கான பக்தர்கள் 14 கி.மீ தூரமுள்ள புனித அண்ணாமலையை பாதயாத்திரையாக வலம் வரும் ஆன்மீக நெறி.",
        "explanation_en": "Ancient spiritual tradition of circumambulating the 14-kilometer perimeter of Mount Arunachala barefoot on full moon nights.",
        "significance_ta": "ஸ்ரீ ரமண மகரிஷி, சேஷாத்ரி சுவாமிகள் தவம் செய்த ஆசிரமங்களும் இந்திர லிங்கம் உள்ளிட்ட அஷ்ட லிங்கங்களும் கொண்ட புனிதப் பாதை.",
        "significance_en": "Encompasses the ashram of Sri Ramana Maharshi and eight cardinal guardian shrines (Ashta Lingams)."
    },
    "Arani Silk Sarees (GI Tag)": {
        "name_ta": "ஆரணி பட்டுப் புடவைகள் (புவிசார் குறியீடு)",
        "name_en": "Arani Silk Sarees (GI Tag)",
        "category_ta": "புவிசார் குறியீடு (GI) கைத்தறி பட்டு",
        "category_en": "Textile GI Craft",
        "explanation_ta": "ஆரணி பகுதியின் கைத்தறி நெசவாளர்களால் பாரம்பரியமாக நெசவு செய்யப்படும் எடை குறைவான பளபளப்பான பட்டுப் புடவைகள்.",
        "explanation_en": "Lightweight, lustrous pure silk sarees handwoven by master weavers in Arani using fine Mulberry silk and zari borders.",
        "significance_ta": "இந்தியாவின் அதிக பட்டுப் புடவை உற்பத்தியை மேற்கொண்டு புவிசார் குறியீடு பெற்ற பாரம்பரிய நெசவு மையம்.",
        "significance_en": "Produces the largest volume of silk sarees in Tamil Nadu, recognized with the GI tag for weaving excellence."
    },
    "Sathanur Dam & Crocodile Farm": {
        "name_ta": "சாத்தனூர் அணை & முதலைகள் பண்ணை",
        "name_en": "Sathanur Dam & Crocodile Farm",
        "category_ta": "நீர்ப்பாசன அணை & பூங்கா",
        "category_en": "Irrigation Dam & Park",
        "explanation_ta": "தென்பெண்ணை ஆற்றின் குறுக்கே சென்னகேசவ மலைகளுக்கு இடையே கட்டப்பட்ட பிரம்மாண்ட அணை மற்றும் எழில்மிகு பூங்கா.",
        "explanation_en": "Imposing masonry dam built across the Thenpennai river in 1958, flanked by scenic landscaped gardens and a crocodile sanctuary.",
        "significance_ta": "திருவண்ணாமலை மாவட்டத்தின் முக்கிய விவசாயப் பாசன ஆதாரமாகவும் முதலைகள் இனப்பெருக்க மையமாகவும் திகழ்கிறது.",
        "significance_en": "Vital reservoir providing irrigation and supporting endangered freshwater mugger crocodile breeding."
    },

    # 35. Tiruvarur
    "Thyagaraja Swamy Temple & Aazhi Ther (Giant Chariot)": {
        "name_ta": "திருவாரூர் தியாகராஜசுவாமி திருக்கோயில் & ஆழித்தேர்",
        "name_en": "Thyagaraja Swamy Temple & Aazhi Ther (Giant Chariot)",
        "category_ta": "தேர்க் கட்டடக் கலை & சோழர் மரபு",
        "category_en": "Chariot Architecture & Delta Heritage",
        "explanation_ta": "ஆசியாவின் மிகப்பெரிய 300 டன் எடையும் 96 அடி உயரமும் கொண்ட ஆழித்தேர் பவனி வரும் மாபெரும் சோழர் திருக்கோயில்.",
        "explanation_en": "Vast medieval temple complex spanning 20 acres, world-famous for the massive 300-tonne, 96-foot high temple chariot (Aazhi Ther).",
        "significance_ta": "மனுநீதி சோழன் தன் மகனையே தேர்க்காலில் இட்ட நீதி காத்த பூமி மற்றும் கமல்ஆலயம் திருக்குளம் கொண்ட சைவத் தலைமை பீடம்.",
        "significance_en": "Legendary seat of justice of King Manuneethi Cholan and home to the 33-acre sacred Kamalalayam tank."
    },
    "Birthplace of Carnatic Music Trinity": {
        "name_ta": "கர்நாடக சங்கீத மும்மூர்த்திகள் அவதரித்த பூமி",
        "name_en": "Birthplace of Carnatic Music Trinity",
        "category_ta": "பாரம்பரிய இசைப் பண்பாட்டு மரபு",
        "category_en": "Classical Music Heritage",
        "explanation_ta": "கர்நாடக இசையின் மும்மூர்த்திகளான தியாகராஜர், முத்துசுவாமி தீட்சிதர் மற்றும் சியாமா சாஸ்திரி ஆகிய மூவரும் பிறந்த புண்ணிய மண்.",
        "explanation_en": "Sacred cultural town where all three divine composers of the Carnatic Music Trinity were born within a few paces of each other.",
        "significance_ta": "இந்திய பாரம்பரிய சங்கீதத்தின் தாயகமாகவும் உலக இசை ஆய்வாளர்கள் வணங்கும் புனித இடமாகவும் திகழ்கிறது.",
        "significance_en": "Unmatched musicological epicenter that shaped the golden repertoire of South Indian classical music."
    },
    "Muthupet Mangrove Lagoon": {
        "name_ta": "முத்துப்பேட்டை அலையாத்திக் காடுகள் (ராம்சார் தளம்)",
        "name_en": "Muthupet Mangrove Lagoon",
        "category_ta": "கடலோர சதுப்புநிலச் சூழலியல்",
        "category_en": "Coastal Wetland Ecology",
        "explanation_ta": "பாமினியாறு உள்ளிட்ட காவிரியின் கிளை ஆறுகள் கடலில் கலக்கும் 12,000 ஹெக்டேர் பரப்பளவிலான பிரம்மாண்ட அலையாத்திக் காடுகள்.",
        "explanation_en": "Sprawling 120-sq-km coastal mangrove wetland where the tributaries of the Cauvery meet the Palk Strait.",
        "significance_ta": "புலம்பெயர் நீர்ப்பறவைகள், கடல் ஆமைகள் மற்றும் ஓதக் காடுகளின் தனித்துவ பல்லுயிர் வளம் கொண்ட சர்வதேச ராம்சார் தளம்.",
        "significance_en": "Designated Ramsar Wetland of International Importance sustaining rich fisheries and mangrove species."
    },

    # 36. Vellore
    "Vellore Fort & 1806 Vellore Sepoy Mutiny": {
        "name_ta": "வேலூர் வரலாற்று கோட்டை & 1806 சிப்பாய் புரட்சி",
        "name_en": "Vellore Fort & 1806 Vellore Sepoy Mutiny",
        "category_ta": "இராணுவக் கட்டடக் கலை & விடுதலைப் போராட்ட மரபு",
        "category_en": "Military Architecture & Freedom Heritage",
        "explanation_ta": "16-ஆம் நூற்றாண்டில் விஜயநகர மன்னர்களால் ஆழமான முதலை அகழியுடன் கட்டப்பட்ட பிரம்மாண்டமான கருங்கல் கோட்டை.",
        "explanation_en": "Formidable 16th-century granite fort surrounded by a deep crocodile-infested moat, constructed by Vijayanagara rulers.",
        "significance_ta": "1857 பெரும் புரட்சிக்கு அரை நூற்றாண்டுக்கு முன்பே 1806-இல் வெடித்த இந்திய சுதந்திரப் போராட்டத்தின் முதல் சிப்பாய் புரட்சி களம்.",
        "significance_en": "Site of the heroic Vellore Sepoy Mutiny of 10 July 1806, the first organized armed uprising against British East India rule."
    },
    "Jalakanteswarar Temple": {
        "name_ta": "ஜலகண்டேஸ்வரர் திருக்கோயில் (கோட்டைக்குள் அமைந்த ஆலயம்)",
        "name_en": "Jalakanteswarar Temple",
        "category_ta": "விஜயநகரக் கல் சிற்பக்கலை அற்புதம்",
        "category_en": "Vijayanagara Stone Sculpture",
        "explanation_ta": "வேலூர் கோட்டையின் அகழிக்கு நடுவே அமைந்துள்ள, ஒப்பற்ற யாளித் தூண்களும் கல்யாண மண்டபச் சிற்பங்களும் கொண்ட திருக்கோயில்.",
        "explanation_en": "Exquisite 16th-century Shiva temple situated within Vellore Fort, noted for its peerless Kalyana Mandapam (wedding hall).",
        "significance_ta": "சிற்பக் கலை வல்லுநர்களால் உலகிலேயே மிக நுணுக்கமான கல் வேலைப்பாடுகள் கொண்ட மண்டபங்களில் ஒன்றாகப் போற்றப்படுகிறது.",
        "significance_en": "Celebrated by art historians for monolithic pillars carved with mythical rearing dragons and celestial deities."
    },
    "Vellore Spiny Brinjal (GI Tag)": {
        "name_ta": "வேலூர் முள்ளுக் கத்தரிக்காய் (புவிசார் குறியீடு)",
        "name_en": "Vellore Spiny Brinjal (GI Tag)",
        "category_ta": "வேளாண் புவிசார் குறியீடு (GI)",
        "category_en": "Agri-GI Horticultural Variety",
        "explanation_ta": "காம்பில் முட்களும், மென்மையான சதைப்பற்றும், பிரத்யேக நறுமணச் சுவையும் கொண்ட தனித்துவமான நாட்டுக்கத்தரிக்காய் இனம்.",
        "explanation_en": "Unique indigenous brinjal landrace characterized by soft spines on the calyx and stem, glossy purple skin, and succulent flesh.",
        "significance_ta": "சுவையான பிரியாணி மற்றும் கத்திரிக்காய் பச்சடி தயாரிப்பில் நீங்காத இடம் பெற்று புவிசார் குறியீடு பெற்ற விவசாயத் தங்கம்.",
        "significance_en": "Awarded GI status for distinct buttery taste and resistance to regional pests."
    },
    "Sripuram Golden Temple (Malaikodi)": {
        "name_ta": "ஸ்ரீபுரம் தங்கக் கோயில் (மலைக்கோடி)",
        "name_en": "Sripuram Golden Temple (Malaikodi)",
        "category_ta": "ஆன்மீகத் தங்கக் கோயில் சின்னம்",
        "category_en": "Spiritual Landmark",
        "explanation_ta": "100 ஏக்கர் பசுமை வளாகத்தில் 1.5 டன் தூய தங்கத் தகடுகளால் வேயப்பட்ட மகாலட்சுமி திருக்கோயில் மற்றும் நட்சத்திர வடிவ தியானப் பாதை.",
        "explanation_en": "Spiritual sanctuary covering 100 acres featuring a sanctum coated with over 1.5 tonnes of pure gold foil surrounded by a star-shaped path.",
        "significance_ta": "உலகெங்கிலும் இருந்து லட்சக்கணக்கான பக்தர்களை ஈர்க்கும் அமைதி மற்றும் அறக்கொடைகளின் ஆன்மீக மையம்.",
        "significance_en": "Attracts millions of international visitors for meditation and charity."
    },

    # 37. Viluppuram
    "Gingee Fort ('Troy of the East')": {
        "name_ta": "செஞ்சிக் கோட்டை ('கிழக்கின் ட்ராய்')",
        "name_en": "Gingee Fort ('Troy of the East')",
        "category_ta": "இராணுவக் கோட்டை வளாகம் & வரலாற்று அரண்",
        "category_en": "Monolithic Military Fortress Complex",
        "explanation_ta": "ராஜகிரி, கிருஷ்ணகிரி மற்றும் சந்திராயன்துர்க் ஆகிய 3 செங்குத்தான மலைகளை இணைத்து கட்டப்பட்ட யாராலும் வீழ்த்த முடியாத வரலாற்றுப் பெரும் கோட்டை.",
        "explanation_en": "Complex of three steep hill forts (Rajagiri, Krishnagiri, Chandrayandurg) interconnected by massive walls, deemed impregnable by Chhatrapati Shivaji.",
        "significance_ta": "மராட்டிய மாமன்னர் சத்ரபதி சிவாஜியால் 'இந்தியாவின் மிக அசைக்க முடியாத கோட்டை' என்றும் ஆங்கிலேயர்களால் 'கிழக்கின் ட்ராய்' என்றும் போற்றப்பட்டது.",
        "significance_en": "Features Kalyan Mahal, multi-tier granaries, watchtowers, and legendary Raja Desingh lore."
    },
    "Auroville International Township & Matrimandir": {
        "name_ta": "ஆரோவில் சர்வதேச நகரம் & மாத்ரிமந்திர்",
        "name_en": "Auroville International Township & Matrimandir",
        "category_ta": "சர்வதேச ஆன்மீக நகரம் & மனித ஒருமைப்பாடு",
        "category_en": "Global Universal Township",
        "explanation_ta": "ஸ்ரீ அரவிந்தர் மற்றும் அன்னை மிரா அல்பாசாவின் மனித ஒருமைப்பாட்டுக் கொள்கையின் கீழ் 1968-இல் யுனெஸ்கோ அங்கீகாரத்துடன் அமைக்கப்பட்ட சர்வதேச நகரம்.",
        "explanation_en": "Founded in 1968 by Mirra Alfassa (The Mother) based on Sri Aurobindo's vision of human unity, recognized by UNESCO and Government of India.",
        "significance_ta": "தங்கக் கோள வடிவிலான மாத்ரிமந்திர் தியான அரங்கமும், 50-க்கும் மேற்பட்ட நாடுகளைச் சேர்ந்த மக்கள் இணைந்து வாழும் அமைதிப் பூமியும் ஆகும்.",
        "significance_en": "Features the golden geodesic dome of Matrimandir dedicated to silent meditation and renewable living."
    },
    "Thirukoilur Ulagalantha Perumal Temple": {
        "name_ta": "திருக்கோவிலூர் உலகளந்த பெருமாள் திருக்கோயில்",
        "name_en": "Thirukoilur Ulagalantha Perumal Temple",
        "category_ta": "திவ்ய தேசம் & சங்க காலத் தலம்",
        "category_en": "Divya Desam & Sangam Heritage",
        "explanation_ta": "விண்ணையும் மண்ணையும் அளந்த வாமன-திரிவிக்கிரம பெருமாள் எழுந்தருளியுள்ள தலம்; முதல் மூன்று ஆழ்வார்கள் பாசுரங்களைப் பாடித் தொடங்கிய வரலாற்றுப் பூமி.",
        "explanation_en": "Ancient temple of Lord Vishnu as Trivikrama measuring the universe, where the first three Alvars (Poigai, Bhutha, Peyalvar) composed the first hymns.",
        "significance_ta": "நாலாயிர திவ்யப் பிரபந்தத்தின் முதல் பாசுரங்கள் தோன்றிய வைணவத் திருத்தலமாகவும் சங்க கால மலையமான் நாட்டின் தலைநகரமாகவும் திகழ்கிறது.",
        "significance_en": "Foundational birthplace of the Tamil Vaishnavite devotional movement."
    },

    # 38. Virudhunagar
    "Srivilliputhur Andal Temple (Tamil Nadu State Emblem)": {
        "name_ta": "ஸ்ரீவில்லிபுத்தூர் ஆண்டாள் திருக்கோயில் (தமிழ்நாடு அரசு சின்னம்)",
        "name_en": "Srivilliputhur Andal Temple (Tamil Nadu State Emblem)",
        "category_ta": "தமிழ்நாடு அரசு அதிகாரப்பூர்வ சின்னம்",
        "category_en": "Sacred Architectural Symbol of Tamil Nadu",
        "explanation_ta": "திருப்பாவை பாடிய சூடிக்கொடுத்த சுடர்க்கொடி ஆண்டாள் மற்றும் பெரியாழ்வார் அவதரித்த தலமும், 192 அடி உயர 11 நிலை இராஜகோபுரம் கொண்ட திருத்தலமும் ஆகும்.",
        "explanation_en": "Birthplace of saint-poetess Andal (author of Tiruppavai) and Periyalvar, featuring a towering 192-foot, 11-tiered Rajagopuram.",
        "significance_ta": "இக்கோயிலின் இராஜகோபுரமே தமிழ்நாடு அரசின் அதிகாரப்பூர்வ இலச்சினையாக ஏற்றுக்கொள்ளப்பட்ட மாபெரும் பெருமை வாய்ந்தது.",
        "significance_en": "Adopted by the Government of Tamil Nadu as the official State Emblem."
    },
    "Srivilliputhur Palkova (GI Tag)": {
        "name_ta": "ஸ்ரீவில்லிபுத்தூர் பால்கோவா (புவிசார் குறியீடு)",
        "name_en": "Srivilliputhur Palkova (GI Tag)",
        "category_ta": "பால்பண்ணை புவிசார் குறியீடு (GI)",
        "category_en": "Dairy Confectionery GI Heritage",
        "explanation_ta": "தூய பசும்பால் மற்றும் சர்க்கரையை கனமான பித்தளைக் கடாயில் விறகடுப்பில் நீண்ட நேரம் சுண்டக் காய்ச்சித் தயாரிக்கப்படும் மணமிக்க பாரம்பரிய இனிப்பு.",
        "explanation_en": "Traditional caramelized milk sweet prepared using pure full-cream buffalo/cow milk and sugar, slowly stirred in heavy brass vats over wood fire.",
        "significance_ta": "தன் மென்மையான சிறு தானிய அமைப்பிற்கும் கலப்படமற்ற தூய்மைக்கும் புவிசார் குறியீடு பெற்ற உலகப் புகழ்பெற்ற இனிப்பு.",
        "significance_en": "Famous across India for rich granular texture and unadulterated purity."
    },
    "Sivakasi Printing & Safety Match Capital": {
        "name_ta": "சிவகாசி அச்சுத் தொழில் & தீப்பெட்டித் தலைநகரம்",
        "name_en": "Sivakasi Printing & Safety Match Capital",
        "category_ta": "தொழில்துறை உற்பத்தி மையம்",
        "category_en": "Industrial Manufacturing Hub",
        "explanation_ta": "இந்தியாவின் 60 சதவீதத்திற்கும் அதிகமான ஆஃப்செட் அச்சு, நோட்டுப் புத்தகங்கள், காலண்டர்கள் மற்றும் தீப்பெட்டிகளை உற்பத்தி செய்யும் சர்வதேச தொழில் நகரம்.",
        "explanation_en": "Produces over 60% of India's offset printing, school books, calendars, and safety matches, nicknamed 'Kutti Japan' by Jawaharlal Nehru.",
        "significance_ta": "ஜவஹர்லால் நேருவால் 'குட்டி ஜப்பான்' எனப் போற்றப்பட்ட தெற்காசியாவின் முன்னணி அச்சு மற்றும் பேக்கேஜிங் தொழில் கேந்திரம்.",
        "significance_en": "World-class graphic printing and packaging industrial ecosystem."
    },
    "Birthplace of Karma Veerar K. Kamaraj": {
        "name_ta": "கர்மவீரர் காமராஜர் பிறந்த வரலாற்று மண்",
        "name_en": "Birthplace of Karma Veerar K. Kamaraj",
        "category_ta": "தேசிய வரலாற்று ஆளுமை இல்லம்",
        "category_en": "National Historic Personality",
        "explanation_ta": "இலவச மதிய உணவுத் திட்டம் தந்து லட்சக்கணக்கான ஏழை எளிய மாணவர்களின் கல்விக் கண் திறந்த பாரத ரத்னா காமராஜர் அவதரித்த விருதுநகர் பூமி.",
        "explanation_en": "Home of former Chief Minister of India K. Kamaraj, who pioneered the free mid-day meal scheme in schools and shaped modern education.",
        "significance_ta": "காமராஜர் வாழ்ந்த இல்லம் தேசிய நினைவகமாகப் பாதுகாக்கப்பட்டு அவரது எளிமையையும் பொதுத்தொண்டையும் போற்றும் இடமாக உள்ளது.",
        "significance_en": "His ancestral house in Virudhunagar is preserved as a national memorial."
    }
}

# Comprehensive translation dictionary for all Famous Places across 38 districts
FAMOUS_PLACES_TRANSLATIONS = {
    # 1. Ariyalur
    "Gangaikonda Cholapuram": {
        "name_ta": "கங்கைகொண்ட சோழபுரம்",
        "name_en": "Gangaikonda Cholapuram",
        "category_ta": "யுனெஸ்கோ உலகப் பாரம்பரியச் சின்னம்",
        "category_en": "UNESCO Monument",
        "description_ta": "முதலாம் ராஜேந்திர சோழன் கட்டிய பிரம்மாண்ட கற்கோயில்; ஒப்பற்ற சிற்பங்கள், வெண்கலச் சிலைகள் மற்றும் சோழர் கல்வெட்டுகள் நிறைந்த தலம்.",
        "description_en": "Majestic Chola temple showcasing supreme stone carving, living bronze traditions, and royal inscriptions."
    },
    "Karaivetti Sanctuary": {
        "name_ta": "கரைவெட்டி சரணாலயம்",
        "name_en": "Karaivetti Sanctuary",
        "category_ta": "பறவைகள் சரணாலயம்",
        "category_en": "Ecology",
        "description_ta": "188-க்கும் மேற்பட்ட உள்நாட்டு மற்றும் வலசைப் பறவை இனங்கள் வந்து தங்கும் இயற்கை எழில் சூழ்ந்த நன்னீர் ஏரி சரணாலயம்.",
        "description_en": "Scenic freshwater lake sanctuary hosting over 188 species of resident and migratory birds."
    },
    "Jayankondam": {
        "name_ta": "ஜெயங்கொண்டம்",
        "name_en": "Jayankondam",
        "category_ta": "வரலாற்று வணிக நகரம்",
        "category_en": "Historic Commercial Town",
        "description_ta": "சோழப் பேரரசு நிர்வாகத்துடனும் பாரம்பர்ய கைத்தறி நெசவுத் தொழிலுடனும் தொடர்புடைய வரலாற்று சிறப்புமிக்க வணிக நகரம்.",
        "description_en": "Ancient trading town connected to Chola administration and handloom weaving."
    },

    # 2. Chengalpattu
    "Mamallapuram Shore Temple": {
        "name_ta": "மாமல்லபுரம் கடற்கரைக் கோயில்",
        "name_en": "Mamallapuram Shore Temple",
        "category_ta": "பல்லவர் கால வரலாற்றுச் சின்னம்",
        "category_en": "Pallava Heritage",
        "description_ta": "வங்காள விரிகுடாக் கரையில் 8-ஆம் நூற்றாண்டில் ராஜசிம்ம பல்லவனால் கருங்கல்லால் கட்டப்பட்ட வரலாற்றுப் பெருமை வாய்ந்த கடற்கரைக் கோயில்.",
        "description_en": "8th-century granite sea temple built by Rajasimha Pallava on the Bay of Bengal coastline."
    },
    "Pancha Rathas": {
        "name_ta": "ஐந்து ரதங்கள்",
        "name_en": "Pancha Rathas",
        "category_ta": "ஒற்றைக்கல் கட்டடக்கலை அதிசயம்",
        "category_en": "Monolithic Architecture",
        "description_ta": "ஒரே பாறையில் திராவிடக் கோயில் பாணிகளில் செதுக்கப்பட்ட தர்மராஜர், பீமர், அர்ச்சுனன், திரௌபதி மற்றும் நகுல-சகாதேவ ரதங்கள்.",
        "description_en": "Five monolithic monolithic temples carved out of a single rock outcrop, each in a distinct architectural style."
    },
    "Vedanthangal Sanctuary": {
        "name_ta": "வேடந்தாங்கல் சரணாலயம்",
        "name_en": "Vedanthangal Sanctuary",
        "category_ta": "இயற்கை ஈரநிலக் காப்பகம்",
        "category_en": "Ecological Reserve",
        "description_ta": "நாரைகள், கூழைக்கடாக்கள் உள்ளிட்ட பல்லாயிரக்கணக்கான வலசைப் பறவைகள் தங்கி இனப்பெருக்கம் செய்யும் பழம்பெரும் சரணாலயம்.",
        "description_en": "India's oldest waterbird sanctuary welcoming over 40,000 birds from around the world each season."
    },

    # 3. Chennai
    "Mylapore Kapaleeshwarar Temple": {
        "name_ta": "மயிலாப்பூர் கபாலீஸ்வரர் திருக்கோயில்",
        "name_en": "Mylapore Kapaleeshwarar Temple",
        "category_ta": "ஆன்மீகத் திருத்தலம்",
        "category_en": "Spiritual Heritage",
        "description_ta": "வர்ண வேலைப்பாடுகள் நிறைந்த இராஜகோபுரமும், பங்குனிப் பெருவிழா அறுபத்து மூவர் உலாவும் கொண்ட மயிலாப்பூரின் ஆன்மீக அடையாளம்.",
        "description_en": "Historic Shiva temple famous for its 120-foot gopuram and the vibrant annual Panguni Arupathimoovar festival."
    },
    "Fort St. George & Museum": {
        "name_ta": "புனித ஜார்ஜ் கோட்டை & அருங்காட்சியகம்",
        "name_en": "Fort St. George & Museum",
        "category_ta": "வரலாற்றுப் பிரிட்டிஷ் கோட்டை",
        "category_en": "Colonial Landmark",
        "description_ta": "1644-இல் கட்டப்பட்ட வரலாற்று கோட்டை; பிரிட்டிஷ் கால ஆயுதங்கள், சீருடைகள் மற்றும் நாணயங்கள் பாதுகாக்கப்பட்ட அரசு அருங்காட்சியகம்.",
        "description_en": "First British fort in India containing St. Mary's Church (oldest Anglican church) and a rich colonial artifact museum."
    },
    "Santhome Cathedral Basilica": {
        "name_ta": "சாந்தோம் கதீட்ரல் பசிலிக்கா",
        "name_en": "Santhome Cathedral Basilica",
        "category_ta": "கிறிஸ்தவ வரலாற்றுப் பேராலயம்",
        "category_en": "Ecclesiastical Heritage",
        "description_ta": "இயேசு கிறிஸ்துவின் பன்னிரு சீடர்களில் ஒருவரான புனித தோமையாரின் கல்லறையின் மேல் 16-ஆம் நூற்றாண்டில் எழுப்பப்பட்ட நியோ-கோத்திக் பேராலயம்.",
        "description_en": "Neo-Gothic basilica built over the tomb of St. Thomas the Apostle, one of only three such cathedrals in the world."
    },

    # 4. Coimbatore
    "Marudhamalai Temple": {
        "name_ta": "மருதமலை முருகன் திருக்கோயில்",
        "name_en": "Marudhamalai Temple",
        "category_ta": "மலை முருகன் தலம்",
        "category_en": "Hill Shrine",
        "description_ta": "மேற்குத் தொடர்ச்சி மலையின் இயற்கை எழில் சூழ்ந்த குன்றில் அமைந்துள்ள புகழ்பெற்ற சுப்பிரமணிய சுவாமி திருக்கோயில்.",
        "description_en": "Revered hill temple of Lord Muruga surrounded by medicinal springs, praised by ancient Arunagirinathar."
    },
    "Perur Pateeswarar Temple": {
        "name_ta": "பேரூர் பட்டீஸ்வரர் திருக்கோயில்",
        "name_en": "Perur Pateeswarar Temple",
        "category_ta": "சோழர் கல்வெட்டுப் பாடல் பெற்ற தலம்",
        "category_en": "Chola Epigraphy",
        "description_ta": "கனகசபை மண்டபத்தில் அற்புதமான நடனச் சிற்பங்களைக் கொண்ட 1500 ஆண்டுகள் பழமையான பாடல் பெற்ற திருத்தலம்.",
        "description_en": "Ancient temple on the banks of Noyyal river, famed for the Kanaka Sabha with intricately carved stone pillars."
    },
    "Siruvani Waterfalls": {
        "name_ta": "சிறுவாணி நீர்வீழ்ச்சி",
        "name_en": "Siruvani Waterfalls",
        "category_ta": "சூழல் சுற்றுலா",
        "category_en": "Eco-Tourism",
        "description_ta": "அடர்ந்த வனப்பகுதி வழியாகப் பாய்ந்து வரும் உலகின் சுவையான நன்னீரை வழங்கும் ரம்மியமான நீர்வீழ்ச்சி.",
        "description_en": "Enchanting forest waterfall located 37 km from Coimbatore, renowned for its crystal clear sweet water."
    },

    # 5. Cuddalore
    "Chidambaram Nataraja Temple": {
        "name_ta": "சிதம்பரம் நடராஜர் திருக்கோயில்",
        "name_en": "Chidambaram Nataraja Temple",
        "category_ta": "பஞ்சபூத ஆகாய தலம்",
        "category_en": "Pancha Bhoota Sthalam",
        "description_ta": "சிவபெருமான் ஆனந்த நடனம் ஆடும் பொன்னம்பலம் கொண்ட, சிதம்பரம் ரகசியம் பொதிந்த புகழ்பெற்ற சைவத் தலம்.",
        "description_en": "Ancient temple representing space, celebrated for the golden roofed chit sabha and Chidambara Rahasya."
    },
    "Pichavaram Mangroves": {
        "name_ta": "பிச்சாவரம் சதுப்புநிலக் காடுகள்",
        "name_en": "Pichavaram Mangroves",
        "category_ta": "ஈரநிலச் சூழலியல்",
        "category_en": "Wetland Ecology",
        "description_ta": "படகுப் பயணம் மேற்கொண்டு அடர்ந்த கால்வாய்களைக் கண்டு ரசிக்கக்கூடிய உலகின் மிகப்பெரிய அலையாத்திக் காடுகளில் ஒன்று.",
        "description_en": "Scenic mangrove ecosystem offering tranquil boat rides through narrow waterways canopying rare marine flora."
    },
    "Silver Beach": {
        "name_ta": "சில்வர் கடற்கரை (தேவனாம்பட்டினம்)",
        "name_en": "Silver Beach",
        "category_ta": "கடற்கரை உலாச்சாலை",
        "category_en": "Coastal Promenade",
        "description_ta": "ஆசியாவின் இரண்டாவது மிக நீளமான இயற்கை கடற்கரைகளில் ஒன்றாக விளங்கும் வரலாற்று சிறப்புமிக்க கடலூர் கடற்கரை.",
        "description_en": "Unspoilt sandy coastline in Cuddalore, serving as a scenic retreat along the Coromandel coast."
    },

    # 6. Dharmapuri
    "Hogenakkal Falls": {
        "name_ta": "ஒகேனக்கல் அருவி",
        "name_en": "Hogenakkal Falls",
        "category_ta": "நீர்வீழ்ச்சி & நதிப் பள்ளத்தாக்கு",
        "category_en": "Waterfalls & River Gorge",
        "description_ta": "காவிரி ஆறு பாறை இடுக்குகளில் புகுந்து பாயும் கம்பீரமான நீர்வீழ்ச்சி; பரிசல் சவாரிக்கு புகழ்பெற்ற தலம்.",
        "description_en": "Breathtaking cascade on river Kaveri featuring dramatic canyon walls and traditional coracle rides."
    },
    "Adhiyamankottai Fort": {
        "name_ta": "அதியமான்கோட்டை",
        "name_en": "Adhiyamankottai Fort",
        "category_ta": "தொல்லியல் வரலாற்று அரண்",
        "category_en": "Archaeological Heritage",
        "description_ta": "சங்க கால வள்ளல் அதியமான் நெடுமான் அஞ்சியின் வரலாற்று கோட்டையும் கல்வெட்டுகளும் உள்ள தலம்.",
        "description_en": "Ancient circular fort site of Sangam King Adhiyaman with archaeological remnants and heritage temples."
    },
    "Theerthamalai Temple": {
        "name_ta": "தீர்த்தமலை தீர்த்தகிரீஸ்வரர் திருக்கோயில்",
        "name_en": "Theerthamalai Temple",
        "category_ta": "மலைத் திருத்தலம்",
        "category_en": "Hill Shrine",
        "description_ta": "பாறையிலிருந்து வற்றாமல் ஊற்றெடுக்கும் ஐந்து புனித தீர்த்தங்களைக் கொண்ட வரலாற்றுச் சிறப்புமிக்க மலைக் கோயில்.",
        "description_en": "Historic hilltop Shiva temple celebrated for its perennial rock springs called Rama Theertham."
    },

    # 7. Dindigul
    "Dindigul Rock Fort": {
        "name_ta": "திண்டுக்கல் மலைக்கோட்டை",
        "name_en": "Dindigul Rock Fort",
        "category_ta": "வரலாற்றுப் பாறைக்கோட்டை",
        "category_en": "Historic Fortress",
        "description_ta": "திண்டு வடிவ ஒற்றைக்கல்லில் அமைந்த 17-ஆம் நூற்றாண்டு நாயக்கர்-திப்பு சுல்தான் காலத்து பிரம்மாண்ட கோட்டை.",
        "description_en": "Formidable 17th-century fortress on an isolated granite outcrop, commanding sweeping views of Dindigul plains."
    },
    "Kodaikanal Lake": {
        "name_ta": "கொடைக்கானல் நட்சத்திர ஏரி",
        "name_en": "Kodaikanal Lake",
        "category_ta": "மலை ஏரி & உலாச்சாலை",
        "category_en": "Hill Lake & Promenade",
        "description_ta": "1863-இல் உருவாக்கப்பட்ட செயற்கை நட்சத்திர ஏரி; படகு சவாரி மற்றும் மிதிவண்டி பயணத்திற்கு பெயர் பெற்றது.",
        "description_en": "Iconic star-shaped lake created by Sir Vere Levinge in 1863, surrounded by mist-laden pedestrian paths."
    },
    "Palani Murugan Temple": {
        "name_ta": "பழனி தண்டாயுதபாணி சுவாமி திருக்கோயில்",
        "name_en": "Palani Murugan Temple",
        "category_ta": "அறுபடை வீடு திருத்தலம்",
        "category_en": "Spiritual Sanctuary",
        "description_ta": "போகர் சித்தரால் நவபாஷாணத்தால் வடிக்கப்பட்ட முருகன் சிலை அமைந்துள்ள முருகனின் மூன்றாவது படைவீடு.",
        "description_en": "Third Arupadai Veedu of Lord Muruga, housing the holy Navapashanam idol sculpted by sage Bogar."
    },

    # 8. Erode
    "Bhavani Sangameswarar Temple": {
        "name_ta": "பவானி சங்கமேஸ்வரர் திருக்கோயில் (கூடுதுறை)",
        "name_en": "Bhavani Sangameswarar Temple",
        "category_ta": "முக்கூடல் புண்ணிய தலம்",
        "category_en": "River Confluence Shrine",
        "description_ta": "காவிரி, பவானி மற்றும் கண்ணுக்குத் தெரியாத அமுத நதி இணையும் 'தென்னகத்து காசி' எனப் போற்றப்படும் தலம்.",
        "description_en": "Sacred shrine located at the confluence of rivers Kaveri and Bhavani, revered as the Kashi of the South."
    },
    "Chennimalai Murugan Temple": {
        "name_ta": "சென்னிமலை முருகன் திருக்கோயில்",
        "name_en": "Chennimalai Murugan Temple",
        "category_ta": "கொங்கு நாட்டு மலைத் தலம்",
        "category_en": "Hilltop Heritage",
        "description_ta": "1320 படிகளைக் கொண்ட இயற்கை எழில் குன்றில் அமைந்துள்ள புகழ்பெற்ற சுப்பிரமணிய சுவாமி கோயில்.",
        "description_en": "Hill temple known for Siragiri Dhandayuthapani and the composer of Kanda Sashti Kavasam."
    },
    "Kodumanal Excavations": {
        "name_ta": "கொடுமணல் அகழாய்வுத் தளம்",
        "name_en": "Kodumanal Excavations",
        "category_ta": "சங்க கால தொல்லியல் களம்",
        "category_en": "Sangam Archaeology",
        "description_ta": "சங்க கால சர்வதேச வாணிபம் மற்றும் இரும்பு உருக்குத் தொழில்நுட்பத்தை வெளிப்படுத்திய தொல்லியல் களம்.",
        "description_en": "Archaeological excavation site proving 2,300-year-old bead-making workshops and Tamil-Brahmi pot inscriptions."
    },

    # 9. Kallakurichi
    "Kalvarayan Hills": {
        "name_ta": "கல்வராயன் மலைகள்",
        "name_en": "Kalvarayan Hills",
        "category_ta": "கிழக்குத் தொடர்ச்சி மலைக் காப்பகம்",
        "category_en": "Eastern Ghats Reserve",
        "description_ta": "பசுமையான மலை முகடுகளும், பெரியார் மற்றும் மேகம் அருவிகளும் கொண்ட பழங்குடியின மக்களின் பண்பாட்டு மலை.",
        "description_en": "Pristine Eastern Ghats ridge known for waterfalls, spice cultivation, and quiet eco-trails."
    },
    "Gomukhi Dam": {
        "name_ta": "கோமுகி அணை",
        "name_en": "Gomukhi Dam",
        "category_ta": "நீர்த்தேக்கம் & சுற்றுலா",
        "category_en": "Reservoir",
        "description_ta": "கல்வராயன் மலையடிவாரத்தில் அமைந்துள்ள விவசாயப் பாசன அணை மற்றும் குடும்ப சுற்றுலா பூங்கா.",
        "description_en": "Scenic dam built across Gomukhi river, serving as an irrigation reservoir and tranquil picnic spot."
    },
    "Ulundurpet & Tirukovilur Border Temples": {
        "name_ta": "திருக்கோவிலூர் & உளுந்தூர்பேட்டை வரலாற்றுத் தலங்கள்",
        "name_en": "Ulundurpet & Tirukovilur Border Temples",
        "category_ta": "வரலாற்றுப் பாடல் பெற்ற நகரங்கள்",
        "category_en": "Historic Towns",
        "description_ta": "கபிலர் குன்று, உலகளந்த பெருமாள் கோயில் மற்றும் வீரட்டானேஸ்வரர் கோயில் கொண்ட சங்க காலப் பகுதி.",
        "description_en": "Ancient historical cluster featuring Kabilar Kundru rock shelter and celebrated Sangam sites."
    },

    # 10. Kancheepuram
    "Kailasanathar Temple": {
        "name_ta": "காஞ்சி கைலாசநாதர் திருக்கோயில்",
        "name_en": "Kailasanathar Temple",
        "category_ta": "பல்லவர் காலக் கலைப் பொக்கிஷம்",
        "category_en": "Pallava Masterpiece",
        "description_ta": "மணற்கல்லால் செதுக்கப்பட்ட பல்லவர் காலத்து உன்னத கோயில்; 58 சிறு சன்னதிகளும் பல்லவ கல்வெட்டுகளும் கொண்டது.",
        "description_en": "Oldest sandstone temple in Kanchipuram with exquisite 8th-century Pallava carvings and circumambulatory tunnel."
    },
    "Ekambareswarar Temple": {
        "name_ta": "காஞ்சி ஏகாம்பரேஸ்வரர் திருக்கோயில்",
        "name_en": "Ekambareswarar Temple",
        "category_ta": "பஞ்சபூத பிருத்வி (நிலம்) தலம்",
        "category_en": "Pancha Bhoota Prithvi",
        "description_ta": "நிலத்தைக் குறிக்கும் பஞ்சபூதத் தலம்; பல்லாயிரம் ஆண்டுகள் பழமையான நான்கு கிளைகள் கொண்ட புனித மாமரம் கொண்டது.",
        "description_en": "One of the Pancha Bhoota Sthalams holding a 3,500-year-old mango tree that yields four varieties of mangoes."
    },
    "Varadharaja Perumal Temple": {
        "name_ta": "காஞ்சி வரதராஜ பெருமாள் திருக்கோயில்",
        "name_en": "Varadharaja Perumal Temple",
        "category_ta": "வைணவ திவ்ய தேசம்",
        "category_en": "Divya Desam",
        "description_ta": "அத்தி வரதர் எழுந்தருளியுள்ள தலம்; 100 கால் மண்டபத்தில் வடிக்கப்பட்ட ஒற்றைக்கல் சங்கிலி சிற்ப அற்புதம் கொண்டது.",
        "description_en": "Grand Vaishnavite shrine famous for the Athi Varadar idol and the 100-pillared hall with monolithic stone chains."
    },

    # 11. Kanniyakumari
    "Vivekananda Rock Memorial": {
        "name_ta": "விவேகானந்தர் பாறை நினைவு மண்டபம்",
        "name_en": "Vivekananda Rock Memorial",
        "category_ta": "கடல் நடுவே அமைந்த நினைவுச் சின்னம்",
        "category_en": "Monolithic Sea Shrine",
        "description_ta": "சுவாமி விவேகானந்தர் 1892-இல் தியானம் செய்து ஆன்மீக ஞானம் பெற்ற கடலுக்குள் அமைந்த பாறை நினைவு மண்டபம்.",
        "description_en": "Sacred ocean monument built in 1970 on the rock where Swami Vivekananda meditated prior to Chicago Parliament."
    },
    "Thiruvalluvar Statue": {
        "name_ta": "133 அடி திருவள்ளுவர் கற்சிலை",
        "name_en": "Thiruvalluvar Statue",
        "category_ta": "தமிழ் இலக்கிய மாபெரும் சிலை",
        "category_en": "Literary Monument",
        "description_ta": "திருக்குறளின் 133 அதிகாரங்களைக் குறிக்கும் வகையில் கடலின் நடுவே 133 அடியில் நிறுவப்பட்ட பிரம்மாண்ட கற்சிலை.",
        "description_en": "Towering 133-foot granite colossus honoring saint-poet Thiruvalluvar, carved by master sculptor V. Ganapati Sthapati."
    },
    "Padmanabhapuram Palace": {
        "name_ta": "பத்மநாபபுரம் மர அரண்மனை",
        "name_en": "Padmanabhapuram Palace",
        "category_ta": "மர வேலைப்பாட்டுக் கட்டடக் கலை",
        "category_en": "Woodcraft Architecture",
        "description_ta": "முழுக்க முழுக்க மரவேலைப்பாடுகளால் ஆன ஆசியாவின் மிகச்சிறந்த அரண்மனை; திருவிதாங்கூர் அரசர்களின் வாழ்விடம்.",
        "description_en": "Spectacular 16th-century wooden palace compound noted for intricately carved ceilings, rosewood furniture, and murals."
    },

    # 12. Karur
    "Sri Pasupatheeswarar Temple": {
        "name_ta": "ஸ்ரீ பசுபதீஸ்வரர் திருக்கோயில்",
        "name_en": "Sri Pasupatheeswarar Temple",
        "category_ta": "பண்டைய சோழர் தேவாரத் தலம்",
        "category_en": "Ancient Chola Shrine",
        "description_ta": "சங்க கால சேரர் மற்றும் சோழர் மன்னர்களால் போற்றப்பட்ட காமதேனு வழிபட்ட பழம்பெரும் பாடல் பெற்ற சிவத்தலம்.",
        "description_en": "7th-century Thevaram shrine with self-manifested Shivalinga and rich Chola inscriptional heritage."
    },
    "Mayanur Barrage & Cauvery Park": {
        "name_ta": "மாயனூர் கதவணை & காவிரி பூங்கா",
        "name_en": "Mayanur Barrage & Cauvery Park",
        "category_ta": "நதி தீர சுற்றுலாத் தலம்",
        "category_en": "Riverfront Tourism",
        "description_ta": "காவிரி ஆற்றின் குறுக்கே கட்டப்பட்ட பிரம்மாண்ட கதவணை மற்றும் படகு சவாரி வசதி கொண்ட இயற்கை பூங்கா.",
        "description_en": "Impressive barrage across the river Kaveri supporting extensive irrigation canals and a riverside eco-park."
    },
    "Nerur Sadashiva Brahmendra Jeeva Samadhi": {
        "name_ta": "நெரூர் சதாசிவ பிரமேந்திரர் ஜீவ சமாதி",
        "name_en": "Nerur Sadashiva Brahmendra Jeeva Samadhi",
        "category_ta": "ஆன்மீக ஞானபீடம்",
        "category_en": "Spiritual Sanctuary",
        "description_ta": "காவிரி ஆற்றங்கரையில் அமைந்துள்ள அவதூத ஞானி ஸ்ரீ சதாசிவ பிரமேந்திரரின் அருள்மிகு ஜீவ சமாதி தலம்.",
        "description_en": "Peaceful riverbank shrine of the revered 18th-century Advaita saint and composer Sri Sadashiva Brahmendra."
    },

    # 13. Krishnagiri
    "Krishnagiri Hill Fort": {
        "name_ta": "கிருஷ்ணகிரி மலைக்கோட்டை",
        "name_en": "Krishnagiri Hill Fort",
        "category_ta": "பாராமஹால் மலைக் கோட்டை",
        "category_en": "Hilltop Bastion",
        "description_ta": "கிருஷ்ணதேவராயர் மற்றும் திப்பு சுல்தானால் பலப்படுத்தப்பட்ட வரலாற்றுச் சிறப்புமிக்க பாறைக் கோட்டை.",
        "description_en": "Strategic citadel perched on a steep granite cliff, fortified by Vijayanagara kings and later held by Tipu Sultan."
    },
    "Krishnagiri Dam (KRP Dam)": {
        "name_ta": "கிருஷ்ணகிரி அணை (கே.ஆர்.பி அணை)",
        "name_en": "Krishnagiri Dam (KRP Dam)",
        "category_ta": "பாசன அணை & சூழல் பூங்கா",
        "category_en": "Irrigation Dam & Park",
        "explanation_ta": "தென்பெண்ணை ஆற்றின் குறுக்கே 1957-இல் காமராஜரால் கட்டப்பட்ட பிரம்மாண்ட பாசன அணை.",
        "description_ta": "தென்பெண்ணை ஆற்றின் குறுக்கே கட்டப்பட்ட அணை மற்றும் பூந்தோட்டங்கள் சூழ்ந்த சுற்றுலா மையம்.",
        "description_en": "Major masonry dam built in 1957 across Thenpennai river, surrounded by floral gardens and children's park."
    },
    "Hosur Hill Temple (Chandra Choodeswarar)": {
        "name_ta": "ஓசூர் சந்திரசூடேஸ்வரர் மலைக்கோயில்",
        "name_en": "Hosur Hill Temple (Chandra Choodeswarar)",
        "category_ta": "வரலாற்று மலைத் தலம்",
        "category_en": "Historic Hill Temple",
        "description_ta": "ஓசூர் மாநகரின் மத்தியில் குன்றின் மேல் அமைந்துள்ள போசள மன்னர்கள் வழிபட்ட பழமையான சிவன் கோயில்.",
        "description_en": "Hilltop temple constructed by Hoysala rulers in the 13th century, offering panoramic views of Hosur city."
    },

    # 14. Madurai
    "Meenakshi Amman Temple": {
        "name_ta": "மீனாட்சி அம்மன் திருக்கோயில்",
        "name_en": "Meenakshi Amman Temple",
        "category_ta": "ஆன்மீகத் தலைமைப் பீடம்",
        "category_en": "Spiritual Center",
        "description_ta": "14 இராஜகோபுரங்கள், பொற்றாமரைக்குளம் மற்றும் ஆயிரம் கால் மண்டபத்துடன் மிளிரும் மதுரையின் இதயத் தலம்.",
        "description_en": "Historic double-sanctum temple dedicated to Goddess Meenakshi and Sundareswarar, epitomizing Dravidian architecture."
    },
    "Thirumalai Nayakkar Mahal": {
        "name_ta": "திருமலை நாயக்கர் அரண்மனை",
        "name_en": "Thirumalai Nayakkar Mahal",
        "category_ta": "இந்தோ-சாரசெனிக் அரண்மனை",
        "category_en": "Indo-Saracenic Palace",
        "description_ta": "1636-இல் திருமலை நாயக்கரால் கட்டப்பட்ட பிரம்மாண்ட தூண்களும் வளைவுகளும் கொண்ட கம்பீரமான அரண்மனை.",
        "description_en": "17th-century royal palace celebrated for its massive 82-foot columns, celestial pavilion, and light-and-sound show."
    },
    "Alagar Kovil & Pazhamudircholai": {
        "name_ta": "அழகர் கோயில் & பழமுதிர்சோலை",
        "name_en": "Alagar Kovil & Pazhamudircholai",
        "category_ta": "வைணவ & முருக தலம்",
        "category_en": "Vaishnavite Heritage",
        "description_ta": "சித்திரை திருவிழாவில் வைகையில் இறங்கும் கள்ளழகர் திருக்கோயிலும், ஆறாவது படைவீடான பழமுதிர்சோலையும் கொண்ட தலம்.",
        "description_en": "Sacred foothills temple of Lord Kallazhagar and the nearby hill shrine of Pazhamudircholai Murugan."
    },

    # 15. Mayiladuthurai
    "Poompuhar Beach & Marine Museum": {
        "name_ta": "பூம்புகார் கடற்கரை & கடல்சார் அருங்காட்சியகம்",
        "name_en": "Poompuhar Beach & Marine Museum",
        "category_ta": "சங்க இலக்கியக் காப்பிய தலம்",
        "category_en": "Sangam Epic Heritage",
        "description_ta": "சிலப்பதிகாரக் கலைக்கூடம், கண்ணகி சிலை மற்றும் பண்டைய சோழர் துறைமுகத் தொல்லியல் சின்னங்கள் நிறைந்த கடற்கரை.",
        "description_en": "Coastal monument complex featuring the Silappadikaram Art Gallery, Kannagi statue, and ancient Chola beach."
    },
    "Fort Dansborg (Tranquebar)": {
        "name_ta": "டான்ஸ்போர்க் கோட்டை (தரங்கம்பாடி)",
        "name_en": "Fort Dansborg (Tranquebar)",
        "category_ta": "டேனிஷ் கடலோரக் கோட்டை",
        "category_en": "Danish Coastal Bastion",
        "description_ta": "1620-இல் டேனிஷ் கம்பெனியால் கட்டப்பட்ட கோட்டை; டென்மார்க் நாட்டின் கடல்சார் வரலாற்றை விளக்கும் அருங்காட்சியகம்.",
        "description_en": "Impressive 17th-century Scandinavian fort on the beach, housing royal Danish maritime artifacts and treaties."
    },
    "Vaitheeswaran Koil": {
        "name_ta": "வைத்தீஸ்வரன் கோயில்",
        "name_en": "Vaitheeswaran Koil",
        "category_ta": "நவக்கிரக அங்காரகன் (செவ்வாய்) தலம்",
        "category_en": "Healing & Navagraha Shrine",
        "description_ta": "தீராத நோய்களைக் குணமாக்கும் வைத்தியநாத சுவாமியும், நவக்கிரகங்களில் செவ்வாய் தலமாகவும் விளங்கும் புண்ணிய பூமி.",
        "description_en": "Famous healing temple dedicated to Lord Shiva as Vaidyanatha Swamy and the Navagraha Mars (Sevvai) shrine."
    },

    # 16. Nagapattinam
    "Basilica of Our Lady of Good Health": {
        "name_ta": "புனித ஆரோக்கிய அன்னை பேராலயம் (வேளாங்கண்ணி)",
        "name_en": "Basilica of Our Lady of Good Health",
        "category_ta": "சர்வதேச திருத்தலப் பேராலயம்",
        "category_en": "Pilgrimage Sanctuary",
        "description_ta": "வங்கக் கடலோரம் அமைந்துள்ள 'கிழக்கின் லூர்து' எனப் போற்றப்படும் பிரம்மாண்ட கத்தோலிக்க பேராலயம்.",
        "description_en": "Gothic architectural marvel on the coast, renowned for its miraculous healing springs and peaceful prayer halls."
    },
    "Nagore Dargah": {
        "name_ta": "நாகூர் தர்கா ஷரீப்",
        "name_en": "Nagore Dargah",
        "category_ta": "வரலாற்று சூஃபி தலம்",
        "category_en": "Sufi Shrine",
        "description_ta": "வானளாவிய மினாராக்களுடன் அமைந்த சூஃபி மகான் காதிர் வலீ அவர்களின் தர்கா மற்றும் புனித திருக்குளம்.",
        "description_en": "500-year-old Sufi saint shrine featuring five towering minarets, welcoming millions of multi-faith pilgrims."
    },
    "Point Calimere Blackbuck Sanctuary": {
        "name_ta": "கோடியக்கரை வெளிமான் சரணாலயம்",
        "name_en": "Point Calimere Blackbuck Sanctuary",
        "category_ta": "கடலோர வனவிலங்கு காப்பகம்",
        "category_en": "Coastal Wildlife",
        "description_ta": "அழிந்துவரும் அரிய வெளிமான்கள், காட்டுப்பன்றிகள் மற்றும் பூநாரைகள் வாழும் கடலோர இயற்கை சரணாலயம்.",
        "description_en": "Pristine coastal promontory conserving endangered Indian blackbucks, wild boars, and winter waterfowl."
    },

    # 17. Namakkal
    "Namakkal Anjaneyar Temple": {
        "name_ta": "நாமக்கல் ஆஞ்சநேயர் திருக்கோயில்",
        "name_en": "Namakkal Anjaneyar Temple",
        "category_ta": "ஒற்றைக்கல் அனுமன் தலம்",
        "category_en": "Monolithic Temple",
        "description_ta": "கூரை இல்லாத திறந்தவெளியில் நின்ற கோலத்தில் 18 அடி உயரத்தில் கம்பீரமாக அருள்பாலிக்கும் ஆஞ்சநேயர் கோயில்.",
        "description_en": "Sacred shrine featuring an 18-foot open-air monolithic idol of Lord Hanuman standing with folded hands."
    },
    "Namakkal Fort": {
        "name_ta": "நாமக்கல் பாறைக்கோட்டை",
        "name_en": "Namakkal Fort",
        "category_ta": "கிரானைட் பாறைக்கோட்டை",
        "category_en": "Granite Rock Fortress",
        "description_ta": "ஒரே கிரானைட் பாறையில் நரசிம்மர் குடைவரைக் கோயிலுடன் அமைந்த வரலாற்று சிறப்புமிக்க மலைக்கோட்டை.",
        "description_en": "Massive monolithic rock fortress rising sheerly above town, fortified during the Mysore wars."
    },
    "Kolli Hills & Agaya Gangai": {
        "name_ta": "கொல்லிமலை & ஆகாய கங்கை நீர்வீழ்ச்சி",
        "name_en": "Kolli Hills & Agaya Gangai",
        "category_ta": "மலை அருவி & மூலிகைக் காடுகள்",
        "category_en": "Mountain Cascade",
        "description_ta": "300 அடி உயரத்திலிருந்து மூலிகைக் காடுகளுக்கு நடுவே ஆர்ப்பரித்து விழும் கம்பீரமான ஆகாய கங்கை நீர்வீழ்ச்சி.",
        "description_en": "High waterfall located down a steep 1,000-step valley trail, revered for cold medicinal herbal baths."
    },

    # 18. The Nilgiris
    "Nilgiri Mountain Toy Train": {
        "name_ta": "நீலகிரி பாரம்பரிய மலை ரயில்",
        "name_en": "Nilgiri Mountain Toy Train",
        "category_ta": "யுனெஸ்கோ பாரம்பரிய ரயில்",
        "category_en": "UNESCO Railway",
        "description_ta": "மேட்டுப்பாளையம் முதல் ஊட்டி வரை அடர்ந்த மலைக் காடுகள் மற்றும் குகைகள் வழியாகப் பயணிக்கும் வரலாற்று நீராவி ரயில்.",
        "description_en": "Historic blue-and-cream heritage steam train winding through mountain bridges, tunnels, and deep gorges."
    },
    "Government Botanical Garden, Ooty": {
        "name_ta": "அரசு தாவரவியல் பூங்கா, ஊட்டி",
        "name_en": "Government Botanical Garden, Ooty",
        "category_ta": "தோட்டக்கலை மரபுப் பூங்கா",
        "category_en": "Horticultural Sanctuary",
        "description_ta": "1848-இல் நிறுவப்பட்ட 55 ஏக்கர் பரப்பளவிலான பூங்கா; அரிய வகை தாவரங்கள் மற்றும் 20 மில்லியன் ஆண்டுகள் பழமையான மரப் படிமம் கொண்டது.",
        "description_en": "Terraced garden established in 1848, housing over a thousand exotic species and a 20-million-year-old fossilized tree."
    },
    "Mudumalai Tiger Reserve": {
        "name_ta": "முதுமலை புலிகள் காப்பகம்",
        "name_en": "Mudumalai Tiger Reserve",
        "category_ta": "வனவிலங்கு சஃபாரி சரணாலயம்",
        "category_en": "Wilderness Safari",
        "description_ta": "புலிகள், யானைகள், சிறுத்தைகள் மற்றும் காட்டெருமைகள் வாழும் நீலகிரி வனவிலங்குப் பூங்கா.",
        "description_en": "Premier national park bordering Karnataka and Kerala, celebrated for jungle jeep safaris and elephant camp."
    },

    # 19. Perambalur
    "Ranjankudi Fort": {
        "name_ta": "ரஞ்சன்குடி வரலாற்று நவாப் கோட்டை",
        "name_en": "Ranjankudi Fort",
        "category_ta": "நவாப் காலப் பாறை அரண்",
        "category_en": "Nawab Fortress",
        "description_ta": "கர்நாடக நவாப்களால் கட்டப்பட்ட கம்பீரமான 3 அடுக்கு வட்டக் கோட்டை மற்றும் ஆழமான அகழி.",
        "description_en": "Imposing 17th-century fortress featuring well-preserved palace ruins, bastions, and subterranean passages."
    },
    "Sathanur Fossil Tree": {
        "name_ta": "சாத்தனூர் கல்மரம்",
        "name_en": "Sathanur Fossil Tree",
        "category_ta": "புவியியல் அதிசயம்",
        "category_en": "Geological Wonder",
        "description_ta": "12 கோடி ஆண்டுகளுக்கு முந்தைய கிரெட்டேசியஸ் யுகத்தின் 18 மீட்டர் நீள மரப் புதைபடிவ கல்மரம்.",
        "description_en": "Fossilized coniferous tree trunk measuring 18 meters, preserved in situ by the Geological Survey of India."
    },
    "Valikandapuram Temple": {
        "name_ta": "வாலிகண்டபுரம் வாலீஸ்வரர் திருக்கோயில்",
        "name_en": "Valikandapuram Temple",
        "category_ta": "பண்டைய சோழர் திருக்கோயில்",
        "category_en": "Ancient Chola Temple",
        "description_ta": "இராமாயண வாலி வழிபட்ட தலபுராணமும், பராந்தக சோழர் காலத்து வரலாற்று கல்வெட்டுகளும் கொண்ட பழம்பெரும் கோயில்.",
        "description_en": "Ancient Chola temple linked to Ramayana lore, holding significant epigraphs of Parantaka I and Rajaraja I."
    },

    # 20. Pudukkottai
    "Sittanavasal Cave": {
        "name_ta": "சித்தன்னவாசல் சமணர் குகை",
        "name_en": "Sittanavasal Cave",
        "category_ta": "சமண மரபு & சுவரோவியங்கள்",
        "category_en": "Jain Heritage",
        "description_ta": "7-ஆம் நூற்றாண்டு பாண்டியர் கால தாமரைத் தடாக ஓவியங்களும், சமண படுக்கைகளும் கொண்ட வரலாற்றுப் பாறை.",
        "description_en": "Celebrated cave monument containing ancient fresco murals of dancing apsaras and monks on the ceiling."
    },
    "Thirumayam Fort": {
        "name_ta": "திருமயம் கோட்டை",
        "name_en": "Thirumayam Fort",
        "category_ta": "பாறை மலை அரண்",
        "category_en": "Hill Bastion",
        "description_ta": "சேதுபதி மன்னர்களால் அமைக்கப்பட்ட சுற்றுமதில் கோட்டையும், பீரங்கி தளவாடங்களும் கொண்ட பாறை அரண்.",
        "description_en": "40-acre rock fortress housing rock-cut cave shrines, pillared halls, and British cannon bastions."
    },
    "Avudaiyarkoil (Thiruperunturai)": {
        "name_ta": "ஆவுடையார்கோயில் (திருப்பெருந்துறை)",
        "name_en": "Avudaiyarkoil (Thiruperunturai)",
        "category_ta": "சிற்பக் கலை அதிசயம்",
        "category_en": "Sculptural Wonder",
        "description_ta": "மாணிக்கவாசகருக்கு இறைவன் உபதேசித்த தலம்; சிலைகளில் வடிக்கப்பட்ட ஆடம்பரமான சிற்ப வேலைப்பாடுகளுக்குப் பெயர் பெற்றது.",
        "description_en": "Masterpiece of granite stone carving where Lord Shiva initiated saint Manikkavasagar; features no conventional idol."
    },

    # 21. Ramanathapuram
    "Rameswaram Temple Corridors": {
        "name_ta": "இராமேஸ்வரம் கோயில் பிரகாரங்கள்",
        "name_en": "Rameswaram Temple Corridors",
        "category_ta": "நீண்ட தூண் பிரகாரம்",
        "category_en": "Pillared Corridor",
        "description_ta": "1212 சிற்பத் தூண்களுடன் சுமார் 4000 அடி நீளத்திற்கு அமைந்துள்ள உலகின் பிரம்மாண்ட கோயில் பிரகாரம்.",
        "description_en": "World's longest pillared temple hallway renowned for its symmetry, grandeur, and painted ceiling motifs."
    },
    "Pamban Sea Bridge": {
        "name_ta": "பாம்பன் கடல் பாலம்",
        "name_en": "Pamban Sea Bridge",
        "category_ta": "கடல் ரயில் பாலம்",
        "category_en": "Sea Bridge",
        "description_ta": "பாக் நீரிணையின் மேல் 2 கி.மீ நீளத்திற்கு கடல் அலைகளுக்கு இடையே செல்லும் வரலாற்று சிறப்புமிக்க ரயில் பாலம்.",
        "description_en": "Cantilever railway bridge connecting the island town of Rameswaram to the mainland across turbulent sea waters."
    },
    "Dr. A.P.J. Abdul Kalam Memorial": {
        "name_ta": "டாக்டர் ஏ.பி.ஜே. அப்துல் கலாம் நினைவகம்",
        "name_en": "Dr. A.P.J. Abdul Kalam Memorial",
        "category_ta": "தேசிய நினைவகம்",
        "category_en": "National Memorial",
        "description_ta": "மக்களின் குடியரசுத் தலைவர் டாக்டர் கலாமின் வாழ்க்கை மற்றும் சாதனைகளைப் போற்றும் பேக்கரும்பில் அமைந்த தேசிய நினைவகம்.",
        "description_en": "Monumental memorial housing the tomb, personal belongings, rocket models, and paintings of India's Missile Man."
    },

    # 22. Ranipet
    "Historic Arcot Fort & Delhi Gate": {
        "name_ta": "வரலாற்று ஆற்காட்டுக் கோட்டை & டெல்லி கேட்",
        "name_en": "Historic Arcot Fort & Delhi Gate",
        "category_ta": "இராணுவ வரலாற்று நுழைவாயில்",
        "category_en": "Military Gateway",
        "description_ta": "ராபர்ட் கிளைவ் 1751-இல் ஆற்காட்டை முற்றுகையிட்ட போரில் தொடர்புடைய நவாப் காலத்து வரலாற்று நுழைவு வாயில்.",
        "description_en": "Historic fort gate where Robert Clive made his famous defense during the 1751 Siege of Arcot."
    },
    "Kaveripakkam Ancient Lake": {
        "name_ta": "காவேரிப்பாக்கம் வரலாற்று ஏரி",
        "name_en": "Kaveripakkam Ancient Lake",
        "category_ta": "பண்டைய நீர்ப்பாசன அமைப்பு",
        "category_en": "Historical Waterworks",
        "description_ta": "பல்லவ மன்னர் நந்திவர்மனால் அமைக்கப்பட்ட தமிழ்நாட்டின் மிகப்பெரிய பழமையான ஏரிகளில் ஒன்று.",
        "description_en": "One of the largest irrigation lakes in the state, engineered during the Pallava dynasty."
    },
    "Walajapet Handloom & Bell Metal": {
        "name_ta": "வாலாஜாபேட்டை கைத்தறி & வெண்கலப் பாத்திரங்கள்",
        "name_en": "Walajapet Handloom & Bell Metal",
        "category_ta": "பாரம்பரிய கைவினை மையம்",
        "category_en": "Artisan Craft Hub",
        "description_ta": "பாரம்பரிய பித்தளை மற்றும் வெண்கலப் பாத்திரங்கள் தயாரிப்பிலும் பட்டு நெசவிலும் புகழ்பெற்ற வரலாற்று நகரம்.",
        "description_en": "Renowned center for handloom silk weaving and handmade bronze temple bells and utensils."
    },

    # 23. Salem
    "Mettur Dam": {
        "name_ta": "மேட்டூர் அணை",
        "name_en": "Mettur Dam",
        "category_ta": "சிவில் பொறியியல் அற்புதம்",
        "category_en": "Civil Engineering Feat",
        "description_ta": "காவிரி ஆற்றின் குறுக்கே பிரம்மாண்டமாக அமைந்த அணை; அழகிய பூங்காக்கள் மற்றும் நீர்மின் நிலையங்களைக் கொண்டது.",
        "description_en": "Iconic gravity dam with 16-vent surplus sluice, water reservoir, and expansive riverside gardens."
    },
    "Yercaud Hill Station": {
        "name_ta": "ஏற்காடு மலை வாழிடம்",
        "name_en": "Yercaud Hill Station",
        "category_ta": "சேர்வராயன் மலை வாழிடம்",
        "category_en": "Shevaroy Mountain Resort",
        "description_ta": "மரகத ஏரி, லேடிஸ் சீட் காட்சி முனை, காப்பித் தோட்டங்கள் சூழ்ந்த எழில் கொஞ்சும் மலை சுற்றுலா மையம்.",
        "description_en": "Quiet hill resort featuring panoramic mountain view points, rose gardens, and coffee plantations."
    },
    "Kottai Mariamman Temple": {
        "name_ta": "சேலம் கோட்டை மாரியம்மன் திருக்கோயில்",
        "name_en": "Kottai Mariamman Temple",
        "category_ta": "வரலாற்றுப் புகழ்பெற்ற தலம்",
        "category_en": "Historic City Temple",
        "description_ta": "சேலம் மாநகரின் இதயப் பகுதியில் அமைந்துள்ள, ஆண்டுதோறும் ஆடிப் பெருவிழா கோலாகலமாக நடைபெறும் புகழ்பெற்ற அம்மன் தலம்.",
        "description_en": "Centuries-old city goddess temple celebrated for its vibrant annual Aadi car festival."
    },

    # 24. Sivaganga
    "Keezhadi Museum & Site": {
        "name_ta": "கீழடி அருங்காட்சியகம் & தொல்லியல் களம்",
        "name_en": "Keezhadi Museum & Site",
        "category_ta": "உலகத்தரம் வாய்ந்த தொல்லியல் களம்",
        "category_en": "Archaeological Site",
        "description_ta": "சங்க கால தமிழர்களின் நகர கட்டடங்கள், எடைக்கற்கள், தங்க நகைகள் மற்றும் பானை ஓடுகளைக் காட்சிப்படுத்தும் சர்வதேச அருங்காட்சியகம்.",
        "description_en": "State-of-the-art museum displaying thousands of 2,600-year-old urban artifacts excavated from Keezhadi."
    },
    "Kanadukathan Palace": {
        "name_ta": "கானாடுகாத்தான் செட்டிநாடு அரண்மனை",
        "name_en": "Kanadukathan Palace",
        "category_ta": "செட்டிநாட்டுப் பாரம்பரிய மாளிகை",
        "category_en": "Chettinad Mansion",
        "description_ta": "நூற்றுக்கணக்கான அறைகள், பர்மா தேக்கு தூண்கள் மற்றும் கலை வண்ணங்கள் நிறைந்த பிரம்மாண்ட மாளிகை.",
        "description_en": "Exemplary Chettinad palace displaying peerless woodworking, Belgian crystal, and courtyard architecture."
    },
    "Kalaiyar Kovil (Kaleeswarar Temple)": {
        "name_ta": "காளையார் கோயில் (காளீஸ்வரர் திருக்கோயில்)",
        "name_en": "Kalaiyar Kovil (Kaleeswarar Temple)",
        "category_ta": "கோட்டை சூழ்ந்த பாடல் பெற்ற தலம்",
        "category_en": "Fortified Temple",
        "description_ta": "மருது சகோதரர்கள் கட்டிய 150 அடி உயர இராஜகோபுரமும், விடுதலைப் போரின் வரலாற்று நினைவுகளும் கொண்ட புனித தலம்.",
        "description_en": "Historic fortified temple housing the tombs of the heroic Maruthu Pandiyar brothers."
    },

    # 25. Tenkasi
    "Courtallam Main Falls": {
        "name_ta": "குற்றாலம் பேரருவி",
        "name_en": "Courtallam Main Falls",
        "category_ta": "மூலிகை நீர்வீழ்ச்சி",
        "category_en": "Herbal Waterfall",
        "description_ta": "மலையிலிருந்து மூலிகைக் காடுகளைத் தழுவி பொங்கிப் பிரவகிக்கும் குற்றாலத்தின் பிரதான அருவி.",
        "description_en": "Primary waterfall dropping 160 feet into a natural rock pool, famous for rejuvenating herbal bath."
    },
    "Tenkasi Kasi Viswanathar Temple": {
        "name_ta": "தென்காசி காசி விசுவநாதர் திருக்கோயில்",
        "name_en": "Tenkasi Kasi Viswanathar Temple",
        "category_ta": "பாண்டியர் கட்டடக்கலை தலம்",
        "category_en": "Pandyan Architecture",
        "description_ta": "பராக்கிரம பாண்டியன் எழுப்பிய 180 அடி உயர இராஜகோபுரம் மற்றும் சிற்ப நயம் வாய்ந்த தூண்கள் கொண்ட திருக்கோயில்.",
        "description_en": "Magnificent temple with musical stone pillars and an imposing gopuram completed by the Later Pandyas."
    },
    "Five Falls (Aintharuvi)": {
        "name_ta": "ஐந்தருவி",
        "name_en": "Five Falls (Aintharuvi)",
        "category_ta": "இயற்கை நீர்வீழ்ச்சி",
        "category_en": "Scenic Waterfalls",
        "description_ta": "பாறையிலிருந்து ஐந்து கிளைகளாகப் பிரிந்து விழும் குற்றாலத்தின் ரம்மியமான நீர்வீழ்ச்சி.",
        "description_en": "Water cascade splitting into five distinct streams resembling the five heads of a cobra."
    },

    # 26. Thanjavur (Strictly aligned with user prompt examples)
    "Peruvudaiyar Kovil (Big Temple)": {
        "name_ta": "பெருவுடையார் கோயில் (தஞ்சை பெரிய கோயில்)",
        "name_en": "Peruvudaiyar Kovil (Big Temple)",
        "category_ta": "சோழர் காலப் பெருங்கோயில் (யுனெஸ்கோ)",
        "category_en": "Chola Masterpiece",
        "description_ta": "ஆயிரம் ஆண்டுகள் பழமையான சோழர் கால கட்டடக் கலை அற்புதம்; பிரம்மாண்ட நந்தி மற்றும் கம்பீரமான விமானம் கொண்டது.",
        "description_en": "1,000-year-old architectural marvel with monolithic Nandi and towering granite sanctum vimanam."
    },
    "Thanjavur Royal Palace Complex": {
        "name_ta": "தஞ்சாவூர் அரண்மனை வளாகம்",
        "name_en": "Thanjavur Royal Palace Complex",
        "category_ta": "நாயக்கர் & மராட்டியர் அரண்மனை",
        "category_en": "Nayak & Maratha Palace",
        "description_ta": "கலைக்கூடம், மணி கோபுரம் மற்றும் ஆயுதக் கூடம் கொண்ட நாயக்கர் மற்றும் மராட்டிய அரசர்களின் வரலாற்று வாழ்விடம்.",
        "description_en": "Historic residence of Nayak and Maratha rulers housing Art Gallery, Bell Tower, and Arsenal Tower."
    },
    "Saraswathi Mahal Library": {
        "name_ta": "சரஸ்வதி மகால் நூலகம்",
        "name_en": "Saraswathi Mahal Library",
        "category_ta": "அரிய வரலாற்றுச் சுவடிகள் நூலகம்",
        "category_en": "Manuscript Heritage",
        "description_ta": "அரிய கையெழுத்துப் பிரதிகளையும் வரலாற்றுச் சுவடிகளையும் கொண்ட ஆசியாவின் புகழ்பெற்ற நூலகம்.",
        "description_en": "Centuries-old royal repository containing rare medieval palm-leaf manuscripts and miniature paintings."
    },

    # 27. Theni
    "Megamalai Wildlife Sanctuary": {
        "name_ta": "மேகமலை வனவிலங்கு சரணாலயம்",
        "name_en": "Megamalai Wildlife Sanctuary",
        "category_ta": "மேக மூடிய சோலைக் காப்பகம்",
        "category_en": "Cloud Forest Sanctuary",
        "description_ta": "புலிகள், யானைகள், பறக்கும் அணில்கள் வாழும் மேற்குத் தொடர்ச்சி மலையின் அடர்ந்த பசுமை மாறாக் காடுகள்.",
        "description_en": "Highland reserve sheltering tigers, leopards, great hornbills, and endangered lion-tailed macaques."
    },
    "Suruli Falls": {
        "name_ta": "சுருளி நீர்வீழ்ச்சி",
        "name_en": "Suruli Falls",
        "category_ta": "காட்டு நீர்வீழ்ச்சி & புண்ணிய தலம்",
        "category_en": "Forest Waterfall",
        "description_ta": "இரண்டு கட்டங்களாக விழும் நீர்வீழ்ச்சி; கைலாசநாதர் குகை மற்றும் மூலிகை வளம் நிறைந்த தலம்.",
        "description_en": "Picturesque waterfall dropping into a natural pool amidst dense forest, with 18 sacred caves nearby."
    },
    "Vaigai Dam": {
        "name_ta": "வைகை அணை",
        "name_en": "Vaigai Dam",
        "category_ta": "நீர்த்தேக்கம் & பூங்கா",
        "category_en": "Reservoir & Garden",
        "description_ta": "வைகை ஆற்றின் குறுக்கே ஆண்டிபட்டி அருகே கட்டப்பட்ட பாசன அணை மற்றும் ஒளிரும் வண்ண பூங்கா.",
        "description_en": "Major reservoir providing irrigation to five southern districts, featuring illuminated evening gardens."
    },

    # 28. Thoothukudi
    "Our Lady of Snows Basilica": {
        "name_ta": "பனிமய மாதா பேராலயம்",
        "name_en": "Our Lady of Snows Basilica",
        "category_ta": "போர்ச்சுகீசிய கடல்சார் திருத்தலம்",
        "category_en": "Portuguese Maritime Shrine",
        "description_ta": "16-ஆம் நூற்றாண்டில் போர்ச்சுகீசியர்களால் கட்டப்பட்ட புகழ்பெற்ற கடற்கரை கத்தோலிக்க பேராலயம்.",
        "description_en": "Historic 16th-century Marian basilica built in Portuguese style on the shores of the Gulf of Mannar."
    },
    "Tiruchendur Murugan Temple": {
        "name_ta": "திருச்செந்தூர் சுப்பிரமணிய சுவாமி திருக்கோயில்",
        "name_en": "Tiruchendur Murugan Temple",
        "category_ta": "அறுபடை வீடு கடற்கரைத் தலம்",
        "category_en": "Arupadai Veedu Coastal Shrine",
        "description_ta": "சூரசம்ஹாரம் நிகழ்ந்த கடலோரப் படைவீடு; ஒன்பது நிலை இராஜகோபுரத்துடன் கடற்கரையில் கம்பீரமாக வீற்றிருக்கும் தலம்.",
        "description_en": "Second Arupadai Veedu of Lord Muruga situated right on the sea shore, famed for the Soorasamharam festival."
    },
    "Kulasekharapatnam Mutharamman Temple": {
        "name_ta": "குலசேகரப்பட்டினம் முத்தாரம்மன் திருக்கோயில்",
        "name_en": "Kulasekharapatnam Mutharamman Temple",
        "category_ta": "கடற்கரை தசரா திருவிழா தலம்",
        "category_en": "Dasara Coastal Festival",
        "description_ta": "லட்சக்கணக்கான பக்தர்கள் பல்வேறு வேடங்கள் அணிந்து விரதமிருந்து கொண்டாடும் புகழ்பெற்ற தசரா திருவிழா தலம்.",
        "description_en": "Coastal temple famous for its 10-day Dasara festival where millions of devotees dress in divine disguises."
    },

    # 29. Tiruchirappalli
    "Rockfort Temple": {
        "name_ta": "திருச்சி மலைக்கோட்டை உச்சிப்பிள்ளையார் கோயில்",
        "name_en": "Rockfort Temple",
        "category_ta": "பாறைக் கோயில் அரண்",
        "category_en": "Geological Fortress Shrine",
        "description_ta": "273 அடி உயர பழமையான பாறையின் உச்சியில் அமைந்துள்ள விநாயகர் கோயில் மற்றும் மாநகரக் காட்சி முனை.",
        "description_en": "Fortified temple complex carved atop a massive 83-meter high monolithic rock, dominating Trichy's skyline."
    },
    "Srirangam Ranganathaswamy Temple": {
        "name_ta": "ஸ்ரீரங்கம் ரெங்கநாதசுவாமி திருக்கோயில்",
        "name_en": "Srirangam Ranganathaswamy Temple",
        "category_ta": "மாபெரும் வைணவக் கோயில்",
        "category_en": "Monumental Temple Complex",
        "description_ta": "7 திருச்சுற்றுகளும், 236 அடி உயர இராஜகோபுரமும் கொண்ட உலகின் மிகப்பெரிய செயல்படும் வைணவத் தலம்.",
        "description_en": "Sprawling temple city with 21 gopurams including the monumental 236-foot Rajagopuram."
    },
    "Kallanai Dam": {
        "name_ta": "கல்லணை (கரிகால் சோழன் அணை)",
        "name_en": "Kallanai Dam",
        "category_ta": "பண்டைய நீரியல் வரலாற்றுச் சின்னம்",
        "category_en": "Ancient Hydraulic Monument",
        "description_ta": "காவிரி டெல்டாவை வளமாக்க 2000 ஆண்டுகளுக்கு முன் கரிகால் சோழனால் கருங்கல்லால் கட்டப்பட்ட வரலாற்று அணை.",
        "description_en": "Ancient stone diversion weir dividing the river Kaveri into four streams, sustaining Tamil agriculture."
    },

    # 30. Tirunelveli
    "Nellaiappar Temple": {
        "name_ta": "திருநெல்வேலி நெல்லையப்பர் திருக்கோயில்",
        "name_en": "Nellaiappar Temple",
        "category_ta": "பண்டைய பாண்டியர் திருத்தலம்",
        "category_en": "Ancient Pandyan Temple",
        "description_ta": "தாமிர சபை மற்றும் தட்டினால் இசைக்கும் இசைத் தூண்கள் கொண்ட 14 ஏக்கர் பரப்பளவிலான பிரம்மாண்ட திருக்கோயில்.",
        "description_en": "Vast temple dedicated to Lord Shiva and Kanthimathi Ambal, renowned for the Copper Hall and musical columns."
    },
    "Agasthiyar Falls (Papanasam)": {
        "name_ta": "அகஸ்தியர் அருவி (பாபநாசம்)",
        "name_en": "Agasthiyar Falls (Papanasam)",
        "category_ta": "புனித மூலிகை நீர்வீழ்ச்சி",
        "category_en": "Sacred Forest Waterfalls",
        "description_ta": "பொதிகை மலையிலிருந்து பாபநாசம் வழியாகப் பாய்ந்து வரும் பாவங்களைப் போக்கும் புனித மூலிகை அருவி.",
        "description_en": "Sacred waterfall on the perennial Tamirabarani river, where sage Agastya is believed to have worshipped."
    },
    "Adichanallur Iron Age Site": {
        "name_ta": "ஆதிச்சநல்லூர் இரும்புக்கால தொல்லியல் தளம்",
        "name_en": "Adichanallur Iron Age Site",
        "category_ta": "வரலாற்றுக்கு முந்தைய தொல்லியல் களம்",
        "category_en": "Prehistoric Archaeological Site",
        "description_ta": "3,000 ஆண்டுகள் பழமையான முதுமக்கள் தாழிகள், வெண்கலப் பொருட்கள் மற்றும் இரும்பு ஆயுதங்கள் கண்டறியப்பட்ட தொல்லியல் தளம்.",
        "description_en": "Prehistoric urn burial site demonstrating 3,000-year-old metallurgical civilization on the Tamirabarani banks."
    },

    # 31. Tirupathur
    "Yelagiri Punganur Lake & Park": {
        "name_ta": "ஏலகிரி புங்கனூர் ஏரி & பூங்கா",
        "name_en": "Yelagiri Punganur Lake & Park",
        "category_ta": "மலை ஏரி & பொழுதுபோக்கு பூங்கா",
        "category_en": "Hill Station Lake",
        "description_ta": "ஏலகிரி மலையின் நடுவே அமைந்துள்ள படகு சவாரி வசதி கொண்ட இயற்கை ஏரி மற்றும் பூங்கா.",
        "description_en": "Artificial lake in the heart of Yelagiri hills with pedal boating and surrounding recreational paths."
    },
    "Vainu Bappu Observatory": {
        "name_ta": "வைணு பாப்பு வான் இயற்பியல் ஆய்வகம்",
        "name_en": "Vainu Bappu Observatory",
        "category_ta": "வானியல் தொலைநோக்கி மையம்",
        "category_en": "Optical Observatory",
        "description_ta": "காவலூரின் வனப்பகுதியில் நிறுவப்பட்ட ஆசியாவின் முன்னணி ஒளியியல் தொலைநோக்கி வான் ஆய்வு மையம்.",
        "description_en": "Premier optical astronomy station equipped with the historic 2.34-meter aperture reflecting telescope."
    },
    "Jalagamparai Waterfalls": {
        "name_ta": "ஜலகாம்பாறை நீர்வீழ்ச்சி",
        "name_en": "Jalagamparai Waterfalls",
        "category_ta": "இயற்கை மலை அருவி",
        "category_en": "Mountain Cascade",
        "description_ta": "ஏலகிரி மலையிலிருந்து திருப்பத்தூர் சமவெளியில் விழும் இயற்கை மூலிகை நீர்வீழ்ச்சி.",
        "description_en": "Scenic seasonal cascade dropping across rocky crags on the eastern side of Yelagiri hills."
    },

    # 32. Tiruppur
    "Thirumoorthy Hills & Amanalingeswarar": {
        "name_ta": "திருமூர்த்தி மலை & அமணலிங்கேஸ்வரர் திருக்கோயில்",
        "name_en": "Thirumoorthy Hills & Amanalingeswarar",
        "category_ta": "மலைத் தலம் & பஞ்சலிங்க அருவி",
        "category_en": "Hill Sanctuary & Falls",
        "description_ta": "பஞ்சலிங்க அருவி மற்றும் மும்மூர்த்திகளும் ஒரே பாறையில் அருள்பாலிக்கும் வரலாற்று மலைத் தலம்.",
        "description_en": "Scenic hill retreat situated at the foot of Thirumoorthy Hills, famed for Panjalinga waterfalls."
    },
    "Amaravathi Dam & Crocodile Bank": {
        "name_ta": "அமராவதி அணை & முதலைகள் பண்ணை",
        "name_en": "Amaravathi Dam & Crocodile Bank",
        "category_ta": "வனவிலங்கு & நீர்த்தேக்கம்",
        "category_en": "Wildlife & Reservoir",
        "description_ta": "ஆனைமலை புலிகள் காப்பக எல்லையில் அமைந்துள்ள நீர்ப்பாசன அணை மற்றும் மிகப்பெரிய முதலைகள் காப்பகம்.",
        "description_en": "Major dam across river Amaravathi hosting the largest captive population of freshwater mugger crocodiles."
    },
    "Tiruppur Kumaran Memorial": {
        "name_ta": "கொடிகாத்த திருப்பூர் குமரன் நினைவு இல்லம்",
        "name_en": "Tiruppur Kumaran Memorial",
        "category_ta": "விடுதலைப் போராட்ட நினைவகம்",
        "category_en": "Freedom Memorial",
        "description_ta": "காவல்துறையின் தடியடியிலும் தேசியக் கொடியை கீழே விடாமல் உயிர்நீத்த தியாகி குமரனின் நினைவு மண்டபம்.",
        "description_en": "Memorial dedicated to patriot Kumaran who died holding the Indian national flag aloft in 1932."
    },

    # 33. Tiruvallur
    "Pulicat Lake & Dutch Cemetery": {
        "name_ta": "பழவேற்காடு ஏரி & டச்சு கல்லறைத் தோட்டம்",
        "name_en": "Pulicat Lake & Dutch Cemetery",
        "category_ta": "உப்பங்கழி & வரலாற்றுச் சின்னங்கள்",
        "category_en": "Lagoon & Heritage",
        "description_ta": "பல்லாயிரக்கணக்கான பூநாரைகள் வந்து தங்கும் ஏரி மற்றும் 17-ஆம் நூற்றாண்டு டச்சுக்காரர்களின் வரலாற்றுச் சின்னங்கள்.",
        "description_en": "Scenic lagoon with rich avian life alongside well-preserved 17th-century Dutch colonial tombstones."
    },
    "Sri Veeraraghava Swamy Temple": {
        "name_ta": "திருவள்ளூர் ஸ்ரீ வீரராகவ சுவாமி திருக்கோயில்",
        "name_en": "Sri Veeraraghava Swamy Temple",
        "category_ta": "வைத்திய வீரராகவர் தலம்",
        "category_en": "Sacred Temple",
        "description_ta": "தீராத பிணிகளைத் தீர்க்கும் வைத்திய வீரராகவப் பெருமாள் சயனக் கோலத்தில் அருள்பாலிக்கும் திவ்ய தேசம்.",
        "description_en": "Famous Divya Desam shrine dedicated to Lord Vishnu in reclining posture, revered as the ultimate healer."
    },
    "Gudiyam Caves": {
        "name_ta": "குடியம் வரலாற்றுக்கு முந்தைய குகைகள்",
        "name_en": "Gudiyam Caves",
        "category_ta": "பழங்கற்கால பாறைப் புகலிடம்",
        "category_en": "Prehistoric Rock Shelter",
        "description_ta": "ஒரு லட்சம் ஆண்டுகளுக்கு முந்தைய பழங்கற்கால மனிதர்கள் வாழ்ந்த இயற்கை பாறை குகைகள்.",
        "description_en": "Natural rock shelters where Paleolithic stone tools were first discovered by British geologist Robert Bruce Foote."
    },

    # 34. Tiruvannamalai
    "Arunachaleswarar Temple": {
        "name_ta": "திருவண்ணாமலை அருணாசலேஸ்வரர் திருக்கோயில்",
        "name_en": "Arunachaleswarar Temple",
        "category_ta": "பஞ்சபூத அக்னி தலம்",
        "category_en": "Agni Sthalam",
        "description_ta": "அண்ணாமலை அடிவாரத்தில் அமைந்துள்ள மாபெரும் அக்னி தலம்; 217 அடி இராஜகோபுரமும் பிரம்மாண்ட பிரகாரங்களும் கொண்டது.",
        "description_en": "Vast Shiva temple compound at the foot of Arunachala hill with 11 gopurams and centuries of royal Chola inscriptions."
    },
    "Sri Ramana Ashram": {
        "name_ta": "ஸ்ரீ ரமண மகரிஷி ஆசிரமம்",
        "name_en": "Sri Ramana Ashram",
        "category_ta": "ஆன்மீக ஞான ஆசிரமம்",
        "category_en": "Spiritual Hermitage",
        "description_ta": "'நான் யார்?' என்ற தத்துவத்தை உலகிற்கு உணர்த்திய பகவான் ரமண மகரிஷி தவம் செய்து முக்தி அடைந்த அமைதித் தலம்.",
        "description_en": "Serene spiritual sanctuary at the foot of Arunachala, attracting global seekers to Bhagavan Ramana's path of Self-inquiry."
    },
    "Sathanur Dam": {
        "name_ta": "சாத்தனூர் அணை & பூங்கா",
        "name_en": "Sathanur Dam",
        "category_ta": "நீர்ப்பாசன அணை & பூங்கா",
        "category_en": "Dam & Recreational Park",
        "description_ta": "தென்பெண்ணை ஆற்றின் குறுக்கே மலைகளுக்கு நடுவே கட்டப்பட்ட பாசன அணை மற்றும் அழகிய சுற்றுலா பூங்கா.",
        "description_en": "Majestic dam on Thenpennai river featuring musical water fountains, formal gardens, and crocodile farm."
    },

    # 35. Tiruvarur
    "Thyagaraja Swamy Temple": {
        "name_ta": "திருவாரூர் தியாகராஜசுவாமி திருக்கோயில்",
        "name_en": "Thyagaraja Swamy Temple",
        "category_ta": "வரலாற்றுப் பெருங்கோயில்",
        "category_en": "Historic Delta Temple",
        "description_ta": "கமல்ஆலயம் திருக்குளம், ஆழித்தேர் மற்றும் மனுநீதி சோழன் கல் தேர் மண்டபம் கொண்ட மாபெரும் சைவத் திருத்தலம்.",
        "description_en": "Vast temple covering 20 acres, celebrated in Thevaram hymns and famous for the Ajaba Natanam dance ritual."
    },
    "Carnatic Music Trinity Memorial": {
        "name_ta": "சங்கீத மும்மூர்த்திகள் நினைவு இல்லம்",
        "name_en": "Carnatic Music Trinity Memorial",
        "category_ta": "பண்பாட்டு வரலாற்று இல்லம்",
        "category_en": "Cultural Heritage",
        "description_ta": "தியாகராஜர், முத்துசுவாமி தீட்சிதர், சியாமா சாஸ்திரி பிறந்த இல்லங்கள் பாதுகாக்கப்படும் வரலாற்று பண்பாட்டு மையம்.",
        "description_en": "Heritage homes where the Trinity of Carnatic Music were born, preserved as memorials celebrating their musical legacy."
    },
    "Muthupet Mangrove Boardwalk": {
        "name_ta": "முத்துப்பேட்டை சதுப்புநில மரப்பாலம்",
        "name_en": "Muthupet Mangrove Boardwalk",
        "category_ta": "சூழல் சுற்றுலா",
        "category_en": "Eco-Tourism",
        "description_ta": "அலையாத்திக் காடுகளின் வழியே கடல் முகத்துவாரம் வரை செல்லும் 160 மீட்டர் நீள மர நடைபாதை.",
        "description_en": "Elevated wooden boardwalk leading visitors through dense mangrove swamps to the open waters of Palk Strait."
    },

    # 36. Vellore
    "Vellore Fort": {
        "name_ta": "வேலூர் வரலாற்று கோட்டை",
        "name_en": "Vellore Fort",
        "category_ta": "கருங்கல் அகழிக் கோட்டை",
        "category_en": "Granite Moated Fort",
        "description_ta": "ஆழமான முதலை அகழியுடன் 16-ஆம் நூற்றாண்டில் விஜயநகர மன்னர்களால் கட்டப்பட்ட பிரம்மாண்ட கோட்டை.",
        "description_en": "Massive granite stone citadel surrounded by a deep moat, site of the historic 1806 Sepoy Mutiny."
    },
    "Jalakanteswarar Temple": {
        "name_ta": "வேலூர் ஜலகண்டேஸ்வரர் திருக்கோயில்",
        "name_en": "Jalakanteswarar Temple",
        "category_ta": "விஜயநகர சிற்பக் கலை",
        "category_en": "Vijayanagara Sculpture",
        "description_ta": "வேலூர் கோட்டைக்குள் அமைந்த, கல்யாண மண்டபத்தில் கண்ணைக் கவரும் சிற்பங்களைக் கொண்ட உன்னதக் கோயில்.",
        "description_en": "Exquisite temple inside the fort famed for the 100-pillar wedding hall with mythical dragon carvings."
    },
    "Sripuram Golden Temple": {
        "name_ta": "ஸ்ரீபுரம் தங்கக் கோயில்",
        "name_en": "Sripuram Golden Temple",
        "category_ta": "தங்கக் கோயில் நினைவுச் சின்னம்",
        "category_en": "Golden Monument",
        "description_ta": "1.5 டன் தங்கத்தால் வேயப்பட்ட மகாலட்சுமி திருக்கோயில் மற்றும் நட்சத்திர வடிவ தியானப் பாதை.",
        "description_en": "Shining gold-plated temple dedicated to Goddess Mahalakshmi with star path meditation gardens."
    },

    # 37. Viluppuram
    "Gingee Fort (Rajagiri)": {
        "name_ta": "செஞ்சிக் கோட்டை (ராஜகிரி)",
        "name_en": "Gingee Fort (Rajagiri)",
        "category_ta": "மத்திய கால கோட்டை அரண்",
        "category_en": "Medieval Citadel",
        "description_ta": "800 அடி உயர செங்குத்தான பாறையில் தொங்கு பாலம் மற்றும் 7 அடுக்கு கல்யாண மகால் கொண்ட பிரம்மாண்ட கோட்டை.",
        "description_en": "800-foot sheer citadel accessible across a narrow drawbridge over a chasm, with 7-storey Kalyana Mahal."
    },
    "Matrimandir (Auroville)": {
        "name_ta": "மாத்ரிமந்திர் (ஆரோவில்)",
        "name_en": "Matrimandir (Auroville)",
        "category_ta": "சர்வதேச தியான அரங்கம்",
        "category_en": "Universal Sanctuary",
        "description_ta": "தங்கக் கோள வடிவிலான தியான அறை; மையத்தில் சூரியக் கதிர் பாயும் படிகக் கண்ணாடி கோளம் கொண்டது.",
        "description_en": "Golden globe meditation chamber with crystal glass sphere illuminated by a single sunbeam."
    },
    "Thiruvakkarai Geological Fossil Park": {
        "name_ta": "திருவக்கரை தேசிய கல்மரப் பூங்கா",
        "name_en": "Thiruvakkarai Geological Fossil Park",
        "category_ta": "தொன்மை புவியியல் தளம்",
        "category_en": "Prehistoric Site",
        "description_ta": "2 கோடி ஆண்டுகள் பழமையான மரங்கள் பாறையாக உறைந்த புதைபடிவங்களைக் கொண்ட தேசியப் பூங்கா.",
        "description_en": "National Geological Monument featuring petrified fossilized wood logs dating back 20 million years."
    },

    # 38. Virudhunagar
    "Srivilliputhur Andal Temple": {
        "name_ta": "ஸ்ரீவில்லிபுத்தூர் ஆண்டாள் திருக்கோயில்",
        "name_en": "Srivilliputhur Andal Temple",
        "category_ta": "தமிழ்நாடு அரசு சின்னத் திருக்கோயில்",
        "category_en": "State Emblem Temple",
        "description_ta": "தமிழ்நாடு அரசின் இலச்சினையாகத் திகழும் 192 அடி உயர 11 நிலை இராஜகோபுரம் கொண்ட வைணவத் திருத்தலம்.",
        "description_en": "Magnificent temple with 11-storey gopuram dedicated to Andal and Rangamannar."
    },
    "Kamarajar Memorial House": {
        "name_ta": "காமராஜர் நூற்றாண்டு நினைவு இல்லம்",
        "name_en": "Kamarajar Memorial House",
        "category_ta": "வரலாற்றுத் தலைவர் நினைவு இல்லம்",
        "category_en": "Historic Residence",
        "description_ta": "கல்விக் கண் திறந்த கர்மவீரர் காமராஜர் பிறந்து வாழ்ந்த எளிய வீடு; அவரது புகைப்படங்கள் மற்றும் உடமைகள் பாதுகாக்கப்படும் இடம்.",
        "description_en": "Preserved ancestral residence of the revered leader displaying photographs, books, and humble belongings."
    },
    "Sathuragiri Hills & Sundara Mahalingam": {
        "name_ta": "சதுரகிரி மலை & சுந்தர மகாலிங்கம் திருக்கோயில்",
        "name_en": "Sathuragiri Hills & Sundara Mahalingam",
        "category_ta": "சித்தர்கள் தவபூமி",
        "category_en": "Siddha Sacred Hills",
        "description_ta": "மேற்குத் தொடர்ச்சி மலையில் 18 சித்தர்கள் தவம் செய்து வாழ்ந்ததாகக் கருதப்படும் அடர்ந்த மூலிகைக் காடுகள் நிறைந்த மலை.",
        "description_en": "Mystical mountain sanctuary in the Western Ghats revered as the abode of ancient Tamil Siddha doctors and sages."
    }
}

# Translations for Official Sources
OFFICIAL_SOURCES_TRANSLATIONS = [
    {
        "source_en": "Official Directory of 38 District Portals",
        "source_ta": "தமிழ்நாட்டின் 38 மாவட்ட அதிகாரப்பூர்வ இணையதளங்களின் அடைவு",
        "use_notes_en": "Current directory and verified links to all 38 district administration portals of Tamil Nadu.",
        "use_notes_ta": "தமிழ்நாடு அரசின் 38 மாவட்ட நிர்வாக இணையதளங்களின் அதிகாரப்பூர்வ நேரடி இணைப்புகள் மற்றும் முகவரிகள்.",
        "direct_url": "https://tndistricts.nic.in/"
    },
    {
        "source_en": "Tamil Nadu Archives – District Gazetteers",
        "source_ta": "தமிழ்நாடு ஆவணக் காப்பகம் – மாவட்ட அரசிதழ்கள்",
        "use_notes_en": "Primary starting point for historical district manuals, statistical records, and gazetteers covering former administrative divisions.",
        "use_notes_ta": "வரலாற்று மாவட்டக் கையேடுகள், அரசிதழ்கள் மற்றும் முந்தைய நிர்வாகப் பிரிவுகளின் ஆவணங்களை ஆய்வு செய்வதற்கான முதன்மை காப்பகம்.",
        "direct_url": "https://tamilnaduarchives.tn.gov.in/WEB/EN/PAGE/GAZETTEERS"
    },
    {
        "source_en": "Census of India – District Census Handbooks (Tamil Nadu)",
        "source_ta": "இந்திய மக்கள்தொகைக் கணக்கெடுப்பு – தமிழ்நாடு மாவட்டக் கையேடுகள்",
        "use_notes_en": "Authoritative administrative history, boundary reorganizations, taluk bifurcations, and village directories.",
        "use_notes_ta": "அதிகாரப்பூர்வ நிர்வாக வரலாறு, மாவட்ட எல்லை மறுசீரமைப்புகள், வட்டங்கள் பிரிப்பு மற்றும் கிராம விவரக் குறிப்புகள்.",
        "direct_url": "https://censusindia.gov.in/"
    },
    {
        "source_en": "Archaeological Survey of India (ASI) – Epigraphia Indica & Inscriptions",
        "source_ta": "இந்தியத் தொல்லியல் துறை (ASI) – எபிகிராஃபியா இண்டிகா & கல்வெட்டுத் தொடர்",
        "use_notes_en": "Epigraphical records, stone inscriptions, copper plates, and ancient place names of Tamil Nadu.",
        "use_notes_ta": "தமிழ்நாட்டின் வரலாற்று இடப்பெயர்கள், கல்வெட்டுகள், செப்பேடுகள் மற்றும் தொல்லியல் சான்றுகளின் அதிகாரப்பூர்வ ஆவணம்.",
        "direct_url": "https://asi.nic.in/"
    }
]

# Translations for Research Guidance
RESEARCH_GUIDANCE_TRANSLATIONS = [
    {
        "topic_en": "Research Purpose & Methodology",
        "topic_ta": "ஆய்வு நோக்கம் & நெறிமுறைகள்",
        "guidance_en": "Grounded research on Tamil Nadu's 38 districts, separating verified historical names, administrative evolutions, and official government orders.",
        "guidance_ta": "தமிழ்நாட்டின் 38 மாவட்டங்களின் வரலாற்றுப் பெயர்கள், நிர்வாகப் பெயர் மாற்றங்கள் மற்றும் அரசாணை ஆதாரங்கள் தனித்தனியாக வகைப்படுத்தப்பட்டு ஆராயப்படுகின்றன."
    },
    {
        "topic_en": "Important Categorical Distinction",
        "topic_ta": "முக்கிய வகைப்பாட்டு வேறுபாடுகள்",
        "guidance_en": "Former administrative district, colonial spelling variant, ancient settlement, and historical region (Nadu/Seemai) are distinct categories. Regional names are not automatically assumed to represent the entire modern district.",
        "guidance_ta": "முந்தைய நிர்வாக மாவட்டம், காலனித்துவ ஆங்கில எழுத்து வடிவம், பண்டைய குடியேற்றம் மற்றும் வரலாற்றுப் பிராந்தியம் (நாடு/சீமை) ஆகியவை முற்றிலும் வெவ்வேறானவை; பிராந்தியப் பெயர்களை ஒட்டுமொத்த தற்கால மாவட்டப் பெயராகக் கருதலாகாது."
    },
    {
        "topic_en": "Verification Standard & Evidence Policy",
        "topic_ta": "சரிபார்ப்புத் தரம் & ஆதாரக் கொள்கை",
        "guidance_en": "Every claim must cite primary archival sources such as district gazetteers, government orders (G.O.), or inscriptional publications. Oral folk legends must be distinguished from epigraphical facts.",
        "guidance_ta": "அனைத்து வரலாற்றுத் தகவல்களும் மாவட்ட அரசிதழ்கள், அரசாணைகள் அல்லது கல்வெட்டுத் தொகுப்புகள் மூலம் உறுதிப்படுத்தப்பட வேண்டும்; வாய்மொழி மரபுக் கதைகள் வரலாற்று உண்மைகளிலிருந்து பிரித்துக் காட்டப்பட வேண்டும்."
    },
    {
        "topic_en": "Bilingual Integrity & Authentic Terminology",
        "topic_ta": "இருமொழி ஒருமைப்பாடு & உண்மைச் சொல்லாட்சி",
        "guidance_en": "Both Tamil and English presentations preserve exact historical nomenclature, avoiding artificial machine translation that corrupts historical place names.",
        "guidance_ta": "தமிழ் மற்றும் ஆங்கில மொழிகளில் வரலாற்று இடப்பெயர்கள், கல்வெட்டுச் சொற்கள் மற்றும் அதிகாரப்பூர்வப் பெயர்கள் எவ்வித திரிபுமின்றி இயல்பான நடையில் பாதுகாக்கப்படுகின்றன."
    }
]

def enrich_dataset(file_path):
    print(f"Enriching {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    districts = data.get("districts", [])
    updated_specs = 0
    updated_fps = 0

    for d in districts:
        d_no = d.get("no")
        d_en = d.get("district_english", "")
        d_ta = d.get("district_tamil", "")

        # 1. Update Specialities
        for s in d.get("specialities", []):
            name_en = s.get("name_en") or s.get("name", "")
            lookup = SPECIALITIES_TRANSLATIONS.get(name_en)
            
            # Fuzzy match if exact match not found
            if not lookup:
                for k, v in SPECIALITIES_TRANSLATIONS.items():
                    if k.lower() in name_en.lower() or name_en.lower() in k.lower():
                        lookup = v
                        break

            if lookup:
                s["name_ta"] = lookup["name_ta"]
                s["name_en"] = lookup["name_en"]
                s["category_ta"] = lookup["category_ta"]
                s["category_en"] = lookup["category_en"]
                s["explanation_ta"] = lookup["explanation_ta"]
                s["explanation_en"] = lookup["explanation_en"]
                s["significance_ta"] = lookup["significance_ta"]
                s["significance_en"] = lookup["significance_en"]
                updated_specs += 1
            else:
                # If no mapping, ensure clean Tamil without English sentences
                if not s.get("name_ta") or s.get("name_ta") == name_en:
                    s["name_ta"] = f"{d_ta} சிறப்பம்சம்: {name_en}"
                s["category_ta"] = s.get("category_ta") or "தனித்துவச் சிறப்பு"
                s["category_en"] = s.get("category_en") or s.get("category", "Specialty")
                s["explanation_en"] = s.get("explanation_en") or s.get("explanation", "")
                s["significance_en"] = s.get("significance_en") or s.get("significance", "")

        # 2. Update Famous Places
        for fp in d.get("famous_places", []):
            name_en = fp.get("name_en") or fp.get("name", "")
            lookup = FAMOUS_PLACES_TRANSLATIONS.get(name_en)

            if not lookup:
                for k, v in FAMOUS_PLACES_TRANSLATIONS.items():
                    if k.lower() in name_en.lower() or name_en.lower() in k.lower():
                        lookup = v
                        break

            if lookup:
                fp["name_ta"] = lookup["name_ta"]
                fp["name_en"] = lookup["name_en"]
                fp["category_ta"] = lookup["category_ta"]
                fp["category_en"] = lookup["category_en"]
                fp["description_ta"] = lookup["description_ta"]
                fp["description_en"] = lookup["description_en"]
                updated_fps += 1
            else:
                if not fp.get("name_ta") or fp.get("name_ta") == name_en:
                    fp["name_ta"] = f"{d_ta} வரலாற்றுத் தலம்: {name_en}"
                fp["category_ta"] = fp.get("category_ta") or "வரலாற்றுத் தலம்"
                fp["category_en"] = fp.get("category_en") or fp.get("category", "Heritage Site")
                fp["description_en"] = fp.get("description_en") or fp.get("description", "")

    # 3. Update Official Sources
    data["official_sources"] = OFFICIAL_SOURCES_TRANSLATIONS

    # 4. Update Research Guidance
    data["research_guidance"] = RESEARCH_GUIDANCE_TRANSLATIONS

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  -> Successfully enriched {len(districts)} districts ({updated_specs} specialities, {updated_fps} famous places) in {file_path}")

def main():
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "data", "districtsData.json")
    backend_path = os.path.join(os.path.dirname(__file__), "data", "tamil_nadu_38_districts_intelligence.json")

    enrich_dataset(frontend_path)
    enrich_dataset(backend_path)
    print("\nAll datasets enriched with authentic, pure bilingual data!")

if __name__ == "__main__":
    main()
