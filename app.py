import streamlit as st
import random
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="GMDSS Sınav Portalı", page_icon="⚓", layout="centered")

# --- CSS İLE MODERN TASARIM ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #ffffff;
        color: #1f77b4;
        border: 2px solid #1f77b4;
        transition: 0.3s;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1f77b4;
        color: white;
    }
    .logo-text {
        font-size: 40px !important;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-logo {
        text-align: center;
        font-size: 20px;
        color: #555;
        margin-bottom: 20px;
    }
    .score-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SORU BANKASI (DOKÜMANDAN AKTARILAN) ---
# Açıklamalar şartname gereği çıkarılmıştır.
QUESTIONS = [
    {"q": "SÜZEN sözcüğü, uluslararası heceleme (fonetik) alfabesi ile nasıl kodlanır?", "a": "C", "options": ["Sette Ultra ZuluEndoNovember", "South Ultra ZouluoEleven North", "Sierra UniformZuluEchoNovember", "Sierra UniformZuluEndoNove", "Sette UniformZouluoEicoNovember"]},
    {"q": "ETAT ücretli servis işaretinin anlamı nedir?", "a": "D", "options": ["Servis telgrafı", "Postrestant telgraf", "Denizcilikle ilgili telgraf", "Devlet telgrafı", "Acele telgraf"]},
    {"q": "Nomanklatürlerde geçen 'CO' kısaltmasının anlamı nedir?", "a": "C", "options": ["Anten ayarı", "Kıyı uydu yer istasyonu", "Yalnız resmi bir kuruluşun haberleşmesini yapan istasyon", "Tarihinde iptal edildi", "Uzay istasyonu"]},
    {"q": "Emisyon sembolünde ilk karakterin 'B' olması neyi tanımlar?", "a": "B", "options": ["Tek yan band bastırılmış taşıyıcı", "İki bağımsız yan band", "Faz modülasyonlu tek yan band", "Çift yan band", "Tek yan band azaltılmış taşıyıcı"]},
    {"q": "Deniz VHF bandında öncelikle seyir güvenliği amacıyla kullanılan kanal hangisidir?", "a": "B", "options": ["Kanal 06", "Kanal 13", "Kanal 16", "Kanal 70", "Kanal 08"]},
    {"q": "Gemide telsiz jurnalleri ne kadar süre saklanmalıdır?", "a": "C", "options": ["6 ay", "1 yıl", "2 yıl", "5 yıl", "Süresiz"]},
    {"q": "156.800 MHz frekansı hangi bandın içindedir?", "a": "D", "options": ["MF", "HF", "UHF", "VHF", "SHF"]},
    {"q": "Mevcut Cospas-Sarsat sisteminin bir sonraki nesli hangisidir?", "a": "E", "options": ["SZNSAR", "GENSAR", "OTSSAR", "AISSAR", "MEOSAR"]},
    {"q": "AIS 1 kanalının frekansı nedir?", "a": "B", "options": ["156.825 MHz", "161.975 MHz", "162.025 MHz", "156.525 MHz", "156.300 MHz"]},
    {"q": "Tıbbi yardım talebi mesajları hangi öncelik derecesiyle gönderilir?", "a": "B", "options": ["Distress", "Urgency", "Safety", "Routine", "Security"]},
    # Not: Diğer sorular da benzer formatta eklenebilir.
]

# --- SESSION STATE BAŞLATMA ---
if 'initialized' not in st.session_state:
    st.session_state.questions = random.sample(QUESTIONS, len(QUESTIONS))
    st.session_state.current_index = 0
    st.session_state.answers = []
    st.session_state.quiz_complete = False
    st.session_state.initialized = True

# --- LOGO VE BAŞLIK ---
st.markdown('<p class="logo-text">⚓ GMDSS PORTAL</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-logo">SERKAN HOCA İLE</p>', unsafe_allow_html=True)
st.divider()

# --- FONKSİYONLAR ---
def next_question(option_index):
    selected_letter = chr(65 + option_index) # 0->A, 1->B...
    st.session_state.answers.append({
        "question": st.session_state.questions[st.session_state.current_index]["q"],
        "selected": selected_letter,
        "correct": st.session_state.questions[st.session_state.current_index]["a"],
        "options": st.session_state.questions[st.session_state.current_index]["options"]
    })
    
    if st.session_state.current_index + 1 < len(st.session_state.questions):
        st.session_state.current_index += 1
    else:
        st.session_state.quiz_complete = True
    st.rerun()

def restart_quiz():
    st.session_state.questions = random.sample(QUESTIONS, len(QUESTIONS))
    st.session_state.current_index = 0
    st.session_state.answers = []
    st.session_state.quiz_complete = False
    st.rerun()

# --- ANA EKRAN MANTIĞI ---
if not st.session_state.quiz_complete:
    # İlerleme Çubuğu
    progress = (st.session_state.current_index) / len(st.session_state.questions)
    st.progress(progress)
    
    # Soru Gösterimi
    q = st.session_state.questions[st.session_state.current_index]
    st.subheader(f"Soru {st.session_state.current_index + 1}:")
    st.info(q["q"])

    # Şıklar (Tıklandığında otomatik geçer)
    cols = st.columns(1)
    for idx, option in enumerate(q["options"]):
        if st.button(f"{chr(65+idx)}) {option}", key=f"btn_{idx}"):
            next_question(idx)

    # Kontrol Butonları (Başa Dön / Kapat)
    st.write("---")
    ctrl_cols = st.columns(2)
    if ctrl_cols[0].button("🏠 Sınavı Kapat / Başa Dön"):
        restart_quiz()
    if ctrl_cols[1].button("🔄 Kaldığım Yerden Devam Et"):
        st.toast("Zaten buradasınız! Soruları çözmeye devam edin.")

else:
    # --- ANALİZ SAYFASI ---
    correct_count = sum(1 for a in st.session_state.answers if a["selected"] == a["correct"])
    total_q = len(st.session_state.questions)
    score_percent = (correct_count / total_q) * 100

    if score_percent >= 80:
        st.balloons()
        st.success("## TEBRİKLER HARİKASIN! 🎉")
    
    st.markdown(f"### Sınav Analizi - Başarı Oranı: %{score_percent:.1f}")
    
    # Sonuç Tablosu
    for i, ans in enumerate(st.session_state.answers):
        with st.expander(f"Soru {i+1}: {ans['selected'] == ans['correct'] and '✅' or '❌'}"):
            st.write(f"**Soru:** {ans['question']}")
            st.write(f"**Senin Cevabın:** {ans['selected']}")
            st.write(f"**Doğru Cevap:** {ans['correct']}")
            if ans['selected'] != ans['correct']:
                correct_text = ans['options'][ord(ans['correct'])-65]
                st.error(f"Doğru Şık: {ans['correct']} - {correct_text}")

    if st.button("Sınavı Yeniden Başlat"):
        restart_quiz()