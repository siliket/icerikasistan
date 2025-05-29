from pytrends.request import TrendReq
from streamlit.components.v1 import html
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import requests # requests kütüphanesini import ettiğinizden emin olun

# games.py dosyanızdan import edildiği varsayılır.
# Eğer bu dosyanız yoksa veya içeriğini değiştirdiyseniz,
# bu değişkenleri kodunuzun başında manuel olarak tanımlamanız gerekebilir.

GAME_COVERS = {
    # Aksiyon
    "Cyberpunk 2077": "https://cdn.cloudflare.steamstatic.com/steam/apps/1091500/header.jpg",
    "God of War: Ragnarök": "https://image.api.playstation.com/vulcan/ap/rnd/202207/1210/4xJ8XB3bi888QTLZYdl7Oi0s.png",
    "Devil May Cry 5": "https://cdn.cloudflare.steamstatic.com/steam/apps/601150/header.jpg",
    "Horizon Forbidden West": "https://image.api.playstation.com/vulcan/ap/rnd/202107/1612/5wLgspQ7kP4538ZXHKJqQd9K.png",

    # RPG
    "The Witcher 3: Wild Hunt": "https://cdn.cloudflare.steamstatic.com/steam/apps/292030/header.jpg",
    "Elden Ring": "https://image.api.playstation.com/vulcan/ap/rnd/202108/0410/4oBNK4UcD8sR7klc8JCT9iST.png",
    "Final Fantasy VII Remake": "https://image.api.playstation.com/vulcan/ap/rnd/202008/1020/T45iRN1bhiWcJUzST6UFGBvO.png",
    "Dragon Age: Inquisition": "https://cdn.cloudflare.steamstatic.com/steam/apps/1222690/header.jpg",

    # Strateji
    "Civilization VI": "https://cdn.cloudflare.steamstatic.com/steam/apps/289070/header.jpg",
    "XCOM 2": "https://cdn.cloudflare.steamstatic.com/steam/apps/268500/header.jpg",
    "Total War: Warhammer III": "https://cdn.cloudflare.steamstatic.com/steam/apps/1142710/header.jpg",
    "StarCraft II": "https://cdn.cloudflare.steamstatic.com/steam/apps/212160/header.jpg",

    # FPS
    "DOOM Eternal": "https://cdn.cloudflare.steamstatic.com/steam/apps/782330/header.jpg",
    "Overwatch 2": "https://cdn.cloudflare.steamstatic.com/steam/apps/2357570/header.jpg",
    "Call of Duty: Modern Warfare II": "https://cdn.cloudflare.steamstatic.com/steam/apps/1938090/header.jpg",

    # Macera
    "The Legend of Zelda: Tears of the Kingdom": "https://assets.nintendo.com/image/upload/ar_16:9,c_lpad,w_1240/b_white/f_auto/q_auto/ncom/software/switch/70010000063709/32b858e0948e48be9a84d70d35274c7ed7d0a1aacdc45d7d0b0d9e0cb9a3d340",
    "Red Dead Redemption 2": "https://cdn.cloudflare.steamstatic.com/steam/apps/1174180/header.jpg",
    "Uncharted 4: A Thief's End": "https://image.api.playstation.com/vulcan/ap/rnd/202201/0711/8vekWyQAjUIPhq5k8wB6Tj3s.png",

    # Survival Horror
    "Resident Evil 4 Remake": "https://cdn.cloudflare.steamstatic.com/steam/apps/2050650/header.jpg",
    "The Last of Us Part I": "https://image.api.playstation.com/vulcan/ap/rnd/202206/0720/eEczyEMDd2BLa3dtkGJVE9At.png",

    # Spor
    "FIFA 23": "https://cdn.cloudflare.steamstatic.com/steam/apps/1811260/header.jpg",
    "NBA 2K23": "https://cdn.cloudflare.steamstatic.com/steam/apps/1919590/header.jpg",

    # Simülasyon
    "Microsoft Flight Simulator": "https://cdn.cloudflare.steamstatic.com/steam/apps/1250410/header.jpg",
    "Cities: Skylines": "https://cdn.cloudflare.steamstatic.com/steam/apps/255710/header.jpg",

    # Battle Royale
    "Fortnite": "https://cdn2.unrealengine.com/egs-social-fortnite-1920x1080-1920x1080-87971829e331.png",
    "Apex Legends": "https://cdn.cloudflare.steamstatic.com/steam/apps/1172470/header.jpg",

    # MMO
    "Final Fantasy XIV": "https://cdn.cloudflare.steamstatic.com/steam/apps/39210/header.jpg",
    "World of Warcraft: Dragonflight": "https://assets-prd.ignimgs.com/2022/04/19/world-of-warcraft-dragonflight-button-01-1650389461383.jpg",

    # Platform
    "Hollow Knight": "https://cdn.cloudflare.steamstatic.com/steam/apps/367520/header.jpg",
    "Celeste": "https://cdn.cloudflare.steamstatic.com/steam/apps/504230/header.jpg",

    # Fighting
    "Street Fighter 6": "https://cdn.cloudflare.steamstatic.com/steam/apps/1364780/header.jpg",
    "Tekken 7": "https://cdn.cloudflare.steamstatic.com/steam/apps/389730/header.jpg"
}

