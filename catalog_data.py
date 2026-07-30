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
VIDEO_LINKS_REVIEWED_ON = date(2026, 7, 30)
VIDEO_CANDIDATES_RESEARCHED_ON = date(2026, 7, 30)


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

# These links are available in the local preview for Tian's manual review.
# Promote an entry to VERIFIED_BILIBILI_VIDEOS only after its visual quality,
# song match, and preferred upload have been accepted.
PENDING_REVIEW_BILIBILI_VIDEO_CANDIDATES = {
    "abuku": {
        "url": "https://www.bilibili.com/video/BV1gTo5BPEbV/",
        "reference_url": "https://www.youtube.com/watch?v=OHAjc-ayhus",
        "kind": "official_mv_repost_with_bilingual_subtitles",
    },
    "akane": {
        "url": "https://www.bilibili.com/video/BV1rL9cBzEaP/",
        "reference_url": "https://www.youtube.com/watch?v=VD_ztcqWBAY",
        "kind": "official_mv_repost",
    },
    "kai": {
        "url": "https://www.bilibili.com/video/BV1N9wFzPECt/",
        "reference_url": "https://www.youtube.com/watch?v=SIwfXPESJ8k",
        "kind": "authorized_official_mv_repost",
    },
    "chidori": {
        "url": "https://www.bilibili.com/video/BV18UPNzfEJH/",
        "reference_url": "https://www.youtube.com/watch?v=t75qlQPXJGw",
        "kind": "authorized_official_mv_repost",
    },
    "august-a-certain-moonlight": {
        "url": "https://www.bilibili.com/video/BV1mYqWBBERB/",
        "reference_url": "https://www.youtube.com/watch?v=Vs5NViM8TSY",
        "kind": "official_mv_repost_with_subtitles",
    },
    "shura": {
        "url": "https://www.bilibili.com/video/BV1pMtozHEsn/",
        "reference_url": "https://www.youtube.com/watch?v=h4F-q-R67H0",
        "kind": "authorized_official_mv_repost",
    },
    "kaseijin": {
        "url": "https://www.bilibili.com/video/BV1Vs5LzpEb3/",
        "reference_url": "https://www.youtube.com/watch?v=OLRbIc8KZ_8",
        "kind": "authorized_official_mv_repost",
    },
    "hebi": {
        "url": "https://www.bilibili.com/video/BV1upPveSEhr/",
        "reference_url": "https://www.youtube.com/watch?v=sf0QFJTvOLM",
        "kind": "authorized_official_mv_repost",
    },
    "taiyou": {
        "url": "https://www.bilibili.com/video/BV1WFUrB5EUc/",
        "reference_url": "https://www.youtube.com/watch?v=Qgj3xHRlGr8",
        "kind": "official_mv_repost",
    },
    "aporia": {
        "url": "https://www.bilibili.com/video/BV1Pp2JYXEBQ/",
        "reference_url": "https://www.youtube.com/watch?v=fhTFysCtF6g",
        "kind": "authorized_official_mv_repost",
    },
    "wasurete-kudasai": {
        "url": "https://www.bilibili.com/video/BV1QZ421T78c/",
        "reference_url": "https://www.youtube.com/watch?v=J_DE2d1F9wU",
        "kind": "authorized_official_mv_repost",
    },
    "gekkouyoku": {
        "url": "https://www.bilibili.com/video/BV13w411X7Ai/",
        "reference_url": "https://www.youtube.com/watch?v=wUzvF5xm2C0",
        "kind": "authorized_official_mv_repost",
    },
    "first-night": {
        "url": "https://www.bilibili.com/video/BV1Yh411P7uY/",
        "reference_url": "https://www.youtube.com/watch?v=-R8UiY_44Y0",
        "kind": "authorized_official_mv_repost",
    },
    "shayou": {
        "url": "https://www.bilibili.com/video/BV1c24y1M7yF/",
        "reference_url": "https://www.youtube.com/watch?v=bqigIHMComE",
        "kind": "authorized_official_mv_repost",
    },
    "four-fifty-one": {
        "url": "https://www.bilibili.com/video/BV1p24y1b7mK/",
        "reference_url": "https://www.youtube.com/watch?v=RmYdZZLOYA8",
        "kind": "authorized_official_mv_repost",
    },
    "telepath": {
        "url": "https://www.bilibili.com/video/BV1jy4y1X7bV/",
        "reference_url": "https://www.youtube.com/watch?v=LTeROfwwtnA",
        "kind": "official_mv_repost_4k60_with_subtitles",
    },
    "chinokate": {
        "url": "https://www.bilibili.com/video/BV1kg411S7y7/",
        "reference_url": "https://www.youtube.com/watch?v=Fq55MMfHoJg",
        "kind": "official_mv_repost",
    },
    "bremen": {
        "url": "https://www.bilibili.com/video/BV1x3CjBwEjy/",
        "reference_url": "https://www.youtube.com/watch?v=oy6MDr6I6rM",
        "kind": "official_mv_repost",
    },
    "eat-the-wind": {
        "url": "https://www.bilibili.com/video/BV1ki4y1L75R/",
        "reference_url": "https://www.youtube.com/watch?v=GVrRXhS0mLs",
        "kind": "official_label_upload",
    },
    "haruhisagi": {
        "url": "https://www.bilibili.com/video/BV1hV411r7xG/",
        "reference_url": "https://www.youtube.com/watch?v=F3cXxqgbx9Y",
        "kind": "official_mv_repost",
    },
    "semi-transparent-boy": {
        "url": "https://www.bilibili.com/video/BV1dW411W7iq/",
        "reference_url": "https://www.youtube.com/watch?v=9ypEFXTakV8",
        "kind": "authorized_official_mv_repost",
    },
    "cloud-and-ghost": {
        "url": "https://www.bilibili.com/video/BV1zs411T7ot/",
        "reference_url": "https://www.youtube.com/watch?v=JJaCwW4HyVs",
        "kind": "authorized_official_mv_repost",
    },
    "kutsu-no-hanabi": {
        "url": "https://www.bilibili.com/video/BV1Ax411U7RV/",
        "reference_url": "https://www.youtube.com/watch?v=BCt9lS_Uv_Y",
        "kind": "authorized_official_mv_repost",
    },
}

