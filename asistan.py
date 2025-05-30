from pytrends.request import TrendReq
import pandas as pd
import streamlit as st
import plotly.express as px
import time
from datetime import datetime
import calendar
import requests
import sqlite3
import hashlib
import secrets

# Oyun veritabanı ve kapak resimleri
GAME_COVERS = {
    # Aksiyon
    "Cyberpunk 2077": "https://cdn.akamai.steamstatic.com/steam/apps/1091500/header.jpg",
    "God of War: Ragnarök": "https://image.api.playstation.com/vulcan/ap/rnd/202207/1210/4xJ8XB3bi888QTLZYdl7Oi0s.png",
    "Devil May Cry 5": "https://cdn.akamai.steamstatic.com/steam/apps/601150/header.jpg",
    "Horizon Forbidden West": "https://image.api.playstation.com/vulcan/ap/rnd/202107/3100/yIa8STLMmCyhj48fGDpaAuRM.jpg",

    # RPG
    "The Witcher 3: Wild Hunt": "https://cdn.akamai.steamstatic.com/steam/apps/292030/header.jpg",
    "Elden Ring": "https://image.api.playstation.com/vulcan/ap/rnd/202108/0410/4oBNK4UcD8sR7klc8JCT9iST.png",
    "Final Fantasy VII Remake": "https://image.api.playstation.com/vulcan/ap/rnd/202008/1020/T45iRN1bhiWcJUzST6UFGBvO.png",
    "Dragon Age: Inquisition": "https://cdn.akamai.steamstatic.com/steam/apps/1222690/header.jpg",

    # Strateji
    "Civilization VI": "https://cdn.akamai.steamstatic.com/steam/apps/289070/header.jpg",
    "XCOM 2": "https://cdn.akamai.steamstatic.com/steam/apps/268500/header.jpg",
    "Total War: Warhammer III": "https://cdn.akamai.steamstatic.com/steam/apps/1142710/header.jpg",
    "StarCraft II": "https://cdn.akamai.steamstatic.com/steam/apps/212160/header.jpg",

    # FPS
    "DOOM Eternal": "https://cdn.akamai.steamstatic.com/steam/apps/782330/header.jpg",
    "Overwatch 2": "https://cdn.akamai.steamstatic.com/steam/apps/2357570/header.jpg",
    "Call of Duty: Modern Warfare II": "https://cdn.akamai.steamstatic.com/steam/apps/1938090/header.jpg",

    # Macera
    "The Legend of Zelda: Tears of the Kingdom": "https://assets.nintendo.com/image/upload/ar_16:9,c_lpad,w_1240/b_white/f_auto/q_auto/ncom/software/switch/70010000063709/32b858e0948e48be9a84d70d35274c7ed7d0a1aacdc45d7d0b0d9e0cb9a3d340",
    "Red Dead Redemption 2": "https://cdn.akamai.steamstatic.com/steam/apps/1174180/header.jpg",
    "Uncharted 4: A Thief's End": "https://image.api.playstation.com/vulcan/ap/rnd/202201/0711/8vekWyQAjUIPhq5k8wB6Tj3s.png",

    # Survival Horror
    "Resident Evil 4 Remake": "https://cdn.akamai.steamstatic.com/steam/apps/2050650/header.jpg",
    "The Last of Us Part I": "https://image.api.playstation.com/vulcan/ap/rnd/202206/0720/eEczyEMDd2BLa3dtkGJVE9At.png",

    # Spor
    "FIFA 23": "https://cdn.akamai.steamstatic.com/steam/apps/1811260/header.jpg",
    "NBA 2K23": "https://cdn.akamai.steamstatic.com/steam/apps/1919590/header.jpg",

    # Simülasyon
    "Microsoft Flight Simulator": "https://cdn.akamai.steamstatic.com/steam/apps/1250410/header.jpg",
    "Cities: Skylines": "https://cdn.akamai.steamstatic.com/steam/apps/255710/header.jpg",

    # Battle Royale
    "Fortnite": "https://cdn2.unrealengine.com/egs-social-fortnite-1920x1080-1920x1080-87971829e331.png",
    "Apex Legends": "https://cdn.akamai.steamstatic.com/steam/apps/1172470/header.jpg",

    # MMO
    "Final Fantasy XIV": "https://cdn.akamai.steamstatic.com/steam/apps/39210/header.jpg",
    "World of Warcraft: Dragonflight": "https://bnetcmsus-a.akamaihd.net/cms/blog_header/dh/DH6B2UZ8HZGH1671044479341.jpg",

    # Platform
    "Hollow Knight": "https://cdn.akamai.steamstatic.com/steam/apps/367520/header.jpg",
    "Celeste": "https://cdn.akamai.steamstatic.com/steam/apps/504230/header.jpg",

    # Fighting
    "Street Fighter 6": "https://cdn.akamai.steamstatic.com/steam/apps/1364780/header.jpg",
    "Tekken 7": "https://cdn.akamai.steamstatic.com/steam/apps/389730/header.jpg",
    
    # Ek oyunlar
    "Grand Theft Auto V": "https://cdn.akamai.steamstatic.com/steam/apps/271590/header.jpg",
    "Minecraft": "https://cdn.akamai.steamstatic.com/steam/apps/322330/header.jpg",
    "League of Legends": "https://cdn.akamai.steamstatic.com/steam/apps/41700/header.jpg",
    "Valorant": "https://cdn.akamai.steamstatic.com/steam/apps/1276810/header.jpg",
    "Counter-Strike: Global Offensive": "https://cdn.akamai.steamstatic.com/steam/apps/730/header.jpg",
    "Among Us": "https://cdn.akamai.steamstatic.com/steam/apps/945360/header.jpg",
    "Animal Crossing: New Horizons": "https://assets.nintendo.com/image/upload/ar_16:9,c_lpad,w_1240/b_white/f_auto/q_auto/ncom/software/switch/70010000027669/3319e2c1cae6d3e80d88a5da0b482d7f6c7a97cacf5b200a1c0a6a5b0d3ad956",
    "Assassin's Creed Valhalla": "https://cdn.akamai.steamstatic.com/steam/apps/2208920/header.jpg",
    "Battlefield 2042": "https://cdn.akamai.steamstatic.com/steam/apps/1517290/header.jpg",
    "Halo Infinite": "https://cdn.akamai.steamstatic.com/steam/apps/1240440/header.jpg",
    "Genshin Impact": "https://cdn.akamai.steamstatic.com/steam/apps/1683310/header.jpg",
    "Roblox": "https://cdn.akamai.steamstatic.com/steam/apps/2670960/header.jpg",
    "Rocket League": "https://cdn.akamai.steamstatic.com/steam/apps/252950/header.jpg",
    "Destiny 2": "https://cdn.akamai.steamstatic.com/steam/apps/1085660/header.jpg",
    "Warframe": "https://cdn.akamai.steamstatic.com/steam/apps/230410/header.jpg",
    "GTA Online": "https://cdn.akamai.steamstatic.com/steam/apps/271590/header.jpg",
    "Rainbow Six Siege": "https://cdn.akamai.steamstatic.com/steam/apps/359550/header.jpg",
    "Dead by Daylight": "https://cdn.akamai.steamstatic.com/steam/apps/381210/header.jpg",
    "Sea of Thieves": "https://cdn.akamai.steamstatic.com/steam/apps/1172620/header.jpg",
    "Fall Guys": "https://cdn.akamai.steamstatic.com/steam/apps/1097150/header.jpg"
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
    },
    "Grand Theft Auto V": {
        "genre": "Aksiyon",
        "release": 2013,
        "metacritic": 96,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "Minecraft": {
        "genre": "Sandbox",
        "release": 2011,
        "metacritic": 93,
        "platforms": ["PC", "PS4", "Xbox One", "Switch", "Mobile"]
    },
    "League of Legends": {
        "genre": "MOBA",
        "release": 2009,
        "metacritic": 78,
        "platforms": ["PC"]
    },
    "Valorant": {
        "genre": "FPS",
        "release": 2020,
        "metacritic": 80,
        "platforms": ["PC"]
    },
    "Counter-Strike: Global Offensive": {
        "genre": "FPS",
        "release": 2012,
        "metacritic": 83,
        "platforms": ["PC"]
    },
    "Among Us": {
        "genre": "Sosyal Dedüksiyon",
        "release": 2018,
        "metacritic": 85,
        "platforms": ["PC", "Mobile", "Switch"]
    },
    "Animal Crossing: New Horizons": {
        "genre": "Simülasyon",
        "release": 2020,
        "metacritic": 90,
        "platforms": ["Nintendo Switch"]
    },
    "Assassin's Creed Valhalla": {
        "genre": "Aksiyon-Macera",
        "release": 2020,
        "metacritic": 84,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "Battlefield 2042": {
        "genre": "FPS",
        "release": 2021,
        "metacritic": 68,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "Halo Infinite": {
        "genre": "FPS",
        "release": 2021,
        "metacritic": 87,
        "platforms": ["PC", "Xbox Series X"]
    },
    "Genshin Impact": {
        "genre": "Action-RPG",
        "release": 2020,
        "metacritic": 86,
        "platforms": ["PC", "PS4", "Mobile"]
    },
    "Roblox": {
        "genre": "MMO",
        "release": 2006,
        "metacritic": 70,
        "platforms": ["PC", "Mobile", "Xbox Series X"]
    },
    "Rocket League": {
        "genre": "Spor",
        "release": 2015,
        "metacritic": 86,
        "platforms": ["PC", "PS4", "Xbox One", "Switch"]
    },
    "Destiny 2": {
        "genre": "FPS",
        "release": 2017,
        "metacritic": 85,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "Warframe": {
        "genre": "MMO",
        "release": 2013,
        "metacritic": 83,
        "platforms": ["PC", "PS4", "Xbox One", "Switch"]
    },
    "GTA Online": {
        "genre": "MMO",
        "release": 2013,
        "metacritic": 80,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "Rainbow Six Siege": {
        "genre": "FPS",
        "release": 2015,
        "metacritic": 79,
        "platforms": ["PC", "PS4", "PS5", "Xbox Series X"]
    },
    "Dead by Daylight": {
        "genre": "Survival Horror",
        "release": 2016,
        "metacritic": 71,
        "platforms": ["PC", "PS4", "Xbox One", "Switch"]
    },
    "Sea of Thieves": {
        "genre": "Macera",
        "release": 2018,
        "metacritic": 69,
        "platforms": ["PC", "Xbox Series X"]
    },
    "Fall Guys": {
        "genre": "Battle Royale",
        "release": 2020,
        "metacritic": 80,
        "platforms": ["PC", "PS4", "Switch", "Xbox Series X"]
    }
}

# Google Trends ve RAWG API ayarları
pytrends = TrendReq(hl='tr-TR', tz=360)
RAWG_API_KEY = "a04a54d4a1384a64b182fc19616f00c4"
BASE_URL = "https://api.rawg.io/api/games"

# ----------------------
# TEMEL AYARLAR
# ----------------------
st.set_page_config(
    page_title="Oyun Pusulası",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=3600)
def get_optimized_image(url, width=800, height=450):
    """Daha büyük ve yüksek kaliteli görseller için optimizasyon"""
    return f"https://images.weserv.nl/?url={url}&w={width}&h={height}&fit=cover&output=webp&q=90"



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
            details_url = f"{BASE_URL}/{game_id}"
            details_response = requests.get(details_url, params={"key": RAWG_API_KEY})
            details_response.raise_for_status()
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

def save_feedback(data):
    df = pd.DataFrame([data])
    df.to_csv("feedback.csv", mode='a', header=False, index=False)

def load_feedback():
    try:
        return pd.read_csv("feedback.csv", names=["game", "rating", "comment", "timestamp"])
    except FileNotFoundError:
        return pd.DataFrame()
# ----------------------
# YAYINCI ARAÇLARI FONKSİYONLARI
# ----------------------

def get_best_stream_times(game_name):
    """Bir oyun için en iyi yayın saatlerini analiz et"""
    try:
        # Google Trends'ten saatlik veri çek
        pytrends.build_payload([game_name], timeframe='now 7-d', geo='TR', gprop='')
        hourly_data = pytrends.interest_over_time()
        
        if hourly_data.empty or game_name not in hourly_data.columns:
            return None
            
        # Saatlere göre grupla
        hourly_data['hour'] = hourly_data.index.hour
        hourly_avg = hourly_data.groupby('hour')[game_name].mean()
        
        # En iyi 3 saati belirle
        best_hours = hourly_avg.sort_values(ascending=False).head(3).index.tolist()
        best_hours_str = ", ".join([f"{h}:00-{h+1}:00" for h in best_hours])
        
        return {
            "best_hours": best_hours_str,
            "chart_data": hourly_avg
        }
    except Exception as e:
        st.error(f"Yayın saati analiz hatası: {str(e)}")
        return None

def schedule_stream():
    """Yayın planlama arayüzü"""
    with st.form("stream_schedule_form"):
        st.subheader("📅 Yayın Planlama")
        
        col1, col2 = st.columns(2)
        with col1:
            game = st.selectbox("Oyun Seçin", list(game_database.keys()), key="schedule_game")
            stream_date = st.date_input("Yayın Tarihi", min_value=datetime.today())
        with col2:
            start_time = st.time_input("Başlangıç Saati", value=datetime.strptime("20:00", "%H:%M"))
            duration = st.selectbox("Süre (saat)", [1, 2, 3, 4])
        
        notes = st.text_area("Plan Notları", placeholder="Yayın içeriği, özel etkinlikler...")
        
        if st.form_submit_button("Planı Kaydet"):
            # Yayın planını session state'e kaydet
            if "stream_schedules" not in st.session_state:
                st.session_state.stream_schedules = []
                
            new_schedule = {
                "game": game,
                "date": stream_date.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M"),
                "duration": duration,
                "notes": notes
            }
            
            st.session_state.stream_schedules.append(new_schedule)
            st.success("✅ Yayın planı kaydedildi! Bildirimlerinizi kontrol edin.")
    
    # Kayıtlı planları göster
    if "stream_schedules" in st.session_state and st.session_state.stream_schedules:
        st.subheader("⏰ Yaklaşan Yayın Planları")
        for idx, schedule in enumerate(st.session_state.stream_schedules):
            with st.expander(f"{schedule['game']} - {schedule['date']} {schedule['start_time']}", expanded=False):
                st.markdown(f"""
                **Tarih:** {schedule['date']}  
                **Saat:** {schedule['start_time']} ({schedule['duration']} saat)  
                **Notlar:** {schedule['notes']}
                """)
                
                # Planı silme butonu
                if st.button("Planı Sil", key=f"delete_{idx}"):
                    del st.session_state.stream_schedules[idx]
                    st.rerun()

def social_engagement():
    """Sosyal medya etkileşim analizi"""
    st.subheader("📱 Sosyal Medya Etkileşimi")
    
    # Oyun seçimi
    game = st.selectbox("Analiz Edilecek Oyun", list(game_database.keys()), key="social_game")
    
    # Sahte verilerle etkileşim analizi
    if st.button("Analiz Et", key="analyze_social"):
        with st.spinner(f"{game} için sosyal medya analizi yapılıyor..."):
            time.sleep(2)
            
            # Rastgele veriler oluştur
            platforms = ["Twitter", "Instagram", "YouTube", "TikTok", "Reddit"]
            data = {
                "platform": platforms,
                "etkilesim": [round(10000 + i*5000) for i in range(len(platforms))],
                "paylasim": [round(500 + i*200) for i in range(len(platforms))]
            }
            df = pd.DataFrame(data)
            
            # Görselleştirme
            fig = px.bar(
                df, 
                x="platform", 
                y="etkilesim", 
                title=f"{game} - Platform Bazında Etkileşim",
                labels={"etkilesim": "Toplam Etkileşim", "platform": "Platform"},
                color="platform",
                text="etkilesim"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tavsiyeler
            st.info("""
            **📈 İçerik Tavsiyeleri:**
            - YouTube'da "Nasıl Yapılır?" videoları yüksek ilgi görüyor
            - TikTok'ta kısa oyun içi klip paylaşımları etkileşimi %40 artırabilir
            - Cumartesi günleri 20:00-22:00 arası canlı yayınlar daha fazla izleyici çekiyor
            """)

# ----------------------
# OYUN DETAY VE KART FONKSİYONLARI
# ----------------------

def show_game_details():
    # Seçilen oyun kontrolü
    if "selected_game" not in st.session_state or st.session_state.selected_game is None or st.session_state.selected_game == "":
        st.info("Oyun detaylarını görmek için lütfen Ana Sayfa'dan bir oyun seçin veya tıklayın.")
        return

    game_name = st.session_state.selected_game

    if game_name not in game_database:
        st.warning(f"'{game_name}' oyunu veritabanımızda bulunamadı. Lütfen farklı bir oyun seçin.")
        return

    details = game_database.get(game_name, {})

    with st.container():
        st.markdown('<div id="game-details"></div>', unsafe_allow_html=True)
        st.subheader(f"🎮 {game_name} Detayları")

        col1, col2 = st.columns([1, 2])
        with col1:
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
                    response.raise_for_status()
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
                            st.progress(details_data.get("rating", 0)/5)
                    else:
                        st.info("RAWG API'sinde bu oyun için detaylı bilgi bulunamadı.")
                except requests.exceptions.RequestException as e:
                    st.error(f"RAWG API isteği hatası: {str(e)}")
                except Exception as e:
                    st.error(f"Beklenmedik API hatası: {str(e)}")

def show_game_card(game, details):
    with st.container():
        st.markdown('<div class="game-card-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 4])  # Görsel için daha geniş alan (3:4 oran)
        
        with col1:
            # Büyük ve net görseller
            st.image(
                get_optimized_image(GAME_COVERS.get(game, 'https://via.placeholder.com/800x450')), 
                use_container_width=True
            )

        with col2:
            st.markdown(f"## {game}")  # Daha büyük başlık
            st.markdown(f"**⭐ Metacritic:** {details.get('metacritic', 'N/A')} | **📅 Çıkış Yılı:** {details.get('release', 'N/A')}")
            st.markdown(f"**🎮 Tür:** {details.get('genre', 'N/A')}")
            st.markdown(f"**🖥️ Platformlar:** {', '.join(details.get('platforms', ['Multiplatform']))}")
            
            if st.button(f"🔍 Detayları Görüntüle", key=f"btn_{game}"):
                st.session_state["selected_game"] = game
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------
# CSS STİLLERİ 
# ----------------------
st.markdown("""
<style>
    /* Pusula temalı renk paleti */
    :root {
        --primary: #1e3a8a;  /* koyu mavi */
        --secondary: #d4af37; /* altın rengi */
        --accent: #8b0000;   /* koyu kırmızı */
    }
    
    .custom-header {
        color: var(--primary);
        text-align: center;
        font-size: 3rem;
        margin-bottom: 20px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Buton renkleri */
    .stButton > button {
        background: linear-gradient(45deg, var(--primary), var(--accent));
    }
    
    /* Sidebar başlığı */
    .sidebar-header {
        color: var(--secondary);
        border-bottom: 2px solid var(--secondary);
    }
    
    /* Pusula animasyonu */
    .compass-icon {
        animation: rotate 8s linear infinite;
        display: inline-block;
        font-size: 2rem;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# ----------------------
# ANA UYGULAMA
# ----------------------
def main():
    # Session state ilk tanımlama
    if "selected_game" not in st.session_state:
        st.session_state.selected_game = None

    st.markdown("<h1 class='custom-header'>Oyun Pusulası</h1>", unsafe_allow_html=True)

    # Eğer bir oyun seçildiyse, detaylar gösterilsin
    if st.session_state.selected_game:
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

    # Filtreleme seçenekleri
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            search_query = st.text_input("🔍 Oyun Ara", key="game_input_2")
        with col2:
            selected_genre = st.selectbox("🎮 Tür Seçin", ["Tümü", "Aksiyon", "RPG", "Strateji", "FPS", "Macera", 
                                                         "Survival Horror", "Spor", "Simülasyon", "Battle Royale", 
                                                         "MMO", "Platform", "Fighting"])
        with col3:
            min_score = st.slider("⭐ Minimum Puan", 0, 100, 75)

    # Sekmeler
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Ana Sayfa", 
        "💬 Değerlendirmeler", 
        "📈 Trendler", 
        "📊 İstatistikler",
        "🎥 Yayıncı Araçları"
    ])

    with tab1:
        # Filtrelenmiş oyunlar
        filtered_games = [
            (game, details) for game, details in game_database.items()
            if (not search_query or search_query.lower() in game.lower())
            and (selected_genre == "Tümü" or details["genre"] == selected_genre)
            and details["metacritic"] >= min_score
        ]

        if not filtered_games:
            st.warning("🚨 Filtrelerinize uygun oyun bulunamadı!")
        else:
            # 3 sütunlu grid
            cols = st.columns(3)
            for idx, (game, details) in enumerate(filtered_games):
                with cols[idx % 3]:
                    show_game_card(game, details)

    with tab2:
        # Değerlendirme formu
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

        # Geçmiş değerlendirmeler
        feedback_df = load_feedback()
        if not feedback_df.empty:
            st.subheader("📜 Geçmiş Değerlendirmeler")
            for _, row in feedback_df.iterrows():
                with st.expander(f"{row['game']} - {'⭐' * row['rating']}", expanded=False):
                    st.markdown(f"**📅 Tarih:** {row['timestamp']} \n**💬 Yorum:** {row['comment']}")
        else:
            st.info("ℹ️ Henüz değerlendirme bulunmamaktadır")

    with tab3:
        # Tekil trend analizi
        st.subheader("🔍 Tekil Trend Analizi")
        keyword_single = st.text_input("Analiz Edilecek Oyun/Kategori Adı:", 
                                      placeholder="Örn: League of Legends", 
                                      key="single_trend_keyword")

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

        # Çoklu trend karşılaştırma
        st.subheader("🏷️ Çoklu Trend Karşılaştırma")
        comparison_keywords = st.text_input("Karşılaştırılacak anahtar kelimeleri virgülle ayırın (en fazla 5):", 
                                           key="multi_trend_keywords")
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
        # İstatistikler sekmesi
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
    with tab5:
        st.header("🎮 Yayıncı Araçları")
    st.markdown("Oyun yayıncıları için özel analiz ve planlama araçları")
    
    # Alt sekmeler oluştur
    stream_tab1, stream_tab2, stream_tab3 = st.tabs([
        "⏰ Yayın Saati Analizi",
        "📅 Yayın Planlama",
        "📱 Sosyal Medya Analizi"
    ])
    
    with stream_tab1:
        st.subheader("En İyi Yayın Saatleri Analizi")
        game_for_time = st.selectbox("Oyun Seçin", list(game_database.keys()), key="time_game")
        
        if st.button("Analiz Et", key="analyze_stream_time"):
            result = get_best_stream_times(game_for_time)
            if result:
                st.success(f"**{game_for_time}** için en iyi yayın saatleri: **{result['best_hours']}**")
                
                # Grafik oluştur
                fig = px.bar(
                    x=result['chart_data'].index, 
                    y=result['chart_data'].values,
                    labels={'x': 'Saat (24h)', 'y': 'Ortalama Popülerlik'},
                    title=f"Günlük Popülerlik - {game_for_time}",
                    text=result['chart_data'].values
                )
                fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Bu oyun için yeterli veri bulunamadı.")
    
    with stream_tab2:
        schedule_stream()  # Yayın planlama fonksiyonunu çağır
    
    with stream_tab3:
        social_engagement()  # Sosyal medya analiz fonksiyonunu çağır

# ----------------------
# YAN PANEL
# ----------------------
with st.sidebar:
    # Pusula animasyonlu başlık
    st.markdown("""
    <div style="text-align:center; margin-bottom:30px;">
        <h1 class="sidebar-header" style="font-size:2rem; margin:0;">Oyun Pusulası</h1>
        <div style="font-size:1.5rem; margin-top:10px; animation: rotate 8s linear infinite;">🧭</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Kullanıcı profili kartı
    with st.container():
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/5976/5976236.png", width=60)
        with col2:
            st.markdown(f"""
            <div style="line-height:1.3">
                <h4 style="margin:0;color:#6a89cc;">Merhaba, Oyuncu!</h4>
                <div style="font-size:0.85em;color:#777;">
                    Seviye: <strong>28</strong>
                    <span style="background:#6a89cc20;color:#6a89cc;padding:3px 10px;border-radius:15px;font-size:0.75em">+3 Rozet</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.progress(0.65, text="Seviye İlerlemesi (%65)")

        # İstatistikler
        st.markdown("""
        <div style="display:flex; justify-content:space-between; margin:15px 0;">
            <div style="text-align:center; flex:1;">
                <div style="font-size:1.3em; color:#6a89cc;">🎮 142</div>
                <div style="font-size:0.75em;color:#888">Oynanan</div>
            </div>
            <div style="text-align:center; flex:1;">
                <div style="font-size:1.3em; color:#f8c291;">⭐ 4.8</div>
                <div style="font-size:0.75em;color:#888">Ortalama</div>
            </div>
            <div style="text-align:center; flex:1;">
                <div style="font-size:1.3em; color:#82ccdd;">🏆 23</div>
                <div style="font-size:0.75em;color:#888">Başarı</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
     # Kişiselleştirilmiş Öneriler
    with st.container():
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### 🎮 Kişiselleştirilmiş Öneriler")
        
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
                    <div style="padding:10px; margin:5px 0; background:rgba(106,137,204,0.1); border-radius:8px">
                        <div style="font-size:0.9em; font-weight:500;">🎮 {game}</div>
                        <div style="font-size:0.8em;color:#777;">
                            ⭐ {details['metacritic']} | 📅 {details['release']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Benzer oyun bulunamadı")
        
        st.markdown("</div>", unsafe_allow_html=True)
    # Canlı Etkinlikler
    with st.container():
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### 🔥 Canlı Etkinlikler")

        st.markdown(f"""
        <div style="margin: 15px 0; padding: 12px; background: rgba(255, 75, 75, 0.1); border-radius: 10px; border-left: 4px solid #ff4b4b;">
            <div style="display:flex; justify-content:space-between; align-items:center">
                <div>
                    <span style="background:#ff4b4b;border-radius:50%;width:10px;height:10px;display:inline-block;"></span>
                    <strong style="color:#ff4b4b">FPS Challenge</strong>
                </div>
                <span style="font-size:0.8em;color:#ff4b4b;background:rgba(255,75,75,0.2);padding:2px 8px;border-radius:12px;">3h left</span>
            </div>
            <div style="font-size:0.8em;margin-top:8px">
                🎯 <span style="color:#777">5.4K katılımcı</span> | 🏆 <span style="color:#777">$2K ödül</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="margin: 15px 0; padding: 12px; background: rgba(155, 89, 182, 0.1); border-radius: 10px; border-left: 4px solid #9b59b6;">
            <div style="display:flex; justify-content:space-between; align-items:center">
                <div>
                    <span style="background:#9b59b6;border-radius:50%;width:10px;height:10px;display:inline-block;"></span>
                    <strong style="color:#9b59b6">Cosplay Yarışması</strong>
                </div>
                <span style="font-size:0.8em;color:#9b59b6;background:rgba(155,89,182,0.2);padding:2px 8px;border-radius:12px;">2gün kaldı</span>
            </div>
            <div style="font-size:0.8em;margin-top:8px">
                🎭 <span style="color:#777">1.2K katılımcı</span> | 📸 <span style="color:#777">En iyi 10'a oy ver</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Size Özel Öneriler
    with st.container():
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### 🎯 Size Özel Öneriler")

        # Öneri 1
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(get_optimized_image(GAME_COVERS["Cyberpunk 2077"], width=1000), width=1000)
        with col2:
            st.markdown("""
            <div>
                <div style="font-weight:bold;margin-bottom:5px;font-size:0.9em">Cyberpunk 2077</div>
                <div style="font-size:0.8em;color:#777;">
                    <div>⏳ Son oynama: 2 gün önce</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Öneri 2
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(get_optimized_image(GAME_COVERS["The Witcher 3: Wild Hunt"], width=1000), width=1000)
        with col2:
            st.markdown("""
            <div>
                <div style="font-weight:bold;margin-bottom:5px;font-size:0.9em">The Witcher 3</div>
                <div style="font-size:0.8em;color:#777;">
                    <div>🎮 Uyumluluk: %85</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Topluluğa Katılın
    with st.container():
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("### 🌐 Topluluğa Katılın")
        
        st.markdown("""
<a href="https://www.youtube.com/channel/..." target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" width="32" style="margin-right:30px;">
</a>
<a href="https://discord.gg/..." target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/2111/2111370.png" width="32" style="margin-right:30px;">
</a>
<a href="https://www.twitch.tv/..." target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/2111/2111668.png" width="32" style="margin-right:30px;">
</a>
""", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align:center;margin-top:30px;font-size:0.8em;color:#888">
        <div>Oyun Pusulası © 2025</div>
        <div>Oyun dünyasında doğru yönünüz</div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()