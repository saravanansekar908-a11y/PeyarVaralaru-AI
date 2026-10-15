import json

en_patch = {
  "app": {
    "title": "PeyarVaralaru AI",
    "subtitle": "Historical Tamil Place Name Research Platform",
    "tagline": "Explore how Tamil Nadu place names evolved across centuries of inscriptions and archives"
  },
  "nav": {
    "home": "Home",
    "districts": "38 Districts",
    "search": "Smart Search",
    "timeline": "Timeline",
    "askAI": "Ask History AI",
    "graph": "Relationship Graph",
    "sources": "Sources",
    "language": "Language",
    "modules": "Research Modules",
    "evidenceGrounded": "Evidence-Grounded",
    "groundedDesc": "Grounded in Tamil Nadu Archives & Government Gazetteers."
  },
  "district": {
    "district": "District",
    "historicalName": "Historical Name",
    "formerName": "Former Name",
    "nameChangeHistory": "Name Change History",
    "administrativeHistory": "Administrative History",
    "specialFeatures": "Special Features",
    "famousPlaces": "Famous Places",
    "officialWebsite": "Official Website",
    "informationSources": "Information Sources",
    "searchPlaceholder": "Search any of 38 districts... (e.g. Madurai, Thanjavur, Ariyalur)",
    "registryTitle": "Official 38 Districts Registry",
    "dashboardTitle": "Tamil Nadu District Intelligence Dashboard",
    "verifiedCount": "38 / 38 Verified",
    "districtOf": "District",
    "of38": "of 38",
    "searchAliases": "Search Aliases & Variants:",
    "evolutionTitle": "Historical Names & Administrative Evolution",
    "gazetteerGrounded": "Gazetteer Grounded",
    "verificationPolicyTitle": "Scholarly Verification Standard:",
    "verificationPolicyDesc": "Former administrative district, colonial spelling variant, ancient settlement, and historical region (Nadu/Seemai) are distinct categories. Regional names are not automatically assumed to represent the entire modern district.",
    "metadataTitle": "Official Record Metadata",
    "formerAdminHistory": "Former Administrative History:",
    "ancientContext": "Ancient / Historical Context:",
    "changeAuthorityNote": "Change Date / Verification Note:",
    "visitPortal": "Visit Official District Portal",
    "askAboutDistrict": "Ask History AI about this District",
    "specialityTitle": "District Specialities",
    "specialitySubtitle": "Evidence-grounded highlights covering GI products, architectural landmarks, natural heritage, and local industries.",
    "whatMakesSpecial": "What Makes {name} Special?",
    "referenceLink": "Reference Link",
    "famousPlacesTitle": "Famous Places & Heritage Sites",
    "famousPlacesSubtitle": "Notable historical sanctuaries, monuments, and ecological landmarks.",
    "exploreSite": "Explore Site",
    "directoryTitle": "All 38 Districts of Tamil Nadu",
    "directorySubtitle": "Click any district card to load its complete heritage intelligence and archival records.",
    "interactiveDirectory": "Interactive District Directory",
    "viewProfile": "View Profile",
    "noMatchFound": "No matching districts found",
    "noMatchDesc": "Try clearing your search query or selecting 'All Regions'.",
    "resetFilters": "Reset Filters",
    "officialSourcesTitle": "Official Sources & Research Guidance",
    "fromWorksheets": "Archived 38 District Sources",
    "govtDirectories": "Official Government Directories",
    "researchDistinctions": "Research Distinctions & Standards",
    "open": "Open",
    "translationUnavailable": "Information currently not available in English."
  }
}

