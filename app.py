import streamlit as st
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="GMDSS Portal", page_icon="⚓", layout="centered")

# --- GELİŞMİŞ CSS (EKRANA SIĞDIRMA VE MODERN TEMA) ---
st.markdown("""
    <style>
    /* Arka plan ve genel yazı tipi */
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    
    /* Buton Tasarımları */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #3060d0;
        background-color: #161B22;
        color: #FFFFFF;
        padding: 8px 15px; /* Kompakt yükseklik */
        margin-bottom: 5px;
        font-size: 14px;
        transition: all 0.2s ease;
        text-align: left;
    }
    .stButton>button:hover {
        border-color: #58a6ff;
        background-color: #1F2937;
    }
    
    /* Başlık ve Logo */
    .serkan-hoca {
        font-size: 28px !important;
        font-weight: 800;
        color: #58a6ff;
        text-align: center;
        margin-top: -50px;
    }
    
    /* Soru ve Sayaç Alanı */
    .question-box {
        background-color: #161B22;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #58a6ff;
        margin-bottom: 10px;
    }
    .counter {
        font-family: monospace;
        color: #8b949e;
        text-align: right;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ (40 SORU) ---
RAW_DATA = [
    {"q": "SÜZEN sözcüğü, uluslararası heceleme (fonetik) alfabesi ile nasıl kodlanır?", "a": "Sierra UniformZuluEchoNovember", "options": ["Sette Ultra ZuluEndoNovember", "South Ultra ZouluoEleven North", "Sierra UniformZuluEchoNovember", "Sierra UniformZuluEndoNove", "Sette UniformZouluoEicoNovember"]},
    {"q": "ETAT ücretli servis işaretinin anlamı nedir?", "a": "Devlet telgrafı", "options": ["Servis telgrafı", "Postrestant telgraf", "Denizcilikle ilgili telgraf", "Devlet telgrafı", "Acele telgraf"]},
    {"q": "Nomanklatürlerde geçen 'CO' kısaltmasının anlamı nedir?", "a": "Yalnız resmi bir kuruluşun haberleşmesini yapan istasyon", "options": ["Anten ayarı", "Kıyı uydu yer istasyonu", "Yalnız resmi bir kuruluşun haberleşmesini yapan istasyon", "Tarihinde iptal edildi", "Uzay istasyonu"]},
    {"q": "Emisyon sembolünde ilk karakterin 'B' olması neyi tanımlar?", "a": "İki bağımsız yan band", "options": ["Tek yan band bastırılmış taşıyıcı", "İki bağımsız yan band", "Faz modülasyonlu tek yan band", "Çift yan band", "Tek yan band azaltılmış taşıyıcı"]},
    {"q": "Deniz VHF bandında öncelikle seyir güvenliği amacıyla kullanılan kanal hangisidir?", "a": "Kanal 13", "options": ["Kanal 06", "Kanal 13", "Kanal 16", "Kanal 70", "Kanal 08"]},
    {"q": "Gemide telsiz jurnalleri ne kadar süre saklanmalıdır?", "a": "2 yıl", "options": ["6 ay", "1 yıl", "2 yıl", "5 yıl", "Süresiz"]},
    {"q": "156.800 MHz frekansı hangi bandın içindedir?", "a": "VHF", "options": ["MF", "HF", "UHF", "VHF", "SHF"]},
    {"q": "Mevcut Cospas-Sarsat sisteminin bir sonraki nesli hangisidir?", "a": "MEOSAR", "options": ["SZNSAR", "GENSAR", "OTSSAR", "AISSAR", "MEOSAR"]},
    {"q": "AIS 1 kanalının frekansı nedir?", "a": "161.975 MHz", "options": ["156.825 MHz", "161.975 MHz", "162.025 MHz", "156.525 MHz", "156.300 MHz"]},
    {"q": "Tıbbi yardım talebi mesajları hangi öncelik derecesiyle gönderilir?", "a": "Urgency", "options": ["Distress", "Urgency", "Safety", "Routine", "Security"]},
    {"q": "VHF Kanal 70 hangi amaçla kullanılır?", "a": "Dijital Seçmeli Çağrı (DSC)", "options": ["Sesli tehlike çağrısı", "Liman kontrol", "Dijital Seçmeli Çağrı (DSC)", "Meteoroloji", "Gemi içi haberleşme"]},
    {"q": "Navtex cihazı hangi frekanstan uluslararası (İngilizce) yayınları alır?", "a": "518 kHz", "options": ["490 kHz", "518 kHz", "2182 kHz", "4209.5 kHz", "156.8 MHz"]},
    {"q": "GMDSS sisteminde A3 deniz bölgesi neyi tanımlar?", "a": "Inmarsat uydularının kapsama alanı", "options": ["Sadece VHF sahası", "Sadece MF sahası", "Inmarsat uydularının kapsama alanı", "Kutup bölgeleri", "Liman sahaları"]},
    {"q": "EPIRB cihazının hidrostatik kilidi (HRU) değişim periyodu genellikle nedir?", "a": "2 yıl", "options": ["Her yıl", "2 yıl", "4 veya 5 yıl", "10 yıl", "Hiçbiri"]},
    {"q": "SART cihazı radar ekranında nasıl görünür?", "a": "12 adet nokta veya yay", "options": ["Büyük bir daire", "Yanıp sönen ışık", "12 adet nokta veya yay", "Gemi adı", "Düz çizgi"]},
    {"q": "'MAYDAY RELAY' ifadesi hangi durumda kullanılır?", "a": "Başka bir geminin tehlike çağrısını aktarırken", "options": ["Kendi gemimiz tehlikedeyken", "Başka bir geminin tehlike çağrısını aktarırken", "Hava raporu verirken", "Test yaparken", "Liman girişi istenirken"]},
    {"q": "GOC belgelerinin geçerlilik süresi nedir?", "a": "5 yıl", "options": ["Ömür boyu", "1 yıl", "5 yıl", "10 yıl", "2 yıl"]},
    {"q": "DSC üzerinden yapılan bir tehlike çağrısında hangisi bulunmaz?", "a": "Bir sonraki liman", "options": ["MMSI numarası", "Tehlikenin cinsi", "Mevki (Koordinat)", "Bir sonraki liman", "Haberleşme tipi"]},
    {"q": "VHF sesli görüşme (telsiz telefon) emisyonu hangisidir?", "a": "F3E (veya G3E)", "options": ["J3E", "F1B", "F3E (veya G3E)", "A1A", "J2B"]},
    {"q": "Inmarsat-C tehlike butonu kaç saniye basılı tutulmalıdır?", "a": "Yaklaşık 5 saniye", "options": ["1 saniye", "Hemen bırakılır", "Yaklaşık 5 saniye", "30 saniye", "Basılmaz"]},
    {"q": "Bir geminin MMSI numarası kaç hanelidir?", "a": "9", "options": ["3", "6", "9", "12", "15"]},
    {"q": "Inmarsat-C üzerinden MSI yayınlarını almaya ne ad verilir?", "a": "SafetyNet", "options": ["Navtex", "SafetyNet", "RadioTelex", "DSC", "GMDSS"]},
    {"q": "Telsiz operatörünün sessizlik periyotlarını takip etmesi gereken frekans hangisidir?", "a": "2182 kHz", "options": ["156.8 MHz", "2182 kHz", "518 kHz", "406 MHz", "1.6 GHz"]},
    {"q": "Navtex mesajlarındaki 'B1' karakteri neyi temsil eder?", "a": "Yayın yapan istasyonu", "options": ["Mesajın konusunu", "Yayın yapan istasyonu", "Mesaj numarasını", "Tarihi", "Geminin adını"]},
    {"q": "A2 deniz bölgesi hangi cihazın kapsama alanıdır?", "a": "MF", "options": ["VHF", "MF", "HF", "Inmarsat", "Iridium"]},
    {"q": "J3E emisyonu neyi ifade eder?", "a": "Genlik Modülasyonlu Ses (SSB)", "options": ["Telgraf", "Genlik Modülasyonlu Ses (SSB)", "Dijital Veri", "Faks", "Radar"]},
    {"q": "EPIRB cihazı hangi frekansta uydulara sinyal gönderir?", "a": "406 MHz", "options": ["156.8 MHz", "121.5 MHz", "406 MHz", "518 kHz", "9 GHz"]},
    {"q": "SART cihazı hangi frekans bandında çalışır?", "a": "9 GHz (X-Band Radar)", "options": ["VHF", "MF", "9 GHz (X-Band Radar)", "3 GHz (S-Band Radar)", "HF"]},
    {"q": "GMDSS sisteminde 'Tehlike' (Distress) mesajının en belirgin özelliği nedir?", "a": "Önceliği en yüksektir ve tüm trafik durdurulur", "options": ["Herkesin cevap vermesi zorunludur", "Önceliği en yüksektir ve tüm trafik durdurulur", "Sadece ücretli mesajlarda kullanılır", "Sadece gündüzleri çekilir", "Sadece Inmarsat üzerinden yapılır"]},
    {"q": "Gemiler arası tehlike trafiğinde Kanal 16 üzerinden konuşulurken sessizliği sağlamak için hangi terim kullanılır?", "a": "Seelonce Mayday", "options": ["Silence Fini", "Seelonce Mayday", "Stop Talking", "PanPan", "Securite"]},
    {"q": "MF DSC tehlike frekansı hangisidir?", "a": "2187.5 kHz", "options": ["2182 kHz", "2187.5 kHz", "518 kHz", "8414.5 kHz", "156.525 MHz"]},
    {"q": "Bir DSC çağrısında 'Safety' (Emniyet) önceliği hangi anonsla başlar?", "a": "Securite", "options": ["Mayday", "PanPan", "Securite", "Urgent", "Warning"]},
    {"q": "Inmarsat-C terminalinde mesajın ulaştığını gösteren onay mesajına ne denir?", "a": "ACK (Acknowledgement)", "options": ["Delivery Notification", "ACK (Acknowledgement)", "Echo", "Receipt", "Done"]},
    {"q": "Telsiz jurnaline hangi bilgiler yazılmaz?", "a": "Personelin yemek saati", "options": ["Günlük testler", "Alınan tehlike mesajları", "Akü voltaj değerleri", "Personelin yemek saati", "Operatör değişimleri"]},
    {"q": "Navtex yayın menzili yaklaşık ne kadardır?", "a": "250-400 mil", "options": ["50 mil", "250-400 mil", "1000 mil", "Küresel", "10 mil"]},
    {"q": "DSC çağrısında 'Urgency' önceliği ne için kullanılır?", "a": "Bir kişi denize düştüyse veya tıbbi aciliyet varsa", "options": ["Gemi batıyorsa", "Bir kişi denize düştüyse veya tıbbi aciliyet varsa", "Fener sönükse", "Gemide boya yapılıyorsa", "Selamlaşma için"]},
    {"q": "VHF telsiz cihazının azami çıkış gücü ne kadardır?", "a": "25 Watt", "options": ["1 Watt", "5 Watt", "25 Watt", "100 Watt", "1.5 kW"]},
    {"q": "VHF CH 16 frekansı nedir?", "a": "156.800 MHz", "options": ["156.300 MHz", "156.525 MHz", "156.800 MHz", "156.650 MHz", "161.975 MHz"]},
    {"q": "Bir EPIRB cihazı suyun kaç metre altında otomatik olarak serbest kalır?", "a": "1.5 - 4 metre", "options": ["1 metre", "1.5 - 4 metre", "10 metre", "20 metre", "Serbest kalmaz"]},
    {"q": "Telsiz operatörü DSC test çağrısını kime yapar?", "a": "Sahil istasyonuna (RCC)", "options": ["Herhangi bir gemiye", "Sahil istasyonuna (RCC)", "Kendi gemisine", "Tanıdık bir tekneye", "Test çağrısı yapılmaz"]}
]

# --- SESSION STATE ---
if 'quiz' not in st.session_state:
    questions = random.sample(RAW_DATA, len(RAW_DATA))
    # Şıkları da karıştırarak sakla
    for item in questions:
        random.shuffle(item["options"])
    st.session_state.quiz = questions
    st.session_state.idx = 0
    st.session_state.results = []
    st.session_state.done = False

# --- UI ---
st.markdown('<p class="serkan-hoca">⚓ SERKAN HOCA İLE</p>', unsafe_allow_html=True)

def restart_quiz():
    st.session_state.clear()
    st.rerun()

if not st.session_state.done:
    # Sayaç ve Soru 
    col_a, col_b = st.columns([1, 4])
    col_a.markdown(f'<p class="counter">{st.session_state.idx + 1} / {len(RAW_DATA)}</p>', unsafe_allow_html=True)
    
    curr = st.session_state.quiz[st.session_state.idx]
    st.markdown(f'<div class="question-box">{curr["q"]}</div>', unsafe_allow_html=True)

    # Şıklar (Otomatik Geçiş ve Dinamik Cevap Anahtarı) [cite: 3, 7]
    for opt in curr["options"]:
        if st.button(opt):
            st.session_state.results.append({
                "question": curr["q"],
                "given": opt,
                "correct": curr["a"]
            })
            if st.session_state.idx + 1 < len(RAW_DATA):
                st.session_state.idx += 1
            else:
                st.session_state.done = True
            st.rerun()

    # Kontrol Paneli
    st.write("---")
    c1, c2 = st.columns(2)
    if c1.button("🏠 Kapat / Başa Dön"): restart_quiz()
    if c2.button("💾 Devam Et"): st.toast("Kaldığınız yer korundu.")

else:
    # --- ANALİZ SAYFASI ---
    correct_total = sum(1 for r in st.session_state.results if r["given"] == r["correct"])
    score = (correct_total / len(RAW_DATA)) * 100

    if score >= 80:
        st.balloons()
        st.success("# TEBRİKLER HARİKASIN! 🚀")
    
    st.metric("BAŞARI ORANI", f"%{score:.1f}")
    
    # Detaylı Analiz
    for i, res in enumerate(st.session_state.results):
        is_correct = res["given"] == res["correct"]
        status = "✅" if is_correct else "❌"
        with st.expander(f"Soru {i+1}: {status}"):
            st.write(f"**Soru:** {res['question']}")
            st.write(f"**Senin Cevabın:** {res['given']}")
            if not is_correct:
                st.error(f"**Doğru Cevap:** {res['correct']}")
                
    if st.button("Sınavı Tekrar Başlat"): restart_quiz()
