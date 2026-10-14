/**
 * NIAT Multilingual Translations & Objection Prompts
 * Supported Languages: English (en), Telugu (te), Tamil (ta), Hindi (hi), Kannada (kn), Malayalam (ml)
 */

const SUPPORTED_LANGUAGES = [
  { code: "en", name: "English", nativeName: "English", flag: "🇬🇧" },
  { code: "te", name: "Telugu", nativeName: "తెలుగు", flag: "🇮🇳" },
  { code: "ta", name: "Tamil", nativeName: "தமிழ்", flag: "🇮🇳" },
  { code: "hi", name: "Hindi", nativeName: "हिन्दी", flag: "🇮🇳" },
  { code: "kn", name: "Kannada", nativeName: "ಕನ್ನಡ", flag: "🇮🇳" },
  { code: "ml", name: "Malayalam", nativeName: "മലയാളം", flag: "🇮🇳" },
];

const PARENT_OBJECTIONS = {
  en: [
    { id: "obj-degree", label: "UGC / AICTE Degree Validity", question: "Is this degree officially recognized by UGC and AICTE, or is NIAT just an unaccredited private coaching institute?", category: "accreditation" },
    { id: "obj-ai-jobs", label: "Will AI Kill Coding Jobs?", question: "Will AI and tools like ChatGPT eliminate junior software developer jobs by 2028 when my child graduates?", category: "ai_threat" },
    { id: "obj-roi", label: "Why ₹8L-12L vs ₹3L Local College?", question: "Why should we invest ₹8 to 12 Lakhs when local engineering colleges cost only ₹3 to 4 Lakhs? What is the real financial ROI?", category: "roi_financial" },
    { id: "obj-campus", label: "Which Partner Campus Fits Us?", question: "Which of NIAT's 35+ partner university campuses is best for our location, budget, and my child's score?", category: "campus_matching" },
  ],
  te: [
    { id: "obj-degree", label: "యూజీసీ / ఏఐసీటీఈ డిగ్రీ చెల్లుబాటు", question: "ఈ డిగ్రీ నిజంగా యూజీసీ (UGC), ఏఐసీటీఈ (AICTE) గుర్తింపు పొందినదేనా? లేదా ఎన్ఐఏటీ కేవలం ఒక ప్రైవేట్ కోచింగ్ సంస్థా?", category: "accreditation" },
    { id: "obj-ai-jobs", label: "ఏఐ వల్ల సాఫ్ట్‌వేర్ ఉద్యోగాలు పోతాయా?", question: "మా అబ్బాయి/అమ్మాయి 2028లో గ్రాడ్యుయేట్ అయ్యే సమయానికి ఏఐ (Artificial Intelligence) వల్ల సాఫ్ట్‌వేర్ కోడింగ్ ఉద్యోగాలు అంతరించిపోతాయా?", category: "ai_threat" },
    { id: "obj-roi", label: "స్థానిక కాలేజీల కంటే ₹8-12 లక్షలు ఎందుకు?", question: "మా స్థానిక ఇంజనీరింగ్ కాలేజీలు ₹3-4 లక్షలకే వస్తుంటే, ఎన్ఐఏటీలో ₹8 నుండి 12 లక్షలు ఎందుకు ఖర్చు చేయాలి? దీని అసలు రాబడి (ROI) ఎంత?", category: "roi_financial" },
    { id: "obj-campus", label: "మాకు సరిపోయే క్యాంపస్ ఏది?", question: "ఎన్ఐఏటీకి ఉన్న 35+ భాగస్వామ్య విశ్వవిద్యాలయాలలో మా ప్రాంతం, మా బడ్జెట్ మరియు ర్యాంకుకు ఏ క్యాంపస్ సరైనది?", category: "campus_matching" },
  ],
  ta: [
    { id: "obj-degree", label: "UGC / AICTE பட்டப்படிப்பு அங்கீகாரம்", question: "இந்த பட்டம் UGC மற்றும் AICTE ஆல் அதிகாரப்பூர்வமாக அங்கீகரிக்கப்பட்டதா? அல்லது NIAT என்பது ஒரு தனியார் பயிற்சி மையமா?", category: "accreditation" },
    { id: "obj-ai-jobs", label: "AI தொழில்நுட்பத்தால் சாப்ட்வேர் வேலைகள் அழியுமா?", question: "என் குழந்தை 2028-ல் பட்டப்படிப்பு முடிக்கும் போது செயற்கை நுண்ணறிவு (AI) மூலம் ஐடி வேலைகள் பறிபோய்விடுமா?", category: "ai_threat" },
    { id: "obj-roi", label: "உள்ளூர் கல்லூரியை விட ₹8-12 லட்சம் ஏன்?", question: "உள்ளூர் இன்ஜினியரிங் கல்லூரிகள் ₹3-4 லட்சத்திற்கு இருக்கும்போது, NIAT-ல் ₹8-12 லட்சம் முதலீடு செய்ய வேண்டுமா? இதன் உண்மையான வருவாய் மதிப்பு என்ன?", category: "roi_financial" },
    { id: "obj-campus", label: "எங்களுக்கு பொருத்தமான கல்லூரி எது?", question: "NIAT-ன் 35+ கூட்டாண்மை பல்கலைக்கழக வளாகங்களில் எங்கள் இருப்பிடம், பட்ஜெட் மற்றும் மதிப்பெண்ணுக்கு எது சிறந்தது?", category: "campus_matching" },
  ],
  hi: [
    { id: "obj-degree", label: "UGC / AICTE डिग्री की मान्यता", question: "क्या यह डिग्री भारत सरकार (UGC/AICTE) द्वारा पूरी तरह मान्य है, या NIAT सिर्फ एक निजी कोचिंग सेंटर है?", category: "accreditation" },
    { id: "obj-ai-jobs", label: "क्या AI कोडिंग की नौकरियां खत्म कर देगा?", question: "2028 में जब मेरा बच्चा पास होगा, क्या AI (आर्टिफिशियल इंटेलिजेंस) के कारण सॉफ्टवेयर इंजीनियरों की नौकरियां खत्म हो जाएंगी?", category: "ai_threat" },
    { id: "obj-roi", label: "लोकल कॉलेज से ज्यादा ₹8-12 लाख क्यों?", question: "जब स्थानीय कॉलेज ₹3-4 लाख में इंजीनियरिंग कराते हैं, तो NIAT में ₹8 से 12 लाख का निवेश क्यों करें? इसकी असल वित्तीय वापसी (ROI) क्या है?", category: "roi_financial" },
    { id: "obj-campus", label: "हमारे लिए सबसे सही यूनिवर्सिटी कौन सी है?", question: "NIAT के 35+ पार्टनर विश्वविद्यालयों में से हमारे बजट, राज्य और बच्चे के स्कोर के अनुसार सबसे बेहतरीन कॉलेज कौन सा है?", category: "campus_matching" },
  ],
  kn: [
    { id: "obj-degree", label: "ಯುಜಿಸಿ / ಎಐಸಿಟಿಇ ಪದವಿ ಮಾನ್ಯತೆ", question: "ಈ ಪದವಿಯು ಯುಜಿಸಿ (UGC) ಮತ್ತು ಎಐಸಿಟಿಇ (AICTE) ಯಿಂದ ಅಧಿಕೃತವಾಗಿ ಮಾನ್ಯತೆ ಪಡೆದಿದೆಯೇ? ಅಥವಾ ಇದು ಕೇವಲ ಖಾಸಗಿ ತರಬೇತಿ ಸಂಸ್ಥೆಯೇ?", category: "accreditation" },
    { id: "obj-ai-jobs", label: "AI ಸಾಫ್ಟ್‌ವೇರ್ ಉದ್ಯೋಗಗಳನ್ನು ಕಸಿದುಕೊಳ್ಳುತ್ತದೆಯೇ?", question: "ನನ್ನ ಮಗ/ಮಗಳು 2028 ರಲ್ಲಿ ಇಂಜಿನಿಯರಿಂಗ್ ಮುಗಿಸುವ ಹೊತ್ತಿಗೆ ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ (AI) ಇಂಜಿನಿಯರ್ ಉದ್ಯೋಗಗಳನ್ನು ಇಲ್ಲವಾಗಿಸುತ್ತದೆಯೇ?", category: "ai_threat" },
    { id: "obj-roi", label: "ಸ್ಥಳೀಯ ಕಾಲೇಜಿಗಿಂತ ₹8-12 ಲಕ್ಷ ಏಕೆ?", question: "ನಮ್ಮ ಸ್ಥಳೀಯ ಕಾಲೇಜುಗಳು ₹3-4 ಲಕ್ಷದಲ್ಲಿರುವಾಗ, NIAT ನಲ್ಲಿ ₹8 ರಿಂದ 12 ಲಕ್ಷ ಏಕೆ ನೀಡಬೇಕು? ಇದರ ನೈಜ ಲಾಭ (ROI) ಏನು?", category: "roi_financial" },
    { id: "obj-campus", label: "ನಮ್ಮ ಬಜೆಟ್‌ಗೆ ಸರಿಹೊಂದುವ ಕ್ಯಾಂಪಸ್ ಯಾವುದು?", question: "NIAT ನ 35+ ಸಹಭಾಗಿತ್ವದ ವಿಶ್ವವಿದ್ಯಾಲಯಗಳಲ್ಲಿ ನಮ್ಮ ಬಜೆಟ್ ಮತ್ತು ಅಂಕಗಳಿಗೆ ಸೂಕ್ತವಾದ ಕ್ಯಾಂಪಸ್ ಯಾವುದು?", category: "campus_matching" },
  ],
  ml: [
    { id: "obj-degree", label: "UGC / AICTE ബിരുദ അംഗീകാരം", question: "ഈ ഡിഗ്രി UGC, AICTE എന്നിവയാൽ ഔദ്യോഗികമായി അംഗീകരിക്കപ്പെട്ടതാണോ? അതോ NIAT കേവലം ഒരു സ്വകാര്യ കോച്ചിംഗ് മാത്രമാണോ?", category: "accreditation" },
    { id: "obj-ai-jobs", label: "AI സോഫ്റ്റ്‌വെയർ ജോലികൾ ഇല്ലാതാക്കുമോ?", question: "എന്റെ കുട്ടി 2028-ൽ ബിരുദം നേടുമ്പോൾ ആർട്ടിഫിഷ്യൽ ഇന്റലിജൻസ് (AI) കാരണം സോഫ്റ്റ്‌വെയർ ജോലികൾ നഷ്ടപ്പെടുമോ?", category: "ai_threat" },
    { id: "obj-roi", label: "ലോക്കൽ കോളേജുകളേക്കാൾ ₹8-12 ലക്ഷം എന്തുകൊണ്ട്?", question: "ലോക്കൽ എഞ്ചിനീയറിംഗ് കോളേജുകൾ ₹3-4 ലക്ഷത്തിന് പഠിപ്പിക്കുമ്പോൾ, NIAT-ൽ ₹8-12 ലക്ഷം ചിലവഴിക്കുന്നത് കൊണ്ട് എന്ത് നേട്ടമാണ് (ROI)?", category: "roi_financial" },
    { id: "obj-campus", label: "ഏറ്റവും അനുയോജ്യമായ കാമ്പസ് ഏത്?", question: "NIAT-ന്റെ 35+ പങ്കാളിത്ത സർവകലാശാലകളിൽ ഞങ്ങളുടെ സ്ഥലത്തിനും ബഡ്ജറ്റിനും ഏറ്റവും അനുയോജ്യമായ കാമ്പസ് ഏതാണ്?", category: "campus_matching" },
  ],
};

module.exports = {
  SUPPORTED_LANGUAGES,
  PARENT_OBJECTIONS,
};
