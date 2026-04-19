import streamlit as st
import random

# --- SAYFA KONFİGÜRASYONU ---
st.set_page_config(page_title="GMDSS Sınav Portalı", page_icon="⚓", layout="centered")

# --- CUSTOM CSS (MODERN & ŞIK TASARIM) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f9; }
    .stButton>button {
        width: 150%;
        border-radius: 12px;
        border: 1px solid #1e3a8a;
        background-color: white;
        color: #1e3a8a;
        font-weight: 600;
        padding: 15px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1e3a8a;
        color: white;
        transform: translateY(-2px);
    }
    .logo-container { text-align: center; padding: 20px; }
    .SERKAN HOCA { font-size: 36px; font-weight: 800; color: #1e3a8a; margin-bottom: 0px; }
    .sub-title { font-size: 18px; color: #64748b; margin-top: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- TÜM 40 SORULUK VERİ SETİ ---
# Şartname: Açıklamalar çıkarıldı, doğru cevaplar kodlandı.
ALL_QUESTIONS = [
    {"q": "1. SÜZEN sözcüğü, uluslararası heceleme (fonetik) alfabesi ile nasıl kodlanır?", "a": "C", "options": ["Sette Ultra ZuluEndoNovember", "South Ultra ZouluoEleven North", "Sierra UniformZuluEchoNovember", "Sierra UniformZuluEndoNove", "Sette UniformZouluoEicoNovember"]},
    {"q": "2. ETAT ücretli servis işaretinin anlamı nedir?", "a": "D", "options": ["Servis telgrafı", "Postrestant telgraf", "Denizcilikle ilgili telgraf", "Devlet telgrafı", "Acele telgraf"]},
    {"q": "3. Nomanklatürlerde geçen 'CO' kısaltmasının anlamı nedir?", "a": "C", "options": ["Anten ayarı", "Kıyı uydu yer istasyonu", "Yalnız resmi bir kuruluşun haberleşmesini yapan istasyon", "Tarihinde iptal edildi", "Uzay istasyonu"]},
    {"q": "4. Emisyon sembolünde ilk karakterin 'B' olması neyi tanımlar?", "a": "B", "options": ["Tek yan band bastırılmış taşıyıcı", "İki bağımsız yan band", "Faz modülasyonlu tek yan band", "Çift yan band", "Tek yan band azaltılmış taşıyıcı"]},
    {"q": "5. Deniz VHF bandında öncelikle seyir güvenliği amacıyla kullanılan kanal hangisidir?", "a": "B", "options": ["Kanal 06", "Kanal 13", "Kanal 16", "Kanal 70", "Kanal 08"]},
    {"q": "6. Gemide telsiz jurnalleri ne kadar süre saklanmalıdır?", "a": "C", "options": ["6 ay", "1 yıl", "2 yıl", "5 yıl", "Süresiz"]},
    {"q": "7. 156.800 MHz frekansı hangi bandın içindedir?", "a": "D", "options": ["MF", "HF", "UHF", "VHF", "SHF"]},
    {"q": "8. Mevcut Cospas-Sarsat sisteminin bir sonraki nesli hangisidir?", "a": "E", "options": ["SZNSAR", "GENSAR", "OTSSAR", "AISSAR", "MEOSAR"]},
    {"q": "9. AIS 1 kanalının frekansı nedir?", "a": "B", "options": ["156.825 MHz", "161.975 MHz", "162.025 MHz", "156.525 MHz", "156.300 MHz"]},
    {"q": "10. Tıbbi yardım talebi mesajları hangi öncelik derecesiyle gönderilir?", "a": "B", "options": ["Distress", "Urgency", "Safety", "Routine", "Security"]},
    {"q": "11. VHF Kanal 70 hangi amaçla kullanılır?", "a": "C", "options": ["Sesli tehlike çağrısı", "Liman kontrol", "Dijital Seçmeli Çağrı (DSC)", "Meteoroloji", "Gemi içi haberleşme"]},
    {"q": "12. Navtex cihazı hangi frekanstan uluslararası (İngilizce) yayınları alır?", "a": "B", "options": ["490 kHz", "518 kHz", "2182 kHz", "4209.5 kHz", "156.8 MHz"]},
    {"q": "13. GMDSS sisteminde A3 deniz bölgesi neyi tanımlar?", "a": "C", "options": ["Sadece VHF sahası", "Sadece MF sahası", "Inmarsat uydularının kapsama alanı", "Kutup bölgeleri", "Liman sahaları"]},
    {"q": "14. EPIRB cihazının hidrostatik kilidi (HRU) değişim periyodu genellikle nedir?", "a": "B", "options": ["Her yıl", "2 yıl", "4 veya 5 yıl", "10 yıl", "Hiçbiri"]},
    {"q": "15. SART cihazı radar ekranında nasıl görünür?", "a": "C", "options": ["Büyük bir daire", "Yanıp sönen ışık", "12 adet nokta veya yay", "Gemi adı", "Düz çizgi"]},
    {"q": "16. 'MAYDAY RELAY' ifadesi hangi durumda kullanılır?", "a": "B", "options": ["Kendi gemimiz tehlikedeyken", "Başka bir geminin tehlike çağrısını aktarırken", "Hava raporu verirken", "Test yaparken", "Liman girişi istenirken"]},
    {"q": "17. GOC belgelerinin geçerlilik süresi nedir?", "a": "C", "options": ["Ömür boyu", "1 yıl", "5 yıl", "10 yıl", "2 yıl"]},
    {"q": "18. DSC üzerinden yapılan bir tehlike çağrısında hangisi bulunmaz?", "a": "D", "options": ["MMSI numarası", "Tehlikenin cinsi", "Mevki (Koordinat)", "Bir sonraki liman", "Haberleşme tipi"]},
    {"q": "19. VHF sesli görüşme (telsiz telefon) emisyonu hangisidir?", "a": "C", "options": ["J3E", "F1B", "F3E (veya G3E)", "A1A", "J2B"]},
    {"q": "20. Inmarsat-C tehlike butonu kaç saniye basılı tutulmalıdır?", "a": "C", "options": ["1 saniye", "Hemen bırakılır", "Yaklaşık 5 saniye", "30 saniye", "Basılmaz"]},
    {"q": "21. Bir geminin MMSI numarası kaç hanelidir?", "a": "C", "options": ["3", "6", "9", "12", "15"]},
    {"q": "22. Inmarsat-C üzerinden MSI yayınlarını almaya ne ad verilir?", "a": "B", "options": ["Navtex", "SafetyNet", "RadioTelex", "DSC", "GMDSS"]},
    {"q": "23. Telsiz operatörünün sessizlik periyotlarını takip etmesi gereken frekans hangisidir?", "a": "B", "options": ["156.8 MHz", "2182 kHz", "518 kHz", "406 MHz", "1.6 GHz"]},
    {"q": "24. Navtex mesajlarındaki 'B1' karakteri neyi temsil eder?", "a": "B", "options": ["Mesajın konusunu", "Yayın yapan istasyonu", "Mesaj numarasını", "Tarihi", "Geminin adını"]},
    {"q": "25. A2 deniz bölgesi hangi cihazın kapsama alanıdır?", "a": "B", "options": ["VHF", "MF", "HF", "Inmarsat", "Iridium"]},
    {"q": "26. J3E emisyonu neyi ifade eder?", "a": "B", "options": ["Telgraf", "Genlik Modülasyonlu Ses (SSB)", "Dijital Veri", "Faks", "Radar"]},
    {"q": "27. EPIRB cihazı hangi frekansta uydulara sinyal gönderir?", "a": "C", "options": ["156.8 MHz", "121.5 MHz", "406 MHz", "518 kHz", "9 GHz"]},
    {"q": "28. SART cihazı hangi frekans bandında çalışır?", "a": "C", "options": ["VHF", "MF", "9 GHz (X-Band Radar)", "3 GHz (S-Band Radar)", "HF"]},
    {"q": "29. GMDSS sisteminde 'Tehlike' (Distress) mesajının en belirgin özelliği nedir?", "a": "B", "options": ["Herkesin cevap vermesi zorunludur", "Önceliği en yüksektir ve tüm trafik durdurulur", "Sadece ücretli mesajlarda kullanılır", "Sadece gündüzleri çekilir", "Sadece Inmarsat üzerinden yapılır"]},
    {"q": "30. Gemiler arası tehlike trafiğinde Kanal 16 üzerinden konuşulurken sessizliği sağlamak için hangi terim kullanılır?", "a": "B", "options": ["Silence Fini", "Seelonce Mayday", "Stop Talking", "PanPan", "Securite"]},
    {"q": "31. MF DSC tehlike frekansı hangisidir?", "a": "B", "options": ["2182 kHz", "2187.5 kHz", "518 kHz", "8414.5 kHz", "156.525 MHz"]},
    {"q": "32. Bir DSC çağrısında 'Safety' (Emniyet) önceliği hangi anonsla başlar?", "a": "C", "options": ["Mayday", "PanPan", "Securite", "Urgent", "Warning"]},
    {"q": "33. Inmarsat-C terminalinde mesajın ulaştığını gösteren onay mesajına ne denir?", "a": "B", "options": ["Delivery Notification", "ACK (Acknowledgement)", "Echo", "Receipt", "Done"]},
    {"q": "34. Telsiz jurnaline hangi bilgiler yazılmaz?", "a": "D", "options": ["Günlük testler", "Alınan tehlike mesajları", "Akü voltaj değerleri", "Personelin yemek saati", "Operatör değişimleri"]},
    {"q": "35. Navtex yayın menzili yaklaşık ne kadardır?", "a": "B", "options": ["50 mil", "250-400 mil", "1000 mil", "Küresel", "10 mil"]},
    {"q": "36. DSC çağrısında 'Urgency' önceliği ne için kullanılır?", "a": "B", "options": ["Gemi batıyorsa", "Bir kişi denize düştüyse veya tıbbi aciliyet varsa", "Fener sönükse", "Gemide boya yapılıyorsa", "Selamlaşma için"]},
    {"q": "37. VHF telsiz cihazının azami çıkış gücü ne kadardır?", "a": "C", "options": ["1 Watt", "5 Watt", "25 Watt", "100 Watt", "1.5 kW"]},
    {"q": "38. 'VHF CH 16' frekansı nedir?", "a": "C", "options": ["156.300 MHz", "156.525 MHz", "156.800 MHz", "156.650 MHz", "161.975 MHz"]},
    {"q": "39. Bir EPIRB cihazı suyun kaç metre altında otomatik olarak serbest kalır?", "a": "B", "options": ["1 metre", "1.5 - 4 metre", "10 metre", "20 metre", "Serbest kalmaz"]},
    {"q": "40. Telsiz operatörü DSC test çağrısını kime yapar?", "a": "B", "options": ["Herhangi bir gemiye", "Sahil istasyonuna (RCC)", "Kendi gemisine", "Tanıdık bir tekneye", "Test çağrısı yapılmaz"]}
]

# --- SESSION STATE YÖNETİMİ ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = random.sample(ALL_QUESTIONS, len(ALL_QUESTIONS))
    st.session_state.current_idx = 0
    st.session_state.user_answers = []
    st.session_state.is_finished = False

# --- UI ELEMENTLERİ ---
st.markdown('<div class="logo-container"><p class="serkan-hoca">SERKAN HOCA İLE</p><p class="sub-title">GMDSS SORU BANKASI (40 SORU TAM LİSTE)</p></div>', unsafe_allow_html=True)

def restart():
    st.session_state.quiz_data = random.sample(ALL_QUESTIONS, len(ALL_QUESTIONS))
    st.session_state.current_idx = 0
    st.session_state.user_answers = []
    st.session_state.is_finished = False
    st.rerun()

if not st.session_state.is_finished:
    # İlerleme Bilgisi
    progress = (st.session_state.current_idx + 1) / len(ALL_QUESTIONS)
    st.progress(progress)
    st.write(f"Soru: {st.session_state.current_idx + 1} / {len(ALL_QUESTIONS)}")
    
    curr_q = st.session_state.quiz_data[st.session_state.current_idx]
    st.info(curr_q["q"])
    
    # Şıklar
    for i, option in enumerate(curr_q["options"]):
        letter = chr(65 + i)
        if st.button(f"{letter}) {option}", key=f"q_{st.session_state.current_idx}_{i}"):
            st.session_state.user_answers.append({
                "question": curr_q["q"],
                "user_choice": letter,
                "correct_choice": curr_q["a"],
                "options": curr_q["options"]
            })
            if st.session_state.current_idx + 1 < len(ALL_QUESTIONS):
                st.session_state.current_idx += 1
                st.rerun()
            else:
                st.session_state.is_finished = True
                st.rerun()
                
    st.divider()
    c1, c2 = st.columns(2)
    if c1.button("❌ Sınavı Kapat / Sıfırla"):
        restart()
    if c2.button("💾 Kaldığım Yerden Devam"):
        st.toast("İlerlemeniz kaydedildi. Pencereyi kapatmadığınız sürece devam edebilirsiniz.")

else:
    # --- ANALİZ EKRANI ---
    corrects = sum(1 for x in st.session_state.user_answers if x["user_choice"] == x["correct_choice"])
    score = (corrects / len(ALL_QUESTIONS)) * 100
    
    if score >= 80:
        st.balloons()
        st.success("# TEBRİKLER HARİKASIN! 🚀")
    
    st.metric("Başarı Yüzdesi", f"%{score:.1f}")
    st.write(f"Toplam {len(ALL_QUESTIONS)} soruda {corrects} doğru cevap verdiniz.")
    
    st.subheader("Hatalı Soruların Analizi")
    for idx, item in enumerate(st.session_state.user_answers):
        if item["user_choice"] != item["correct_choice"]:
            with st.expander(f"Soru {idx+1} (Yanlış)"):
                st.write(f"**Soru:** {item['question']}")
                st.error(f"Senin Cevabın: {item['user_choice']}")
                st.success(f"Doğru Cevap: {item['correct_choice']}")
                
    if st.button("Sınava Baştan Başla"):
        restart()
