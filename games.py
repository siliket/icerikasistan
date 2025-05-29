# games.py
PLACEHOLDER_IMAGE = "https://via.placeholder.com/400x225"
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