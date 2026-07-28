"""Source-backed Yorushika release and track metadata.

Release membership and track order follow the linked Yorushika official
discography pages. Bilibili links are optional, manually verified listening
links retained from the original Music Hub catalog.
"""

from datetime import date


CATALOG_REVIEWED_ON = date(2026, 7, 28)


VERIFIED_BILIBILI_VIDEOS = {
    "haru": "https://www.bilibili.com/video/BV1kQ4y1L77o/",
    "spring-thief": "https://www.bilibili.com/video/BV16k8bzGE31/",
    "just-a-sunny-day-for-you": "https://www.bilibili.com/video/BV1dW41137on/",
    "night-journey": "https://www.bilibili.com/video/BV1A7tBzYEuw/",
    "left-right-confusion": "https://www.bilibili.com/video/BV1Nznrz8EUR/",
    "algernon": "https://www.bilibili.com/video/BV1Nk5izhEsB/",
    "thoughtcrime": "https://www.bilibili.com/video/BV1gw411e7Dk/",
    "flower-and-badger-game": "https://www.bilibili.com/video/BV1uY4y1z7n6/",
    "nautilus": "https://www.bilibili.com/video/BV1GhHJzJESB/",
    "thats-why-i-gave-up-on-music": "https://www.bilibili.com/video/BV1HA411973b/",
    "ghost-in-a-flower": "https://www.bilibili.com/video/BV1nc3mz7EDT/",
    "hitchcock": "https://www.bilibili.com/video/BV15KaNziEv1/",
    "say-it": "https://www.bilibili.com/video/BV1ELraBoEaf/",
    "deep-indigo": "https://www.bilibili.com/video/BV1KV411N7to/",
    "rain-with-cappuccino": "https://www.bilibili.com/video/BV13AaYzGE6G/",
    "parade": "https://www.bilibili.com/video/BV1ZFpmzMEah/",
    "walking": "https://www.bilibili.com/video/BV13B4y1q7cV/",
    "elma": "https://www.bilibili.com/video/BV1ypxuzUEpu/",
    "hole-in-the-heart": "https://www.bilibili.com/video/BV1Pa4y157fr/",
    "plagiarism": "https://www.bilibili.com/video/BV1UX8nzaEz8/",
    "miyakoochi": "https://www.bilibili.com/video/BV1ZM4y1y7Yp/",
    "howl-at-the-moon": "https://www.bilibili.com/video/BV1Cq4y1V7Kv/",
    "matasaburo": "https://www.bilibili.com/video/BV16V411x7rA/",
    "false-moon": "https://www.bilibili.com/video/BV1zh411h7bY/",
}


TRACK_DETAILS = {
    "haru": ("Sunny", "季节与前行"),
    "spring-thief": ("Spring Thief", "春日、短暂与留恋"),
    "just-a-sunny-day-for-you": ("Just a Sunny Day for You", "夏日与回望"),
    "night-journey": ("Night Journey", "夜晚、行走与告别"),
    "left-right-confusion": ("Left-Right Confusion", "距离与选择"),
    "algernon": ("Algernon", "变化与理解"),
    "thoughtcrime": ("Thoughtcrime", "创作与自我审视"),
    "flower-and-badger-game": ("Flower and Badger Game", "触碰与确认"),
    "nautilus": ("Nautilus", "书信与叙事终点"),
    "thats-why-i-gave-up-on-music": (
        "That's Why I Gave Up on Music",
        "青年、音乐与告别",
    ),
    "ghost-in-a-flower": ("Ghost in a Flower", "夏日、记忆与告别"),
    "hitchcock": ("Hitchcock", "成长与提问"),
    "say-it": ("Say It.", "表达与错过"),
    "deep-indigo": ("Deep Indigo", "创作旅程的起点"),
    "rain-with-cappuccino": ("Rain with Cappuccino", "雨、城市与日记"),
    "parade": ("Parade", "旅行、回忆与书信"),
    "walking": ("Walking", "旅途与继续前行"),
    "elma": ("Elma", "人物与概念专辑的联系"),
    "hole-in-the-heart": ("Hole in the Heart", "缺失与继续前行"),
    "plagiarism": ("Plagiarism", "模仿、创作与自我审视"),
}