ta_patch = {
  "app": {
    "title": "பெயர்வரலாறு AI",
    "subtitle": "வரலாற்றுத் தமிழ் இடப்பெயர் ஆராய்ச்சி தளம்",
    "tagline": "தமிழ்நாட்டின் வரலாற்று இடப்பெயர்களை AI துணையுடன் சான்றுகளோடு ஆராயுங்கள்"
  },
  "nav": {
    "home": "முகப்பு",
    "districts": "மாவட்டங்கள் (38)",
    "search": "தேடல்",
    "timeline": "வரலாற்றுக் காலவரிசை",
    "askAI": "AI ஆய்வு",
    "graph": "உறவு வரைபடம்",
    "sources": "ஆதாரங்கள்",
    "language": "மொழி",
    "modules": "ஆய்வுத் தளங்கள்",
    "evidenceGrounded": "சான்றாதார அமைப்பு",
    "groundedDesc": "தமிழ்நாடு ஆவணக் காப்பகம் மற்றும் அரசிதழ் சான்றுகள் அடிப்படையில் உருவாக்கப்பட்டது."
  },
  "district": {
    "district": "மாவட்டம்",
    "historicalName": "வரலாற்றுப் பெயர்",
    "formerName": "பழைய பெயர்",
    "nameChangeHistory": "பெயர் மாற்ற வரலாறு",
    "administrativeHistory": "நிர்வாக வரலாறு",
    "specialFeatures": "சிறப்பம்சங்கள்",
    "famousPlaces": "புகழ்பெற்ற இடங்கள்",
    "officialWebsite": "அதிகாரப்பூர்வ இணையதளம்",
    "informationSources": "தகவல் ஆதாரங்கள்",
    "searchPlaceholder": "38 மாவட்டங்களில் தேடுக... (எ.கா: மதுரை, தஞ்சாவூர், அரியலூர்)",
    "registryTitle": "அதிகாரப்பூர்வ 38 மாவட்ட ஆவணம்",
    "dashboardTitle": "தமிழ்நாடு மாவட்ட வரலாற்று நுண்ணறிவு",
    "verifiedCount": "38 / 38 சரிபார்க்கப்பட்டது",
    "districtOf": "மாவட்டம்",
    "of38": "/ 38",
    "searchAliases": "தேடல் மாற்றுப் பெயர்கள்:",
    "evolutionTitle": "வரலாற்றுப் பெயர் மற்றும் நிர்வாகப் பரிணாமம்",
    "gazetteerGrounded": "அரசிதழ் ஆதாரங்கள்",
    "verificationPolicyTitle": "ஆய்வுத் தரம் & சரிபார்ப்புக் கொள்கை:",
    "verificationPolicyDesc": "முந்தைய நிர்வாகப் பெயர், முந்தைய ஆங்கில ஒலிபெயர்ப்பு, பண்டைய குடியேற்றப் பெயர், மற்றும் வரலாற்றுப் பிராந்தியப் பெயர் (நாடு / சீமை) ஆகியவை வெவ்வேறானவை. பிராந்தியப் பெயர்களை ஒட்டுமொத்த தற்கால மாவட்டத்தின் பண்டைய பெயராகக் கருதாமல், தனித்தனியாக ஆவணப்படுத்த வேண்டும்.",
    "metadataTitle": "அரசு ஆவணக் குறிப்புகள்",
    "formerAdminHistory": "முந்தைய நிர்வாக வரலாறு:",
    "ancientContext": "பண்டைய / வரலாற்றுப் பின்னணி:",
    "changeAuthorityNote": "அரசாணை / சரிபார்ப்புக் குறிப்பு:",
    "visitPortal": "மாவட்ட அதிகாரப்பூர்வ இணையதளம்",
    "askAboutDistrict": "இந்த மாவட்டம் பற்றி AI-யிடம் கேட்க",
    "specialityTitle": "தனித்துவச் சிறப்புகள்",
    "specialitySubtitle": "புவிசார் குறியீடு (GI), கலாச்சார சின்னங்கள், பிரத்யேகத் தொழில்கள், உணவு மற்றும் வரலாற்றுச் சான்றுகள்",
    "whatMakesSpecial": "இந்த மாவட்டத்தின் தனித்துவம் என்ன? ({name})",
    "referenceLink": "ஆதார இணைப்பு",
    "famousPlacesTitle": "முக்கிய வரலாற்றுத் தலங்கள் & இடங்கள்",
    "famousPlacesSubtitle": "இந்த மாவட்டத்தில் அமைந்துள்ள வரலாற்று முக்கியத்துவம் வாய்ந்த இடங்கள்",
    "exploreSite": "மேலும் விவரங்கள்",
    "directoryTitle": "தமிழ்நாட்டின் 38 மாவட்டங்கள்",
    "directorySubtitle": "எந்தவொரு மாவட்டத்தையும் தேர்ந்தெடுத்து அதன் வரலாற்றுப் பின்னணி மற்றும் தனித்துவத்தை ஆராயுங்கள்.",
    "interactiveDirectory": "அனைத்து மாவட்டங்களின் வழிகாட்டி",
    "viewProfile": "விவரங்களைக் காண்க",
    "noMatchFound": "பொருத்தமான மாவட்டம் கிடைக்கவில்லை",
    "noMatchDesc": "வேறு தேடல் சொல்லை அல்லது மண்டல வடிகட்டியைப் பயன்படுத்தவும்.",
    "resetFilters": "வடிகட்டிகளை மீட்டமைக்க",
    "officialSourcesTitle": "அதிகாரப்பூர்வ அரசு மூலங்கள் & வழிகாட்டுதல்கள்",
    "fromWorksheets": "ஆவணப்படுத்தப்பட்ட 38 மாவட்ட மூலங்கள்",
    "govtDirectories": "அரசு ஆவணக் காப்பக இணைப்புகள்",
    "researchDistinctions": "வரலாற்றுப் பெயர் ஆய்வு நெறிமுறைகள்",
    "open": "திறக்க",
    "translationUnavailable": "தமிழ் விளக்கம் தற்போது கிடைக்கவில்லை."
  }
}

def update_json(file_path, patch):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in patch.items():
        if isinstance(v, dict):
            if k not in data:
                data[k] = {}
            data[k].update(v)
        else:
            data[k] = v
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

update_json("frontend/src/locales/en.json", en_patch)
update_json("frontend/src/locales/ta.json", ta_patch)
print("Updated en.json and ta.json with complete district keys!")
