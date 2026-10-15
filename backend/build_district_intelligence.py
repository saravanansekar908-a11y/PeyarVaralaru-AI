"""
District Intelligence Dataset Generator for PeyarVaralaru AI.
Merges the official 38 Districts Excel records with verified heritage,
GI products, famous landmarks, cuisine, and administrative timelines.
"""
import json
import os

with open('data/districts_raw.json', 'r', encoding='utf-8') as f:
    raw_districts = json.load(f)

with open('data/sources_and_readme.json', 'r', encoding='utf-8') as f:
    extra_data = json.load(f)

# Comprehensive, verified metadata for each of Tamil Nadu's 38 districts
DISTRICT_DETAILS = {
    1: {
        "region": "Cauvery Delta / Central",
        "intro_ta": "அரியலூர் மாவட்டம் வரலாற்றுச் சிறப்புமிக்க கங்கைகொண்ட சோழபுரம் உலகப் பாரம்பரியக் கோயிலையும், பல மில்லியன் ஆண்டுகள் பழமையான கிரெட்டேசியஸ் புதைபடிவ பாறைப்படிவுகளையும் கொண்ட பூமி.",
        "intro_en": "Ariyalur is globally renowned for the UNESCO World Heritage Brihadisvara Temple at Gangaikonda Cholapuram, as well as rich Cretaceous paleontological fossil beds.",
        "search_aliases": ["Ariyalur", "அரியலூர்", "Gangaikonda Cholapuram", "கங்கைகொண்ட சோழபுரம்"],
        "hero_image": "/images/thanjavur.jpg",
        "specialities": [
            {
                "name": "Gangaikonda Cholapuram Temple (UNESCO)",
                "category": "UNESCO World Heritage & Imperial Architecture",
                "explanation": "Built by Rajendra Chola I around 1035 CE to commemorate his victorious expedition to the Ganges. One of the Great Living Chola Temples.",
                "significance": "Served as the imperial capital of the Chola Empire for nearly 250 years.",
                "source_url": "https://ariyalur.nic.in/tourist-place/gangaikonda-cholapuram/"
            },
            {
                "name": "Cretaceous Era Fossil Beds & Ammonites",
                "category": "Paleontological Heritage",
                "explanation": "Ariyalur's sedimentary limestone terrain holds extensive marine fossils, dinosaur eggs, and ammonite shells dating back 65 to 100 million years.",
                "significance": "A critical geological field site for paleontology in South Asia, often called a geological wonderland.",
                "source_url": "https://ariyalur.nic.in/"
            },
            {
                "name": "Cement Capital of Tamil Nadu",
                "category": "Industrial & Mineral Economy",
                "explanation": "Rich high-grade limestone deposits have made Ariyalur host to numerous major cement manufacturing plants.",
                "significance": "Powers infrastructure across Tamil Nadu and neighbouring states.",
                "source_url": "https://ariyalur.nic.in/"
            },
            {
                "name": "Karaivetti Bird Sanctuary",
                "category": "Ecology & Wildlife",
                "explanation": "One of the largest freshwater lake bird sanctuaries in Tamil Nadu, hosting thousands of migratory waterfowl every winter.",
                "significance": "Ramsar-recognized habitat supporting bar-headed geese and migratory birds.",
                "source_url": "https://ariyalur.nic.in/tourist-place/karaivetti-birds-sanctuary/"
            }
        ],
        "famous_places": [
            {
                "name": "Gangaikonda Cholapuram",
                "category": "UNESCO Monument",
                "description": "Majestic Chola temple showcasing supreme stone carving, living bronze traditions, and royal inscriptions.",
                "link": "https://ariyalur.nic.in/tourist-place/gangaikonda-cholapuram/"
            },
            {
                "name": "Karaivetti Sanctuary",
                "category": "Ecology",
                "description": "Scenic freshwater lake sanctuary hosting over 188 species of resident and migratory birds.",
                "link": "https://ariyalur.nic.in/tourist-place/karaivetti-birds-sanctuary/"
            },
            {
                "name": "Jayankondam",
                "category": "Historic Commercial Town",
                "description": "Ancient trading town connected to Chola administration and handloom weaving.",
                "link": "https://ariyalur.nic.in/"
            }
        ]
    },
    2: {
        "region": "Northern Coastal / Tondaimandalam",
        "intro_ta": "செங்கல்பட்டு மாவட்டம் மாமல்லபுரம் யுனெஸ்கோ கடற்கரைக் கோயில்கள், வேடந்தாங்கல் பறவைகள் சரணாலயம் மற்றும் நவீன தொழில் வளர்ச்சியைத் தன்னுள் அடக்கிய வரலாற்றுப் பகுதி.",
        "intro_en": "Chengalpattu spans the ancient Pallava coastal heritage of Mamallapuram, historical Vedanthangal sanctuary, and modern manufacturing hubs.",
        "search_aliases": ["Chengalpattu", "செங்கல்பட்டு", "Chingleput", "Mamallapuram", "Mahabalipuram", "மாமல்லபுரம்"],
        "hero_image": "/images/mamallapuram.jpg",
        "specialities": [
            {
                "name": "Group of Monuments at Mamallapuram (UNESCO)",
                "category": "UNESCO World Heritage Site",
                "explanation": "7th and 8th-century Pallava coastal sanctuary featuring the monolithic Shore Temple, Five Rathas, and Arjuna's Penance.",
                "significance": "Premier open-air rock sculpture sanctuary illustrating Pallava maritime greatness.",
                "source_url": "https://chengalpattu.nic.in/tourist-place/mamallapuram/"
            },
            {
                "name": "Vedanthangal Bird Sanctuary",
                "category": "Wildlife & Conservation",
                "explanation": "Established in 1798, it is the oldest water bird sanctuary in India, conserved by local community protection for centuries.",
                "significance": "Critical breeding habitat for migratory herons, storks, egrets, and spoonbills.",
                "source_url": "https://chengalpattu.nic.in/tourist-place/vedanthangal-birds-sanctuary/"
            },
            {
                "name": "Automobile & Electronics Corridor (Maraimalai Nagar & Oragadam)",
                "category": "Industrial Innovation",
                "explanation": "Major hub for automobile manufacturing and electronic engineering in South Asia.",
                "significance": "A major contributor to Tamil Nadu's industrial and automotive export economy.",
                "source_url": "https://chengalpattu.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Mamallapuram Shore Temple",
                "category": "Pallava Heritage",
                "description": "Ancient coastal granite temple facing the Bay of Bengal, built by Narasimhavarman II.",
                "link": "https://chengalpattu.nic.in/tourist-place/mamallapuram/"
            },
            {
                "name": "Pancha Rathas",
                "category": "Monolithic Architecture",
                "description": "Five monolithic carved temples each sculpted from a single granite boulder.",
                "link": "https://chengalpattu.nic.in/tourist-place/mamallapuram/"
            },
            {
                "name": "Vedanthangal Sanctuary",
                "category": "Ecological Reserve",
                "description": "Historic bird sanctuary attracting thousands of nesting migratory birds each winter.",
                "link": "https://chengalpattu.nic.in/tourist-place/vedanthangal-birds-sanctuary/"
            }
        ]
    },
    3: {
        "region": "Northern Coastal / Capital",
        "intro_ta": "சென்னை — தமிழ்நாட்டின் தலைநகரம்; 1639-ஆம் ஆண்டு கிழக்கிந்திய கம்பெனியின் வணிகத் தளமாகத் தொடங்கி 1996-இல் சென்னை என அதிகாரப்பூர்வமாகப் பெயர் மாற்றப்பட்ட கலாச்சார, வரலாற்று மாநகரம்.",
        "intro_en": "Chennai, capital of Tamil Nadu, transitioned from colonial Madras (1639) to officially Chennai in 1996, serving as the cultural and economic gateway of South India.",
        "search_aliases": ["Chennai", "சென்னை", "Madras", "மெட்ராஸ்", "Madraspatnam", "Chennapatnam", "மதராசப்பட்டினம்"],
        "hero_image": "/images/hero-temple.jpg",
        "specialities": [
            {
                "name": "Kapaleeshwarar Temple & Mylapore Heritage",
                "category": "Dravidian Temple Heritage",
                "explanation": "Ancient temple of Lord Shiva and Goddess Karpagambal with celebrated 7th-century Tevaram hymnal documentation.",
                "significance": "Ancient maritime centre praised by Greek and Roman geographers as Malliarpha.",
                "source_url": "https://chennai.nic.in/"
            },
            {
                "name": "Fort St. George & Tamil Nadu Secretariat",
                "category": "Colonial Administrative Heritage",
                "explanation": "Founded in 1639 by the British East India Company, it is the first British fortress in India and currently houses the Tamil Nadu Assembly.",
                "significance": "Birthplace of modern municipal administration and colonial documentation in South India.",
                "source_url": "https://chennai.nic.in/tourist-place/fort-st-george/"
            },
            {
                "name": "Marina Beach & Promenade",
                "category": "Natural Urban Landmark",
                "explanation": "Extending over 13 km along the Bay of Bengal, it is the second longest natural urban beach in the world.",
                "significance": "Historic public promenade adorned with iconic statues of Tamil literary giants.",
                "source_url": "https://chennai.nic.in/tourist-place/marina-beach/"
            },
            {
                "name": "Healthcare & Automobile Capital of India",
                "category": "Economy & Healthcare",
                "explanation": "Produces over 30% of India's automobile parts and attracts international medical tourists.",
                "significance": "Earned global recognition as the Detroit of South Asia.",
                "source_url": "https://chennai.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Mylapore Kapaleeshwarar Temple",
                "category": "Spiritual Heritage",
                "description": "7th-century Dravidian temple complex celebrating ancient Tevaram songs and the annual Panguni festival.",
                "link": "https://chennai.nic.in/"
            },
            {
                "name": "Fort St. George & Museum",
                "category": "Colonial Landmark",
                "description": "17th-century coastal fortress housing historical weaponry, coins, and official archives.",
                "link": "https://chennai.nic.in/tourist-place/fort-st-george/"
            },
            {
                "name": "Santhome Cathedral Basilica",
                "category": "Ecclesiastical Heritage",
                "description": "Historic Neo-Gothic minor basilica erected over the tomb of St. Thomas the Apostle.",
                "link": "https://chennai.nic.in/"
            }
        ]
    },
    4: {
        "region": "Kongu Nadu / Western",
        "intro_ta": "கோயம்புத்தூர் — 'தென்னிந்தியாவின் மான்செஸ்டர்'; வரலாற்றுச் சிறப்புமிக்க கொங்கு நாட்டின் தொழில், நெசவு மற்றும் கல்வித் தலைநகரம்.",
        "intro_en": "Coimbatore, often styled the 'Manchester of South India', is the premier industrial, educational, and textile power of the historic Kongu region.",
        "search_aliases": ["Coimbatore", "கோயம்புத்தூர்", "Kovai", "கோவை", "Kongu", "கொங்கு"],
        "hero_image": "/images/tiruvannamalai.jpg",
        "specialities": [
            {
                "name": "Kovai Kora Cotton Sarees (GI Tag)",
                "category": "Geographical Indication (GI) Craft",
                "explanation": "A traditional lightweight blend of superior silk and pure cotton woven in and around Coimbatore.",
                "significance": "Renowned across India for breezy comfort and subtle border motifs.",
                "source_url": "https://coimbatore.nic.in/"
            },
            {
                "name": "Coimbatore Wet Grinder (GI Tag)",
                "category": "Engineering GI Tag",
                "explanation": "Innovative domestic and commercial table-top wet grinder using locally quarried stones.",
                "significance": "Revolutionized traditional South Indian cuisine preparation worldwide.",
                "source_url": "https://coimbatore.nic.in/"
            },
            {
                "name": "Siruvani Water",
                "category": "Natural Resource",
                "explanation": "Water sourced from Siruvani Hills celebrated as one of the sweetest drinking waters in the world.",
                "significance": "Treasured lifespring cherished by generations of Kovai residents.",
                "source_url": "https://coimbatore.nic.in/"
            },
            {
                "name": "Marudhamalai Murugan Temple",
                "category": "Spiritual Heritage",
                "explanation": "Scenic hill temple surrounded by medicinal herbs on the Western Ghats, mentioned in Sangam folklore.",
                "significance": "Celebrated 12th-century shrine of Lord Dhandayuthapani.",
                "source_url": "https://coimbatore.nic.in/tourist-place/marudhamalai-murugan-temple/"
            }
        ],
        "famous_places": [
            {
                "name": "Marudhamalai Temple",
                "category": "Hill Shrine",
                "description": "Hilltop shrine dedicated to Lord Murugan set amidst the Western Ghats biosphere.",
                "link": "https://coimbatore.nic.in/tourist-place/marudhamalai-murugan-temple/"
            },
            {
                "name": "Perur Pateeswarar Temple",
                "category": "Chola Epigraphy",
                "description": "Ancient temple on the Noyyal river renowned for the Kanaka Sabha and intricate stone pillar sculptures.",
                "link": "https://coimbatore.nic.in/"
            },
            {
                "name": "Siruvani Waterfalls",
                "category": "Eco-Tourism",
                "description": "Picturesque waterfalls amidst virgin rainforests supplying pristine mineral-rich water.",
                "link": "https://coimbatore.nic.in/"
            }
        ]
    },
    5: {
        "region": "Northern Coastal / Chola & Pallava Border",
        "intro_ta": "கடலூர் — முன்னாள் தென் ஆற்காடு பகுதியின் முக்கிய மாவட்டம்; சிதம்பரம் நடராஜர் ஆலயம், பிச்சாவரம் சதுப்புநிலக் காடுகள் மற்றும் சில்வர் பீச் கடற்கரையைக் கொண்டது.",
        "intro_en": "Cuddalore, historic core of the former South Arcot district, features the Chidambaram Nataraja temple, Pichavaram mangroves, and the port of Silver Beach.",
        "search_aliases": ["Cuddalore", "கடலூர்", "South Arcot", "தென் ஆற்காடு", "Chidambaram", "சிதம்பரம்"],
        "hero_image": "/images/madurai.jpg",
        "specialities": [
            {
                "name": "Chidambaram Thillai Nataraja Temple",
                "category": "Sacred Architecture & Epigraphy",
                "explanation": "Ancient temple representing Akasha (Space) among the Pancha Bhoota Sthalams, celebrated for the Cosmic Dance of Lord Shiva.",
                "significance": "Centuries of Chola imperial patronage and inscriptional land grants recorded on its stone walls.",
                "source_url": "https://cuddalore.nic.in/tourist-place/chidambaram-temple/"
            },
            {
                "name": "Pichavaram Mangrove Forest",
                "category": "Eco-Tourism & Coastal Mangroves",
                "explanation": "One of the largest mangrove forests in India, covering over 1,100 hectares with hundreds of interconnected water channels.",
                "significance": "Pristine wetland ecosystem acting as a natural storm surge barrier and wildlife sanctuary.",
                "source_url": "https://cuddalore.nic.in/tourist-place/pichavaram-mangrove-forest/"
            },
            {
                "name": "Neyveli Lignite Corporation (NLC)",
                "category": "Energy & Mining",
                "explanation": "Major opencast lignite mining and thermal power generation centre established in the 1950s.",
                "significance": "A vital Navratna public energy producer for South India.",
                "source_url": "https://cuddalore.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Chidambaram Nataraja Temple",
                "category": "Pancha Bhoota Sthalam",
                "description": "Famed temple of the Cosmic Dance with golden roofed sanctum and 108 Bharatanatyam stone poses.",
                "link": "https://cuddalore.nic.in/tourist-place/chidambaram-temple/"
            },
            {
                "name": "Pichavaram Mangroves",
                "category": "Wetland Ecology",
                "description": "Breathtaking boat rides through serene mangrove tunnels between Vellar and Coleroon estuaries.",
                "link": "https://cuddalore.nic.in/tourist-place/pichavaram-mangrove-forest/"
            },
            {
                "name": "Silver Beach",
                "category": "Coastal Promenade",
                "description": "Long tranquil coastline facing the Bay of Bengal, formerly near British Fort St. David.",
                "link": "https://cuddalore.nic.in/tourist-place/silver-beach/"
            }
        ]
    },
    6: {
        "region": "North-Western / Adhiyaman Heritage",
        "intro_ta": "தருமபுரி — தகடூர் சங்க கால அதியமான் மன்னனின் தலைநகரம்; ஒகேனக்கல் நீர்வீழ்ச்சி, மாம்பழ விளைச்சல் மற்றும் பட்டுப்புழு வளர்ப்பிற்குப் புகழ்பெற்ற மாவட்டம்.",
        "intro_en": "Dharmapuri is the historic seat of Sangam king Adhiyaman at ancient Tagadur, celebrated for Hogenakkal Falls, silk sericulture, and mango orchards.",
        "search_aliases": ["Dharmapuri", "தருமபுரி", "Tagadur", "தகடூர்", "Hogenakkal", "ஒகேனக்கல்"],
        "hero_image": "/images/tiruvannamalai.jpg",
        "specialities": [
            {
                "name": "Tagadur & King Adhiyaman Neduman Anji Heritage",
                "category": "Sangam Epigraphy & Literature",
                "explanation": "Capital of the legendary Sangam Chieftain Adhiyaman, praised by poetess Avvaiyar in Purananuru for gifting the immortal gooseberry.",
                "significance": "Foundational site of classical Sangam Tamil literary history and hero-stone epigraphy.",
                "source_url": "https://dharmapuri.nic.in/"
            },
            {
                "name": "Hogenakkal Waterfalls ('Niagara of India')",
                "category": "Natural Attraction",
                "explanation": "Where the Kaveri river enters Tamil Nadu forming scenic cascades over carbonatite rock formations with famous coracle rides.",
                "significance": "Geologically unique river gorge famous for natural mineral baths and traditional massages.",
                "source_url": "https://dharmapuri.nic.in/tourist-place/hogenakkal/"
            },
            {
                "name": "Sericulture & Silk Reeling",
                "category": "Traditional Industry",
                "explanation": "Leading producer of mulberry cocoons and raw silk thread in Tamil Nadu.",
                "significance": "Feeds silk weaving hubs across Kanchipuram, Arani, and Salem.",
                "source_url": "https://dharmapuri.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Hogenakkal Falls",
                "category": "Waterfalls & River Gorge",
                "description": "Spectacular cascading waterfalls on the Kaveri river with coracle rides and carbonatite rock formations.",
                "link": "https://dharmapuri.nic.in/tourist-place/hogenakkal/"
            },
            {
                "name": "Adhiyamankottai Fort",
                "category": "Archaeological Heritage",
                "description": "Ruins of the ancient oval-shaped mud and stone fort of Sangam ruler Adhiyaman.",
                "link": "https://dharmapuri.nic.in/"
            },
            {
                "name": "Theerthamalai Temple",
                "category": "Hill Shrine",
                "description": "Ancient hilltop temple with five perennial sacred springs set in lush greenery.",
                "link": "https://dharmapuri.nic.in/"
            }
        ]
    },
    7: {
        "region": "Southern Central / Hill Country",
        "intro_ta": "திண்டுக்கல் — வரலாற்று மலைக்கோட்டை, உலகப் புகழ்பெற்ற பூட்டுகள், திண்டுக்கல் பிரியாணி மற்றும் கொடைக்கானல் மலைவாசஸ்தலத்தைக் கொண்ட பெருமைமிக்க மாவட்டம்.",
        "intro_en": "Dindigul is acclaimed for its massive 17th-century rock fort, GI-tagged handmade locks, unique Thalappakatti biryani tradition, and Kodaikanal hills.",
        "search_aliases": ["Dindigul", "திண்டுக்கல்", "Kodaikanal", "கொடைக்கானல்"],
        "hero_image": "/images/madurai.jpg",
        "specialities": [
            {
                "name": "Dindigul Lock (GI Tag)",
                "category": "Geographical Indication (GI) Craft",
                "explanation": "Handmade iron, brass, and steel lever tumbler locks manufactured since the early 1930s with unmatched security mechanisms.",
                "significance": "Exported across India and trusted for temple treasuries and government vaults.",
                "source_url": "https://dindigul.nic.in/"
            },
            {
                "name": "Dindigul Rock Fort",
                "category": "Military Heritage Architecture",
                "explanation": "Massive 280-foot high monolithic rock fort built in 1605 by Nayak rulers and later fortified by Hyder Ali and Tipu Sultan.",
                "significance": "Strategic defense fortress in the Carnatic Wars and Anglo-Mysore Wars.",
                "source_url": "https://dindigul.nic.in/tourist-place/dindigul-rock-fort/"
            },
            {
                "name": "Sirumalai Hill Banana (GI Tag)",
                "category": "Agri-GI Horticultural Heritage",
                "explanation": "Unique small, sweet, and aromatic mountain banana grown organically in the microclimate of Sirumalai hills.",
                "significance": "Celebrated for medicinal properties and extended natural shelf life.",
                "source_url": "https://dindigul.nic.in/"
            },
            {
                "name": "Kodaikanal ('Princess of Hill Stations')",
                "category": "Hill Station & Eco-Reserve",
                "explanation": "Popular retreat nestled in the Palani hills featuring star-shaped Kodaikanal lake, Pillar Rocks, and kurinji flower blooms.",
                "significance": "A biodiversity hotspot and prominent South Indian tourist haven.",
                "source_url": "https://dindigul.nic.in/tourist-place/kodaikanal/"
            }
        ],
        "famous_places": [
            {
                "name": "Dindigul Rock Fort",
                "category": "Historic Fortress",
                "description": "Majestic granite rock bastion offering panoramic valley vistas and ancient cannon batteries.",
                "link": "https://dindigul.nic.in/tourist-place/dindigul-rock-fort/"
            },
            {
                "name": "Kodaikanal Lake",
                "category": "Hill Lake & Promenade",
                "description": "Star-shaped artificial lake built in 1863 surrounded by weeping willows and boating piers.",
                "link": "https://dindigul.nic.in/tourist-place/kodaikanal/"
            },
            {
                "name": "Palani Murugan Temple",
                "category": "Spiritual Sanctuary",
                "description": "Third of the Arupadai Veedu shrines of Lord Murugan, consecrated with Navapashanam idol.",
                "link": "https://dindigul.nic.in/"
            }
        ]
    },
    8: {
        "region": "Kongu Nadu / Textile & Agriculture",
        "intro_ta": "ஈரோடு — 'மஞ்சள் நகரம்'; பவானி ஜமக்காளம், சென்னிமலை கைத்தறி மற்றும் பவானி-காவேரி கூடல்துறை சங்கமத்தைக் கொண்ட வரலாற்றுத் தலம்.",
        "intro_en": "Erode, the 'Yellow City', is India's leading turmeric marketplace, renowned for Bhavani Jamakkalam carpets, Chennimalai handlooms, and Kodumanal archaeology.",
        "search_aliases": ["Erode", "ஈரோடு", "Bhavani", "பவானி", "Periyar"],
        "hero_image": "/images/tiruvannamalai.jpg",
        "specialities": [
            {
                "name": "Erode Turmeric (GI Tag)",
                "category": "Agri-GI Heritage",
                "explanation": "Special finger turmeric grown along the Kaveri river with high curcumin content (over 3%) giving deep golden pigmentation.",
                "significance": "Major turmeric trading hub in Asia, setting global benchmark prices.",
                "source_url": "https://erode.nic.in/"
            },
            {
                "name": "Bhavani Jamakkalam (GI Tag)",
                "category": "Textile GI Craft",
                "explanation": "Coarse cotton and art-silk floor mats woven by traditional weavers in Bhavani since the late 19th century.",
                "significance": "Durable geometric carpets popular throughout rural and urban celebrations.",
                "source_url": "https://erode.nic.in/"
            },
            {
                "name": "Kodumanal Megalithic Archaeological Site",
                "category": "Archaeological Heritage",
                "explanation": "Ancient industrial and trade settlement dating from 5th century BCE to 2nd century CE on the Noyyal river.",
                "significance": "Excavated quartz, carnelian beads, high-carbon crucible wootz steel, and Tamil-Brahmi inscribed potsherds.",
                "source_url": "https://erode.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Bhavani Sangameswarar Temple",
                "category": "River Confluence Shrine",
                "description": "Sacred confluence of Kaveri, Bhavani, and the mystical Amutha rivers, known as the Dakshina Triveni.",
                "link": "https://erode.nic.in/tourist-place/bhavani-sangameshwarar-temple/"
            },
            {
                "name": "Chennimalai Murugan Temple",
                "category": "Hilltop Heritage",
                "description": "Hill sanctuary famed for its handloom weaving community and Siragiri Velayudhaswami temple.",
                "link": "https://erode.nic.in/"
            },
            {
                "name": "Kodumanal Excavations",
                "category": "Sangam Archaeology",
                "description": "Archaeological site revealing ancient bead workshops, wootz steel smelting furnaces, and urn burials.",
                "link": "https://erode.nic.in/"
            }
        ]
    },
    9: {
        "region": "Northern Central / Hill & Plain",
        "intro_ta": "கள்ளக்குறிச்சி — 2019-இல் உருவான புதிய மாவட்டம்; கல்வராயன் மலைகள், கோமுகி அணை மற்றும் கரும்பு-சர்க்கரை ஆலைகளுக்குப் புகழ்பெற்ற பகுதி.",
        "intro_en": "Kallakurichi, formed in 2019 from Viluppuram, is marked by the scenic Kalvarayan hills, Gomukhi reservoir, and extensive agro-sugar industries.",
        "search_aliases": ["Kallakurichi", "கள்ளக்குறிச்சி", "Kalvarayan", "கல்வராயன்"],
        "hero_image": "/images/hero-temple.jpg",
        "specialities": [
            {
                "name": "Kalvarayan Hills & Waterfalls",
                "category": "Mountain Ecosystem & Eco-Tourism",
                "explanation": "Part of the Eastern Ghats range, home to Periyar falls, Megam falls, and unique tribal cultural settlements.",
                "significance": "Popular trekking and nature trail destination with untouched forest cover.",
                "source_url": "https://kallakurichi.nic.in/tourist-place/kalrayan-hills/"
            },
            {
                "name": "Gomukhi Dam & Reservoir",
                "category": "Water Resource & Recreation",
                "explanation": "Major dam built across Gomukhi river irrigating thousands of hectares of paddy, sugarcane, and pulses.",
                "significance": "Lifeline for local agrarian communities and scenic recreational spot.",
                "source_url": "https://kallakurichi.nic.in/tourist-place/gomukhi-dam/"
            },
            {
                "name": "Agro-Sugar Mills & Grain Markets",
                "category": "Agricultural Economy",
                "explanation": "Major cooperative and private sugar mills along with bustling wholesale rice and pulse mandis.",
                "significance": "Economic backbone of the newly carved district.",
                "source_url": "https://kallakurichi.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Kalvarayan Hills",
                "category": "Eastern Ghats Reserve",
                "description": "Cool forested hill range featuring cascading streams, botanical gardens, and tribal villages.",
                "link": "https://kallakurichi.nic.in/tourist-place/kalrayan-hills/"
            },
            {
                "name": "Gomukhi Dam",
                "category": "Reservoir",
                "description": "Sprawling reservoir situated at the foothills of Kalvarayan hills with scenic views.",
                "link": "https://kallakurichi.nic.in/tourist-place/gomukhi-dam/"
            },
            {
                "name": "Ulundurpet & Tirukovilur Border Temples",
                "category": "Historic Towns",
                "description": "Ancient temple transit town linking central Tamil Nadu to the Coromandel coast.",
                "link": "https://kallakurichi.nic.in/"
            }
        ]
    },
    10: {
        "region": "Northern / Tondaimandalam",
        "intro_ta": "காஞ்சிபுரம் — 'ஆயிரம் கோயில்களின் நகரம்'; பட்டுச் சேலைகளின் தலைநகரம் மற்றும் பல்லவர் பேரரசின் கலை, கல்வி, ஆன்மீகத் தலைமை மையம்.",
        "intro_en": "Kancheepuram, the historic 'City of Thousand Temples', was the grand capital of the Pallavas, celebrated for Kanchipuram Silk Sarees and ancient Ghatikasthanam learning.",
        "search_aliases": ["Kancheepuram", "காஞ்சிபுரம்", "Kanchi", "காஞ்சி", "Conjeevaram"],
        "hero_image": "/images/mamallapuram.jpg",
        "specialities": [
            {
                "name": "Kanchipuram Silk Sarees (GI Tag)",
                "category": "World-Renowned Textile GI Craft",
                "explanation": "Handwoven from pure mulberry silk and silver zari using the distinctive Korvai interlocking weaving technique.",
                "significance": "Considered India's most prestigious bridal and ceremonial attire, practiced for over four centuries.",
                "source_url": "https://kancheepuram.nic.in/"
            },
            {
                "name": "Kailasanathar Temple (Pallava Epigraphy)",
                "category": "Dravidian Architectural Heritage",
                "explanation": "Oldest sandstone temple in Kanchipuram, built in 685-705 CE by Narasimhavarman II (Rajasimha).",
                "significance": "Foundational monument that set the stylistic blueprint for all subsequent classical Dravidian architecture.",
                "source_url": "https://kancheepuram.nic.in/tourist-place/kailasanathar-temple/"
            },
            {
                "name": "Ekambareswarar Temple (Earth Element)",
                "category": "Pancha Bhoota Sthalam",
                "explanation": "Massive 25-acre temple complex representing Prithvi (Earth) with a 59-meter tall Rajagopuram built by Krishnadevaraya.",
                "significance": "Home to the revered 3,500-year-old sacred mango tree venerated in ancient hymns.",
                "source_url": "https://kancheepuram.nic.in/tourist-place/ekambareswarar-temple/"
            },
            {
                "name": "Ancient Ghatikasthanam (University of Kanchi)",
                "category": "Scholarly & Philosophical Center",
                "explanation": "Premier ancient university for Vedic, Buddhist, and Jain philosophical debate attended by scholars from across Asia.",
                "significance": "Birthplace and spiritual retreat of celebrated thinkers including Bodhidharma and Ramanuja.",
                "source_url": "https://kancheepuram.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Kailasanathar Temple",
                "category": "Pallava Masterpiece",
                "description": "Sandstone masterpiece decorated with early Pallava frescoes and over fifty shrine panels.",
                "link": "https://kancheepuram.nic.in/tourist-place/kailasanathar-temple/"
            },
            {
                "name": "Ekambareswarar Temple",
                "category": "Pancha Bhoota Prithvi",
                "description": "Towering temple complex symbolizing Earth element with a 1000-pillar hall.",
                "link": "https://kancheepuram.nic.in/tourist-place/ekambareswarar-temple/"
            },
            {
                "name": "Varadharaja Perumal Temple",
                "category": "Divya Desam",
                "description": "Historic Vaishnavite shrine with carved stone chain and subterranean Athi Varadar wooden idol.",
                "link": "https://kancheepuram.nic.in/tourist-place/varadharaja-perumal-temple/"
            }
        ]
    },
    11: {
        "region": "Southernmost Coastal / Nanjil Nadu",
        "intro_ta": "கன்னியாகுமரி — முக்கடல் கூடும் தென்கோடி முனை; விவேகானந்தர் பாறை நினைவு மண்டபம், 133 அடி திருவள்ளுவர் சிலை மற்றும் நாஞ்சில் நாட்டின் வளமான பாரம்பரியம்.",
        "intro_en": "Kanniyakumari marks the tri-sea confluence (Triveni Sangamam) at the southern tip of India, celebrated for Vivekananda Rock, Thiruvalluvar Statue, and Nanjil agrarian culture.",
        "search_aliases": ["Kanniyakumari", "கன்னியாகுமரி", "Kanyakumari", "Cape Comorin", "Nanjil Nadu", "நாஞ்சில் நாடு"],
        "hero_image": "/images/hero-temple.jpg",
        "specialities": [
            {
                "name": "Thiruvalluvar Statue & Vivekananda Rock Memorial",
                "category": "Iconic Maritime Heritage",
                "explanation": "133-foot stone statue celebrating the 133 chapters of the Tirukkural, alongside the 1970 rock memorial on the southern sea rocks.",
                "significance": "A defining global monument of Tamil literary philosophy and meditative discipline.",
                "source_url": "https://kanniyakumari.nic.in/tourist-place/thiruvalluvar-statue/"
            },
            {
                "name": "Triveni Sangamam (Three Seas Confluence)",
                "category": "Geographical Landmark",
                "explanation": "Where the Arabian Sea, Bay of Bengal, and Indian Ocean merge, allowing spectators to witness both sunrise and sunset from the same point.",
                "significance": "Celebrated in ancient Sangam epics and foreign geographical accounts for over two millennia.",
                "source_url": "https://kanniyakumari.nic.in/tourist-place/kanyakumari-beach/"
            },
            {
                "name": "Padmanabhapuram Palace",
                "category": "Timber Architectural Wonder",
                "explanation": "16th-century wooden palace complex built by the Venad rulers featuring master carved ceilings, secret passages, and mural art.",
                "significance": "Recognized as the finest preserved example of traditional Kerala-Tamil timber architecture.",
                "source_url": "https://kanniyakumari.nic.in/tourist-place/padmanabhapuram-palace/"
            },
            {
                "name": "Mathur Aqueduct",
                "category": "Engineering Landmark",
                "explanation": "One of the longest and highest trough aqueducts in South Asia, spanning 1,240 feet across the Pahrali river.",
                "significance": "Built in 1966 to carry irrigation waters across drought-prone hilly terrains.",
                "source_url": "https://kanniyakumari.nic.in/tourist-place/mathur-hanging-bridge/"
            }
        ],
        "famous_places": [
            {
                "name": "Vivekananda Rock Memorial",
                "category": "Monolithic Sea Shrine",
                "description": "Architectural marvel on a sea rock where Swami Vivekananda attained spiritual enlightenment in 1892.",
                "link": "https://kanniyakumari.nic.in/tourist-place/vivekananda-rock-memorial/"
            },
            {
                "name": "Thiruvalluvar Statue",
                "category": "Literary Monument",
                "description": "133-foot tall granite tribute to the immortal Tamil poet and philosopher Tiruvalluvar.",
                "link": "https://kanniyakumari.nic.in/tourist-place/thiruvalluvar-statue/"
            },
            {
                "name": "Padmanabhapuram Palace",
                "category": "Woodcraft Architecture",
                "description": "Intricately carved palace with Chinese granite floors, mica windows, and antique king's council hall.",
                "link": "https://kanniyakumari.nic.in/tourist-place/padmanabhapuram-palace/"
            }
        ]
    },
    12: {
        "region": "Central Kongu / Amaravathi Basin",
        "intro_ta": "கரூர் — சங்க கால சேரர்களின் பண்டைய தலைநகரமான கருவூர்; சர்வதேச வீட்டு ஜவுளி ஏற்றுமதி மையம் மற்றும் கொங்கு நாட்டு வரலாற்று தலம்.",
        "intro_en": "Karur is the ancient Sangam Chera royal seat of Karuvoor on the Amaravathi river, today celebrated as India's premier home textile manufacturing and export capital.",
        "search_aliases": ["Karur", "கரூர்", "Karuvoor", "கருவூர்"],
        "hero_image": "/images/tiruvannamalai.jpg",
        "specialities": [
            {
                "name": "Home Textiles Export Capital",
                "category": "Global Industrial Hub",
                "explanation": "Produces and exports bed linen, table runners, kitchen textiles, and curtains worth billions of rupees to worldwide retail chains.",
                "significance": "Earned Karur recognition as the Textile Town of Export Excellence.",
                "source_url": "https://karur.nic.in/"
            },
            {
                "name": "Ancient Karuvoor Chera Epigraphy",
                "category": "Sangam Archaeological Center",
                "explanation": "Identified by epigraphists as the Sangam Chera capital Vanji/Karuvoor, yielding Roman coin hoards, Chera punch-marked coins, and gemstone beads.",
                "significance": "Proof of classical trade links between ancient Tamil country and the Mediterranean Roman Empire.",
                "source_url": "https://karur.nic.in/"
            },
            {
                "name": "Pasupatheeswarar Temple",
                "category": "Chola & Pandyan Temple Heritage",
                "explanation": "7th-century Shiva temple lauded in Tevaram hymns, featuring a Swayambhu Lingam, stone inscriptions, and five-tiered Rajagopuram.",
                "significance": "Spiritual landmark adorned with ancient sculptural friezes.",
                "source_url": "https://karur.nic.in/tourist-place/sri-pasupatheeswarar-temple/"
            }
        ],
        "famous_places": [
            {
                "name": "Sri Pasupatheeswarar Temple",
                "category": "Ancient Chola Shrine",
                "description": "Tevaram-praised shrine with massive lingam displaying the hoof mark of Kamadhenu the sacred cow.",
                "link": "https://karur.nic.in/tourist-place/sri-pasupatheeswarar-temple/"
            },
            {
                "name": "Mayanur Barrage & Cauvery Park",
                "category": "Riverfront Tourism",
                "description": "Expansive barrage on the Cauvery river surrounded by botanical parks and boating amenities.",
                "link": "https://karur.nic.in/tourist-place/mayanur/"
            },
            {
                "name": "Nerur Sadashiva Brahmendra Jeeva Samadhi",
                "category": "Spiritual Sanctuary",
                "description": "Sacred riverside samadhi of the revered 18th-century Advaita saint and composer Sadashiva Brahmendra.",
                "link": "https://karur.nic.in/tourist-place/nerur/"
            }
        ]
    },
    13: {
        "region": "North-Western / Baramahal",
        "intro_ta": "கிருஷ்ணகிரி — வரலாற்றுப் பாராமஹால் பகுதி; மாம்பழ விளைச்சலின் தலைநகரம், ஓசூர் தொழில்துறை நகரம் மற்றும் சையது பாஷா மலைக்கோட்டையைக் கொண்டது.",
        "intro_en": "Krishnagiri, heart of the historic Baramahal region, is the mango capital of Tamil Nadu and home to the high-tech industrial manufacturing hub of Hosur.",
        "search_aliases": ["Krishnagiri", "கிருஷ்ணகிரி", "Baramahal", "Hosur", "ஓசூர்"],
        "hero_image": "/images/tiruvannamalai.jpg",
        "specialities": [
            {
                "name": "Mango Capital of Tamil Nadu",
                "category": "Horticultural Heritage",
                "explanation": "Cultivates over 40,000 hectares of premium mangoes including Totapuri, Alphonso, and Banganapalli, with large-scale pulp processing industries.",
                "significance": "Supplies fresh fruit and mango pulp to international beverage producers across the globe.",
                "source_url": "https://krishnagiri.nic.in/"
            },
            {
                "name": "Hosur Advanced EV & Industrial Ecosystem",
                "category": "Modern Engineering Hub",
                "explanation": "A major centre for two-wheeler, automobile, electric vehicle (EV), and aerospace precision manufacturing.",
                "significance": "A powerhouse of modern technological employment in northern Tamil Nadu.",
                "source_url": "https://krishnagiri.nic.in/"
            },
            {
                "name": "Baramahal Historic Forts",
                "category": "Military Architecture",
                "explanation": "Part of the twelve strategic hill forts (Baramahal) contested between Vijayanagara, Bijapur, Hyder Ali, and the British.",
                "significance": "Distinctive granite hill fortifications with reservoirs and bastions.",
                "source_url": "https://krishnagiri.nic.in/tourist-place/krishnagiri-fort/"
            }
        ],
        "famous_places": [
            {
                "name": "Krishnagiri Hill Fort",
                "category": "Hilltop Bastion",
                "description": "Imposing granite hill fortress overlooking the town, dating to the Vijayanagara and Hyder Ali eras.",
                "link": "https://krishnagiri.nic.in/tourist-place/krishnagiri-fort/"
            },
            {
                "name": "Krishnagiri Dam (KRP Dam)",
                "category": "Irrigation Dam & Park",
                "description": "Constructed in 1957 across Thenpennai river with lush landscaped gardens and boating.",
                "link": "https://krishnagiri.nic.in/tourist-place/krp-dam/"
            },
            {
                "name": "Hosur Hill Temple (Chandra Choodeswarar)",
                "category": "Historic Hill Temple",
                "description": "Ancient Shiva temple built on a hilltop offering panoramic views of the growing city of Hosur.",
                "link": "https://krishnagiri.nic.in/"
            }
        ]
    },
    14: {
        "region": "Southern / Pandya Heartland",
        "intro_ta": "மதுரை — 'தூங்கா நகரம்'; 2,500 ஆண்டுகள் பழமையான சங்கத் தமிழின் தலைநகரம், மீனாட்சி அம்மன் ஆலயம், மல்லிகைப் பூ மற்றும் ஜிகர்தண்டா பெருமை.",
        "intro_en": "Madurai, the timeless 'Athens of the East', is the cradle of Tamil Sangam academies on the Vaigai, world-famous for the Meenakshi Temple, GI-tagged jasmine, and Sungudi craft.",
        "search_aliases": ["Madurai", "மதுரை", "Koodal", "கூடல்", "Athens of the East"],
        "hero_image": "/images/madurai.jpg",
        "specialities": [
            {
                "name": "Meenakshi Sundareswarar Temple",
                "category": "Iconic Dravidian Monument",
                "explanation": "Magnificent temple complex with 14 towering gopurams, the Ashta Shakti Mandapam, and the world-renowned Hall of Thousand Pillars.",
                "significance": "Cultural epicenter of the Pandya dynasty and supreme achievement of Nayak architecture.",
                "source_url": "https://madurai.nic.in/tourist-place/arulmigu-meenakshi-sundareswarar-temple/"
            },
            {
                "name": "Madurai Malli (GI Tag)",
                "category": "Botanical GI Heritage",
                "explanation": "Special variety of jasmine (Jasminum sambac) with dense petals, deep fragrance, and extended freshness grown in Madurai's clayey soil.",
                "significance": "Flown daily to global perfume houses and traditional festivals across India.",
                "source_url": "https://madurai.nic.in/"
            },
            {
                "name": "Madurai Sungudi Sarees (GI Tag)",
                "category": "Textile GI Craft",
                "explanation": "Traditional tie-and-dye cotton sarees created by Saurashtrian weavers patronized by Nayak kings.",
                "significance": "Distinctive micro-dot bandhani patterns and contrasting zari borders.",
                "source_url": "https://madurai.nic.in/"
            },
            {
                "name": "Madurai Jigarthanda & Culinary Tradition",
                "category": "Iconic Culinary Heritage",
                "explanation": "Unique cooling dessert beverage made with almond gum (badam pisin), condensed milk, nannari syrup, and handcrafted ice cream.",
                "significance": "Beloved culinary trademark of Madurai street food culture.",
                "source_url": "https://madurai.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Meenakshi Amman Temple",
                "category": "Spiritual Center",
                "description": "Centuries-old living temple complex famous for polychrome sculpted gopurams and sacred Golden Lotus tank.",
                "link": "https://madurai.nic.in/tourist-place/arulmigu-meenakshi-sundareswarar-temple/"
            },
            {
                "name": "Thirumalai Nayakkar Mahal",
                "category": "Indo-Saracenic Palace",
                "description": "17th-century palace constructed in 1636 renowned for massive white stucco pillars and grand celestial dome.",
                "link": "https://madurai.nic.in/tourist-place/thirumalai-nayakar-mahal/"
            },
            {
                "name": "Alagar Kovil & Pazhamudircholai",
                "category": "Vaishnavite Heritage",
                "description": "Picturesque forest hill temple of Lord Kallazhagar and the final Arupadai Veedu shrine.",
                "link": "https://madurai.nic.in/tourist-place/alagar-kovil/"
            }
        ]
    },
    15: {
        "region": "Cauvery Delta / Chola Coast",
        "intro_ta": "மயிலாடுதுறை — தமிழ்நாட்டின் 38-வது மாவட்டம் (2020); சங்க காலப் பூம்புகார் துறைமுகம், தரங்கம்பாடி டேனிஷ் கோட்டை மற்றும் மயூரநாதர் ஆலயத் தலம்.",
        "intro_en": "Mayiladuthurai, formed as Tamil Nadu's 38th district in 2020, encompasses the legendary ancient port of Poompuhar, Tranquebar Danish Fort, and sacred Cauvery delta temples.",
        "search_aliases": ["Mayiladuthurai", "மயிலாடுதுறை", "Mayavaram", "மாயவரம்", "Poompuhar", "பூம்புகார்", "Tranquebar", "தரங்கம்பாடி"],
        "hero_image": "/images/thanjavur.jpg",
        "specialities": [
            {
                "name": "Ancient Port of Poompuhar (Kaveripoompattinam)",
                "category": "Sangam Maritime Archaeology",
                "explanation": "Legendary early Chola coastal metropolis celebrated in Silappathikaram and Manimekalai as the maritime capital of Karikala Chola.",
                "significance": "Undersea marine archaeology has revealed submerged brick docks, ring wells, and Roman coins.",
                "source_url": "https://mayiladuthurai.nic.in/tourist-place/poompuhar/"
            },
            {
                "name": "Tharangambadi (Tranquebar) Danish Fort",
                "category": "Colonial Maritime Heritage",
                "explanation": "Historic Danish settlement dating to 1620 featuring Fort Dansborg, the second largest Danish fort in the world.",
                "significance": "Site of the first Protestant mission and printing press in India established by Ziegenbalg in 1706.",
                "source_url": "https://mayiladuthurai.nic.in/tourist-place/tharangambadi/"
            },
            {
                "name": "Mayuranathar Temple & Cauvery Thula Utsavam",
                "category": "Sacred Delta Heritage",
                "explanation": "Ancient temple where Goddess Parvati worshipped Lord Shiva in the form of a peacock (Mayura).",
                "significance": "Host to the holy month-long Thula Snanam pilgrimage at Thula Kattam on the Cauvery.",
                "source_url": "https://mayiladuthurai.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Poompuhar Beach & Marine Museum",
                "category": "Sangam Epic Heritage",
                "description": "Historic coastline featuring Silappathikaram art gallery showcasing scenes from Kannagi's epic life.",
                "link": "https://mayiladuthurai.nic.in/tourist-place/poompuhar/"
            },
            {
                "name": "Fort Dansborg (Tranquebar)",
                "category": "Danish Coastal Bastion",
                "description": "Well-preserved 1620 Danish fort overlooking the Bay of Bengal with a maritime museum.",
                "link": "https://mayiladuthurai.nic.in/tourist-place/tharangambadi/"
            },
            {
                "name": "Vaitheeswaran Koil",
                "category": "Healing & Navagraha Shrine",
                "description": "Sacred shrine dedicated to Lord Shiva as the Divine Healer and the Angarakan (Mars) temple.",
                "link": "https://mayiladuthurai.nic.in/"
            }
        ]
    },
    16: {
        "region": "Coastal Delta / Maritime Heritage",
        "intro_ta": "நாகப்பட்டினம் — சோழர் கடற்படைத் துறைமுகம்; வேளாங்கண்ணி அன்னை ஆரோக்கிய பேராலயம், நாகூர் தர்கா மற்றும் கோடியக்கரை சரணாலயத்தைக் கொண்ட பன்முகக் கலாச்சார பூமி.",
        "intro_en": "Nagapattinam is a historic Chola maritime harbor, celebrated worldwide for the Velankanni Basilica, the Sufi shrine of Nagore Dargah, and Point Calimere wildlife sanctuary.",
        "search_aliases": ["Nagapattinam", "நாகப்பட்டினம்", "Nagapatnam", "Velankanni", "வேளாங்கண்ணி", "Nagore", "நாகூர்"],
        "hero_image": "/images/mamallapuram.jpg",
        "specialities": [
            {
                "name": "Velankanni Basilica of Our Lady of Good Health",
                "category": "International Pilgrimage Center",
                "explanation": "Revered Catholic Marian shrine often called the 'Lourdes of the East', attracting millions of pilgrims of all faiths annually.",
                "significance": "Elevated to a Minor Basilica by Pope John XXIII in 1962.",
                "source_url": "https://nagapattinam.nic.in/tourist-place/velankanni/"
            },
            {
                "name": "Nagore Dargah (Hazrat Syed Shahul Hameed)",
                "category": "Sufi Pilgrimage & Interfaith Harmony",
                "explanation": "500-year-old Islamic shrine of Sufi saint Hazrat Shahul Hameed with five soaring minarets, including the 131-foot Sahib Minaret.",
                "significance": "A symbol of deep communal harmony, with royal land grants gifted by Thanjavur Maratha kings.",
                "source_url": "https://nagapattinam.nic.in/tourist-place/nagore-dargah/"
            },
            {
                "name": "Point Calimere (Kodiakkarai) Wildlife Sanctuary",
                "category": "Ramsar Wetland Site",
                "explanation": "A coastal wildlife sanctuary featuring tidal flats, sand bars, blackbuck antelopes, and thousands of greater flamingos.",
                "significance": "Crucial refueling ground along the Central Asian Flyway for migratory avifauna.",
                "source_url": "https://nagapattinam.nic.in/tourist-place/point-calimere/"
            }
        ],
        "famous_places": [
            {
                "name": "Basilica of Our Lady of Good Health",
                "category": "Pilgrimage Sanctuary",
                "description": "Gothic style Basilica facing the Bay of Bengal, revered for miraculous healing traditions.",
                "link": "https://nagapattinam.nic.in/tourist-place/velankanni/"
            },
            {
                "name": "Nagore Dargah",
                "category": "Sufi Shrine",
                "description": "Historic Sufi shrine known for Kanduri festival and majestic gold-capped minarets.",
                "link": "https://nagapattinam.nic.in/tourist-place/nagore-dargah/"
            },
            {
                "name": "Point Calimere Blackbuck Sanctuary",
                "category": "Coastal Wildlife",
                "description": "Protected coastal ecosystem with blackbuck herds, spotted deer, wild horses, and flamingo flocks.",
                "link": "https://nagapattinam.nic.in/tourist-place/point-calimere/"
            }
        ]
    },
    17: {
        "region": "Kongu / Central Plains",
        "intro_ta": "நாமக்கல் — 'முட்டை மற்றும் லாரி நகரம்'; ஒற்றைக்கல் பாறை ஆஞ்சநேயர் கோயில், கொல்லிமலை நீர்வீழ்ச்சி மற்றும் இந்தியாவின் முன்னணி கோழிப்பண்ணை மையம்.",
        "intro_en": "Namakkal is India's 'Egg City' and transport body-building center, famous for the monolithic 18-foot Anjaneyar statue, Rock Fort, and the misty Kolli Hills.",
        "search_aliases": ["Namakkal", "நாமக்கல்", "Kolli Hills", "கொல்லிமலை"],
        "hero_image": "/images/tiruvannamalai.jpg",
        "specialities": [
            {
                "name": "Poultry Capital & Egg Production of India",
                "category": "Agricultural Economy",
                "explanation": "Produces over 35 million table eggs daily, supplying markets across India and exporting to the Middle East.",
                "significance": "A pioneer of modern scientific poultry farming and grain supply chain logistics.",
                "source_url": "https://namakkal.nic.in/"
            },
            {
                "name": "Namakkal Anjaneyar & Monolithic Rock Fort",
                "category": "Sculptural & Military Monument",
                "explanation": "Features an 18-foot single-stone open-air Anjaneyar statue facing Lord Narasimha swamy at the foot of an ancient granite rock fort.",
                "significance": "Noted 8th-century rock-cut Adiyan cave temples and Nayak-era defense bastions.",
                "source_url": "https://namakkal.nic.in/tourist-place/anjaneyar-temple/"
            },
            {
                "name": "Kolli Hills & Agaya Gangai Waterfalls",
                "category": "Hill Tourism & Medicinal Flora",
                "explanation": "A scenic mountain range with 70 hairpin bends, ancient Arapaleeswarar temple, organic spices, and valvil ori heritage.",
                "significance": "Celebrated in classical Sangam literature for King Valvil Ori's archery mastery.",
                "source_url": "https://namakkal.nic.in/tourist-place/kolli-hills/"
            }
        ],
        "famous_places": [
            {
                "name": "Namakkal Anjaneyar Temple",
                "category": "Monolithic Temple",
                "description": "Famous 18-foot open-air monolithic idol of Lord Hanuman standing with folded hands.",
                "link": "https://namakkal.nic.in/tourist-place/anjaneyar-temple/"
            },
            {
                "name": "Namakkal Fort",
                "category": "Granite Rock Fortress",
                "description": "Historical rock citadel built on a single monolithic rock summit with ancient water tanks.",
                "link": "https://namakkal.nic.in/tourist-place/namakkal-fort/"
            },
            {
                "name": "Kolli Hills & Agaya Gangai",
                "category": "Mountain Cascade",
                "description": "300-foot waterfall cascading into the Aiyaru river reached by descending 1,000 steps.",
                "link": "https://namakkal.nic.in/tourist-place/kolli-hills/"
            }
        ]
    },
    18: {
        "region": "Western Ghats / Mountain Biosphere",
        "intro_ta": "நீலகிரி — 'மலைகளின் அரசி'; யுனெஸ்கோ நீலகிரி மலை ரயில், பழங்குடியினர் தோடா எம்பிராய்டரி, தேயிலைத் தோட்டங்கள் மற்றும் முதுமலை புலிகள் காப்பகம்.",
        "intro_en": "The Nilgiris, 'Queen of Hill Stations', features the UNESCO Nilgiri Mountain Railway, Toda tribal embroidery, high-grown Orthodox tea, and Mudumalai Tiger Reserve.",
        "search_aliases": ["The Nilgiris", "Nilgiris", "நீலகிரி", "Ooty", "ஊட்டி", "Udhagamandalam", "உதகமண்டலம்"],
        "hero_image": "/images/tiruvannamalai.jpg",
        "specialities": [
            {
                "name": "Nilgiri Mountain Railway (UNESCO)",
                "category": "UNESCO World Heritage Site",
                "explanation": "Built by the British in 1908, it is the only operational rack and pinion mountain railway in India, scaling 2,200 meters from Mettupalayam to Ooty.",
                "significance": "A triumph of 19th-century railway engineering through dense Shola cloud forests.",
                "source_url": "https://nilgiris.nic.in/tourist-place/nilgiri-mountain-railway/"
            },
            {
                "name": "Toda Embroidery (GI Tag)",
                "category": "Tribal Textile GI Craft",
                "explanation": "Distinctive red and black wool embroidery on white unbleached cotton shawls (Poothkuli) created by the indigenous Toda pastoral community.",
                "significance": "Reflects ancient geometric motifs rooted in buffalo pastoralism and tribal cosmology.",
                "source_url": "https://nilgiris.nic.in/"
            },
            {
                "name": "Nilgiri Orthodox Tea (GI Tag)",
                "category": "Agri-GI Beverage Heritage",
                "explanation": "High-grown fragrant teas cultivated above 5,000 feet, celebrated for luminous golden liquor and brisk, flowery bouquet.",
                "significance": "Prized internationally in European and North American gourmet tea markets.",
                "source_url": "https://nilgiris.nic.in/"
            },
            {
                "name": "Mudumalai National Park & Tiger Reserve",
                "category": "Biosphere Conservation",
                "explanation": "Part of the Nilgiri Biosphere Reserve, sheltering endangered Bengal tigers, Asian elephants, Indian leopards, and gaurs.",
                "significance": "One of the most critical elephant corridors in South Asia.",
                "source_url": "https://nilgiris.nic.in/tourist-place/mudumalai-national-park/"
            }
        ],
        "famous_places": [
            {
                "name": "Nilgiri Mountain Toy Train",
                "category": "UNESCO Railway",
                "description": "Historic steam train chugging through 16 tunnels, 250 bridges, and scenic mountain tea slopes.",
                "link": "https://nilgiris.nic.in/tourist-place/nilgiri-mountain-railway/"
            },
            {
                "name": "Government Botanical Garden, Ooty",
                "category": "Horticultural Sanctuary",
                "description": "Established in 1848 spanning 55 acres with over a thousand plant species and a 20-million-year-old fossil tree trunk.",
                "link": "https://nilgiris.nic.in/tourist-place/botanical-garden/"
            },
            {
                "name": "Mudumalai Tiger Reserve",
                "category": "Wilderness Safari",
                "description": "Vast deciduous forest park offering elephant camp experiences and wildlife safaris.",
                "link": "https://nilgiris.nic.in/tourist-place/mudumalai-national-park/"
            }
        ]
    },
    19: {
        "region": "Central / Agricultural Plain",
        "intro_ta": "பெரம்பலூர் — வரலாற்று ரஞ்சன்குடி கோட்டை, தேசிய கல்மரப் பூங்கா மற்றும் தமிழ்நாட்டின் முக்கிய மக்காச்சோளம்-சின்ன வெங்காய உற்பத்தி மையம்.",
        "intro_en": "Perambalur is known for the 17th-century Ranjankudi Fort, National Fossil Wood Park, and extensive production of shallots and maize.",
        "search_aliases": ["Perambalur", "பெரம்பலூர்", "Ranjankudi", "ரஞ்சன்குடி"],
        "hero_image": "/images/thanjavur.jpg",
        "specialities": [
            {
                "name": "Ranjankudi Fort",
                "category": "Military Architecture",
                "explanation": "Formidable 17th-century rock fort built by the Jagirdar under the Nawab of the Carnatic, complete with moat, bastions, and royal audience halls.",
                "significance": "Site of the historic 1751 Battle of Valikondah during the Second Carnatic War.",
                "source_url": "https://perambalur.nic.in/tourist-place/ranjankudi-fort/"
            },
            {
                "name": "National Fossil Wood Park, Sathanur",
                "category": "Geological Heritage",
                "explanation": "Geological park preserving petrified coniferous tree trunks dating back over 120 million years to the Cretaceous era.",
                "significance": "Declared a National Geological Monument by the Geological Survey of India.",
                "source_url": "https://perambalur.nic.in/tourist-place/sathanur-fossil-tree/"
            },
            {
                "name": "Shallot (Small Onion) & Maize Hub",
                "category": "Agricultural Economy",
                "explanation": "Produces a vast portion of Tamil Nadu's small onions (chinna vengayam) and high-yield hybrid maize.",
                "significance": "Supplies fresh culinary ingredients across the entire state of Tamil Nadu.",
                "source_url": "https://perambalur.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Ranjankudi Fort",
                "category": "Nawab Fortress",
                "description": "Well-preserved stone fortress with defensive ramparts, arched gateways, and ancient watchtowers.",
                "link": "https://perambalur.nic.in/tourist-place/ranjankudi-fort/"
            },
            {
                "name": "Sathanur Fossil Tree",
                "category": "Geological Wonder",
                "description": "18-meter long petrified fossilized tree trunk revealing the prehistoric marine environment of central Tamil Nadu.",
                "link": "https://perambalur.nic.in/tourist-place/sathanur-fossil-tree/"
            },
            {
                "name": "Valikandapuram Temple",
                "category": "Ancient Chola Temple",
                "description": "Ancient Shiva temple carrying inscriptions of Rajaraja Chola and later Vijayanagara emperors.",
                "link": "https://perambalur.nic.in/"
            }
        ]
    },
    20: {
        "region": "Central Southern / Princely Heritage",
        "intro_ta": "புதுக்கோட்டை — தனித்துவ சமஸ்தான வரலாறு; சித்தன்னவாசல் சமணர் குகை ஓவியங்கள், திருமயம் கோட்டை மற்றும் குடுமியான்மலை இசைக்கல்வெட்டுகள்.",
        "intro_en": "Pudukkottai, former autonomous princely state of the Tondaiman rulers, is celebrated for Sittanavasal Jain frescoes, Thirumayam fort, and musical inscriptions.",
        "search_aliases": ["Pudukkottai", "புதுக்கோட்டை", "Sittanavasal", "சித்தன்னவாசல்", "Thirumayam", "திருமயம்"],
        "hero_image": "/images/thanjavur.jpg",
        "specialities": [
            {
                "name": "Sittanavasal Cave Paintings & Jain Beds",
                "category": "Ancient Fresco Art & Inscriptions",
                "explanation": "2nd century BCE to 9th century CE rock-cut Jain cave featuring exquisite natural vegetable-dye murals of lotus ponds and celestial dancers.",
                "significance": "Considered India's finest classical post-Ajanta Jain fresco art.",
                "source_url": "https://pudukkottai.nic.in/tourist-place/sittanavasal/"
            },
            {
                "name": "Thirumayam Rock Fort & Cave Temples",
                "category": "Rock-Cut Architecture",
                "explanation": "17th-century fort built by Sethupathi Vijaya Raghunatha, housing twin rock-cut cave temples dedicated to Shiva and Vishnu.",
                "significance": "Contains one of South India's largest reclining Anantasayana Vishnu rock sculptures.",
                "source_url": "https://pudukkottai.nic.in/tourist-place/thirumayam-fort/"
            },
            {
                "name": "Kudumiyanmalai Musical Inscription",
                "category": "Musicological Epigraphy",
                "explanation": "7th-century rock inscription attributed to Pallava king Mahendravarman I documenting classical Indian musical ragas and notations.",
                "significance": "One of the earliest and most complete stone treatises on classical Indian musicology.",
                "source_url": "https://pudukkottai.nic.in/tourist-place/kudumiyanmalai/"
            }
        ],
        "famous_places": [
            {
                "name": "Sittanavasal Cave",
                "category": "Jain Heritage",
                "description": "Ancient rock-cut hermitage with lotus pond frescoes and stone beds with Tamil-Brahmi inscriptions.",
                "link": "https://pudukkottai.nic.in/tourist-place/sittanavasal/"
            },
            {
                "name": "Thirumayam Fort",
                "category": "Hill Bastion",
                "description": "Massive ring fortress built on a solitary boulder with rock-cut temples and ancient armory.",
                "link": "https://pudukkottai.nic.in/tourist-place/thirumayam-fort/"
            },
            {
                "name": "Avudaiyarkoil (Thiruperunturai)",
                "category": "Sculptural Wonder",
                "description": "Atmospheric temple where saint Manikkavasagar composed Thiruvasagam, renowned for ceiling stone chains and woodwork.",
                "link": "https://pudukkottai.nic.in/tourist-place/avudaiyarkoil/"
            }
        ]
    },
    21: {
        "region": "Southern Coastal / Sethupathi Realm",
        "intro_ta": "இராமநாதபுரம் — சேதுபதி மன்னர்களின் பூமி; ராமேஸ்வரம் ராமநாதசுவாமி கோயில், பாம்பன் பாலம், தனுஷ்கோடி மற்றும் குண்டு மிளகாய் பெருமை.",
        "intro_en": "Ramanathapuram, historic seat of the Sethupathi dynasty, encompasses Rameswaram's grand Jyotirlinga corridors, engineering marvel Pamban Bridge, and Dhanushkodi.",
        "search_aliases": ["Ramanathapuram", "இராமநாதபுரம்", "Ramnad", "Rameswaram", "ராமேஸ்வரம்", "Dhanushkodi", "தனுஷ்கோடி"],
        "hero_image": "/images/madurai.jpg",
        "specialities": [
            {
                "name": "Ramanathaswamy Temple, Rameswaram",
                "category": "Sacred Jyotirlinga Architecture",
                "explanation": "One of the twelve sacred Jyotirlingas, boasting the longest temple corridor in the world with over 1,200 intricately carved sandstone pillars.",
                "significance": "Major pilgrimage terminus visited by millions of spiritual seekers from across the globe.",
                "source_url": "https://ramanathapuram.nic.in/tourist-place/arunmigu-ramanathaswamy-temple/"
            },
            {
                "name": "Historic Pamban Rail Bridge",
                "category": "Maritime Engineering Landmark",
                "explanation": "India's first sea bridge opened in 1914, featuring a Scherzer rolling lift span that opens to allow ships to pass through Palk Strait.",
                "significance": "A legendary symbol of Indian railway engineering over the surging sea.",
                "source_url": "https://ramanathapuram.nic.in/tourist-place/pamban-bridge/"
            },
            {
                "name": "Ramnad Mundu Chilli (GI Tag)",
                "category": "Agri-GI Horticultural Heritage",
                "explanation": "Unique round, thick-skinned dry red chilli grown in saline soils of Ramanathapuram, renowned for rich red colour and moderate pungency.",
                "significance": "Crucial ingredient for traditional Chettinad and South Indian culinary pastes.",
                "source_url": "https://ramanathapuram.nic.in/"
            },
            {
                "name": "Dhanushkodi ('Ghost Town')",
                "category": "Maritime Landmark & Pilgrimage",
                "explanation": "Destroyed in the 1964 cyclone, the windswept ruins at the eastern tip of Pamban island overlook the shallow waters of Rama's Bridge.",
                "significance": "Spiritual confluence of the Bay of Bengal and Indian Ocean.",
                "source_url": "https://ramanathapuram.nic.in/tourist-place/dhanushkodi/"
            }
        ],
        "famous_places": [
            {
                "name": "Rameswaram Temple Corridors",
                "category": "Pillared Corridor",
                "description": "World's longest stone temple corridor measuring nearly 4,000 feet in total length with 22 sacred teerthams.",
                "link": "https://ramanathapuram.nic.in/tourist-place/arunmigu-ramanathaswamy-temple/"
            },
            {
                "name": "Pamban Sea Bridge",
                "category": "Sea Bridge",
                "description": "Iconic railway viaduct stretching across 2 kilometers of open ocean connecting mainland to island.",
                "link": "https://ramanathapuram.nic.in/tourist-place/pamban-bridge/"
            },
            {
                "name": "Dr. A.P.J. Abdul Kalam Memorial",
                "category": "National Memorial",
                "description": "National memorial dedicated to the beloved former President and Missile Scientist of India.",
                "link": "https://ramanathapuram.nic.in/tourist-place/dr-a-p-j-abdulkalam-memorial/"
            }
        ]
    },
    22: {
        "region": "Northern / Palar Basin",
        "intro_ta": "இராணிப்பேட்டை — 2019-இல் வேலூரிலிருந்து பிரிந்த புதிய மாவட்டம்; தோல் பதனிடும் தொழில், பெல் (BHEL) ஆலை மற்றும் ஆற்காடு மக்கன் பேடா இனிப்புப் பெருமை.",
        "intro_en": "Ranipet, carved from Vellore in 2019, is a major global leather tanning and manufacturing hub, famous for BHEL engineering and Arcot Makkan Peda.",
        "search_aliases": ["Ranipet", "இராணிப்பேட்டை", "Arcot", "ஆற்காடு", "Walajah"],
        "hero_image": "/images/hero-temple.jpg",
        "specialities": [
            {
                "name": "Global Leather Footwear & Tanning Cluster",
                "category": "Industrial Export Cluster",
                "explanation": "Home to hundreds of modern tanneries and footwear factories producing finished leather for luxury fashion brands worldwide.",
                "significance": "Generates substantial foreign exchange and industrial employment in Tamil Nadu.",
                "source_url": "https://ranipet.nic.in/"
            },
            {
                "name": "Arcot Makkan Peda & Historic Arcot",
                "category": "Culinary & Historical Heritage",
                "explanation": "Signature dessert created during the Nawab of Arcot era, prepared from khoa, stuffed with nuts, and soaked in cardamom sugar syrup.",
                "significance": "A legendary royal sweetmeat celebrated across South India.",
                "source_url": "https://ranipet.nic.in/"
            },
            {
                "name": "BHEL Boiler Auxiliaries Plant",
                "category": "Heavy Engineering",
                "explanation": "Massive public sector enterprise facility manufacturing air preheaters and electrostatic precipitators for thermal power plants.",
                "significance": "Premier heavy engineering manufacturing anchor in northern Tamil Nadu.",
                "source_url": "https://ranipet.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Historic Arcot Fort & Delhi Gate",
                "category": "Military Gateway",
                "description": "Historical gate surviving from the fortified town of Arcot, linked to Robert Clive's 1751 defense.",
                "link": "https://ranipet.nic.in/"
            },
            {
                "name": "Kaveripakkam Ancient Lake",
                "category": "Historical Waterworks",
                "description": "Massive historic irrigation tank built during Pallava and Chola eras, spanning over 10 miles in perimeter.",
                "link": "https://ranipet.nic.in/"
            },
            {
                "name": "Walajapet Handloom & Bell Metal",
                "category": "Artisan Craft Hub",
                "description": "Traditional settlement established by the Nawabs, famed for silk handloom sarees and brass idols.",
                "link": "https://ranipet.nic.in/"
            }
        ]
    },
    23: {
        "region": "Western Central / Kongu Heartland",
        "intro_ta": "சேலம் — 'மாம்பழ நகரம் & எஃகு நகரம்'; மேட்டூர் அணை, ஏற்காடு மலைவாழிடம், சேலம் பட்டு மற்றும் இரும்பு-எஃகு தொழில்துறை தலைநகரம்.",
        "intro_en": "Salem, celebrated as the 'Mango City' and 'Steel City', is home to the historic Mettur Dam on the Cauvery, Yercaud hill resort, and Salem silk fabric.",
        "search_aliases": ["Salem", "சேலம்", "Mettur", "மேட்டூர்", "Yercaud", "ஏற்காடு"],
        "hero_image": "/images/tiruvannamalai.jpg",
        "specialities": [
            {
                "name": "Salem Steel Plant (SAIL)",
                "category": "Heavy Metallurgy",
                "explanation": "Specializes in high-quality cold-rolled stainless steel sheets and coin blanks supplying mints across the globe.",
                "significance": "Flagship industrial producer giving Salem its identity as the Steel City.",
                "source_url": "https://salem.nic.in/"
            },
            {
                "name": "Salem Fabric & Venpattu Silk (GI Tag)",
                "category": "Textile GI Heritage",
                "explanation": "Superior white silk dhotis and Angavastram woven with fine pure mulberry silk and pure gold zari borders.",
                "significance": "A benchmark of ceremonial dignity and cultural prestige in South India.",
                "source_url": "https://salem.nic.in/"
            },
            {
                "name": "Mettur Dam & Stanley Reservoir",
                "category": "Historic Engineering Landmark",
                "explanation": "Constructed in 1934 across the Cauvery river, it is one of the oldest and largest multi-purpose dams in India.",
                "significance": "Agricultural lifeline providing irrigation to over 2.7 million acres across the Cauvery delta.",
                "source_url": "https://salem.nic.in/tourist-place/mettur-dam/"
            },
            {
                "name": "Yercaud ('Jewel of the Shevaroys')",
                "category": "Hill Station & Eco-Tourism",
                "explanation": "Scenic hill retreat situated at 1,515 meters on the Shevaroy hills, known for coffee plantations, spice gardens, and Emerald Lake.",
                "significance": "Popular mountain getaway offering tranquil climate and orange groves.",
                "source_url": "https://salem.nic.in/tourist-place/yercaud/"
            }
        ],
        "famous_places": [
            {
                "name": "Mettur Dam",
                "category": "Civil Engineering Feat",
                "description": "Massive masonry dam with a sprawling reservoir, Ellis park, and hydroelectric power stations.",
                "link": "https://salem.nic.in/tourist-place/mettur-dam/"
            },
            {
                "name": "Yercaud Hill Station",
                "category": "Shevaroy Mountain Resort",
                "description": "Charming hill station featuring Big Lake, Lady's Seat viewpoint, and coffee orchards.",
                "link": "https://salem.nic.in/tourist-place/yercaud/"
            },
            {
                "name": "Kottai Mariamman Temple",
                "category": "Historic City Temple",
                "description": "Ancient guardian temple of Salem town located in the historic fort area, famed for Aadi festival.",
                "link": "https://salem.nic.in/"
            }
        ]
    },
    24: {
        "region": "Southern / Chettinad & Maruthu Realm",
        "intro_ta": "சிவகங்கை — வீரத்தின் பூமி; மருது சகோதரர்களின் சுதேசி விடுதலைப் போராட்ட தளம், செட்டிநாடு மாளிகைகள், ஆத்தங்குடி டைல்ஸ் மற்றும் கீழடி தொல்லியல் களம்.",
        "intro_en": "Sivaganga is the land of freedom fighters Maruthu Pandiyars, palatial Chettinad heritage mansions, Athangudi handmade tiles, and the historic Keezhadi excavations.",
        "search_aliases": ["Sivaganga", "சிவகங்கை", "Chettinad", "செட்டிநாடு", "Keezhadi", "கீழடி", "Karaikudi", "காரைக்குடி"],
        "hero_image": "/images/madurai.jpg",
        "specialities": [
            {
                "name": "Keezhadi Archaeological Excavations",
                "category": "Sangam Urban Civilization",
                "explanation": "Archaeological excavations on the Vaigai river proving an advanced, literate, secular urban civilization in Tamil Nadu dating to 6th century BCE.",
                "significance": "Rewrote ancient Indian historiography by demonstrating contemporary urbanism with Gangetic cities.",
                "source_url": "https://sivaganga.nic.in/tourist-place/keeladi-excavation-site/"
            },
            {
                "name": "Chettinad Heritage Architecture & Palaces",
                "category": "Architectural Marvel",
                "explanation": "Vast palatial residences built by Nagarathar merchant bankers with Burma teak, Italian marble, Belgian mirrors, and grand courtyards.",
                "significance": "A world-renowned heritage treasure celebrated for indigenous cooling engineering.",
                "source_url": "https://sivaganga.nic.in/tourist-place/kanadukathan-palace/"
            },
            {
                "name": "Chettinad Athangudi Tiles (GI Tag)",
                "category": "Handcrafted GI Heritage",
                "explanation": "Handmade patterned floor tiles crafted from local sand, cement, and synthetic oxides using glass casting moulds.",
                "significance": "Famous for brilliant sheen and intricate floral/geometric designs that last generations.",
                "source_url": "https://sivaganga.nic.in/"
            },
            {
                "name": "Maruthu Pandiyars & 1801 Tiruchirappalli Proclamation",
                "category": "Freedom Struggle Heritage",
                "explanation": "Seat of legendary rulers Maruthu Singam and Chinna Maruthu who issued the first pan-Indian call to arms against British colonial rule in 1801.",
                "significance": "Foundational heroes of early anti-colonial Indian independence struggle.",
                "source_url": "https://sivaganga.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Keezhadi Museum & Site",
                "category": "Archaeological Site",
                "description": "World-class museum displaying over 5,000 artifacts including Tamil-Brahmi pottery, ivory dice, and terracotta figurines.",
                "link": "https://sivaganga.nic.in/tourist-place/keeladi-excavation-site/"
            },
            {
                "name": "Kanadukathan Palace",
                "category": "Chettinad Mansion",
                "description": "Opulent Chettinad palace featuring hand-carved teak doors, chandeliers, and marble halls.",
                "link": "https://sivaganga.nic.in/tourist-place/kanadukathan-palace/"
            },
            {
                "name": "Kalaiyar Kovil (Kaleeswarar Temple)",
                "category": "Fortified Temple",
                "description": "Historic temple defended by the Maruthu brothers with a majestic 157-foot Rajagopuram.",
                "link": "https://sivaganga.nic.in/tourist-place/kalaiyarkoil-temple/"
            }
        ]
    },
    25: {
        "region": "Southern Western Ghats / Waterfalls",
        "intro_ta": "தென்காசி — 'தெற்கின் காசி'; குற்றாலம் மூலிகை நீர்வீழ்ச்சிகள், காசி விஸ்வநாதர் ஆலயம் மற்றும் பூலித்தேவரின் நெற்கட்டும்செவல் சுதந்திரப் போராட்ட தளம்.",
        "intro_en": "Tenkasi, 'Kasi of the South', formed in 2019 from Tirunelveli, is celebrated for Courtallam's herbal waterfalls, Kasi Viswanathar temple, and early freedom hero Puli Thevar.",
        "search_aliases": ["Tenkasi", "தென்காசி", "Courtallam", "குற்றாலம்", "Kutralam"],
        "hero_image": "/images/madurai.jpg",
        "specialities": [
            {
                "name": "Courtallam Waterfalls ('Spa of South India')",
                "category": "Natural Herbal Therapy",
                "explanation": "Series of cascades (Main Falls, Five Falls, Old Courtallam, Tiger Falls) flowing through dense Western Ghats medicinal forest reserves.",
                "significance": "Celebrated for healing natural mineral baths and rejuvenating holiday seasons during the southwest monsoon.",
                "source_url": "https://tenkasi.nic.in/tourist-place/courtallam/"
            },
            {
                "name": "Kasi Viswanathar Temple, Tenkasi",
                "category": "Pandyan Sacred Heritage",
                "explanation": "Built in the 15th century by Pandyan King Parakkirama Pandiyan who brought a sacred lingam from Varanasi so pilgrims could worship without traveling north.",
                "significance": "Features a towering 180-foot Rajagopuram with an acoustic wind passage and musical pillar halls.",
                "source_url": "https://tenkasi.nic.in/tourist-place/kasi-viswanathar-temple/"
            },
            {
                "name": "Puli Thevar & Nerkattumseval Freedom Struggle",
                "category": "Early Anti-Colonial Resistance",
                "explanation": "Seat of Palayakarar chieftain Puli Thevar who waged the earliest armed resistance against the British East India Company in the 1750s.",
                "significance": "Honored as one of India's earliest indigenous freedom fighters.",
                "source_url": "https://tenkasi.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Courtallam Main Falls",
                "category": "Herbal Waterfall",
                "description": "Cascading medicinal waterfall originating in the Western Ghats dropping into a natural stone basin.",
                "link": "https://tenkasi.nic.in/tourist-place/courtallam/"
            },
            {
                "name": "Tenkasi Kasi Viswanathar Temple",
                "category": "Pandyan Architecture",
                "description": "Magnificent temple with musical pillars and breeze passage built by king Parakkirama Pandiyan.",
                "link": "https://tenkasi.nic.in/tourist-place/kasi-viswanathar-temple/"
            },
            {
                "name": "Five Falls (Aintharuvi)",
                "category": "Scenic Waterfalls",
                "description": "Spectacular waterfall where the stream divides into five distinct cascades over the rocks.",
                "link": "https://tenkasi.nic.in/tourist-place/courtallam/"
            }
        ]
    },
    26: {
        "region": "Cauvery Delta / Chola Imperial Heart",
        "intro_ta": "தஞ்சாவூர் — 'தமிழ்நாட்டின் நெற்களஞ்சியம்'; ராஜராஜ சோழனின் பெருவுடையார் கோயில் (யுனெஸ்கோ), தஞ்சாவூர் ஓவியங்கள், தட்டு, வீணை மற்றும் சரசுவதி மகால் நூலகம்.",
        "intro_en": "Thanjavur, the 'Rice Bowl of Tamil Nadu', is the imperial crown of the Cholas, home to the UNESCO Brihadeeswarar Temple, Saraswathi Mahal Library, and GI arts.",
        "search_aliases": ["Thanjavur", "தஞ்சாவூர்", "Tanjore", "தஞ்சை", "Brihadeeswarar", "பெருவுடையார்"],
        "hero_image": "/images/thanjavur.jpg",
        "specialities": [
            {
                "name": "Brihadeeswarar Temple (UNESCO Great Living Chola Temple)",
                "category": "UNESCO World Heritage Site",
                "explanation": "Built in 1010 CE by Emperor Rajaraja Chola I, featuring a 216-foot granite Vimana topped by an 80-tonne single-stone Kumbam.",
                "significance": "Pinnacle of pure granite Dravidian architecture with monumental Chola frescoes and inscriptional records.",
                "source_url": "https://thanjavur.nic.in/tourist-place/brihadeeswarar-temple/"
            },
            {
                "name": "Thanjavur Paintings (GI Tag)",
                "category": "Geographical Indication (GI) Fine Art",
                "explanation": "Classical South Indian painting style characterized by rich, vivid colors, gesso work, and precious gold leaf overlay with semi-precious stones.",
                "significance": "Flourished under the Maratha rulers of Thanjavur since the 17th century.",
                "source_url": "https://thanjavur.nic.in/"
            },
            {
                "name": "Thanjavur Art Plate & Dancing Dolls (GI Tag)",
                "category": "Handicraft GI Heritage",
                "explanation": "Circular brass and copper plates inlaid with silver motifs of deities, alongside the iconic roly-poly bobblehead Thanjavur dolls (Thalaiyatti Bommai).",
                "significance": "Cherished globally for mathematical centre-of-gravity balance and artisanal elegance.",
                "source_url": "https://thanjavur.nic.in/"
            },
            {
                "name": "Saraswathi Mahal Library",
                "category": "Ancient Manuscripts Repository",
                "explanation": "One of the oldest libraries in Asia established by the Nayak and Maratha rulers, housing over 60,000 rare palm-leaf and paper manuscripts.",
                "significance": "Described by encyclopedia scholars as the most remarkable library in India.",
                "source_url": "https://thanjavur.nic.in/tourist-place/saraswathi-mahal-library/"
            }
        ],
        "famous_places": [
            {
                "name": "Peruvudaiyar Kovil (Big Temple)",
                "category": "Chola Masterpiece",
                "description": "1,000-year-old architectural marvel with monolithic Nandi and towering granite sanctum vimanam.",
                "link": "https://thanjavur.nic.in/tourist-place/brihadeeswarar-temple/"
            },
            {
                "name": "Thanjavur Royal Palace Complex",
                "category": "Nayak & Maratha Palace",
                "description": "Historic residence of Nayak and Maratha rulers housing Art Gallery, Bell Tower, and Arsenal Tower.",
                "link": "https://thanjavur.nic.in/tourist-place/thanjavur-palace/"
            },
            {
                "name": "Saraswathi Mahal Library",
                "category": "Manuscript Heritage",
                "description": "Ancient royal library preserving manuscripts in Tamil, Sanskrit, Telugu, Marathi, and Modi script.",
                "link": "https://thanjavur.nic.in/tourist-place/saraswathi-mahal-library/"
            }
        ]
    },
    27: {
        "region": "Western Ghats / Vaigai Valley",
        "intro_ta": "தேனி — மேற்குத் தொடர்ச்சி மலையடிவார இயற்கை சொர்க்கம்; மேகமலை ஏலக்காய் தோட்டங்கள், சுருளி நீர்வீழ்ச்சி மற்றும் கம்பம் பள்ளத்தாக்கு திராட்சைத் தோட்டம்.",
        "intro_en": "Theni, framed by the Western Ghats and Vaigai basin, is celebrated for Megamalai tea estates, the herbal cascades of Suruli Falls, and Cumbum Valley grapes.",
        "search_aliases": ["Theni", "தேனி", "Megamalai", "மேகமலை", "Suruli", "சுருளி", "Cumbum", "கம்பம்"],
        "hero_image": "/images/madurai.jpg",
        "specialities": [
            {
                "name": "Cumbum Panneer Thratchai (Grape) (GI Tag)",
                "category": "Agri-GI Horticultural Pride",
                "explanation": "Muscat Hamburg black grapes cultivated year-round in the sunny microclimate of Cumbum Valley.",
                "significance": "Constitutes over 85% of India's Muscat grape production with year-round harvest cycles.",
                "source_url": "https://theni.nic.in/"
            },
            {
                "name": "Megamalai ('Highwavy Mountains')",
                "category": "Cardamom & Wildlife Sanctuary",
                "explanation": "Misty mountain range rising over 1,500 meters, teeming with tea gardens, cardamom plantations, and the Srivilliputhur-Megamalai Tiger Reserve.",
                "significance": "A pristine habitat for endangered Nilgiri tahrs, leopards, and hornbills.",
                "source_url": "https://theni.nic.in/tourist-place/megamalai/"
            },
            {
                "name": "Suruli Falls & Herbal Stream",
                "category": "Natural Cascade",
                "explanation": "Two-stage cascading waterfall in the Suruli hills, praised in the Sangam epic Silappathikaram for its curative properties.",
                "significance": "Sacred and scenic pilgrim bathing site during Chithirai festival.",
                "source_url": "https://theni.nic.in/tourist-place/suruli-falls/"
            }
        ],
        "famous_places": [
            {
                "name": "Megamalai Wildlife Sanctuary",
                "category": "Cloud Forest Sanctuary",
                "description": "Picturesque hill country with misty tea gardens, man-made lakes, and elephant herds.",
                "link": "https://theni.nic.in/tourist-place/megamalai/"
            },
            {
                "name": "Suruli Falls",
                "category": "Forest Waterfall",
                "description": "Historic waterfall flowing through rock-cut caves near Kailasanathar shrine.",
                "link": "https://theni.nic.in/tourist-place/suruli-falls/"
            },
            {
                "name": "Vaigai Dam",
                "category": "Reservoir & Garden",
                "description": "Historic irrigation dam built across the Vaigai river with illuminated botanical parks.",
                "link": "https://theni.nic.in/tourist-place/vaigai-dam/"
            }
        ]
    },
    28: {
        "region": "Southern Coastal / Gulf of Mannar",
        "intro_ta": "தூத்துக்குடி — 'முத்து நகரம்'; வ.உ.சி துறைமுகம், பனிமய மாதா பேராலயம், கோவில்பட்டி கடலை மிட்டாய் மற்றும் தூத்துக்குடி மக்கரூன் பெருமை.",
        "intro_en": "Thoothukudi, the historic 'Pearl City', is a major seaport honoring V.O. Chidambaranar, famed for Kovilpatti Kadalai Mittai, salt pans, and macaroon treats.",
        "search_aliases": ["Thoothukudi", "தூத்துக்குடி", "Tuticorin", "Pearl City", "முத்து நகர்", "Kovilpatti", "கோவில்பட்டி"],
        "hero_image": "/images/mamallapuram.jpg",
        "specialities": [
            {
                "name": "Kovilpatti Kadalai Mittai (GI Tag)",
                "category": "Confectionery GI Heritage",
                "explanation": "Crispy traditional peanut brittle bar crafted with pure organic jaggery syrup and native roasted groundnuts, garnished with coconut flakes.",
                "significance": "A cherished nutritious sweetmeat exported globally.",
                "source_url": "https://thoothukudi.nic.in/"
            },
            {
                "name": "V.O. Chidambaranar Port & Maritime Legacy",
                "category": "Seaport & Maritime Trade",
                "explanation": "One of India's 12 major ports, historic home to freedom fighter V.O. Chidambaram Pillai who founded the first indigenous Swadeshi Steam Navigation Company in 1906.",
                "significance": "Pivotal hub for international container shipping and thermal energy imports.",
                "source_url": "https://thoothukudi.nic.in/"
            },
            {
                "name": "Pearl Fishery & Salt Manufacturing",
                "category": "Natural Resource & Industry",
                "explanation": "Ancient natural pearl diving coast recorded by Marco Polo and Ptolemy, now India's second largest salt producing hub.",
                "significance": "Supplies over 2 million tonnes of industrial and edible salt annually.",
                "source_url": "https://thoothukudi.nic.in/"
            },
            {
                "name": "Thoothukudi Macaroon",
                "category": "Colonial Pastry Tradition",
                "explanation": "Light, crispy, spiral-shaped macaroon baked with egg whites, cashew nuts, and sugar, adapted from Portuguese colonial baking.",
                "significance": "Famous signature confectionery sought by food lovers across Tamil Nadu.",
                "source_url": "https://thoothukudi.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Our Lady of Snows Basilica",
                "category": "Portuguese Maritime Shrine",
                "description": "16th-century Catholic shrine dedicated to Our Lady of the Snows, honored with annual golden car festival.",
                "link": "https://thoothukudi.nic.in/tourist-place/our-lady-of-snows-basilica/"
            },
            {
                "name": "Tiruchendur Murugan Temple",
                "category": "Arupadai Veedu Coastal Shrine",
                "description": "Second shrine of Lord Murugan located directly on the seashore where Lord Murugan conquered Surapadman.",
                "link": "https://thoothukudi.nic.in/tourist-place/arunmigu-subramaniaswamy-temple/"
            },
            {
                "name": "Kulasekharapatnam Mutharamman Temple",
                "category": "Dasara Coastal Festival",
                "description": "Famous coastal temple celebrated for its grand 10-day Dasara festival where devotees disguise themselves in sacred avatars.",
                "link": "https://thoothukudi.nic.in/tourist-place/kulasekharapatnam-mutharamman-temple/"
            }
        ]
    },
    29: {
        "region": "Cauvery Delta / Central Heartland",
        "intro_ta": "திருச்சிராப்பள்ளி — வரலாற்று மலைக்கோட்டை; ஸ்ரீரங்கம் ரங்கநாதசுவாமி கோயில், கரிகால சோழனின் கல்லணை மற்றும் மணப்பாறை முறுக்கு பெருமை.",
        "intro_en": "Tiruchirappalli, centered around the iconic Rockfort, is home to the sprawling Sri Ranganathaswamy Temple, Karikala Chola's Kallanai dam, and Manapparai Murukku.",
        "search_aliases": ["Tiruchirappalli", "திருச்சிராப்பள்ளி", "Trichy", "திருச்சி", "Trichinopoly", "Srirangam", "ஸ்ரீரங்கம்"],
        "hero_image": "/images/thanjavur.jpg",
        "specialities": [
            {
                "name": "Sri Ranganathaswamy Temple, Srirangam",
                "category": "Premier Vaishnavite Heritage & UNESCO Award",
                "explanation": "The foremost of the 108 Divya Desams, spanning 156 acres with 21 grand gopurams including the 236-foot Rajagopuram.",
                "significance": "Often considered the largest functioning Hindu temple complex in the world.",
                "source_url": "https://tiruchirappalli.nic.in/tourist-place/srirangam-temple/"
            },
            {
                "name": "Kallanai (Grand Anicut Built by Karikala Chola)",
                "category": "World's Oldest Water Regulating Dam",
                "explanation": "Built in the 2nd century CE across the Cauvery river, it remains in continuous functional use diverting irrigation waters.",
                "significance": "Recognized internationally as an engineering wonder of ancient hydraulic civilization.",
                "source_url": "https://tiruchirappalli.nic.in/tourist-place/kallanai-dam/"
            },
            {
                "name": "Tiruchirappalli Rockfort & Ucchi Pillayar Temple",
                "category": "Geological & Military Wonder",
                "explanation": "Ancient 272-foot high monolithic rock hill dating back 3.8 billion years (older than the Himalayas) with Pallava rock-cut cave temples.",
                "significance": "Served as a military fortress for Nayaks and Carnatic Nawabs.",
                "source_url": "https://tiruchirappalli.nic.in/tourist-place/rock-fort-temple/"
            },
            {
                "name": "Manapparai Murukku (GI Tag)",
                "category": "Culinary GI Specialty",
                "explanation": "Crispy traditional spiral snack made with rice flour, sesame, and native spring water, double-fried for golden crunchiness.",
                "significance": "A legendary snack trademark across South India.",
                "source_url": "https://tiruchirappalli.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Rockfort Temple",
                "category": "Geological Fortress Shrine",
                "description": "Historic hill temple reached by 437 stone-cut steps offering 360-degree views of the Cauvery valley.",
                "link": "https://tiruchirappalli.nic.in/tourist-place/rock-fort-temple/"
            },
            {
                "name": "Srirangam Ranganathaswamy Temple",
                "category": "Monumental Temple Complex",
                "description": "Vast temple city within seven concentric enclosures and the soaring 73-meter Rajagopuram.",
                "link": "https://tiruchirappalli.nic.in/tourist-place/srirangam-temple/"
            },
            {
                "name": "Kallanai Dam",
                "category": "Ancient Hydraulic Monument",
                "description": "2nd-century diversion dam built by Karikala Chola splitting the Cauvery into Vennar and Kollidam.",
                "link": "https://tiruchirappalli.nic.in/tourist-place/kallanai-dam/"
            }
        ]
    },
    30: {
        "region": "Southern / Thamirabarani Basin",
        "intro_ta": "திருநெல்வேலி — தாமிரபரணி நதிக்கரை கலாச்சாரம்; நெல்லையப்பர் கோயில் இசைத் தூண்கள், உலகப் புகழ்பெற்ற திருநெல்வேலி அல்வா மற்றும் மாஞ்சோலை தேயிலை மலை.",
        "intro_en": "Tirunelveli, nourished by the perennial Thamirabarani river, is famed for the ancient Nellaiappar Temple's musical pillars, GI Tirunelveli Halwa, and Manjolai hills.",
        "search_aliases": ["Tirunelveli", "திருநெல்வேலி", "Nellai", "நெல்லை", "Tinnevelly"],
        "hero_image": "/images/madurai.jpg",
        "specialities": [
            {
                "name": "Tirunelveli Halwa (GI Tag)",
                "category": "Geographical Indication (GI) Culinary Legend",
                "explanation": "Made from fermented whole-wheat milk, clarified cow's butter (ghee), and sugar, slowly simmered with mineral-rich Thamirabarani water.",
                "significance": "Celebrated since the mid-19th century as one of India's most iconic confections.",
                "source_url": "https://tirunelveli.nic.in/"
            },
            {
                "name": "Nellaiappar & Kanthimathi Temple (Musical Pillars)",
                "category": "Dravidian Architectural Wonder",
                "explanation": "Massive 14-acre temple complex dating back to 700 CE, featuring the Mani Mandapam with intricate musical stone pillars that resonate with musical notes.",
                "significance": "Contains the celebrated Tamra Sabha (Copper Hall of Dance), one of the five Pancha Sabhas.",
                "source_url": "https://tirunelveli.nic.in/tourist-place/sri-nellaiappar-temple/"
            },
            {
                "name": "Thamirabarani Perennial River",
                "category": "Perennial River System",
                "explanation": "Only perennial river entirely within Tamil Nadu originating in Agasthiyar hills, sustaining fertile agriculture and ancient civilizations.",
                "significance": "Archaeological findings at Adichanallur on its banks date back over 3,000 years.",
                "source_url": "https://tirunelveli.nic.in/"
            },
            {
                "name": "Manjolai Hill Tea Estates",
                "category": "Eco-Tourism & Mist Reserve",
                "explanation": "Serene tea plantations and cloud forests situated inside the Kalakkad Mundanthurai Tiger Reserve.",
                "significance": "Known as the poor man's Ooty with quiet viewpoint reservoirs like Kakkachi.",
                "source_url": "https://tirunelveli.nic.in/tourist-place/manjolai/"
            }
        ],
        "famous_places": [
            {
                "name": "Nellaiappar Temple",
                "category": "Ancient Pandyan Temple",
                "description": "Double temple dedicated to Shiva and Kanthimathi with musical pillars and Golden Lotus tank.",
                "link": "https://tirunelveli.nic.in/tourist-place/sri-nellaiappar-temple/"
            },
            {
                "name": "Agasthiyar Falls (Papanasam)",
                "category": "Sacred Forest Waterfalls",
                "description": "Picturesque falls on Thamirabarani river believed to cure ailments with medicinal water.",
                "link": "https://tirunelveli.nic.in/tourist-place/papanasam/"
            },
            {
                "name": "Adichanallur Iron Age Site",
                "category": "Prehistoric Archaeological Site",
                "description": "Archaeological excavation site revealing 3,000-year-old burial urns, bronze artifacts, and gold diadems.",
                "link": "https://tirunelveli.nic.in/"
            }
        ]
    },
    31: {
        "region": "Northern / Javadhu Hills & Palar",
        "intro_ta": "திருப்பத்தூர் — 2019-இல் உருவான புதிய மாவட்டம்; ஏலகிரி மலைகள், வைணு பாப்பு வானாய்வகம், ஆம்பூர் பிரியாணி மற்றும் தோல் தொழில் பெருமை.",
        "intro_en": "Tirupathur, established in 2019 from Vellore, is framed by the Yelagiri Hills, Asia's major Vainu Bappu Observatory at Kavalur, and Ambur biryani heritage.",
        "search_aliases": ["Tirupathur", "திருப்பத்தூர்", "Yelagiri", "ஏலகிரி", "Ambur", "ஆம்பூர்", "Vaniyambadi", "வாணியம்பாடி"],
        "hero_image": "/images/tiruvannamalai.jpg",
        "specialities": [
            {
                "name": "Yelagiri Hills ('Poor Man's Ooty')",
                "category": "Hill Station & Adventure Hub",
                "explanation": "Peaceful hill cluster located at 1,110 meters comprising 14 tribal hamlets, rose gardens, and a man-made boating lake.",
                "significance": "Famous paragliding, rock climbing, and nature trekking destination.",
                "source_url": "https://tirupathur.nic.in/tourist-place/yelagiri-hills/"
            },
            {
                "name": "Vainu Bappu Observatory, Kavalur",
                "category": "Astronomical Science Heritage",
                "explanation": "Home to the 2.34-meter Vainu Bappu Telescope, one of the largest optical telescopes in Asia operated by the Indian Institute of Astrophysics.",
                "significance": "Major global astronomical discoveries made from this clear night-sky observatory.",
                "source_url": "https://tirupathur.nic.in/tourist-place/vainu-bappu-observatory/"
            },
            {
                "name": "Ambur Biryani & Leather Cluster",
                "category": "Culinary & Industrial Heritage",
                "explanation": "Famous Seeraga Samba dum biryani created during Arcot Nawab rule, alongside world-renowned leather tanning and export industries.",
                "significance": "Culinary signature of Tamil Nadu with global food appreciation.",
                "source_url": "https://tirupathur.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Yelagiri Punganur Lake & Park",
                "category": "Hill Station Lake",
                "description": "Scenic boating lake surrounded by rose gardens, children's park, and herbal nature walks.",
                "link": "https://tirupathur.nic.in/tourist-place/yelagiri-hills/"
            },
            {
                "name": "Vainu Bappu Observatory",
                "category": "Optical Observatory",
                "description": "Asia's premier astronomical facility situated in dense forest clearing near Kavalur.",
                "link": "https://tirupathur.nic.in/tourist-place/vainu-bappu-observatory/"
            },
            {
                "name": "Jalagamparai Waterfalls",
                "category": "Mountain Cascade",
                "description": "Cascading waterfall created by the Attaru river cutting through the Yelagiri hills.",
                "link": "https://tirupathur.nic.in/tourist-place/jalagamparai-waterfalls/"
            }
        ]
    },
    32: {
        "region": "Kongu / Western Textile Hub",
        "intro_ta": "திருப்பூர் — 'இந்தியாவின் பின்னலாடைத் தலைநகரம்'; உலகளாவிய பருத்தி பனியன் ஏற்றுமதி, ஊத்துக்குளி வெண்ணெய் மற்றும் காங்கேயம் காளைகள் பெருமை.",
        "intro_en": "Tiruppur, the 'Knitwear Capital of India', produces over 90% of the country's cotton knitwear exports, famed for Kangeyam cattle and Uthukuli butter.",
        "search_aliases": ["Tiruppur", "திருப்பூர்", "Knitwear Capital", "Kangeyam", "காங்கேயம்", "Uthukuli", "ஊத்துக்குளி"],
        "hero_image": "/images/tiruvannamalai.jpg",
        "specialities": [
            {
                "name": "Knitwear Capital of India ('Dollar City')",
                "category": "Global Garment Export Hub",
                "explanation": "World-class textile cluster manufacturing cotton hosiery, casual wear, and sportswear exported to top global fashion brands.",
                "significance": "Generates over 30,000 crore rupees in annual foreign exchange earnings.",
                "source_url": "https://tiruppur.nic.in/"
            },
            {
                "name": "Kangeyam Bull Breed & Heritage",
                "category": "Indigenous Cattle Heritage",
                "explanation": "Hardy indigenous draught cattle breed celebrated for stamina, speed, and drought resistance, recognized as Tamil Nadu's pride.",
                "significance": "Integral to traditional Jallikattu and sustainable organic farming.",
                "source_url": "https://tiruppur.nic.in/"
            },
            {
                "name": "Uthukuli Butter",
                "category": "Culinary Dairy Specialty",
                "explanation": "Traditional churned butter made from buffalo milk, famed across South India for rich aroma and extended natural freshness.",
                "significance": "Classic culinary staple used by fine sweetmakers and households.",
                "source_url": "https://tiruppur.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Thirumoorthy Hills & Amanalingeswarar",
                "category": "Hill Sanctuary & Falls",
                "description": "Scenic hill temple set near the Panjalingam falls and Thirumoorthy dam reservoir.",
                "link": "https://tiruppur.nic.in/tourist-place/thirumoorthy-dam/"
            },
            {
                "name": "Amaravathi Dam & Crocodile Bank",
                "category": "Wildlife & Reservoir",
                "description": "Massive reservoir at the foot of Indira Gandhi National Park housing a large mugger crocodile breeding farm.",
                "link": "https://tiruppur.nic.in/tourist-place/amaravathy-dam/"
            },
            {
                "name": "Tiruppur Kumaran Memorial",
                "category": "Freedom Memorial",
                "description": "Memorial honoring freedom fighter Kodikatha Kumaran who sacrificed his life holding the Indian national flag in 1932.",
                "link": "https://tiruppur.nic.in/tourist-place/tirupur-kumaran-memorial/"
            }
        ]
    },
    33: {
        "region": "Northern Coastal / Industrial & Sacred",
        "intro_ta": "திருவள்ளூர் — பூண்டி நீர்த்தேக்கம், வீரராகவர் திருக்கோயில், பழவேற்காடு (புலிகாட்) பறவைகள் சரணாலயம் மற்றும் நவீன வாகனத் தொழில்துறை மையம்.",
        "intro_en": "Tiruvallur features the ancient Sri Veeraraghava Swamy temple, Poondi reservoir (Chennai's water lifeline), historic Pulicat Lake, and heavy industries.",
        "search_aliases": ["Tiruvallur", "திருவள்ளூர்", "Thiruvallur", "Pulicat", "பழவேற்காடு", "Poondi", "பூண்டி"],
        "hero_image": "/images/hero-temple.jpg",
        "specialities": [
            {
                "name": "Pulicat Lake & Bird Sanctuary",
                "category": "Coastal Lagoon Ecosystem",
                "explanation": "Second largest brackish-water lagoon in India, home to Fort Geldria (1613 Dutch fort) and tens of thousands of wintering flamingos.",
                "significance": "Crucial coastal wetland reserve with 400 years of colonial maritime trade history.",
                "source_url": "https://tiruvallur.nic.in/tourist-place/pulicat-lake/"
            },
            {
                "name": "Sri Veeraraghava Swamy Temple",
                "category": "Divya Desam Heritage",
                "explanation": "Ancient Vaishnavite temple dedicated to Lord Vishnu in Bhujanga Sayanam (reclining posture), renowned for healing curative powers.",
                "significance": "Celebrated in Tevaram and Nalayira Divya Prabandham hymns.",
                "source_url": "https://tiruvallur.nic.in/tourist-place/sri-veeraraghava-swamy-temple/"
            },
            {
                "name": "Poondi Reservoir (Sathyamurthy Sagar)",
                "category": "Water Lifeline Reservoir",
                "explanation": "Constructed across the Kosasthalaiyar river in 1944, storing drinking water for Chennai metropolitan area.",
                "significance": "Essential reservoir supporting municipal supplies and groundwater recharge.",
                "source_url": "https://tiruvallur.nic.in/tourist-place/poondi-reservoir/"
            }
        ],
        "famous_places": [
            {
                "name": "Pulicat Lake & Dutch Cemetery",
                "category": "Lagoon & Heritage",
                "description": "Vast bird sanctuary lagoon with historic Dutch cemetery and Fort Geldria ruins.",
                "link": "https://tiruvallur.nic.in/tourist-place/pulicat-lake/"
            },
            {
                "name": "Sri Veeraraghava Swamy Temple",
                "category": "Sacred Temple",
                "description": "Ancient Divya Desam temple with massive Hrit-Tapa-Nasini temple tank.",
                "link": "https://tiruvallur.nic.in/tourist-place/sri-veeraraghava-swamy-temple/"
            },
            {
                "name": "Gudiyam Caves",
                "category": "Prehistoric Rock Shelter",
                "description": "Paleolithic rock shelter caves excavated by Robert Bruce Foote yielding early Stone Age stone tools.",
                "link": "https://tiruvallur.nic.in/"
            }
        ]
    },
    34: {
        "region": "Northern Central / Spiritual Mountain",
        "intro_ta": "திருவண்ணாமலை — பஞ்சபூத அக்னி தலம்; அருணாசலேஸ்வரர் திருக்கோயில், 14 கி.மீ கிரிவலப் பாதை, ஆரணி பட்டு மற்றும் சாத்தனூர் அணைப் பெருமை.",
        "intro_en": "Tiruvannamalai is the holy Agni (Fire) Sthalam of Lord Arunachaleswarar, celebrated for the 14 km Girivalam circumambulation, Sathanur Dam, and Arani silk.",
        "search_aliases": ["Tiruvannamalai", "திருவண்ணாமலை", "Arunachala", "அருணாசலம்", "Arani", "ஆரணி"],
        "hero_image": "/images/tiruvannamalai.jpg",
        "specialities": [
            {
                "name": "Arunachaleswarar Temple (Agni Sthalam)",
                "category": "Pancha Bhoota Architectural Wonder",
                "explanation": "Sprawling 25-acre temple at the foothills of the holy Arunachala mountain, representing the Fire element with 66-meter eastern Rajagopuram.",
                "significance": "Centuries of inscriptions from Chola, Hoysala, and Vijayanagara dynasties; venue of the Kartikai Deepam beacon.",
                "source_url": "https://tiruvannamalai.nic.in/tourist-place/arunachaleswarar-temple/"
            },
            {
                "name": "Girivalam (Sacred Hill Circumambulation)",
                "category": "Spiritual Practice & Hermitage Heritage",
                "explanation": "14-kilometer barefoot walk around the base of sacred Mount Arunachala passing eight sacred Ashta Lingams.",
                "significance": "Attracts millions of spiritual devotees during Chitra Pournami and monthly full-moon nights.",
                "source_url": "https://tiruvannamalai.nic.in/"
            },
            {
                "name": "Arani Silk Sarees (GI Tag)",
                "category": "Textile GI Craft",
                "explanation": "Fine traditional mulberry silk sarees with rich dual-colored borders, woven by thousands of master handloom weavers in Arani.",
                "significance": "One of Tamil Nadu's foremost silk-producing clusters alongside Kanchipuram.",
                "source_url": "https://tiruvannamalai.nic.in/"
            },
            {
                "name": "Sathanur Dam & Crocodile Farm",
                "category": "Irrigation Dam & Park",
                "explanation": "Constructed in 1958 across Thenpennai river featuring scenic botanical parks, hanging bridges, and crocodile rearing facility.",
                "significance": "Major irrigation source and weekend family destination.",
                "source_url": "https://tiruvannamalai.nic.in/tourist-place/sathanur-dam/"
            }
        ],
        "famous_places": [
            {
                "name": "Arunachaleswarar Temple",
                "category": "Agni Sthalam",
                "description": "Massive granite temple with four majestic gopurams and the sacred thousand-pillar hall.",
                "link": "https://tiruvannamalai.nic.in/tourist-place/arunachaleswarar-temple/"
            },
            {
                "name": "Sri Ramana Ashram",
                "category": "Spiritual Hermitage",
                "description": "Serene ashram at the foot of Arunachala where Sage Ramana Maharshi lived and taught self-inquiry.",
                "link": "https://tiruvannamalai.nic.in/tourist-place/sri-ramana-ashram/"
            },
            {
                "name": "Sathanur Dam",
                "category": "Dam & Recreational Park",
                "description": "Sprawling reservoir surrounded by landscaped gardens and mini zoo in Chengam taluk.",
                "link": "https://tiruvannamalai.nic.in/tourist-place/sathanur-dam/"
            }
        ]
    },
    35: {
        "region": "Cauvery Delta / Music & Chariot Capital",
        "intro_ta": "திருவாரூர் — ஆழித்தேர் நகரம்; கர்நாடக இச மும்மூர்த்திகள் அவதரித்த பூமி, தியாகராஜ சுவாமி கோயில் மற்றும் முத்துப்பேட்டை சதுப்புநிலக் காடுகள்.",
        "intro_en": "Tiruvarur is famed for the massive Thyagaraja Temple and Asia's largest temple chariot (Aazhi Ther), as the birthplace of the Carnatic Music Trinity.",
        "search_aliases": ["Tiruvarur", "திருவாரூர்", "Thiruvarur", "Aazhi Ther", "ஆழித்தேர்"],
        "hero_image": "/images/thanjavur.jpg",
        "specialities": [
            {
                "name": "Thyagaraja Swamy Temple & Aazhi Ther (Giant Chariot)",
                "category": "Chariot Architecture & Delta Heritage",
                "explanation": "Ancient temple covering 20 acres with the massive Kamalalayam tank, famous for the 96-foot, 300-tonne Aazhi Ther temple chariot.",
                "significance": "Celebrated in Tevaram hymns; pulled by thousands of devotees during the Chithirai festival.",
                "source_url": "https://tiruvarur.nic.in/tourist-place/thiyagaraja-swamy-temple/"
            },
            {
                "name": "Birthplace of Carnatic Music Trinity",
                "category": "Classical Music Heritage",
                "explanation": "All three revered Carnatic music composers — Saint Thyagaraja, Muthuswami Dikshitar, and Syama Sastri — were born in Tiruvarur in the 18th century.",
                "significance": "Considered the spiritual capital and fountainhead of classical Carnatic music.",
                "source_url": "https://tiruvarur.nic.in/tourist-place/carnatic-music-trinity-memorial/"
            },
            {
                "name": "Muthupet Mangrove Lagoon",
                "category": "Coastal Wetland Ecology",
                "explanation": "Spans over 12,000 hectares of mangrove forests in the Palk Strait, intersected by winding brackish water channels.",
                "significance": "Critical sanctuary for marine life and thousands of wintering migratory birds.",
                "source_url": "https://tiruvarur.nic.in/tourist-place/muthupet-mangrove-forest/"
            }
        ],
        "famous_places": [
            {
                "name": "Thyagaraja Swamy Temple",
                "category": "Historic Delta Temple",
                "description": "Massive Shaivite shrine with Kamalalayam tank and sacred shrines for the Navagrahas.",
                "link": "https://tiruvarur.nic.in/tourist-place/thiyagaraja-swamy-temple/"
            },
            {
                "name": "Carnatic Music Trinity Memorial",
                "category": "Cultural Heritage",
                "description": "Memorial preserving the birth houses of Thyagaraja, Muthuswami Dikshitar, and Syama Sastri.",
                "link": "https://tiruvarur.nic.in/tourist-place/carnatic-music-trinity-memorial/"
            },
            {
                "name": "Muthupet Mangrove Boardwalk",
                "category": "Eco-Tourism",
                "description": "Scenic wooden boardwalk extending deep into the heart of the mangrove forest and lagoon.",
                "link": "https://tiruvarur.nic.in/tourist-place/muthupet-mangrove-forest/"
            }
        ]
    },
    36: {
        "region": "Northern / Palar Basin",
        "intro_ta": "வேலூர் — 16-ஆம் நூற்றாண்டு வரலாற்று அகழி கோட்டை, 1806 வேலூர் சிப்பாய் புரட்சி, ஜலகண்டேஸ்வரர் திருக்கோயில், தங்கக் கோயில் மற்றும் சி.எம்.சி மருத்துவமனை.",
        "intro_en": "Vellore is centered around the formidable 16th-century stone moat fort (site of the 1806 Vellore Mutiny), Jalakanteswarar temple, Sripuram Golden Temple, and CMC.",
        "search_aliases": ["Vellore", "வேலூர்", "North Arcot", "வட ஆற்காடு", "Vellore Fort", "வேலூர் கோட்டை"],
        "hero_image": "/images/hero-temple.jpg",
        "specialities": [
            {
                "name": "Vellore Fort & 1806 Vellore Sepoy Mutiny",
                "category": "Military Architecture & Freedom Heritage",
                "explanation": "Massive 16th-century granite fort surrounded by a deep water moat built by Vijayanagara Nayaks; site of the first major armed uprising against the British in 1806.",
                "significance": "A landmark of anti-colonial resistance preceding the 1857 Revolt by half a century.",
                "source_url": "https://vellore.nic.in/tourist-place/vellore-fort/"
            },
            {
                "name": "Jalakanteswarar Temple",
                "category": "Vijayanagara Stone Sculpture",
                "explanation": "Magnificent temple inside Vellore Fort renowned for the Kalyana Mandapam with intricate stone pillars of riders on rearing yalis.",
                "significance": "Acclaimed by colonial art historians as an unrivaled masterpiece of Vijayanagara stone carving.",
                "source_url": "https://vellore.nic.in/tourist-place/jalakandeswarar-temple/"
            },
            {
                "name": "Vellore Spiny Brinjal (GI Tag)",
                "category": "Agri-GI Horticultural Variety",
                "explanation": "Unique oval, spiny, glossy purple brinjal with tender flesh and rich flavor cultivated in Anaicut and Vellore valley.",
                "significance": "Celebrated in royal and local gourmet cuisines for traditional curries.",
                "source_url": "https://vellore.nic.in/"
            },
            {
                "name": "Sripuram Golden Temple (Malaikodi)",
                "category": "Spiritual Landmark",
                "explanation": "Spiritual park covering 100 acres featuring a sanctum coated with over 1.5 tonnes of pure gold foil surrounded by a star-shaped path.",
                "significance": "Attracts millions of international visitors for meditation and charity.",
                "source_url": "https://vellore.nic.in/tourist-place/sripuram-golden-temple/"
            }
        ],
        "famous_places": [
            {
                "name": "Vellore Fort",
                "category": "Granite Moated Fort",
                "description": "Massive double-walled stone citadel with deep crocodile moat, Tipu Mahal, and state museum.",
                "link": "https://vellore.nic.in/tourist-place/vellore-fort/"
            },
            {
                "name": "Jalakanteswarar Temple",
                "category": "Vijayanagara Sculpture",
                "description": "Exquisite temple inside the fort famed for the 100-pillar wedding hall with mythical dragon carvings.",
                "link": "https://vellore.nic.in/tourist-place/jalakandeswarar-temple/"
            },
            {
                "name": "Sripuram Golden Temple",
                "category": "Golden Monument",
                "description": "Shining gold-plated temple dedicated to Goddess Mahalakshmi with star path meditation gardens.",
                "link": "https://vellore.nic.in/tourist-place/sripuram-golden-temple/"
            }
        ]
    },
    37: {
        "region": "Northern Central / Gingee & Coast",
        "intro_ta": "விழுப்புரம் — வரலாற்றுச் சிறப்புமிக்க செஞ்சிக் கோட்டை ('கிழக்கின் ட்ராய்'), ஆரோவில் சர்வதேச ஆன்மீக நகரம் மற்றும் திருக்கோவிலூர் உலகுளந்த பெருமாள் கோயில்.",
        "intro_en": "Viluppuram hosts the invincible Gingee Fort ('Troy of the East' as termed by Shivaji), Auroville International Township, and ancient temple centers.",
        "search_aliases": ["Viluppuram", "விழுப்புரம்", "Villupuram", "Gingee", "செஞ்சி", "Auroville", "ஆரோவில்"],
        "hero_image": "/images/mamallapuram.jpg",
        "specialities": [
            {
                "name": "Gingee Fort ('Troy of the East')",
                "category": "Monolithic Military Fortress Complex",
                "explanation": "Complex of three steep hill forts (Rajagiri, Krishnagiri, Chandrayandurg) interconnected by massive walls, deemed impregnable by Chhatrapati Shivaji.",
                "significance": "Features Kalyan Mahal, multi-tier granaries, watchtowers, and legendary Raja Desingh lore.",
                "source_url": "https://viluppuram.nic.in/tourist-place/gingee-fort/"
            },
            {
                "name": "Auroville International Township & Matrimandir",
                "category": "Global Universal Township",
                "explanation": "Founded in 1968 by Mirra Alfassa (The Mother) based on Sri Aurobindo's vision of human unity, recognized by UNESCO and Government of India.",
                "significance": "Features the golden geodesic dome of Matrimandir dedicated to silent meditation and renewable living.",
                "source_url": "https://viluppuram.nic.in/tourist-place/auroville/"
            },
            {
                "name": "Thirukoilur Ulagalantha Perumal Temple",
                "category": "Divya Desam & Sangam Heritage",
                "explanation": "Ancient temple of Lord Vishnu as Trivikrama measuring the universe, where the first three Alvars (Poigai, Bhutha, Peyalvar) composed the first hymns.",
                "significance": "Foundational birthplace of the Tamil Vaishnavite devotional movement.",
                "source_url": "https://viluppuram.nic.in/"
            }
        ],
        "famous_places": [
            {
                "name": "Gingee Fort (Rajagiri)",
                "category": "Medieval Citadel",
                "description": "800-foot sheer citadel accessible across a narrow drawbridge over a chasm, with 7-storey Kalyana Mahal.",
                "link": "https://viluppuram.nic.in/tourist-place/gingee-fort/"
            },
            {
                "name": "Matrimandir (Auroville)",
                "category": "Universal Sanctuary",
                "description": "Golden globe meditation chamber with crystal glass sphere illuminated by a single sunbeam.",
                "link": "https://viluppuram.nic.in/tourist-place/auroville/"
            },
            {
                "name": "Thiruvakkarai Geological Fossil Park",
                "category": "Prehistoric Site",
                "description": "National Geological Monument featuring petrified fossilized wood logs dating back 20 million years.",
                "link": "https://viluppuram.nic.in/"
            }
        ]
    },
    38: {
        "region": "Southern / Cotton & Firework Heartland",
        "intro_ta": "விருதுநகர் — கர்மவீரர் காமராஜர் அவதரித்த பூமி; ஸ்ரீவில்லிபுத்தூர் ஆண்டாள் கோயில் (தமிழக அரசு முத்திரை), பால்கோவா, சாத்தூர் சேவு மற்றும் சிவகாசி அச்சுத் தொழில்.",
        "intro_en": "Virudhunagar is the birthplace of visionary leader K. Kamaraj, famed for the Srivilliputhur Andal Temple tower (the official Tamil Nadu State Emblem), GI Palkova, and Sivakasi printing.",
        "search_aliases": ["Virudhunagar", "விருதுநகர்", "Srivilliputhur", "ஸ்ரீவில்லிபுத்தூர்", "Sivakasi", "சிவகாசி", "Kamarajar", "காமராஜர்"],
        "hero_image": "/images/madurai.jpg",
        "specialities": [
            {
                "name": "Srivilliputhur Andal Temple (Tamil Nadu State Emblem)",
                "category": "Sacred Architectural Symbol of Tamil Nadu",
                "explanation": "Birthplace of saint-poetess Andal (author of Tiruppavai) and Periyalvar, featuring a towering 192-foot, 11-tiered Rajagopuram.",
                "significance": "Adopted by the Government of Tamil Nadu as the official State Emblem.",
                "source_url": "https://virudhunagar.nic.in/tourist-place/srivilliputhur-andal-temple/"
            },
            {
                "name": "Srivilliputhur Palkova (GI Tag)",
                "category": "Dairy Confectionery GI Heritage",
                "explanation": "Traditional caramelized milk sweet prepared using pure full-cream buffalo/cow milk and sugar, slowly stirred in heavy brass vats over wood fire.",
                "significance": "Famous across India for rich granular texture and unadulterated purity.",
                "source_url": "https://virudhunagar.nic.in/"
            },
            {
                "name": "Sivakasi Printing & Safety Match Capital",
                "category": "Industrial Manufacturing Hub",
                "explanation": "Produces over 60% of India's offset printing, school books, calendars, and safety matches, nicknamed 'Kutti Japan' by Jawaharlal Nehru.",
                "significance": "World-class graphic printing and packaging industrial ecosystem.",
                "source_url": "https://virudhunagar.nic.in/"
            },
            {
                "name": "Birthplace of Karma Veerar K. Kamaraj",
                "category": "National Historic Personality",
                "explanation": "Home of former Chief Minister of India K. Kamaraj, who pioneered the free mid-day meal scheme in schools and shaped modern education.",
                "significance": "His ancestral house in Virudhunagar is preserved as a national memorial.",
                "source_url": "https://virudhunagar.nic.in/tourist-place/kamarajar-memorial-house/"
            }
        ],
        "famous_places": [
            {
                "name": "Srivilliputhur Andal Temple",
                "category": "State Emblem Temple",
                "description": "Magnificent temple with 11-storey gopuram dedicated to Andal and Rangamannar.",
                "link": "https://virudhunagar.nic.in/tourist-place/srivilliputhur-andal-temple/"
            },
            {
                "name": "Kamarajar Memorial House",
                "category": "Historic Residence",
                "description": "Preserved ancestral residence of the revered leader displaying photographs, books, and humble belongings.",
                "link": "https://virudhunagar.nic.in/tourist-place/kamarajar-memorial-house/"
            },
            {
                "name": "Sathuragiri Hills & Sundara Mahalingam",
                "category": "Siddha Sacred Hills",
                "description": "Mystical mountain sanctuary in the Western Ghats revered as the abode of ancient Tamil Siddha doctors and sages.",
                "link": "https://virudhunagar.nic.in/"
            }
        ]
    }
}

