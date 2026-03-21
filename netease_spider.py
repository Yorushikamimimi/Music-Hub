import os
import requests
from bs4 import BeautifulSoup
import pymysql
import time
import random
from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f'Missing required environment variable for spider: {name}')
    return value.strip()


# --- database config ---
DB_CONFIG = {
    'host': _require_env('DB_HOST'),
    'user': _require_env('DB_USER'),
    'password': _require_env('DB_PASSWORD'),
    'database': _require_env('DB_NAME'),
    'charset': 'utf8mb4',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://music.163.com/',
}

# Added dummy year (2020) and cover path (placeholder.jpg) for existing items
BACKUP_YORUSHIKA = [
    ("Sunny (鏅淬倠)", "Haru no saki de mata aou", "HOT 99%", "https://www.bilibili.com/video/BV1kQ4y1L77o/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2024, "sunny.jpg"),
    ("Spring Thief (鏄ユ偿妫?", "Hana hiraita hana otoshita", "HOT 98%", "https://www.bilibili.com/video/BV16k8bzGE31/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2021, "spring_thief.jpg"),
    ("Just a Sunny Day for You (銇熴仩鍚涖伀鏅淬倢)", "Tsuini bokura ni me ga samete", "HOT 97%", "https://www.bilibili.com/video/BV1dW41137on/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2018, "sunny_day.jpg"),
    ("Night Journey (澶滆)", "Otona ni nattara wasurete shimau no ka na", "HOT 96%", "https://www.bilibili.com/video/BV1A7tBzYEuw/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2020, "night_journey.jpg"),
    ("Left-Right Confusion (宸﹀彸鐩?", "Sukoshi zutsu wasurete iku ne", "HOT 95%", "https://www.bilibili.com/video/BV1Nznrz8EUR/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2022, "left_right.jpg"),
    ("Algernon (銈儷銈搞儯銉笺儙銉?", "Yukkuri to kawatte iku", "HOT 95%", "https://www.bilibili.com/video/BV1Nk5izhEsB/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2023, "algernon.jpg"),
    ("Thoughtcrime (鎬濇兂鐘?", "Soredemo boku wa", "HOT 94%", "https://www.bilibili.com/video/BV1gw411e7Dk/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2020, "thoughtcrime.jpg"),
    ("Flower and Badger Game (鑺变汉灞€)", "Anata wo sawatte tashikametai", "HOT 93%", "https://www.bilibili.com/video/BV1uY4y1z7n6/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2020, "flower_badger.jpg"),
    ("Nautilus (銉庛兗銉併儵銈?", "Mou wasurete shimatta ka na", "HOT 92%", "https://www.bilibili.com/video/BV1GhHJzJESB/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2019, "nautilus.jpg"),
    ("That's Why I Gave Up on Music (鎵€浠ユ垜涓嶅仛闊充箰浜?", "Dakara boku wa ongaku wo yameta", "HOT 99%", "https://www.bilibili.com/video/BV1HA411973b/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2019, "gave_up_music.jpg"),
    ("Ghost in a Flower (鑺便伀浜￠湂)", "Natsu no nioi ga suru", "HOT 91%", "https://www.bilibili.com/video/BV1nc3mz7EDT/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2020, "ghost_flower.jpg"),
    ("Hitchcock (銉掋儍銉併偝銉冦偗)", "Sensei, jinsei soudan desu", "HOT 90%", "https://www.bilibili.com/video/BV15KaNziEv1/?share_source=copy_web", 2018, "hitchcock.jpg"),
    ("Say It. (瑷€銇ｃ仸銆?", "Motto, motto, motto, motto", "HOT 89%", "https://www.bilibili.com/video/BV1ELraBoEaf/?share_source=copy_web", 2017, "say_it.jpg"),
    ("Deep Indigo (钘嶄簩涔?", "Kaware, kaware, kaware", "HOT 88%", "https://www.bilibili.com/video/BV1KV411N7to/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2018, "deep_indigo.jpg"),
    ("Rain with Cappuccino (闆ㄣ仺銈儣銉併兗銉?", "Haiiro ni shiraketa kokoro wa", "HOT 87%", "https://www.bilibili.com/video/BV13AaYzGE6G/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2019, "rain_cappuccino.jpg"),
    ("Parade (銉戙儸銉笺儔)", "Kimi no soba ni isasete", "HOT 86%", "https://www.bilibili.com/video/BV1ZFpmzMEah/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2019, "parade.jpg"),
    ("Walking (姝┿亸)", "Aruku, aruku, aruku", "HOT 85%", "https://www.bilibili.com/video/BV13B4y1q7cV/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2018, "walking.jpg"),
    ("Elma (銈ㄣ儷銉?", "Kono mama zutto", "HOT 84%", "https://www.bilibili.com/video/BV1ypxuzUEpu/?share_source=copy_web", 2019, "elma.jpg"),
    ("Hole in the Heart (蹇冦伀绌淬亴绌恒亜銇?", "Yoru no sukima ni", "HOT 83%", "https://www.bilibili.com/video/BV1Pa4y157fr/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2019, "hole_heart.jpg"),
    ("Plagiarism (鐩椾綔)", "Mada tarinai, mada tarinai", "HOT 82%", "https://www.bilibili.com/video/BV1UX8nzaEz8/?share_source=copy_web&vd_source=72c94b8be878480502e724f337faa470", 2020, "plagiarism.jpg")
]

COVER_MAPPING = {
    'Sunny (鏅淬倠)': 'sunny.jpg',
    'Spring Thief (鏄ユ偿妫?': 'spring_thief.jpg',
    'Just a Sunny Day for You (銇熴仩鍚涖伀鏅淬倢)': 'sunny_day.jpg',
    'Night Journey (澶滆)': 'night_journey.jpg',
    'Left-Right Confusion (宸﹀彸鐩?': 'left_right.jpg',
    'Algernon (銈儷銈搞儯銉笺儙銉?': 'algernon.jpg',
    'Thoughtcrime (鎬濇兂鐘?': 'thoughtcrime.jpg',
    'Flower and Badger Game (鑺变汉灞€)': 'flower_badger.jpg',
    'Nautilus (銉庛兗銉併儵銈?': 'nautilus.jpg',
    "That's Why I Gave Up on Music (鎵€浠ユ垜涓嶅仛闊充箰浜?": 'gave_up_music.jpg',
    'Ghost in a Flower (鑺便伀浜￠湂)': 'ghost_flower.jpg',
    'Hitchcock (銉掋儍銉併偝銉冦偗)': 'hitchcock.jpg',
    'Say It. (瑷€銇ｃ仸銆?': 'say_it.jpg',
    'Deep Indigo (钘嶄簩涔?': 'deep_indigo.jpg',
    'Rain with Cappuccino (闆ㄣ仺銈儣銉併兗銉?': 'rain_cappuccino.jpg',
    'Parade (銉戙儸銉笺儔)': 'parade.jpg',
    'Walking (姝┿亸)': 'walking.jpg',
    'Elma (銈ㄣ儷銉?': 'elma.jpg',
    'Hole in the Heart (蹇冦伀绌淬亴绌恒亜銇?': 'hole_heart.jpg',
    'Plagiarism (鐩椾綔)': 'plagiarism.jpg'
}

def init_tables():
    """ 馃敟 寤鸿〃閫昏緫锛氬彧鍦ㄧ▼搴忓紑濮嬫椂杩愯涓€娆?"""
    print("馃敤 [鍒濆鍖朷 姝ｅ湪閲嶇疆鎵€鏈夎〃缁撴瀯...")
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS music_yorushika")
    cursor.execute("DROP TABLE IF EXISTS music_jpop")
    
    cursor.execute("""
        CREATE TABLE music_yorushika (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            album VARCHAR(255),
            rating VARCHAR(255),
            link VARCHAR(255),
            release_year INT,
            cover_path VARCHAR(255)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE music_jpop (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            artist VARCHAR(255),
            rating VARCHAR(255),
            link VARCHAR(255)
        )
    """)
    conn.commit()
    conn.close()
    print("鉁?[鍒濆鍖朷 琛ㄧ粨鏋勯噸缃畬鎴愶紒")

def save_to_db(table_name, data_list):
    """ 瀛樻暟鎹€昏緫锛氫笉鍐嶅垹琛紝鍙礋璐ｆ彃鍏?"""
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    if table_name == 'music_yorushika':
        sql = f"INSERT INTO {table_name} (title, album, rating, link, release_year, cover_path) VALUES (%s, %s, %s, %s, %s, %s)"
    else:
        sql = f"INSERT INTO {table_name} (title, artist, rating, link) VALUES (%s, %s, %s, %s)"
        
    try:
        cursor.executemany(sql, data_list)
        conn.commit()
        print(f"鉁?[{table_name}] 鎴愬姛鍏ュ簱 {len(data_list)} 鏉℃暟鎹紒")
    except Exception as e:
        print(f"鉂?鍏ュ簱澶辫触: {e}")
        
    conn.close()

def get_bilibili_search_link(keyword):
    return f"https://search.bilibili.com/all?keyword={keyword} MV"

def crawl_yorushika():
    print("馃殌 姝ｅ湪鐢熸垚 Yorushika 鏁版嵁...")
    
    # Process data to apply cover mapping
    processed_data = []
    for item in BACKUP_YORUSHIKA:
        # Item structure: (title, album, rating, link, release_year, cover_path)
        title = item[0]
        # Default placeholder
        final_cover = 'placeholder.jpg'
        
        # Check mapping
        for key, val in COVER_MAPPING.items():
            if key in title:
                final_cover = val
                break
        
        # Create new tuple with updated cover_path
        # (title, album, rating, link, release_year, new_cover_path)
        # item[5] is the existing 'sunny.jpg' data from BACKUP_YORUSHIKA which was hardcoded
        # The key logic requested was to check if title matches COVER_MAPPING.
        # But BACKUP_YORUSHIKA already has some cover paths. 
        # However, to be dynamic as requested:
        
        new_item = (item[0], item[1], item[2], item[3], item[4], final_cover)
        processed_data.append(new_item)
        
    save_to_db('music_yorushika', processed_data)

def crawl_jpop_rank():
    print("馃殌 姝ｅ湪杩炴帴缃戞槗浜?(鏃ヨ姒?...")
    url = "https://music.163.com/discover/toplist?id=60131"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        song_list = soup.find('ul', class_='f-hide')
        data = []
        if song_list:
            for i, li in enumerate(song_list.find_all('li')[:10]):
                title = li.find('a').text
                link = get_bilibili_search_link(title)
                artist = "Oricon Top"
                hot_score = f"Top {i+1}"
                data.append((title, artist, hot_score, link))
        if len(data) == 0:
            data = [("Lemon", "Kenshi Yonezu", "Rank 1", get_bilibili_search_link("Lemon"))]
        save_to_db('music_jpop', data)
    except Exception as e:
        print(f"鉂?J-Pop 鎶撳彇澶辫触: {e}")

if __name__ == '__main__':
    # 馃敟 鍏抽敭淇敼锛氬彧鍦ㄨ繖閲岃皟鐢ㄤ竴娆″缓琛紒
    init_tables()
    
    crawl_yorushika()
    time.sleep(1)
    # crawl_jpop_rank() # Disabled as per user request

