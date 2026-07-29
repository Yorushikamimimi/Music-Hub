"""Source-backed Yorushika release and track metadata.

Release membership and track order follow the linked Yorushika official
discography pages. The catalog scope is the music releases listed under the
official Yorushika artist tab; live video products, books, and solo works are
outside that scope. Bilibili links are optional third-party references whose
availability and matching titles were reviewed manually.
"""

from datetime import date


CATALOG_SCOPE_URL = "https://yorushika.com/discography/artist/2/"
CATALOG_REVIEWED_ON = date(2026, 7, 29)
VIDEO_LINKS_REVIEWED_ON = date(2026, 7, 29)


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


LEGACY_TRACK_SLUG_ALIASES = {
    "bakudanma-makeinu": "bakudanma",
    "bakudanma-tousaku": "bakudanma",
    "kutsu-no-hanabi-natsukusa": "kutsu-no-hanabi",
    "kutsu-no-hanabi-gentou": "kutsu-no-hanabi",
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


LEGACY_RELEASES = (
    {
        "slug": "haru",
        "title": "晴る",
        "release_type": "Digital Single",
        "release_date": date(2024, 1, 5),
        "cover_path": "release_haru.webp",
        "source_url": "https://yorushika.com/discography/detail/37/",
        "tracks": (("haru", "晴る"),),
    },
    {
        "slug": "gentou",
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
            ("kutsu-no-hanabi", "靴の花火"),
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
        "slug": "sousaku",
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
        "slug": "tousaku",
        "title": "盗作",
        "release_type": "Full Album",
        "release_date": date(2020, 7, 29),
        "cover_path": "release_tousaku.webp",
        "source_url": "https://yorushika.com/discography/detail/15/",
        "tracks": (
            ("music-thief-confession", "音楽泥棒の自白"),
            ("daytime-nighthawk", "昼鳶"),
            ("haruhisagi", "春ひさぎ"),
            ("bakudanma", "爆弾魔"),
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
        "slug": "elma",
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
        "slug": "dakara-boku-wa-ongaku-wo-yameta",
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
        "slug": "makeinu-ni-encore-wa-iranai",
        "title": "負け犬にアンコールはいらない",
        "release_type": "Mini Album",
        "release_date": date(2018, 5, 9),
        "cover_path": "release_makeinu.webp",
        "source_url": "https://yorushika.com/discography/detail/7/",
        "tracks": (
            ("previous-life", "前世"),
            ("makeinu-ni-encore-wa-iranai", "負け犬にアンコールはいらない"),
            ("bakudanma", "爆弾魔"),
            ("hitchcock", "ヒッチコック"),
            ("falling", "落下"),
            ("semi-transparent-boy", "準透明少年"),
            ("just-a-sunny-day-for-you", "ただ君に晴れ"),
            ("hibernation", "冬眠"),
            ("summer-bus-stop-waiting-for-you", "夏、バス停、君を待つ"),
        ),
    },
    {
        "slug": "natsukusa-ga-jama-wo-suru",
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
            ("kutsu-no-hanabi", "靴の花火"),
            ("cloud-and-ghost", "雲と幽霊"),
        ),
    },
)


NEW_RELEASES = (
    {
        "slug": "nininsyou",
        "title": "二人称",
        "release_type": "Digital Album",
        "release_date": date(2026, 3, 4),
        "cover_path": "release_nininsyou.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/75/",
        "tracks": (
            ("kumo-ni-naru", "雲になる"),
            ("hana-mo-zawameku", "花も騒めく"),
            ("mashou", "魔性"),
            ("play-sick", "プレイシック"),
            ("post-haru", "ポスト春"),
            ("taiyou", "太陽"),
            ("haru", "晴る"),
            ("wasurete-kudasai", "忘れてください"),
            ("shura", "修羅"),
            ("kaseijin", "火星人"),
            ("rubato", "ルバート"),
            ("kasou", "火葬"),
            ("aporia", "アポリア"),
            ("hebi", "へび"),
            ("umeki", "うめき"),
            ("kitsutsuki", "啄木鳥"),
            ("hitchcock", "ヒッチコック"),
            ("gekkouyoku", "月光浴"),
            ("chidori", "千鳥"),
            ("kai", "櫂"),
        ),
    },
    {
        "slug": "abuku",
        "title": "あぶく",
        "release_type": "Digital Single",
        "release_date": date(2026, 4, 22),
        "cover_path": "release_abuku.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/76/",
        "tracks": (("abuku", "あぶく"),),
    },
    {
        "slug": "akane",
        "title": "茜",
        "release_type": "Digital Single",
        "release_date": date(2026, 2, 4),
        "cover_path": "release_akane.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/74/",
        "tracks": (("akane", "茜"),),
    },
    {
        "slug": "play-sick",
        "title": "プレイシック",
        "release_type": "Digital Single",
        "release_date": date(2025, 12, 22),
        "cover_path": "release_play_sick.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/73/",
        "tracks": (("play-sick", "プレイシック"),),
    },
    {
        "slug": "shura",
        "title": "修羅",
        "release_type": "Digital Single",
        "release_date": date(2025, 8, 8),
        "cover_path": "release_shura.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/65/",
        "tracks": (("shura", "修羅"),),
    },
    {
        "slug": "kaseijin",
        "title": "火星人",
        "release_type": "Digital Single",
        "release_date": date(2025, 5, 9),
        "cover_path": "release_kaseijin.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/63/",
        "tracks": (("kaseijin", "火星人"),),
    },
    {
        "slug": "hebi",
        "title": "へび",
        "release_type": "Digital Single",
        "release_date": date(2025, 1, 17),
        "cover_path": "release_hebi.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/61/",
        "tracks": (("hebi", "へび"),),
    },
    {
        "slug": "taiyou",
        "title": "太陽",
        "release_type": "Digital Single",
        "release_date": date(2024, 11, 22),
        "cover_path": "release_taiyou.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/57/",
        "tracks": (("taiyou", "太陽"),),
    },
    {
        "slug": "aporia",
        "title": "アポリア",
        "release_type": "Digital Single",
        "release_date": date(2024, 10, 7),
        "cover_path": "release_aporia.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/56/",
        "tracks": (("aporia", "アポリア"),),
    },
    {
        "slug": "wasurete-kudasai",
        "title": "忘れてください",
        "release_type": "Digital Single",
        "release_date": date(2024, 7, 13),
        "cover_path": "release_wasurete_kudasai.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/52/",
        "tracks": (("wasurete-kudasai", "忘れてください"),),
    },
    {
        "slug": "rubato",
        "title": "ルバート",
        "release_type": "Digital Single",
        "release_date": date(2024, 5, 29),
        "cover_path": "release_rubato.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/50/",
        "tracks": (("rubato", "ルバート"),),
    },
    {
        "slug": "gekkouyoku",
        "title": "月光浴",
        "release_type": "Digital Single",
        "release_date": date(2023, 10, 13),
        "cover_path": "release_gekkouyoku.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/47/",
        "tracks": (("gekkouyoku", "月光浴"),),
    },
    {
        "slug": "shayou",
        "title": "斜陽",
        "release_type": "Digital Single",
        "release_date": date(2023, 5, 8),
        "cover_path": "release_shayou.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/48/",
        "tracks": (("shayou", "斜陽"),),
    },
    {
        "slug": "telepath",
        "title": "テレパス",
        "release_type": "Digital Single",
        "release_date": date(2023, 1, 12),
        "cover_path": "release_telepath.webp",
        "source_url": "https://yorushika.com/discography/artist/2/detail/46/",
        "tracks": (("telepath", "テレパス"),),
    },
)


CATALOG_RELEASES = tuple(
    sorted(
        LEGACY_RELEASES + NEW_RELEASES,
        key=lambda release: release["release_date"],
        reverse=True,
    )
)


def _build_release_tracks():
    return tuple(
        {
            "release_slug": release["slug"],
            "track_slug": slug,
            "track_number": track_number,
        }
        for release in CATALOG_RELEASES
        for track_number, (slug, _title_ja) in enumerate(
            release["tracks"],
            start=1,
        )
    )


CATALOG_RELEASE_TRACKS = _build_release_tracks()


def _build_catalog_tracks():
    primary_release_by_track = {}
    title_by_track = {}
    for release in LEGACY_RELEASES + NEW_RELEASES:
        for track_number, (slug, title_ja) in enumerate(
            release["tracks"],
            start=1,
        ):
            primary_release_by_track.setdefault(
                slug,
                (release, track_number),
            )
            title_by_track.setdefault(slug, title_ja)

    catalog = []
    seen = set()
    for release in CATALOG_RELEASES:
        for slug, _title_ja in release["tracks"]:
            if slug in seen:
                continue
            seen.add(slug)
            primary_release, track_number = primary_release_by_track[slug]
            title_ja = title_by_track[slug]
            title_en, note_theme = TRACK_DETAILS.get(slug, ("", "作品脉络"))
            title = f"{title_en} ({title_ja})" if title_en else title_ja
            catalog.append(
                {
                    "slug": slug,
                    "title": title,
                    "title_ja": title_ja,
                    "title_en": title_en,
                    "album_title": primary_release["title"],
                    "release_type": primary_release["release_type"],
                    "release_date": primary_release["release_date"],
                    "release_year": primary_release["release_date"].year,
                    "track_number": track_number,
                    "cover_path": primary_release["cover_path"],
                    "story_summary": (
                        f"《{primary_release['title']}》官方曲序第 {track_number} 首。"
                        f"本站把它放在“{note_theme}”的个人整理路径中；"
                        "当前仅记录官方收录信息，不转载完整歌词。"
                    ),
                    "source_url": primary_release["source_url"],
                    "source_checked_at": CATALOG_REVIEWED_ON,
                    "mv_url": VERIFIED_BILIBILI_VIDEOS.get(slug),
                }
            )

    return tuple(catalog)


CATALOG_TRACKS = _build_catalog_tracks()