# Many album tracks do not have a standalone official music video. These
# candidates point to the exact part of a high-resolution full-album upload,
# so every link still opens the reviewed song instead of the album's first
# track. Standalone verified/video candidates keep higher priority below.
BILIBILI_ALBUM_VIDEO_SOURCES = {
    "nininsyou": {
        "url": "https://www.bilibili.com/video/BV1uDQBBWE54/",
        "release_title": "二人称",
        "reference_url": "https://yorushika.com/discography/artist/2/detail/75/",
        "uploader": "荒牧-Aramaki",
    },
    "gentou": {
        "url": "https://www.bilibili.com/video/BV1XTC1B4E16/",
        "release_title": "幻燈",
        "reference_url": "https://yorushika.com/discography/detail/30/",
        "uploader": "荒牧-Aramaki",
    },
    "sousaku": {
        "url": "https://www.bilibili.com/video/BV1sAUaBHEQ3/",
        "release_title": "創作",
        "reference_url": "https://yorushika.com/discography/detail/18/",
        "uploader": "荒牧-Aramaki",
    },
    "tousaku": {
        "url": "https://www.bilibili.com/video/BV1RH1eBNEbN/",
        "release_title": "盗作",
        "reference_url": "https://yorushika.com/discography/detail/15/",
        "uploader": "荒牧-Aramaki",
    },
    "elma": {
        "url": "https://www.bilibili.com/video/BV1HRWRzqE73/",
        "release_title": "エルマ",
        "reference_url": "https://yorushika.com/discography/detail/2/",
        "uploader": "荒牧-Aramaki",
    },
    "dakara-boku-wa-ongaku-wo-yameta": {
        "url": "https://www.bilibili.com/video/BV1gtWtz3ELo/",
        "release_title": "だから僕は音楽を辞めた",
        "reference_url": "https://yorushika.com/discography/detail/6/",
        "uploader": "荒牧-Aramaki",
    },
    "makeinu-ni-encore-wa-iranai": {
        "url": "https://www.bilibili.com/video/BV1x3Wmz9ESk/",
        "release_title": "負け犬にアンコールはいらない",
        "reference_url": "https://yorushika.com/discography/detail/7/",
        "uploader": "荒牧-Aramaki",
    },
    "natsukusa-ga-jama-wo-suru": {
        "url": "https://www.bilibili.com/video/BV1G2sZzeE6Z/",
        "release_title": "夏草が邪魔をする",
        "reference_url": "https://yorushika.com/discography/detail/8/",
        "uploader": "荒牧-Aramaki",
    },
}

