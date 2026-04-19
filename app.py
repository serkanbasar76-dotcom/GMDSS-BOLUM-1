import streamlit as st
import random

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="GMDSS Sınav Sistemi", page_icon="⚓", layout="centered")

# --- ULTRA-KOMPAKT VE MODERN CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 0.5rem; padding-bottom: 0rem; max-width: 800px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    .main-header {
        font-size: 26px !important;
        font-weight: 800;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }
    .serkan-hoca {
        font-size: 18px !important;
        font-weight: 600;
        color: #58a6ff;
        text-align: center;
        margin-top: -5px;
        margin-bottom: 10px;
    }
    .question-header {
        font-size: 14px;
        color: #8b949e;
        text-align: center;
        margin-bottom: 5px;
    }
    .question-box {
        background-color: #161B22;
        padding: 12px 18px;
        border-radius: 8px;
        border-left: 5px solid #58a6ff;
        font-size: 15px;
        line-height: 1.4;
        margin-bottom: 10px;
    }
    /* Şık Butonları */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        border: 1px solid #3060d0;
        background-color: #1c2128;
        color: #FFFFFF;
        padding: 6px 12px;
        font-size: 14px;
        text-align: left;
        margin-bottom: -10px; /* Dikey boşluğu daraltır */
        transition: 0.1s;
    }
    .stButton>button:hover { background-color: #3060d0; border-color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SETİ (DOKÜMANDAKİ TÜM SORULAR) ---
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
    {"q": "Navtex cihazı hangi frekanstan uluslararası yayınları alır?", "a": "518 kHz", "options": ["490 kHz", "518 kHz", "2182 kHz", "4209.5 kHz", "156.8 MHz"]},
    {"q": "GMDSS sisteminde A3 deniz bölgesi neyi tanımlar?", "a": "Inmarsat uydularının kapsama alanı", "options": ["Sadece VHF sahası", "Sadece MF sahası", "Inmarsat uydularının kapsama alanı", "Kutup bölgeleri", "Liman sahaları"]},
    {"q": "EPIRB cihazının hidrostatik kilidi (HRU) değişim periyodu nedir?", "a": "2 yıl", "options": ["Her yıl", "2 yıl", "4 veya 5 yıl", "10 yıl", "Hiçbiri"]},
    {"q": "SART cihazı radar ekranında nasıl görünür?", "a": "12 adet nokta veya yay", "options": ["Büyük bir daire", "Yanıp sönen ışık", "12 adet nokta veya yay", "Gemi adı", "Düz çizgi"]},
    {"q": "'MAYDAY RELAY' ifadesi hangi durumda kullanılır?", "a": "Başka bir geminin tehlike çağrısını aktarırken", "options": ["Kendi gemimiz tehlikedeyken", "Başka bir geminin tehlike çağrısını aktarırken", "Hava raporu verirken", "Test yaparken", "Liman girişi istenirken"]},
    {"q": "GOC belgelerinin geçerlilik süresi nedir?", "a": "5 yıl", "options": ["Ömür boyu", "1 yıl", "5 yıl", "10 yıl", "2 yıl"]},
    {"q": "DSC üzerinden yapılan bir tehlike çağrısında hangisi bulunmaz?", "a": "Bir sonraki liman", "options": ["MMSI numarası", "Tehlikenin cinsi", "Mevki (Koordinat)", "Bir sonraki liman", "Haberleşme tipi"]},
    {"q": "VHF sesli görüşme emisyonu hangisidir?", "a": "F3E (veya G3E)", "options": ["J3E", "F1B", "F3E (veya G3E)", "A1A", "J2B"]},
    {"q": "Inmarsat-C tehlike butonu kaç saniye basılı tutulmalıdır?", "a": "Yaklaşık 5 saniye", "options": ["1 saniye", "Hemen bırakılır", "Yaklaşık 5 saniye", "30 saniye", "Basılmaz"]},
    {"q": "Bir geminin MMSI numarası kaç hanelidir?", "a": "9", "options": ["3", "6", "9", "12", "15"]},
    {"q": "Inmarsat-C üzerinden MSI yayınlarını almaya ne ad verilir?", "a": "SafetyNet", "options": ["Navtex", "SafetyNet", "RadioTelex", "DSC", "GMDSS"]},
    {"q": "Telsiz operatörünün sessizlik periyotlarını izlemesi gereken frekans?", "a": "2182 kHz", "options": ["156.8 MHz", "2182 kHz", "518 kHz", "406 MHz", "1.6 GHz"]},
    {"q": "Navtex mesajlarındaki 'B1' karakteri neyi temsil eder?", "a": "Yayın yapan istasyonu", "options": ["Mesajın konusunu", "Yayın yapan istasyonu", "Mesaj numarasını", "Tarihi", "Geminin adını"]},
    {"q": "A2 deniz bölgesi hangi cihazın kapsama alanıdır?", "a": "MF", "options": ["VHF", "MF", "HF", "Inmarsat", "Iridium"]},
    {"q": "J3E emisyonu neyi ifade eder?", "a": "Genlik Modülasyonlu Ses (SSB)", "options": ["Telgraf", "Genlik Modülasyonlu Ses (SSB)", "Dijital Veri", "Faks", "Radar"]},
    {"q": "EPIRB cihazı hangi frekansta uydulara sinyal gönderir?", "a": "406 MHz", "options": ["156.8 MHz", "121.5 MHz", "406 MHz", "518 kHz", "9 GHz"]},
    {"q": "SART cihazı hangi frekans bandında çalışır?", "a": "9 GHz (X-Band Radar)", "options": ["VHF", "MF", "9 GHz (X-Band Radar)", "3 GHz (S-Band Radar)", "HF"]},
    {"q": "GMDSS sisteminde 'Tehlike' mesajının en belirgin özelliği?", "a": "Önceliği en yüksektir ve tüm trafik durdurulur", "options": ["Herkesin cevap vermesi zorunludur", "Önceliği en yüksektir ve tüm trafik durdurulur", "Sadece ücretli mesajlarda kullanılır", "Sadece gündüzleri çekilir", "Sadece Inmarsat üzerinden yapılır"]},
    {"q": "Kanal 16 üzerinden konuşulurken sessizliği sağlamak için kullanılan terim?", "a": "Seelonce Mayday", "options": ["Silence Fini", "Seelonce Mayday", "Stop Talking", "PanPan", "Securite"]},
    {"q": "MF DSC tehlike frekansı hangisidir?", "a": "2187.5 kHz", "options": ["2182 kHz", "2187.5 kHz", "518 kHz", "8414.5 kHz", "156.525 MHz"]},
    {"q": "Bir DSC çağrısında 'Safety' önceliği hangi anonsla başlar?", "a": "Securite", "options": ["Mayday", "PanPan", "Securite", "Urgent", "Warning"]},
    {"q": "Inmarsat-C terminalinde mesajın ulaştığını gösteren onay?", "a": "ACK (Acknowledgement)", "options": ["Delivery Notification", "ACK (Acknowledgement)", "Echo", "Receipt", "Done"]},
    {"q": "Telsiz jurnaline hangi bilgiler yazılmaz?", "a": "Personelin yemek saati", "options": ["Günlük testler", "Alınan tehlike mesajları", "Akü voltaj değerleri", "Personelin yemek saati", "Operatör değişimleri"]},
    {"q": "Navtex yayın menzili yaklaşık ne kadardır?", "a": "250-400 mil", "options": ["50 mil", "250-400 mil", "1000 mil", "Küresel", "10 mil"]},
    {"q": "DSC çağrısında 'Urgency' önceliği ne için kullanılır?", "a": "Bir kişi denize düştüyse veya tıbbi aciliyet varsa", "options": ["Gemi batıyorsa", "Bir kişi denize düştüyse veya tıbbi aciliyet varsa", "Fener sönükse", "Gemide boya yapılıyorsa", "Selamlaşma için"]},
    {"q": "VHF telsiz cihazının azami çıkış gücü nedir?", "a": "25 Watt", "options": ["1 Watt", "5 Watt", "25 Watt", "100 Watt", "1.5 kW"]},
    {"q": "VHF CH 16 frekansı nedir?", "a": "156.800 MHz", "options": ["156.300 MHz", "156.525 MHz", "156.800 MHz", "156.650 MHz", "161.975 MHz"]},
    {"q": "EPIRB cihazı suyun kaç metre altında otomatik açılır?", "a": "1.5 - 4 metre", "options": ["1 metre", "1.5 - 4 metre", "10 metre", "20 metre", "Serbest kalmaz"]},
    {"q": "Telsiz operatörü DSC test çağrısını kime yapar?", "a": "Sahil istasyonuna (RCC)", "options": ["Herhangi bir gemiye", "Sahil istasyonuna (RCC)", "Kendi gemisine", "Tanıdık bir tekneye", "Test çağrısı yapılmaz"]}
]