CATALOG_RELEASES = (
    {
        "title": "晴る",
        "release_type": "Digital Single",
        "release_date": date(2024, 1, 5),
        "cover_path": "release_haru.webp",
        "source_url": "https://yorushika.com/discography/detail/37/",
        "tracks": (("haru", "晴る"),),
    },
    {
        "title": "幻燈",
        "release_type": "Music Art Book",
        "release_date": date(2023, 4, 5),
        "cover_path": "release_gentou.webp",
        "source_url": "https://yorushika.com/discography/detail/30/",
        "tracks": (
            ("summer-portrait", "夏の肖像"),
            ("miyakoochi", "都落ち"),
            ("bremen", "ブレーメン"),
            ("chinokate", "チノカテ"),
            ("snow-country", "雪国"),
            ("howl-at-the-moon", "月に吠える"),
            ("four-fifty-one", "451"),
            ("pas-de-deux", "パドドゥ"),
            ("matasaburo", "又三郎"),
            ("kutsu-no-hanabi-gentou", "靴の花火"),
            ("old-man-and-the-sea", "老人と海"),
            ("goodbye-molten", "さよならモルテン"),
            ("isana", "いさな"),
            ("left-right-confusion", "左右盲"),
            ("algernon", "アルジャーノン"),
            ("first-night", "第一夜"),
            ("second-night", "第二夜"),
            ("third-night", "第三夜"),
            ("fourth-night", "第四夜"),
            ("fifth-night", "第五夜"),
            ("sixth-night", "第六夜"),
            ("seventh-night", "第七夜"),
            ("eighth-night", "第八夜"),
            ("ninth-night", "第九夜"),
            ("tenth-night", "第十夜"),
        ),
    },
    {
        "title": "創作",
        "release_type": "EP",
        "release_date": date(2021, 1, 27),
        "cover_path": "release_sousaku.webp",
        "source_url": "https://yorushika.com/discography/detail/18/",
        "tracks": (
            ("robbery-and-bouquet", "強盗と花束"),
            ("spring-thief", "春泥棒"),
            ("creation", "創作"),
            ("eat-the-wind", "風を食む"),
            ("false-moon", "嘘月"),
        ),
    },
    {
        "title": "盗作",
        "release_type": "Full Album",
        "release_date": date(2020, 7, 29),
        "cover_path": "release_tousaku.webp",
        "source_url": "https://yorushika.com/discography/detail/15/",
        "tracks": (
            ("music-thief-confession", "音楽泥棒の自白"),
            ("daytime-nighthawk", "昼鳶"),
            ("haruhisagi", "春ひさぎ"),
            ("bakudanma-tousaku", "爆弾魔"),
            ("youth-burglary", "青年期、空き巣"),
            ("replicant", "レプリカント"),
            ("flower-and-badger-game", "花人局"),
            ("midsummer-music-thief", "朱夏期、音楽泥棒"),
            ("plagiarism", "盗作"),
            ("thoughtcrime", "思想犯"),
            ("escape", "逃亡"),
            ("childhood-in-memories", "幼年期、思い出の中"),
            ("night-journey", "夜行"),
            ("ghost-in-a-flower", "花に亡霊"),
        ),
    },
    {
        "title": "エルマ",
        "release_type": "Full Album",
        "release_date": date(2019, 8, 28),
        "cover_path": "release_elma.webp",
        "source_url": "https://yorushika.com/discography/detail/2/",
        "tracks": (
            ("train-window", "車窓"),
            ("only-sorrow", "憂一乗"),
            ("evening-calm-flower-confusion", "夕凪、某、花惑い"),
            ("rain-with-cappuccino", "雨とカプチーノ"),
            ("lake-town", "湖の街"),
            ("dance-of-god", "神様のダンス"),
            ("rain-clears", "雨晴るる"),
            ("walking", "歩く"),
            ("hole-in-the-heart", "心に穴が空いた"),
            ("forest-church", "森の教会"),
            ("voice", "声"),
            ("amy", "エイミー"),
            ("seabed-moonlight", "海底、月明かり"),
            ("nautilus", "ノーチラス"),
        ),
    },
    {
        "title": "だから僕は音楽を辞めた",
        "release_type": "Full Album",
        "release_date": date(2019, 4, 10),
        "cover_path": "release_dakara_boku.webp",
        "source_url": "https://yorushika.com/discography/detail/6/",
        "tracks": (
            ("august-31", "8/31"),
            ("deep-indigo", "藍二乗"),
            ("august-a-certain-moonlight", "八月、某、月明かり"),
            ("poet-and-coffee", "詩書きとコーヒー"),
            ("july-13", "7/13"),
            ("lets-dance", "踊ろうぜ"),
            ("june-writes-rain-cleared-city", "六月は雨上がりの街を書く"),
            ("from-the-window-of-may", "五月は花緑青の窓辺から"),
            ("night-imitation", "夜紛い"),
            ("may-6", "5/6"),
            ("parade", "パレード"),
            ("elma", "エルマ"),
            ("april-10", "4/10"),
            ("thats-why-i-gave-up-on-music", "だから僕は音楽を辞めた"),
        ),
    },
    {
        "title": "負け犬にアンコールはいらない",
        "release_type": "Mini Album",
        "release_date": date(2018, 5, 9),
        "cover_path": "release_makeinu.webp",
        "source_url": "https://yorushika.com/discography/detail/7/",
        "tracks": (
            ("previous-life", "前世"),
            ("makeinu-ni-encore-wa-iranai", "負け犬にアンコールはいらない"),
            ("bakudanma-makeinu", "爆弾魔"),
            ("hitchcock", "ヒッチコック"),
            ("falling", "落下"),
            ("semi-transparent-boy", "準透明少年"),
            ("just-a-sunny-day-for-you", "ただ君に晴れ"),
            ("hibernation", "冬眠"),
            ("summer-bus-stop-waiting-for-you", "夏、バス停、君を待つ"),
        ),
    },
    {
        "title": "夏草が邪魔をする",
        "release_type": "Mini Album",
        "release_date": date(2017, 6, 28),
        "cover_path": "release_natsukusa.webp",
        "source_url": "https://yorushika.com/discography/detail/8/",
        "tracks": (
            ("summer-shadow-playing-piano", "夏陰、ピアノを弾く"),
            ("cattleya", "カトレア"),
            ("say-it", "言って。"),
            ("bloom-in-that-summer", "あの夏に咲け"),
            ("flight", "飛行"),
            ("kutsu-no-hanabi-natsukusa", "靴の花火"),
            ("cloud-and-ghost", "雲と幽霊"),
        ),
    },
)


def _build_catalog_tracks():
    catalog = []

    for release in CATALOG_RELEASES:
        for track_number, (slug, title_ja) in enumerate(
            release["tracks"],
            start=1,
        ):
            title_en, note_theme = TRACK_DETAILS.get(slug, ("", "作品脉络"))
            title = f"{title_en} ({title_ja})" if title_en else title_ja
            catalog.append(
                {
                    "slug": slug,
                    "title": title,
                    "title_ja": title_ja,
                    "title_en": title_en,
                    "album_title": release["title"],
                    "release_type": release["release_type"],
                    "release_date": release["release_date"],
                    "release_year": release["release_date"].year,
                    "track_number": track_number,
                    "cover_path": release["cover_path"],
                    "story_summary": (
                        f"《{release['title']}》官方曲序第 {track_number} 首。"
                        f"本站把它放在“{note_theme}”的个人整理路径中；"
                        "当前仅记录官方收录信息，不转载完整歌词。"
                    ),
                    "source_url": release["source_url"],
                    "source_checked_at": CATALOG_REVIEWED_ON,
                    "mv_url": VERIFIED_BILIBILI_VIDEOS.get(slug),
                }
            )

    return tuple(catalog)


CATALOG_TRACKS = _build_catalog_tracks()