enriched_districts = []
for d in raw_districts:
    no = d['no']
    meta = DISTRICT_DETAILS.get(no, {})
    
    # Categorized timeline records based on workbook guidance
    timeline = []
    
    # 1. Former administrative / parent district
    timeline.append({
        "era": "Administrative Background",
        "category": "Former Administrative District / Parent District",
        "title": "Administrative Formation & Parent Territory",
        "title_ta": "நிர்வாக உருவாக்கம் & மூல மாவட்டம்",
        "description": d['former_administrative_name_history'],
        "evidence_type": "official_record"
    })
    
    # 2. Ancient or Historical Name Context
    timeline.append({
        "era": "Historical & Epigraphical Context",
        "category": "Ancient Settlement / Regional Association",
        "title": "Ancient / Historical Regional Context",
        "title_ta": "பண்டைய / வரலாற்றுப் பின்னணி",
        "description": d['ancient_or_historical_name_context'],
        "evidence_type": "historical_record"
    })
    
    # 3. Verification & Authority Notes
    timeline.append({
        "era": "Official Authority & Notes",
        "category": "Change Date / Authority / Verification Notes",
        "title": "Government Order & Verification Standard",
        "title_ta": "அரசாணை & சரிபார்ப்புக் குறிப்புகள்",
        "description": d['change_date_authority_verification_notes'],
        "evidence_type": "government_order_gazette"
    })

    enriched = {
        "no": d['no'],
        "district_english": d['district_english'],
        "district_tamil": d['district_tamil'],
        "region": meta.get("region", "Tamil Nadu"),
        "intro_ta": meta.get("intro_ta", f"{d['district_tamil']} மாவட்டம் தமிழ்நாட்டின் 38 நிர்வாக மாவட்டங்களில் ஒன்றாகும்."),
        "intro_en": meta.get("intro_en", f"{d['district_english']} is one of the 38 administrative districts of Tamil Nadu."),
        "former_administrative_name_history": d['former_administrative_name_history'],
        "ancient_or_historical_name_context": d['ancient_or_historical_name_context'],
        "change_date_authority_verification_notes": d['change_date_authority_verification_notes'],
        "official_district_portal": d['official_district_portal'],
        "search_aliases": meta.get("search_aliases", [d['district_english'], d['district_tamil']]),
        "hero_image": meta.get("hero_image", "/images/hero-temple.jpg"),
        "timeline": timeline,
        "specialities": meta.get("specialities", []),
        "famous_places": meta.get("famous_places", [])
    }
    enriched_districts.append(enriched)

final_data = {
    "total_districts": len(enriched_districts),
    "districts": enriched_districts,
    "official_sources": extra_data.get("sources", []),
    "research_guidance": extra_data.get("readme", [])
}

# Save to backend
with open('data/tamil_nadu_38_districts_intelligence.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

# Save to frontend data directory
os.makedirs('../frontend/src/data', exist_ok=True)
with open('../frontend/src/data/districtsData.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print('Generated intelligence dataset for all 38 districts successfully!')