# --- DENGELİ CEVAP ANAHTARI ALGORİTMASI (%20 DAĞILIM) ---
def build_balanced_quiz(data):
    shuffled = random.sample(data, len(data))
    # Her harf için eşit slot (40 soru / 5 harf = 8'er adet)
    slots = (["A"] * 8) + (["B"] * 8) + (["C"] * 8) + (["D"] * 8) + (["E"] * 8)
    random.shuffle(slots)
    
    quiz = []
    for i, item in enumerate(shuffled):
        correct = item["a"]
        wrongs = [o for o in item["options"] if o != correct]
        random.shuffle(wrongs)
        
        final_opts = [None] * 5
        target_idx = ord(slots[i]) - 65
        final_opts[target_idx] = correct
        
        w_ptr = 0
        for j in range(5):
            if final_opts[j] is None:
                final_opts[j] = wrongs[w_ptr]
                w_ptr += 1
        
        item_copy = item.copy()
        item_copy["options"] = final_opts
        quiz.append(item_copy)
    return quiz

# --- SESSION STATE ---
if 'st' not in st.session_state:
    st.session_state.quiz = build_balanced_quiz(RAW_DATA)
    st.session_state.idx = 0
    st.session_state.results = []
    st.session_state.done = False
    st.session_state.st = True

