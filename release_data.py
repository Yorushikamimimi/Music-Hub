"""Source-backed release stories kept separate from database catalog facts."""

from datetime import date


RELEASE_STORIES = {
    "tousaku": {
        "album_title": "盗作",
        "title_en": "Plagiarism",
        "sequence_number": "03",
        "archive_label": "3rd Full Album · Concept Album",
        "source_checked_at": date(2026, 7, 28),
        "official_summary": (
            "官方将《盗作》介绍为一张以“盗取音乐的男人”为主人公、"
            "把他的破坏冲动写入十四首曲目的概念专辑。"
        ),
        "official_facts": (
            "2020 年 7 月 29 日发行，是 Yorushika 的第三张 Full Album。",
            "全作收录十四首曲目，四段器乐过场穿插在十首歌曲之间。",
            "初回限定版采用书籍装帧，包含约 130 页小说《盗作》与一盘"
            "录有少年弹奏《月光奏鸣曲》的卡带。",
        ),
        "editorial_note": (
            "本站更愿意把《盗作》看成一段不断改变观看距离的叙事："
            "器乐过场像章节页，把自白、闯入、复制、逃亡与回望分隔开来。"
            "下面的三段路径是夜鹿集的个人整理，不是官方章节划分。"
        ),
        "interlude_slugs": (
            "music-thief-confession",
            "youth-burglary",
            "midsummer-music-thief",
            "childhood-in-memories",
        ),
        "chapters": (
            {
                "number": "01",
                "title": "自白与侵入",
                "description": (
                    "从一段自白进入白昼的偷窃现场，再以《爆弾魔》结束第一次冲撞。"
                ),
                "track_slugs": (
                    "music-thief-confession",
                    "daytime-nighthawk",
                    "haruhisagi",
                    "bakudanma-tousaku",
                ),
            },
            {
                "number": "02",
                "title": "复制与盛夏",
                "description": (
                    "第二段把青年期、复制品与创作者的自我审视放在同一条线上。"
                ),
                "track_slugs": (
                    "youth-burglary",
                    "replicant",
                    "flower-and-badger-game",
                    "midsummer-music-thief",
                    "plagiarism",
                    "thoughtcrime",
                ),
            },
            {
                "number": "03",
                "title": "逃亡与回望",
                "description": (
                    "最后从逃离转向童年、夜路与初夏，让破坏之后留下的记忆重新显形。"
                ),
                "track_slugs": (
                    "escape",
                    "childhood-in-memories",
                    "night-journey",
                    "ghost-in-a-flower",
                ),
            },
        ),
        "sources": (
            {
                "label": "Yorushika 官方发行页",
                "url": "https://yorushika.com/discography/detail/15/",
            },
            {
                "label": "Yorushika 官方发售公告",
                "url": "https://yorushika.com/news/detail/11126",
            },
            {
                "label": "Universal Music《盗作》特设页",
                "url": "https://sp.universal-music.co.jp/yorushika/tousaku/",
            },
        ),
    },
}


RELEASE_SLUGS_BY_TITLE = {
    release["album_title"]: slug
    for slug, release in RELEASE_STORIES.items()
}