game_database = {
    "Cyberpunk 2077": {
        "genre": "Aksiyon",
        "release": 2020,
        "metacritic": 75,
        "platforms": ["PC", "PS5", "Xbox Series X"]
    },
    "God of War: Ragnarök": {
        "genre": "Aksiyon",
        "release": 2022,
        "metacritic": 94,
        "platforms": ["PS4", "PS5"]
    },
    "Devil May Cry 5": {
        "genre": "Aksiyon",
        "release": 2019,
        "metacritic": 89,
        "platforms": ["PC", "PS4", "Xbox One"]
    },
    "Horizon Forbidden West": {
        "genre": "Aksiyon",
        "release": 2022,
        "metacritic": 88,
        "platforms": ["PS4", "PS5"]
    },
    "The Witcher 3: Wild Hunt": {
        "genre": "RPG",
        "release": 2015,
        "metacritic": 93,
        "platforms": ["PC", "PS4", "Xbox One", "Switch"]
    },
    "Elden Ring": {
        "genre": "RPG",
        "release": 2022,
        "metacritic": 96,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "Final Fantasy VII Remake": {
        "genre": "RPG",
        "release": 2020,
        "metacritic": 87,
        "platforms": ["PS4", "PS5"]
    },
    "Dragon Age: Inquisition": {
        "genre": "RPG",
        "release": 2014,
        "metacritic": 89,
        "platforms": ["PC", "PS3", "PS4", "Xbox 360", "Xbox One"]
    },
    "Civilization VI": {
        "genre": "Strateji",
        "release": 2016,
        "metacritic": 88,
        "platforms": ["PC", "PS4", "Xbox One", "Switch"]
    },
    "XCOM 2": {
        "genre": "Strateji",
        "release": 2016,
        "metacritic": 88,
        "platforms": ["PC", "PS4", "Xbox One"]
    },
    "Total War: Warhammer III": {
        "genre": "Strateji",
        "release": 2022,
        "metacritic": 86,
        "platforms": ["PC"]
    },
    "StarCraft II": {
        "genre": "Strateji",
        "release": 2010,
        "metacritic": 92,
        "platforms": ["PC"]
    },
    "DOOM Eternal": {
        "genre": "FPS",
        "release": 2020,
        "metacritic": 88,
        "platforms": ["PC", "PS4", "Xbox One", "Switch"]
    },
    "Overwatch 2": {
        "genre": "FPS",
        "release": 2022,
        "metacritic": 81,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "Call of Duty: Modern Warfare II": {
        "genre": "FPS",
        "release": 2022,
        "metacritic": 79,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "The Legend of Zelda: Tears of the Kingdom": {
        "genre": "Macera",
        "release": 2023,
        "metacritic": 96,
        "platforms": ["Nintendo Switch"]
    },
    "Red Dead Redemption 2": {
        "genre": "Macera",
        "release": 2018,
        "metacritic": 97,
        "platforms": ["PC", "PS4", "Xbox One"]
    },
    "Uncharted 4: A Thief's End": {
        "genre": "Macera",
        "release": 2016,
        "metacritic": 93,
        "platforms": ["PS4"]
    },
    "Resident Evil 4 Remake": {
        "genre": "Survival Horror",
        "release": 2023,
        "metacritic": 93,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "The Last of Us Part I": {
        "genre": "Survival Horror",
        "release": 2022,
        "metacritic": 88,
        "platforms": ["PS5"]
    },
    "FIFA 23": {
        "genre": "Spor",
        "release": 2022,
        "metacritic": 76,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "NBA 2K23": {
        "genre": "Spor",
        "release": 2022,
        "metacritic": 79,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "Microsoft Flight Simulator": {
        "genre": "Simülasyon",
        "release": 2020,
        "metacritic": 90,
        "platforms": ["PC", "Xbox Series X"]
    },
    "Cities: Skylines": {
        "genre": "Simülasyon",
        "release": 2015,
        "metacritic": 85,
        "platforms": ["PC", "PS4", "Xbox One", "Switch"]
    },
    "Fortnite": {
        "genre": "Battle Royale",
        "release": 2017,
        "metacritic": 78,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X", "Switch"]
    },
    "Apex Legends": {
        "genre": "Battle Royale",
        "release": 2019,
        "metacritic": 89,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "Final Fantasy XIV": {
        "genre": "MMO",
        "release": 2013,
        "metacritic": 86,
        "platforms": ["PC", "PS4", "PS5"]
    },
    "World of Warcraft: Dragonflight": {
        "genre": "MMO",
        "release": 2022,
        "metacritic": 83,
        "platforms": ["PC"]
    },
    "Hollow Knight": {
        "genre": "Platform",
        "release": 2017,
        "metacritic": 90,
        "platforms": ["PC", "PS4", "Xbox One", "Switch"]
    },
    "Celeste": {
        "genre": "Platform",
        "release": 2018,
        "metacritic": 94,
        "platforms": ["PC", "PS4", "Xbox One", "Switch"]
    },
    "Street Fighter 6": {
        "genre": "Fighting",
        "release": 2023,
        "metacritic": 92,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "Tekken 7": {
        "genre": "Fighting",
        "release": 2015,
        "metacritic": 82,
        "platforms": ["PC", "PS4", "Xbox One"]
    }
}


pytrends = TrendReq(hl='tr-TR', tz=360) # Türkçe ve UTC+3 için
RAWG_API_KEY = "a04a54d4a1384a64b182fc19616f00c4"
BASE_URL = "https://api.rawg.io/api/games"

# ----------------------
# TEMEL AYARLAR
# ----------------------
st.set_page_config(
    page_title="Game Advisor Pro",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=3600)  # 1 saat önbellekleme
def get_optimized_image(url):
    return f"https://images.weserv.nl/?url={url}&w=400&h=225&fit=cover"

# ----------------------
# ORTAK FONKSİYONLAR
# ----------------------

def get_game_popularity(game_name):
    """Oyun popülerlik verilerini RAWG API'den çek"""
    params = {
        "key": RAWG_API_KEY,
        "search": game_name,
        "page_size": 1
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data["count"] > 0:
            game_id = data["results"][0]["id"]
            # Detaylı istatistikler için ikinci bir istek
            details_url = f"{BASE_URL}/{game_id}"
            details_response = requests.get(details_url, params={"key": RAWG_API_KEY})
            details_response.raise_for_status() # Hata durumunda istisna fırlatır
            details = details_response.json()

            return {
                "rating": details.get("rating", 0),
                "playtime": details.get("playtime", "Bilinmiyor"),
                "metacritic": details.get("metacritic", 0),
                "reviews_count": details.get("reviews_count", 0)
            }
        return None
    except Exception as e:
        st.error(f"API Hatası: {str(e)}")
        return None

def show_game_details():
    # Seçilen oyunun session_state'te olup olmadığını ve boş olup olmadığını kontrol edin
    if "selected_game" not in st.session_state or st.session_state.selected_game is None or st.session_state.selected_game == "":
        st.info("Oyun detaylarını görmek için lütfen Ana Sayfa'dan bir oyun seçin veya tıklayın.")
        return # Fonksiyondan çık, çünkü seçilen oyun yok

    game_name = st.session_state.selected_game

    # Şimdi game_name'in game_database'de olup olmadığını kontrol edin
    if game_name not in game_database:
        st.warning(f"'{game_name}' oyunu veritabanımızda bulunamadı. Lütfen farklı bir oyun seçin.")
        return # Fonksiyondan çık

    # Artık game_name'in geçerli ve game_database'de olduğundan eminiz
    details = game_database.get(game_name, {}) # .get() kullanarak güvenli erişim

    with st.container():
        st.markdown('<div id="game-details"></div>', unsafe_allow_html=True)
        st.subheader(f"🎮 {game_name} Detayları")

        col1, col2 = st.columns([1, 2])
        with col1:
            # Resim URL'si kontrolü, eğer GAME_COVERS içinde yoksa varsayılan resim göster
            image_url = GAME_COVERS.get(game_name, "https://via.placeholder.com/400x225?text=Resim+Yok")
            st.image(image_url, use_container_width=True)
        with col2:
            st.markdown(f"""
            **Metacritic Puanı:** ⭐ {details.get('metacritic', 'N/A')}  
            **Çıkış Yılı:** 📅 {details.get('release', 'N/A')}  
            **Tür:** {details.get('genre', 'N/A')}  
            **Platformlar:** 🖥️ {', '.join(details.get('platforms', ['Multiplatform']))}
            """)

            # RAWG API'den gerçek verileri çek
            with st.spinner("Gerçek zamanlı veriler yükleniyor..."):
                try:
                    params = {"key": RAWG_API_KEY, "search": game_name}
                    response = requests.get("https://api.rawg.io/api/games", params=params)
                    response.raise_for_status() # Hata durumunda istisna fırlatır
                    data = response.json()

                    if data["count"] > 0:
                        game_id = data["results"][0]["id"]
                        details_response = requests.get(f"https://api.rawg.io/api/games/{game_id}", params={"key": RAWG_API_KEY})
                        details_response.raise_for_status()
                        details_data = details_response.json()

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Toplam Oy", details_data.get("reviews_count", "Bilinmiyor"))
                            st.metric("Ortalama Oynama Süresi", f"{details_data.get('playtime', 0)} saat")
                        with col2:
                            st.metric("Topluluk Puanı", f"{details_data.get('rating', 0):.2f}")
                            st.progress(details_data.get("rating", 0)/5) # Puanı 5 üzerinden ilerleme çubuğuna çevir
                    else:
                        st.info("RAWG API'sinde bu oyun için detaylı bilgi bulunamadı.")
                except requests.exceptions.RequestException as e:
                    st.error(f"RAWG API isteği hatası: {str(e)}")
                except Exception as e:
                    st.error(f"Beklenmedik API hatası: {str(e)}")

def save_feedback(data):
    df = pd.DataFrame([data])
    df.to_csv("feedback.csv", mode='a', header=False, index=False)

def load_feedback():
    try:
        return pd.read_csv("feedback.csv", names=["game", "rating", "comment", "timestamp"])
    except FileNotFoundError:
        return pd.DataFrame()

def show_game_card(game, details):
    

    try:
        optimized_img = f"https://images.weserv.nl/?url={GAME_COVERS.get(game, 'https://via.placeholder.com/400x225?text=Resim+Yok')}&w=400&h=225&fit=cover"
        # HTML ID'leri ve JS fonksiyon adları için güvenli hale getir
        # " ", ":", "'" gibi karakterleri kaldırarak güvenli bir ID oluştur
        card_id = "".join(filter(str.isalnum, game.replace(" ", "_").replace(":", "").replace("'", "")))

        # Tıklama JS kodu
        # Streamlit'in DOM'undaki gizli text input'u bulup değerini güncelleyeceğiz.
        # Bu, Streamlit'in değişiklik algılamasını tetikleyecektir.
        html(f"""
        <script>
            function handleClick('{card_id}')() {{
                // Ana penceredeki gizli st.text_input'u bul.
                // st.text_input'a verdiğimiz '__clicked_game_placeholder__' label'ı aria-label olarak kullanılır.
                const hiddenInput = window.parent.document.querySelector('input[aria-label="__clicked_game_placeholder__"]');
                if (hiddenInput) {{
                    hiddenInput.value = '{game}';
                    // Input değerinin değiştiğini Streamlit'e bildirmek için bir 'input' olayı tetikle.
                    // Streamlit bu olayı dinler ve bir değişiklik olduğunda yeniden çalışır.
                    const event = new Event('input', {{ bubbles: true }});
                    hiddenInput.dispatchEvent(event);

                    // Detaylar bölümüne kaydır
                    const detailsSection = window.parent.document.getElementById('details-section');
                    if (detailsSection) {{
                        detailsSection.scrollIntoView({{
                            behavior: 'smooth'
                        }});
                    }}
                }}
            }}
        </script>
        """, height=0) # Bu html bileşenini görünmez yapıyoruz.

        # Kart HTML
        st.markdown(f"""
        <div class="game-card" id="{card_id}">
            <div class="clickable-overlay" onclick="handleClick('{card_id}')()"></div>
            <img src="{optimized_img}" style="width:100%;height:180px;object-fit:cover;">
            <div style="padding:12px;">
                <h4 style="margin:0;color:#4a90e2;">{game}</h4>
                <div style="font-size:14px;color:#888;margin-top:8px;">
                    ⭐ {details.get('metacritic', 'N/A')} | 📅 {details.get('release', 'N/A')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Oyun kartı oluşturulurken hata: {str(e)}")
        # Hata durumunda alternatif bir kart göster
        st.markdown(f"""
        <div class="game-card">
            <img src="https://via.placeholder.com/400x225" class="game-image">
            <div class="game-info">
                <div class="game-title">{game}</div>
                <div class="game-details">⚠️ Resim veya detaylar yüklenemedi</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# handle_game_clicks fonksiyonu kaldırıldı, çünkü doğrudan Streamlit.setComponentValue yerine gizli input kullanılıyor.

# ----------------------
# CSS STİLLERİ 
# ----------------------
st.markdown("""
<style>
    
    .game-card {
        position: relative;
        border-radius: 10px;
        overflow: hidden;
        transition: transform 0.3s, box-shadow 0.3s;
        cursor: pointer;
        background: #1a1a1a;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .clickable-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 2; /* Kartın üzerindeki tıklanabilir alanı sağlar */
    }
    /* Diğer CSS'ler */
    .custom-header {
        color: #4a90e2; /* Mavi tonu */
        text-align: center;
        padding: 10px;
        margin-bottom: 20px;
        border-bottom: 2px solid #4a90e2;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.1rem;
        font-weight: bold;
    }
    .sidebar-card {
        background: #2a2a2a;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .badge {
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.75em;
        margin-left: 8px;
        background: #4a90e225;
        color: #4a90e2;
    }
    .live-dot {
        height: 10px;
        width: 10px;
        background-color: #ff4b4b;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 1; }
        70% { transform: scale(1.1); opacity: 0.7; }
        100% { transform: scale(0.95); opacity: 1; }
    }
    .stProgress > div > div > div > div {
        background-color: #4a90e2; /* İlerleme çubuğu rengi */
    }
</style>
""", unsafe_allow_html=True)

# ----------------------
# ANA UYGULAMA
# ----------------------
def main():
    st.markdown("<h1 class='custom-header'>Game Advisor Pro</h1>", unsafe_allow_html=True)
    selected_game = st.text_input("__clicked_game_placeholder__", key="selected_game", value="", label_visibility="collapsed")
    
    st.write("Seçilen oyun:", st.session_state.get("selected_game", "Henüz seçilmedi"))

    

    if "selected_game" not in st.session_state:
        st.session_state.selected_game = None
    
    if "__last_clicked_game_from_js__" not in st.session_state:
        st.session_state.__last_clicked_game_from_js__ = ""
      
    # Hata veren 'hidden_game_click_detector' key'ini dinamik hale getirerek çakışmayı önlüyoruz.
    # Bu, Streamlit'in her yeniden çalışma döngüsünde benzersiz bir key oluşturmasını sağlar.
    dynamic_key = f"hidden_game_click_detector_{datetime.now().timestamp()}" 

    
    
    if st.session_state.selected_game is not None and st.session_state.selected_game != "":
        st.markdown(f'<div id="details-section"></div>', unsafe_allow_html=True)
        show_game_details()

    st.subheader("🔍 Trend Karşılaştırması İçin Oyunları Seçin")
    user_input = st.text_input(
        "Karşılaştırılacak oyun isimlerini virgülle ayırarak girin:",
        placeholder="Örn: Cyberpunk 2077, Elden Ring, FIFA 23",
        key="game_input_1"

    )

    if user_input:
        kw_list = [x.strip() for x in user_input.split(",") if x.strip()]

        if len(kw_list) < 1:
            st.warning("Lütfen en az 1 oyun ismi girin!")
        else:
            try:
                with st.spinner(f"{', '.join(kw_list)} için trend verileri yükleniyor..."):
                    pytrends.build_payload(
                        kw_list=kw_list,
                        timeframe="today 3-m",
                        geo="TR"
                    )
                    trend_data = pytrends.interest_over_time()

                    df_clean = trend_data.drop(columns=["isPartial"]).reset_index()
                    df_long = df_clean.melt(
                        id_vars="date",
                        var_name="Oyun",
                        value_name="Popülerlik"
                    )

                    df_long["date"] = pd.to_datetime(df_long["date"])
                    df_long["Popülerlik"] = df_long["Popülerlik"].astype(int)

                    fig = px.line(
                        df_long,
                        x="date",
                        y="Popülerlik",
                        color="Oyun",
                        title=f"Google Trends Karşılaştırması",
                        labels={"date": "Tarih", "Popülerlik": "Trend Skoru"},
                        template="plotly_dark"
                    )
                    fig.update_layout(hovermode="x unified")

                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Trend verileri yüklenirken hata oluştu: {str(e)}")
                st.info("""
                Olası Nedenler:
                - Geçersiz oyun ismi (Google Trends'te bulunmuyor olabilir)
                - Google Trends API limiti aşımı
                - İnternet bağlantısı sorunu
                """)

    
    key=dynamic_key
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            search_query = st.text_input("🔍 Oyun Ara"), key == "game_input_2"
        with col2:
            selected_genre = st.selectbox("🎮 Tür Seçin", ["Tümü", "Aksiyon", "RPG", "Strateji"])
        with col3:
            min_score = st.slider("⭐ Minimum Puan", 0, 100, 75)

    tab1, tab2, tab3, tab4, = st.tabs([
    "🏠 Ana Sayfa", 
    "💬 Değerlendirmeler", 
    "📈 Trendler", 
    "📊 İstatistikler", 
     
])

    with tab1:
         search_text = search_query[0] if isinstance(search_query, tuple) else search_query

    filtered_games = [
        (game, details) for game, details in game_database.items()
    if search_text.lower() in game.lower() and
    (selected_genre == "Tümü" or details["genre"] == selected_genre) and
    (details["metacritic"] >= min_score)
    ]
    

    if not filtered_games:
        st.warning("🚨 Filtrelerinize uygun oyun bulunamadı!")
    else:
        cols = st.columns(3)
        for idx, (game, details) in enumerate(filtered_games):
            with cols[idx % 3]:
                show_game_card(game, details)


    with tab2:
        with st.form("feedback_form"):
            cols = st.columns([2, 1, 1])
            selected_game_feedback = cols[0].selectbox("Oyun Seçin", list(game_database.keys()))
            rating = cols[1].selectbox("Puan", options=["⭐"*i for i in range(1,6)])
            comment = cols[2].text_area("Yorum", height=100, placeholder="En az 20 karakter...")

            if st.form_submit_button("📤 Gönder"):
                if len(comment) >= 20:
                    save_feedback({
                        "game": selected_game_feedback,
                        "rating": len(rating),
                        "comment": comment,
                        "timestamp": datetime.now().strftime("%Y-%m-%d")
                    })
                    st.success("✅ Değerlendirme kaydedildi!")
                else:
                    st.error("❌ Lütfen en az 20 karakterlik yorum yazınız")

        feedback_df = load_feedback()
        if not feedback_df.empty:
            st.subheader("📜 Geçmiş Değerlendirmeler")
            for _, row in feedback_df.iterrows():
                with st.expander(f"{row['game']} - {'⭐' * row['rating']}", expanded=False):
                    st.markdown(f"**📅 Tarih:** {row['timestamp']} \n**💬 Yorum:** {row['comment']}")
        else:
            st.info("ℹ️ Henüz değerlendirme bulunmamaktadır")

    with tab3:
        st.subheader("🔍 Tekil Trend Analizi")
        keyword_single = st.text_input("Analiz Edilecek Oyun/Kategori Adı:", placeholder="Örn: League of Legends", key="single_trend_keyword")

        if st.button("Trendleri Getir", key="get_single_trend"):
            if keyword_single:
                with st.spinner("Trend verileri yükleniyor..."):
                    try:
                        pytrends.build_payload([keyword_single], timeframe='today 3-m', geo='TR')
                        trend_data = pytrends.interest_over_time()

                        if trend_data.empty or keyword_single not in trend_data.columns:
                            st.warning(f"'{keyword_single}' için trend verisi bulunamadı. Lütfen farklı bir anahtar kelime deneyin.")
                        else:
                            df_clean = trend_data.drop(columns=['isPartial']).reset_index()
                            df_long = df_clean.melt(
                                id_vars='date',
                                var_name='Oyun',
                                value_name='Popülerlik'
                            )

                            fig = px.line(
                                df_long,
                                x='date',
                                y='Popülerlik',
                                color='Oyun',
                                title=f"'{keyword_single}' Popülerlik Trendleri",
                                labels={'date': 'Tarih', 'Popülerlik': 'Google Trends Skoru'},
                                template='plotly_dark'
                            )
                            fig.update_layout(hovermode="x unified")
                            st.plotly_chart(fig, use_container_width=True)

                    except Exception as e:
                        st.error(f"Hata oluştu: {str(e)}")
                        st.info("Lütfen geçerli bir anahtar kelime girin.")
            else:
                st.warning("Lütfen bir anahtar kelime girin.")

        st.subheader("🏷️ Çoklu Trend Karşılaştırma")
        comparison_keywords = st.text_input("Karşılaştırılacak anahtar kelimeleri virgülle ayırın (en fazla 5):", key="multi_trend_keywords")
        if st.button("Karşılaştır", key="compare_trends"):
            keywords = [kw.strip() for kw in comparison_keywords.split(",") if kw.strip()]
            if len(keywords) > 5:
                st.warning("En fazla 5 anahtar kelime karşılaştırabilirsiniz.")
            elif len(keywords) < 2:
                st.warning("Karşılaştırmak için en az 2 anahtar kelime girin.")
            else:
                with st.spinner(f"{', '.join(keywords)} karşılaştırılıyor..."):
                    try:
                        pytrends.build_payload(keywords, timeframe='today 3-m', geo='TR')
                        trend_data = pytrends.interest_over_time()

                        if trend_data.empty:
                            st.warning("Seçilen anahtar kelimeler için trend verisi bulunamadı.")
                        else:
                            df_clean = trend_data.drop(columns=["isPartial"]).reset_index()
                            df_long = df_clean.melt(
                                id_vars="date",
                                var_name="Anahtar Kelime",
                                value_name="Popülerlik"
                            )

                            fig = px.line(
                                df_long,
                                x="date",
                                y="Popülerlik",
                                color="Anahtar Kelime",
                                title=f"{', '.join(keywords)} Trend Karşılaştırması",
                                labels={'date': 'Tarih', 'Popülerlik': 'Google Trends Skoru'},
                                template="plotly_dark"
                            )
                            fig.update_layout(hovermode="x unified")
                            st.plotly_chart(fig, use_container_width=True)

                    except Exception as e:
                        st.error(f"Hata: {str(e)}")
                        st.info("Trend verilerini getirirken bir sorun oluştu. Anahtar kelimelerinizi kontrol edin.")


    with tab4:
        feedback_df = load_feedback()
        if not feedback_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(
                    feedback_df,
                    names='game',
                    title='🎮 Oyunlara Göre Yorum Dağılımı',
                    color_discrete_sequence=px.colors.sequential.Blues_r
                )
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.histogram(
                    feedback_df,
                    x='rating',
                    title='⭐ Puan Dağılımı',
                    nbins=5,
                    color_discrete_sequence=['#8B00FF']
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ Henüz yeterli değerlendirme verisi bulunmamaktadır.")   
with st.sidebar:
    st.markdown("""
    <style>
        .badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.75em;
            margin-left: 8px;
        }
        .live-dot {
            height: 10px;
            width: 10px;
            background-color: #ff4b4b;
            border-radius: 50%;
            display: inline-block;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); }
            70% { transform: scale(1.1); }
            100% { transform: scale(0.95); }
        }
        .sidebar-card {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)

        col1, col2 = st.columns([1,3])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/686/686589.png", width=50)
        with col2:
            st.markdown(f"""
            <div style="line-height:1.2">
                <h4 style="margin:0;color:#4a90e2">Merhaba, Oyuncu!</h4>
                <div style="font-size:0.8em;color:#888">
                    Seviye: <strong>28</strong>
                    <span class="badge" style="background:#4a90e225;color:#4a90e2">+3 Yeni Rozet</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.progress(0.65, text="Seviye İlerlemesi (%65)")

        st.markdown("""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin: 12px 0;">
            <div style="text-align:center">
                <div style="font-size:1.2em">🎮 142</div>
                <div style="font-size:0.7em;color:#888">Oynanan</div>
            </div>
            <div style="text-align:center">
                <div style="font-size:1.2em">⭐ 4.8</div>
                <div style="font-size:0.7em;color:#888">Ortalama</div>
            </div>
            <div style="text-align:center">
                <div style="font-size:1.2em">🏆 23</div>
                <div style="font-size:0.7em;color:#888">Başarı</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### 🔥 Canlı Etkinlikler")

        st.markdown(f"""
        <div style="margin: 8px 0; padding: 8px; border-left: 3px solid #4a90e2; background: #4a90e210">
            <div style="display:flex; justify-content:space-between">
                <div>
                    <span class="live-dot"></span>
                    <strong style="color:#4a90e2">FPS Challenge</strong>
                </div>
                <span style="font-size:0.8em;color:#888">3h left</span>
            </div>
            <div style="font-size:0.8em">
                🎯 5.4K katılımcı | 🏆 $2K ödül
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin: 8px 0; padding: 8px; border-left: 3px solid #ff4b4b; background: #ff4b4b10">
            <div style="display:flex; justify-content:space-between">
                <div>
                    <span class="live-dot"></span>
                    <strong style="color:#ff4b4b">Cosplay Yarışması</strong>
                </div>
                <span style="font-size:0.8em;color:#888">2gün kaldı</span>
            </div>
            <div style="font-size:0.8em">
                🎭 1.2K katılımcı | 📸 En iyi 10'a oy ver
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### 🎯 Size Özel Öneriler")

        st.markdown(f"""
        <div style="display:flex; align-items:center; margin:8px 0; padding:8px; background:#2a2a2a; border-radius:8px">
            <img src="{get_optimized_image(GAME_COVERS['Cyberpunk 2077'])}" width="40" style="border-radius:4px">
            <div style="margin-left:12px">
                <div style="font-size:0.9em"><strong>Cyberpunk 2077</strong></div>
                <div style="font-size:0.7em;color:#888">⏳ Son oynama: 2 gün önce</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex; align-items:center; margin:8px 0; padding:8px; background:#2a2a2a; border-radius:8px">
            <img src="{get_optimized_image(GAME_COVERS['The Witcher 3: Wild Hunt'])}" width="40" style="border-radius:4px">
            <div style="margin-left:12px">
                <div style="font-size:0.9em"><strong>The Witcher 3</strong></div>
                <div style="font-size:0.7em;color:#888">🎮 85% uyumluluk</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### 🌐 Topluluğa Katılın")

        social_cols = st.columns(4)
        social_platforms = [
            ("Discord", "https://cdn-icons-png.flaticon.com/512/9062/9062704.png", "#5865F2", "https://discord.gg/your-community-link"),
            ("Reddit", "https://cdn-icons-png.flaticon.com/512/3670/3670157.png", "#FF4500", "https://www.reddit.com/r/your-subreddit"),
            ("Twitter", "https://cdn-icons-png.flaticon.com/512/733/733579.png", "#1DA1F2", "https://twitter.com/your-handle"),
            ("YouTube", "https://cdn-icons-png.flaticon.com/512/1384/1384060.png", "#FF0000", "https://www.youtube.com")
        ]

        for (name, icon, color, url), col in zip(social_platforms, social_cols):
            with col:
                st.markdown(f"""
                <a href="{url}"
                   target="_blank"
                   rel="noopener noreferrer"
                   style="display:block;text-align:center">
                    <img src="{icon}"
                         width="24"
                         style="filter: drop-shadow(0 2px 4px {color}40)"
                         title="{name}">
                </a>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------
# YAN PANEL (GELİŞMİŞ)
# ----------------------
with st.sidebar:
    st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Kişiselleştirilmiş Öneriler")
    
    # Basit öneri algoritması
    liked_game = st.selectbox("⭐ Beğendiğiniz bir oyun seçin", 
                            list(game_database.keys()))
    
    if st.button("Benzer Oyunları Göster"):
        target_genre = game_database[liked_game]["genre"]
        target_score = game_database[liked_game]["metacritic"]
        
        recommendations = [
            (game, details) for game, details in game_database.items()
            if details["genre"] == target_genre 
            and abs(details["metacritic"] - target_score) <= 10
            and game != liked_game
        ][:3]
        
        if recommendations:
            for game, details in recommendations:
                st.markdown(f"""
                <div style="padding:10px; margin:5px 0; background:#2a2a2a; border-radius:8px">
                    <div style="font-size:0.9em">🎮 {game}</div>
                    <div style="font-size:0.8em;color:#888">
                        ⭐ {details['metacritic']} | 📅 {details['release']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Benzer oyun bulunamadı")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""
    <style>
        .badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.75em;
            margin-left: 8px;
        }
        .live-dot {
            height: 10px;
            width: 10px;
            background-color: #ff4b4b;
            border-radius: 50%;
            display: inline-block;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); }
            70% { transform: scale(1.1); }
            100% { transform: scale(0.95); }
        }
        .sidebar-card {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main();