# --- ARA YÜZ ---
st.markdown('<p class="main-header">GMDSS SORULARI</p>', unsafe_allow_html=True)
st.markdown('<p class="serkan-hoca">⚓ SERKAN HOCA İLE</p>', unsafe_allow_html=True)

if not st.session_state.done:
    # Başlık: SORU 1/40
    st.markdown(f'<p class="question-header">SORU {st.session_state.idx + 1} / {len(RAW_DATA)}</p>', unsafe_allow_html=True)
    
    curr = st.session_state.quiz[st.session_state.idx]
    st.markdown(f'<div class="question-box">{curr["q"]}</div>', unsafe_allow_html=True)

    # Şıklar A-E
    letters = ["A", "B", "C", "D", "E"]
    for i, opt in enumerate(curr["options"]):
        if st.button(f"{letters[i]}) {opt}", key=f"btn_{st.session_state.idx}_{i}"):
            st.session_state.results.append({
                "n": st.session_state.idx + 1,
                "q": curr["q"],
                "u": opt,
                "c": curr["a"]
            })
            if st.session_state.idx + 1 < len(RAW_DATA):
                st.session_state.idx += 1
            else:
                st.session_state.done = True
            st.rerun()

    st.divider()
    c1, c2 = st.columns(2)
    if c1.button("🏠 Kapat / Başa Dön", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    if c2.button("💾 Kaldığım Yerden", use_container_width=True): 
        st.toast("İlerleme kaydedildi.")

else:
    # --- ANALİZ SAYFASI ---
    corrects = sum(1 for r in st.session_state.results if r["u"] == r["c"])
    score = (corrects / len(RAW_DATA)) * 100

    if score >= 80:
        st.balloons()
        st.success(f"# TEBRİKLER HARİKASIN! 🚀\nBaşarı Oranı: %{score:.1f}")
    else:
        st.info(f"Sınav Tamamlandı. Başarı Oranı: %{score:.1f}")
    
    st.subheader("Hata Analizi")
    for r in st.session_state.results:
        if r["u"] != r["c"]:
            with st.expander(f"Soru {r['n']} - Yanlış ❌"):
                st.write(f"**Soru:** {r['q']}")
                st.error(f"Senin Cevabın: {r['u']}")
                st.success(f"Doğru Cevap: {r['c']}")
                
    if st.button("Sınava Baştan Başla", use_container_width=True):
        st.session_state.clear()
        st.rerun()
