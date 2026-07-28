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
        "track_badges": {
            "music-thief-confession": "器乐过场",
            "youth-burglary": "器乐过场",
            "midsummer-music-thief": "器乐过场",
            "childhood-in-memories": "器乐过场",
        },
        "secondary_source_label": "专辑特设页",
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
    "dakara-boku-wa-ongaku-wo-yameta": {
        "album_title": "だから僕は音楽を辞めた",
        "title_en": "That's Why I Gave Up on Music",
        "sequence_number": "01",
        "archive_label": "1st Full Album · Concept Album",
        "source_checked_at": date(2026, 7, 28),
        "official_summary": (
            "官方发行页将本作列为 Yorushika 的首张 Full Album；"
            "后续《エルマ》特设页进一步说明，两张作品以书信、旅行与"
            "成对曲序连接，本作收录青年在瑞典旅途中写给エルマ的十四首作品。"
        ),
        "official_facts": (
            "2019 年 4 月 10 日发行，是 Yorushika 的首张 Full Album，"
            "全作收录十四首曲目。",
            "初回生产限定盘采用“写给エルマ的信”复原盒装，"
            "把音乐之外的书信也纳入作品体验。",
            "官方访谈将故事舞台设在瑞典：青年一边旅行，"
            "一边创作寄给エルマ的歌曲；后续《エルマ》沿着他的足迹展开。",
            "《だから僕は音楽を辞めた》与《エルマ》各有十四首曲目，"
            "标题顺序与叙事线索彼此成对。",
        ),
        "editorial_note": (
            "本站把四个日期曲目视作旅途中的时间戳：八月打开书信，"
            "七月到五月让创作与城市景象不断回返，四月则把故事送向最后的告别。"
            "下面的三段路径是夜鹿集的个人整理，不是官方章节划分。"
        ),
        "track_badges": {
            "august-31": "日期节点",
            "july-13": "日期节点",
            "may-6": "日期节点",
            "april-10": "日期节点",
        },
        "secondary_source_label": "双作关系特设页",
        "chapters": (
            {
                "number": "01",
                "title": "八月与出发",
                "description": (
                    "从 8/31 进入青年写作的起点，再把月光、诗与咖啡留在旅途开篇。"
                ),
                "track_slugs": (
                    "august-31",
                    "deep-indigo",
                    "august-a-certain-moonlight",
                    "poet-and-coffee",
                ),
            },
            {
                "number": "02",
                "title": "季节与创作",
                "description": (
                    "日期从七月走向五月，城市、雨后与写作的冲动在途中反复出现。"
                ),
                "track_slugs": (
                    "july-13",
                    "lets-dance",
                    "june-writes-rain-cleared-city",
                    "from-the-window-of-may",
                    "night-imitation",
                    "may-6",
                ),
            },
            {
                "number": "03",
                "title": "写给エルマ的告别",
                "description": (
                    "最后四首把游行、名字、四月的时间点与放下音乐的决定连在一起。"
                ),
                "track_slugs": (
                    "parade",
                    "elma",
                    "april-10",
                    "thats-why-i-gave-up-on-music",
                ),
            },
        ),
        "sources": (
            {
                "label": "Yorushika 官方发行页",
                "url": "https://yorushika.com/discography/detail/6/",
            },
            {
                "label": "Universal Music 初回限定盘商品页",
                "url": "https://store.universal-music.co.jp/products/dued1266",
            },
            {
                "label": "Universal Music《エルマ》特设页",
                "url": "https://sp.universal-music.co.jp/yorushika/elma/",
            },
        ),
    },
}


RELEASE_SLUGS_BY_TITLE = {
    release["album_title"]: slug
    for slug, release in RELEASE_STORIES.items()
}