_ALBUM_TRACK_PARTS_PENDING_REVIEW = {
    "early-morning-mailbox": ("nininsyou", 1),
    "kumo-ni-naru": ("nininsyou", 2),
    "hana-mo-zawameku": ("nininsyou", 3),
    "mashou": ("nininsyou", 4),
    "play-sick": ("nininsyou", 5),
    "post-haru": ("nininsyou", 6),
    "rubato": ("nininsyou", 12),
    "kasou": ("nininsyou", 13),
    "umeki": ("nininsyou", 16),
    "kitsutsuki": ("nininsyou", 17),
    "to-the-sea": ("nininsyou", 22),
    "summer-portrait": ("gentou", 1),
    "snow-country": ("gentou", 5),
    "pas-de-deux": ("gentou", 8),
    "old-man-and-the-sea": ("gentou", 11),
    "goodbye-molten": ("gentou", 12),
    "isana": ("gentou", 13),
    "second-night": ("gentou", 17),
    "third-night": ("gentou", 18),
    "fourth-night": ("gentou", 19),
    "fifth-night": ("gentou", 20),
    "sixth-night": ("gentou", 21),
    "seventh-night": ("gentou", 22),
    "eighth-night": ("gentou", 23),
    "ninth-night": ("gentou", 24),
    "tenth-night": ("gentou", 25),
    "robbery-and-bouquet": ("sousaku", 1),
    "creation": ("sousaku", 3),
    "music-thief-confession": ("tousaku", 1),
    "daytime-nighthawk": ("tousaku", 2),
    "bakudanma": ("tousaku", 4),
    "youth-burglary": ("tousaku", 5),
    "replicant": ("tousaku", 6),
    "midsummer-music-thief": ("tousaku", 8),
    "escape": ("tousaku", 11),
    "childhood-in-memories": ("tousaku", 12),
    "train-window": ("elma", 1),
    "only-sorrow": ("elma", 2),
    "evening-calm-flower-confusion": ("elma", 3),
    "lake-town": ("elma", 5),
    "dance-of-god": ("elma", 6),
    "rain-clears": ("elma", 7),
    "forest-church": ("elma", 10),
    "voice": ("elma", 11),
    "amy": ("elma", 12),
    "seabed-moonlight": ("elma", 13),
    "august-31": ("dakara-boku-wa-ongaku-wo-yameta", 1),
    "poet-and-coffee": ("dakara-boku-wa-ongaku-wo-yameta", 4),
    "july-13": ("dakara-boku-wa-ongaku-wo-yameta", 5),
    "lets-dance": ("dakara-boku-wa-ongaku-wo-yameta", 6),
    "june-writes-rain-cleared-city": (
        "dakara-boku-wa-ongaku-wo-yameta",
        7,
    ),
    "from-the-window-of-may": ("dakara-boku-wa-ongaku-wo-yameta", 8),
    "night-imitation": ("dakara-boku-wa-ongaku-wo-yameta", 9),
    "may-6": ("dakara-boku-wa-ongaku-wo-yameta", 10),
    "april-10": ("dakara-boku-wa-ongaku-wo-yameta", 13),
    "previous-life": ("makeinu-ni-encore-wa-iranai", 1),
    "makeinu-ni-encore-wa-iranai": (
        "makeinu-ni-encore-wa-iranai",
        2,
    ),
    "falling": ("makeinu-ni-encore-wa-iranai", 5),
    "hibernation": ("makeinu-ni-encore-wa-iranai", 8),
    "summer-bus-stop-waiting-for-you": (
        "makeinu-ni-encore-wa-iranai",
        9,
    ),
    "summer-shadow-playing-piano": ("natsukusa-ga-jama-wo-suru", 1),
    "cattleya": ("natsukusa-ga-jama-wo-suru", 2),
    "bloom-in-that-summer": ("natsukusa-ga-jama-wo-suru", 4),
    "flight": ("natsukusa-ga-jama-wo-suru", 5),
}

PENDING_REVIEW_BILIBILI_ALBUM_TRACK_CANDIDATES = {
    slug: {
        "url": (
            f"{BILIBILI_ALBUM_VIDEO_SOURCES[source_slug]['url']}"
            f"?p={part_number}"
        ),
        "reference_url": BILIBILI_ALBUM_VIDEO_SOURCES[source_slug][
            "reference_url"
        ],
        "kind": "hi_res_album_track",
        "release_title": BILIBILI_ALBUM_VIDEO_SOURCES[source_slug][
            "release_title"
        ],
        "uploader": BILIBILI_ALBUM_VIDEO_SOURCES[source_slug]["uploader"],
        "part": part_number,
    }
    for slug, (source_slug, part_number) in (
        _ALBUM_TRACK_PARTS_PENDING_REVIEW.items()
    )
}

BILIBILI_VIDEO_LINKS = {
    **{
        slug: candidate["url"]
        for slug, candidate in (
            PENDING_REVIEW_BILIBILI_ALBUM_TRACK_CANDIDATES.items()
        )
    },
    **VERIFIED_BILIBILI_VIDEOS,
    **{
        slug: candidate["url"]
        for slug, candidate in PENDING_REVIEW_BILIBILI_VIDEO_CANDIDATES.items()
    },
}


LEGACY_TRACK_SLUG_ALIASES = {
    "bakudanma-makeinu": "bakudanma",
    "bakudanma-tousaku": "bakudanma",
    "kutsu-no-hanabi-natsukusa": "kutsu-no-hanabi",
    "kutsu-no-hanabi-gentou": "kutsu-no-hanabi",
}


TRACK_DETAILS = {
    "early-morning-mailbox": ("", "器乐、序章与来信"),
    "to-the-sea": ("", "器乐、尾声与远行"),
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
            ("early-morning-mailbox", "早朝、郵便受け"),
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
            ("to-the-sea", "海へ"),
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
                    "mv_url": BILIBILI_VIDEO_LINKS.get(slug),
                }
            )

    return tuple(catalog)


CATALOG_TRACKS = _build_catalog_tracks()
