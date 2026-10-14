/**
 * NIAT ParentTrust AI — Client-Side Static Data
 * Contains: translations, objection prompts, campus data
 * No module system — attached to window object for use in app.js
 */

window.NIAT_DATA = {

  SUPPORTED_LANGUAGES: [
    { code: "en", name: "English",   nativeName: "English",    flag: "🇬🇧" },
    { code: "te", name: "Telugu",    nativeName: "తెలుగు",      flag: "🇮🇳" },
    { code: "ta", name: "Tamil",     nativeName: "தமிழ்",       flag: "🇮🇳" },
    { code: "hi", name: "Hindi",     nativeName: "हिन्दी",       flag: "🇮🇳" },
    { code: "kn", name: "Kannada",   nativeName: "ಕನ್ನಡ",       flag: "🇮🇳" },
    { code: "ml", name: "Malayalam", nativeName: "മലയാളം",     flag: "🇮🇳" },
  ],

  // ── Parent Objection Prompts ──
  PARENT_OBJECTIONS: {
    en: [
      { id:"obj-degree",  label:"UGC / AICTE Degree Validity",       question:"Is this degree officially recognized by UGC and AICTE, or is NIAT just an unaccredited private coaching institute?",                                                                 category:"accreditation"    },
      { id:"obj-ai-jobs", label:"Will AI Kill Coding Jobs?",          question:"Will AI and tools like ChatGPT eliminate junior software developer jobs by 2028 when my child graduates?",                                                                            category:"ai_threat"        },
      { id:"obj-roi",     label:"Why ₹8L-12L vs ₹3L Local College?", question:"Why should we invest ₹8 to 12 Lakhs when local engineering colleges cost only ₹3 to 4 Lakhs? What is the real financial ROI?",                                                       category:"roi_financial"    },
      { id:"obj-campus",  label:"Which Partner Campus Fits Us?",      question:"Which of NIAT's 35+ partner university campuses is best for our location, budget, and my child's score?",                                                                             category:"campus_matching"  },
    ],
    te: [
      { id:"obj-degree",  label:"యూజీసీ / ఏఐసీటీఈ డిగ్రీ చెల్లుబాటు",                    question:"ఈ డిగ్రీ నిజంగా యూజీసీ (UGC), ఏఐసీటీఈ (AICTE) గుర్తింపు పొందినదేనా? లేదా ఎన్ఐఏటీ కేవలం ఒక ప్రైవేట్ కోచింగ్ సంస్థా?",                                    category:"accreditation"    },
      { id:"obj-ai-jobs", label:"ఏఐ వల్ల సాఫ్ట్‌వేర్ ఉద్యోగాలు పోతాయా?",                    question:"మా అబ్బాయి/అమ్మాయి 2028లో గ్రాడ్యుయేట్ అయ్యే సమయానికి ఏఐ (Artificial Intelligence) వల్ల సాఫ్ట్‌వేర్ కోడింగ్ ఉద్యోగాలు అంతరించిపోతాయా?",               category:"ai_threat"        },
      { id:"obj-roi",     label:"స్థానిక కాలేజీల కంటే ₹8-12 లక్షలు ఎందుకు?",               question:"మా స్థానిక ఇంజనీరింగ్ కాలేజీలు ₹3-4 లక్షలకే వస్తుంటే, ఎన్ఐఏటీలో ₹8 నుండి 12 లక్షలు ఎందుకు ఖర్చు చేయాలి? దీని అసలు రాబడి (ROI) ఎంత?",                  category:"roi_financial"    },
      { id:"obj-campus",  label:"మాకు సరిపోయే క్యాంపస్ ఏది?",                               question:"ఎన్ఐఏటీకి ఉన్న 35+ భాగస్వామ్య విశ్వవిద్యాలయాలలో మా ప్రాంతం, మా బడ్జెట్ మరియు ర్యాంకుకు ఏ క్యాంపస్ సరైనది?",                                            category:"campus_matching"  },
    ],
    ta: [
      { id:"obj-degree",  label:"UGC / AICTE பட்டப்படிப்பு அங்கீகாரம்",                  question:"இந்த பட்டம் UGC மற்றும் AICTE ஆல் அதிகாரப்பூர்வமாக அங்கீகரிக்கப்பட்டதா? அல்லது NIAT என்பது ஒரு தனியார் பயிற்சி மையமா?",                              category:"accreditation"    },
      { id:"obj-ai-jobs", label:"AI தொழில்நுட்பத்தால் சாப்ட்வேர் வேலைகள் அழியுமா?",     question:"என் குழந்தை 2028-ல் பட்டப்படிப்பு முடிக்கும் போது செயற்கை நுண்ணறிவு (AI) மூலம் ஐடி வேலைகள் பறிபோய்விடுமா?",                                          category:"ai_threat"        },
      { id:"obj-roi",     label:"உள்ளூர் கல்லூரியை விட ₹8-12 லட்சம் ஏன்?",              question:"உள்ளூர் இன்ஜினியரிங் கல்லூரிகள் ₹3-4 லட்சத்திற்கு இருக்கும்போது, NIAT-ல் ₹8-12 லட்சம் முதலீடு செய்ய வேண்டுமா? இதன் உண்மையான வருவாய் மதிப்பு என்ன?", category:"roi_financial"    },
      { id:"obj-campus",  label:"எங்களுக்கு பொருத்தமான கல்லூரி எது?",                    question:"NIAT-ன் 35+ கூட்டாண்மை பல்கலைக்கழக வளாகங்களில் எங்கள் இருப்பிடம், பட்ஜெட் மற்றும் மதிப்பெண்ணுக்கு எது சிறந்தது?",                                    category:"campus_matching"  },
    ],
    hi: [
      { id:"obj-degree",  label:"UGC / AICTE डिग्री की मान्यता",                          question:"क्या यह डिग्री भारत सरकार (UGC/AICTE) द्वारा पूरी तरह मान्य है, या NIAT सिर्फ एक निजी कोचिंग सेंटर है?",                                                    category:"accreditation"    },
      { id:"obj-ai-jobs", label:"क्या AI कोडिंग की नौकरियां खत्म कर देगा?",              question:"2028 में जब मेरा बच्चा पास होगा, क्या AI (आर्टिफिशियल इंटेलिजेंस) के कारण सॉफ्टवेयर इंजीनियरों की नौकरियां खत्म हो जाएंगी?",                             category:"ai_threat"        },
      { id:"obj-roi",     label:"लोकल कॉलेज से ज्यादा ₹8-12 लाख क्यों?",                question:"जब स्थानीय कॉलेज ₹3-4 लाख में इंजीनियरिंग कराते हैं, तो NIAT में ₹8 से 12 लाख का निवेश क्यों करें? इसकी असल वित्तीय वापसी (ROI) क्या है?",               category:"roi_financial"    },
      { id:"obj-campus",  label:"हमारे लिए सबसे सही यूनिवर्सिटी कौन सी है?",            question:"NIAT के 35+ पार्टनर विश्वविद्यालयों में से हमारे बजट, राज्य और बच्चे के स्कोर के अनुसार सबसे बेहतरीन कॉलेज कौन सा है?",                                  category:"campus_matching"  },
    ],
    kn: [
      { id:"obj-degree",  label:"ಯುಜಿಸಿ / ಎಐಸಿಟಿಇ ಪದವಿ ಮಾನ್ಯತೆ",                         question:"ಈ ಪದವಿಯು ಯುಜಿಸಿ (UGC) ಮತ್ತು ಎಐಸಿಟಿಇ (AICTE) ಯಿಂದ ಅಧಿಕೃತವಾಗಿ ಮಾನ್ಯತೆ ಪಡೆದಿದೆಯೇ? ಅಥವಾ ಇದು ಕೇವಲ ಖಾಸಗಿ ತರಬೇತಿ ಸಂಸ್ಥೆಯೇ?",                                       category:"accreditation"    },
      { id:"obj-ai-jobs", label:"AI ಸಾಫ್ಟ್‌ವೇರ್ ಉದ್ಯೋಗಗಳನ್ನು ಕಸಿದುಕೊಳ್ಳುತ್ತದೆಯೇ?",       question:"ನನ್ನ ಮಗ/ಮಗಳು 2028 ರಲ್ಲಿ ಇಂಜಿನಿಯರಿಂಗ್ ಮುಗಿಸುವ ಹೊತ್ತಿಗೆ ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ (AI) ಇಂಜಿನಿಯರ್ ಉದ್ಯೋಗಗಳನ್ನು ಇಲ್ಲವಾಗಿಸುತ್ತದೆಯೇ?",                                    category:"ai_threat"        },
      { id:"obj-roi",     label:"ಸ್ಥಳೀಯ ಕಾಲೇಜಿಗಿಂತ ₹8-12 ಲಕ್ಷ ಏಕೆ?",                    question:"ನಮ್ಮ ಸ್ಥಳೀಯ ಕಾಲೇಜುಗಳು ₹3-4 ಲಕ್ಷದಲ್ಲಿರುವಾಗ, NIAT ನಲ್ಲಿ ₹8 ರಿಂದ 12 ಲಕ್ಷ ಏಕೆ ನೀಡಬೇಕು? ಇದರ ನೈಜ ಲಾಭ (ROI) ಏನು?",                                                category:"roi_financial"    },
      { id:"obj-campus",  label:"ನಮ್ಮ ಬಜೆಟ್‌ಗೆ ಸರಿಹೊಂದುವ ಕ್ಯಾಂಪಸ್ ಯಾವುದು?",              question:"NIAT ನ 35+ ಸಹಭಾಗಿತ್ವದ ವಿಶ್ವವಿದ್ಯಾಲಯಗಳಲ್ಲಿ ನಮ್ಮ ಬಜೆಟ್ ಮತ್ತು ಅಂಕಗಳಿಗೆ ಸೂಕ್ತವಾದ ಕ್ಯಾಂಪಸ್ ಯಾವುದು?",                                                            category:"campus_matching"  },
    ],
    ml: [
      { id:"obj-degree",  label:"UGC / AICTE ബിരുദ അംഗീകാരം",                            question:"ഈ ഡിഗ്രി UGC, AICTE എന്നിവയാൽ ഔദ്യോഗികമായി അംഗീകരിക്കപ്പെട്ടതാണോ? അതോ NIAT കേവലം ഒരു സ്വകാര്യ കോച്ചിംഗ് മാത്രമാണോ?",                            category:"accreditation"    },
      { id:"obj-ai-jobs", label:"AI സോഫ്റ്റ്‌വെയർ ജോലികൾ ഇല്ലാതാക്കുമോ?",               question:"എന്റെ കുട്ടി 2028-ൽ ബിരുദം നേടുമ്പോൾ ആർട്ടിഫിഷ്യൽ ഇന്റലിജൻസ് (AI) കാരണം സോഫ്റ്റ്‌വെയർ ജോലികൾ നഷ്ടപ്പെടുമോ?",                                    category:"ai_threat"        },
      { id:"obj-roi",     label:"ലോക്കൽ കോളേജുകളേക്കാൾ ₹8-12 ലക്ഷം എന്തുകൊണ്ട്?",       question:"ലോക്കൽ എഞ്ചിനീയറിംഗ് കോളേജുകൾ ₹3-4 ലക്ഷത്തിന് പഠിപ്പിക്കുമ്പോൾ, NIAT-ൽ ₹8-12 ലക്ഷം ചിലവഴിക്കുന്നത് കൊണ്ട് എന്ത് നേട്ടമാണ് (ROI)?",             category:"roi_financial"    },
      { id:"obj-campus",  label:"ഏറ്റവും അനുയോജ്യമായ കാമ്പസ് ഏത്?",                     question:"NIAT-ന്റെ 35+ പങ്കാളിത്ത സർവകലാശാലകളിൽ ഞങ്ങളുടെ സ്ഥലത്തിനും ബഡ്ജറ്റിനും ഏറ്റവും അനുയോജ്യമായ കാമ്പസ് ഏതാണ്?",                                         category:"campus_matching"  },
    ],
  },

  // ── UI Strings ──
  UI_STRINGS: {
    en: {
      heroTitle: "Empowering Parents with Complete Admissions Transparency",
      heroSubtitle: "Instant, evidence-backed answers on UGC degrees, AI job security, campus matching across 35+ partner universities, and 5-year financial returns.",
      askQuestionPlaceholder: "Ask any question about fees, degree validity, AI careers, or campuses in your language...",
      downloadDossier: "Download Official Dossier (PDF)",
      lockSeat: "Lock Provisional Seat (₹10,000 Refundable)",
      agentReasoning: "AI Agent Reasoning & Tool Calls",
      campusesFound: "Partner Campuses Matched",
      roiBreakEven: "Payback Period",
      wealthDelta: "5-Year Net Wealth Gain",
      consultingText: "Consulting...",
      consultBtnText: "Consult Agent",
    },
    te: {
      heroTitle: "తల్లిదండ్రులకు పూర్తి పారదర్శకతతో కూడిన అడ్మిషన్ల మార్గదర్శి",
      heroSubtitle: "యూజీసీ డిగ్రీ గుర్తింపు, ఏఐ భద్రత, 35+ భాగస్వామ్య విశ్వవిద్యాలయాల వివరాలు మరియు 5 ఏళ్ల ఆర్థిక రాబడిపై నిష్పాక్షికమైన నిజాలు.",
      askQuestionPlaceholder: "ఫీజులు, డిగ్రీ గుర్తింపు, ఏఐ ఉద్యోగాలు లేదా కాలేజీల గురించి మీ స్వంత భాషలో అడగండి...",
      downloadDossier: "అధికారిక రిపోర్ట్ డౌన్‌లోడ్ చేసుకోండి (PDF)",
      lockSeat: "సీటును రిజర్వ్ చేసుకోండి (₹10,000 వాపసు లభించును)",
      agentReasoning: "ఏఐ ఏజెంట్ డేటా విశ్లేషణ & టూల్స్ అమలు",
      campusesFound: "సరిపోలిన విశ్వవిద్యాలయ క్యాంపస్‌లు",
      roiBreakEven: "పెట్టుబడి తిరిగి వచ్చే కాలం",
      wealthDelta: "5 ఏళ్ల నికర ఆర్థిక లాభం",
      consultingText: "విచారిస్తున్నారు...",
      consultBtnText: "ఏజెంట్‌ను సంప్రదించండి",
    },
    ta: {
      heroTitle: "பெற்றோர்களுக்கான முழுமையான வெளிப்படைத்தன்மையுடன் கூடிய சேர்க்கை வழிகாட்டி",
      heroSubtitle: "UGC பட்டப்படிப்பு அங்கீகாரம், AI வேலை பாதுகாப்பு, 35+ கூட்டாண்மை கல்லூரிகள் மற்றும் 5 ஆண்டு நிதி ஆதாயம் பற்றிய உண்மைகள்.",
      askQuestionPlaceholder: "கட்டணம், பட்டம், AI வேலைகள் அல்லது கல்லூரிகள் பற்றி உங்கள் மொழியில் கேளுங்கள்...",
      downloadDossier: "அதிகாரப்பூர்வ அறிக்கையை பதிவிறக்கவும் (PDF)",
      lockSeat: "இடத்தை முன்பதிவு செய்க (₹10,000 திருப்பி அளிக்கக்கூடியது)",
      agentReasoning: "AI ஏஜென்ட் பகுப்பாய்வு & டூல்ஸ் செயல்படுத்தல்",
      campusesFound: "பொருத்தமான பல்கலைக்கழக வளாகங்கள்",
      roiBreakEven: "முதலீடு திரும்பப்பெறும் காலம்",
      wealthDelta: "5 ஆண்டு நிகர நிதி ஆதாயம்",
      consultingText: "ஆலோசிக்கிறது...",
      consultBtnText: "ஏஜென்டை கலந்தாலோசிக்கவும்",
    },
    hi: {
      heroTitle: "अभिभावकों के लिए शत-प्रतिशत पारदर्शी एडमिशन परामर्श",
      heroSubtitle: "UGC डिग्री मान्यता, AI से सुरक्षित भविष्य, 35+ पार्टनर यूनिवर्सिटीज का चयन और 5 वर्षों का वित्तीय लाभ।",
      askQuestionPlaceholder: "फीस, डिग्री की मान्यता, AI करियर या यूनिवर्सिटी के बारे में अपनी भाषा में पूछें...",
      downloadDossier: "आधिकारिक डोजियर डाउनलोड करें (PDF)",
      lockSeat: "सीट सुरक्षित करें (₹10,000 रिफंडेबल टोकन)",
      agentReasoning: "AI एजेंट लाइव डेटा विश्लेषण एवं टूल्स",
      campusesFound: "उपयुक्त पार्टनर यूनिवर्सिटीज",
      roiBreakEven: "लागत वसूली की अवधि",
      wealthDelta: "5 वर्षों का शुद्ध वित्तीय लाभ",
      consultingText: "परामर्श हो रहा है...",
      consultBtnText: "एजेंट से परामर्श करें",
    },
    kn: {
      heroTitle: "ಪೋಷಕರಿಗೆ ಸಂಪೂರ್ಣ ಪಾರದರ್ಶಕತೆಯ ಪ್ರವೇಶ ಮಾರ್ಗದರ್ಶಿ",
      heroSubtitle: "UGC ಪದವಿ ಮಾನ್ಯತೆ, AI ಉದ್ಯೋಗ ಭದ್ರತೆ, 35+ ಪಾಲುದಾರ ವಿಶ್ವವಿದ್ಯಾಲಯಗಳು ಮತ್ತು 5 ವರ್ಷಗಳ ಆರ್ಥಿಕ ಲಾಭದ ಸತ್ಯಾಂಶಗಳು.",
      askQuestionPlaceholder: "ಶುಲ್ಕ, ಪದವಿ, AI ಉದ್ಯೋಗಗಳು ಅಥವಾ ಕಾಲೇಜುಗಳ ಬಗ್ಗೆ ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಕೇಳಿ...",
      downloadDossier: "ಅಧಿಕೃತ ವರದಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ (PDF)",
      lockSeat: "ಸೀಟನ್ನು ಕಾಯ್ದಿರಿಸಿ (₹10,000 ಮರುಪಾವತಿಸಬಹುದಾದ)",
      agentReasoning: "AI ಏಜೆಂಟ್ ಡೇಟಾ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಉಪಕರಣಗಳು",
      campusesFound: "ಹೊಂದಿಕೆಯಾಗುವ ವಿಶ್ವವಿದ್ಯಾಲಯ ಕ್ಯಾಂಪಸ್‌ಗಳು",
      roiBreakEven: "ಹೂಡಿಕೆ ಮರುಪಾವತಿ ಅವಧಿ",
      wealthDelta: "5 ವರ್ಷಗಳ ನಿವ್ವಳ ಆರ್ಥಿಕ ಗಳಿಕೆ",
      consultingText: "ಸಲಹೆ ಪಡೆಯುತ್ತಿದ್ದೇವೆ...",
      consultBtnText: "ಏಜೆಂಟ್ ಸಲಹೆ ಪಡೆಯಿರಿ",
    },
    ml: {
      heroTitle: "രക്ഷിതാക്കൾക്ക് പൂർണ്ണ സുതാര്യതയുള്ള പ്രവേശന മാർഗ്ഗനിർദ്ദേശം",
      heroSubtitle: "UGC ബിരുദ അംഗീകാരം, AI തൊഴിൽ സുരക്ഷ, 35+ പങ്കാളിത്ത സർവകലാശാലകൾ, 5 വർഷത്തെ സാമ്പത്തിക നേട്ടം.",
      askQuestionPlaceholder: "ഫീസ്, ബിരുദം, AI തൊഴിലുകൾ അല്ലെങ്കിൽ ക്യാമ്പസുകൾ എന്നിവയെക്കുറിച്ച് നിങ്ങളുടെ ഭാഷയിൽ ചോദിക്കുക...",
      downloadDossier: "ഔദ്യോഗിക റിപ്പോർട്ട് ഡൗൺലോഡ് ചെയ്യുക (PDF)",
      lockSeat: "സീറ്റ് റിസർവ് ചെയ്യുക (₹10,000 തിരികെ ലഭിക്കുന്നത്)",
      agentReasoning: "AI ഏജന്റ് ഡാറ്റ വിശകലനവും ഉപകരണങ്ങളും",
      campusesFound: "യോജിച്ച സർവകലാശാലാ കാമ്പസുകൾ",
      roiBreakEven: "നിക്ഷേപം തിരിച്ചുപിടിക്കുന്ന സമയം",
      wealthDelta: "5 വർഷത്തെ മൊത്തം സാമ്പത്തിക നേട്ടം",
      consultingText: "ഉപദേശം ലഭ്യമാക്കുന്നു...",
      consultBtnText: "ഏജന്റിനോട് ആലോചിക്കുക",
    },
  },

  // ── Campus data (subset shown to client) ──
  CAMPUSES: [
    { id:"campus-chaitanya-hyd",   name:"NIAT @ Chaitanya (Deemed to be University)", shortName:"Chaitanya University",     universityName:"Chaitanya Deemed to be University",                     city:"Hyderabad / Warangal",    state:"Telangana",     region:"South", accreditation:"UGC Approved · NAAC 'A' Grade · AICTE Compliant",          ugcApproved:true, aicteApproved:true, degreeAwarded:"B.Tech CSE (AI & ML)",         specializations:["AI & Machine Learning","Full-Stack Architecture"],  annualTuitionFee:175000, nxtwaveProgramFee:125000, totalAnnualFee:300000,  totalFourYearFee:1200000, hostelFeeAnnual:85000,  minNatPercentile:70, minBoardPercentage:60, labType:"Lab 5.0 High-Performance Compute Pod",          featuredHighlight:"NxtWave's founding campus partner; 450+ students placed with avg ₹8.4 LPA.",   establishedYear:1991 },
    { id:"campus-dypatil-pune",    name:"NIAT @ Dr. D.Y. Patil University",           shortName:"D.Y. Patil University",    universityName:"Dr. D.Y. Patil Pratishthan Deemed University",           city:"Pune",                    state:"Maharashtra",   region:"West",  accreditation:"UGC Recognized · NAAC 'A++' Grade · NBA Accredited",        ugcApproved:true, aicteApproved:true, degreeAwarded:"B.Tech CSE (Data Science & AI)", specializations:["Data Science & Analytics","Applied Generative AI"],  annualTuitionFee:210000, nxtwaveProgramFee:140000, totalAnnualFee:350000,  totalFourYearFee:1400000, hostelFeeAnnual:110000, minNatPercentile:78, minBoardPercentage:65, labType:"Lab 5.0 Generative AI Innovation Centre",       featuredHighlight:"Hinjewadi tech corridor — direct hackathons & semester internships.",           establishedYear:2002 },
    { id:"campus-yenepoya-mng",    name:"NIAT @ Yenepoya (Deemed to be University)",  shortName:"Yenepoya University",      universityName:"Yenepoya Deemed to be University",                      city:"Mangalore / Bengaluru",   state:"Karnataka",     region:"South", accreditation:"UGC Approved · NAAC 'A+' Grade · NIRF Ranked",              ugcApproved:true, aicteApproved:true, degreeAwarded:"B.Tech CSE (Cloud & DevOps)",   specializations:["Cloud Native Computing","Cybersecurity & DevOps"],  annualTuitionFee:190000, nxtwaveProgramFee:120000, totalAnnualFee:310000,  totalFourYearFee:1240000, hostelFeeAnnual:95000,  minNatPercentile:72, minBoardPercentage:60, labType:"Lab 5.0 Cloud & Distributed Systems Pod",       featuredHighlight:"Strong Karnataka tech linkages; dual NxtWave + NSDC certifications.",          establishedYear:2008 },
    { id:"campus-niu-delhi",       name:"NIAT @ Noida International University",       shortName:"Noida International Univ",universityName:"Noida International University (NIU)",                   city:"Greater Noida (Delhi-NCR)",state:"Uttar Pradesh", region:"North", accreditation:"UGC Recognized · AICTE Approved · NAAC Accredited",         ugcApproved:true, aicteApproved:true, degreeAwarded:"B.Tech CSE (AI & Emerging Tech)", specializations:["Autonomous AI Agents","Full-Stack Web3 & Cloud"],   annualTuitionFee:180000, nxtwaveProgramFee:130000, totalAnnualFee:310000,  totalFourYearFee:1240000, hostelFeeAnnual:100000, minNatPercentile:68, minBoardPercentage:60, labType:"Lab 5.0 AI & Autonomous Robotics Pod",           featuredHighlight:"Premier Delhi-NCR gateway; 75-acre campus with modern AI curriculum.",          establishedYear:2010 },
    { id:"campus-svyasa-blr",      name:"NIAT @ S-VYASA Deemed University",            shortName:"S-VYASA University",       universityName:"S-VYASA Deemed to be University",                       city:"Bengaluru",               state:"Karnataka",     region:"South", accreditation:"UGC Category-1 Deemed University · NAAC 'A+' Grade",        ugcApproved:true, aicteApproved:true, degreeAwarded:"B.Tech CS (AI & ML)",           specializations:["AI/ML Algorithms","Enterprise Software Engineering"], annualTuitionFee:220000, nxtwaveProgramFee:140000, totalAnnualFee:360000,  totalFourYearFee:1440000, hostelFeeAnnual:105000, minNatPercentile:80, minBoardPercentage:65, labType:"Lab 5.0 Bengaluru Silicon Pod",                  featuredHighlight:"Direct access to Bangalore startup ecosystem; ex-FAANG Saturday Masterclasses.", establishedYear:2002 },
    { id:"campus-crescent-chennai",name:"NIAT @ B.S. Abdur Rahman Crescent Institute", shortName:"Crescent Institute",       universityName:"B.S. Abdur Rahman Crescent Institute of Science and Tech", city:"Chennai",                 state:"Tamil Nadu",    region:"South", accreditation:"UGC Approved · NAAC 'A+' Grade · AICTE Approved",           ugcApproved:true, aicteApproved:true, degreeAwarded:"B.Tech IT & AI Solutions",      specializations:["Enterprise AI Applications","Mobile Computing"],    annualTuitionFee:185000, nxtwaveProgramFee:125000, totalAnnualFee:310000,  totalFourYearFee:1240000, hostelFeeAnnual:90000,  minNatPercentile:70, minBoardPercentage:60, labType:"Lab 5.0 Full-Stack Innovation Pod",              featuredHighlight:"Strong SaaS industry ties to OMR IT Corridor companies.",                       establishedYear:1984 },
    { id:"campus-mallareddy-hyd",  name:"NIAT @ Malla Reddy University",               shortName:"Malla Reddy University",   universityName:"Malla Reddy University",                                city:"Hyderabad",               state:"Telangana",     region:"South", accreditation:"State Private University · UGC Recognized",                 ugcApproved:true, aicteApproved:true, degreeAwarded:"B.Tech CSE (AI & Data Engineering)", specializations:["Data Engineering & Pipelines","AI Agentic Workflows"], annualTuitionFee:170000, nxtwaveProgramFee:110000, totalAnnualFee:280000, totalFourYearFee:1120000, hostelFeeAnnual:80000,  minNatPercentile:65, minBoardPercentage:60, labType:"Lab 5.0 Data Engineering Pod",                   featuredHighlight:"Popular for AP & Telangana students; high hostel capacity & affordable fees.",   establishedYear:2020 },
    { id:"campus-amet-chennai",    name:"NIAT @ AMET Deemed to be University",          shortName:"AMET University",          universityName:"AMET Deemed to be University",                          city:"Chennai (ECR)",           state:"Tamil Nadu",    region:"South", accreditation:"UGC Approved · NAAC 'A' Grade",                             ugcApproved:true, aicteApproved:true, degreeAwarded:"B.Tech AI and Machine Learning",specializations:["Applied Machine Learning","IoT & AI"],               annualTuitionFee:165000, nxtwaveProgramFee:115000, totalAnnualFee:280000,  totalFourYearFee:1120000, hostelFeeAnnual:85000,  minNatPercentile:62, minBoardPercentage:55, labType:"Lab 5.0 IoT & AI Hybrid Pod",                    featuredHighlight:"Scenic ECR coastal campus; dedicated NxtWave coding workstations & 24/7 mentors.", establishedYear:1993 },
  ],

};
