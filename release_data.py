"""Source-backed release stories kept separate from database catalog facts."""

from catalog_data import CATALOG_REVIEWED_ON


RELEASE_STORIES = {
    "tousaku": {
        "album_title": "盗作",
        "title_en": "Plagiarism",
        "sequence_number": "03",
        "archive_label": "3rd Full Album · Concept Album",
        "source_checked_at": CATALOG_REVIEWED_ON,
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
        "secondary_source_index": 2,
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
                    "bakudanma",
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
        "source_checked_at": CATALOG_REVIEWED_ON,
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
        "secondary_source_index": 2,
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
    "elma": {
        "album_title": "エルマ",
        "title_en": "Elma",
        "sequence_number": "02",
        "archive_label": "2nd Full Album · Concept Album",
        "source_checked_at": CATALOG_REVIEWED_ON,
        "official_summary": (
            "官方将《エルマ》介绍为《だから僕は音楽を辞めた》的续篇："
            "エルマ受到青年书信影响，沿着他在瑞典留下的足迹旅行，"
            "并把这段旅程写成十四首作品。"
        ),
        "official_facts": (
            "2019 年 8 月 28 日发行，是 Yorushika 的第二张 Full Album，"
            "全作收录十四首曲目。",
            "官方特设页明确说明，本作与《だから僕は音楽を辞めた》"
            "在故事与曲序上互为一组。",
            "初回限定盘采用“エルマ写下的日记本”规格，"
            "随附她追随青年旅途拍摄的照片与日记。",
            "官方访谈将舞台设在瑞典，并说明两张专辑的曲目"
            "按顺序形成对应关系。",
        ),
        "editorial_note": (
            "如果前作是一封不断远去的信，《エルマ》更像收到信之后的回声。"
            "本站把曲序整理为出发、追随与抵达三段，重点观察雨、城市、脚步、"
            "声音与海底月光如何逐渐把エルマ带到故事终点。"
        ),
        "track_badges": {
            "train-window": "旅途节点",
            "lake-town": "旅途节点",
            "forest-church": "旅途节点",
            "seabed-moonlight": "旅途节点",
        },
        "secondary_source_label": "专辑特设页",
        "chapters": (
            {
                "number": "01",
                "title": "车窗、雨与出发",
                "description": (
                    "从车窗进入旅途，让雨、花与一杯卡布奇诺建立最初的观看距离。"
                ),
                "track_slugs": (
                    "train-window",
                    "only-sorrow",
                    "evening-calm-flower-confusion",
                    "rain-with-cappuccino",
                ),
            },
            {
                "number": "02",
                "title": "城市、舞步与追随",
                "description": (
                    "湖边城市与森林教堂成为路标，行走本身逐渐替代明确的答案。"
                ),
                "track_slugs": (
                    "lake-town",
                    "dance-of-god",
                    "rain-clears",
                    "walking",
                    "hole-in-the-heart",
                    "forest-church",
                ),
            },
            {
                "number": "03",
                "title": "声音、名字与终点",
                "description": (
                    "最后四首从声音与名字走向海底月光，并在《ノーチラス》收束旅程。"
                ),
                "track_slugs": (
                    "voice",
                    "amy",
                    "seabed-moonlight",
                    "nautilus",
                ),
            },
        ),
        "sources": (
            {
                "label": "Yorushika 官方发行页",
                "url": "https://yorushika.com/discography/detail/2/",
            },
            {
                "label": "Universal Music《エルマ》特设页",
                "url": "https://sp.universal-music.co.jp/yorushika/elma/",
            },
        ),
    },
    "gentou": {
        "album_title": "幻燈",
        "title_en": "Magic Lantern",
        "sequence_number": "MA",
        "archive_label": "Music Art Book · 2 Chapters",
        "source_checked_at": CATALOG_REVIEWED_ON,
        "official_summary": (
            "《幻燈》不是普通 CD 专辑，而是由 Yorushika 的音乐与"
            "加藤隆的绘画共同构成的“可聆听画集”；官方曲序分为"
            "“夏の肖像”与“踊る動物”两章，共二十五首。"
        ),
        "official_facts": (
            "2023 年 4 月 5 日发行，官方将作品类型标注为音乐画集。",
            "画集由加藤隆绘制的图像构成，音乐由 Yorushika 创作，"
            "每组作品从音乐与绘画两个方向表现同一主题。",
            "实体画集收录二十五首作品，分为“夏の肖像”十五首与"
            "“踊る動物”十首。",
            "官方说明本作没有 CD 版本；实体画集通过移动设备识别图像"
            "进入专用播放页面，数字发行版只包含其中部分曲目。",
        ),
        "editorial_note": (
            "这里保留官方两章结构，不把数字发行的十首误当成完整画集。"
            "第一章适合沿着文学、城市与夏日肖像逐首阅读，"
            "第二章则把十个夜晚作为另一套连续的观看节奏。"
        ),
        "track_badges": {
            "summer-portrait": "第一章起点",
            "first-night": "第二章起点",
        },
        "secondary_source_label": "音乐画集特设页",
        "chapters": (
            {
                "number": "01",
                "title": "夏の肖像",
                "description": (
                    "官方第一章共十五首，把夏日、城市、动物与文学题材放入同一组肖像。"
                ),
                "track_slugs": (
                    "summer-portrait",
                    "miyakoochi",
                    "bremen",
                    "chinokate",
                    "snow-country",
                    "howl-at-the-moon",
                    "four-fifty-one",
                    "pas-de-deux",
                    "matasaburo",
                    "kutsu-no-hanabi",
                    "old-man-and-the-sea",
                    "goodbye-molten",
                    "isana",
                    "left-right-confusion",
                    "algernon",
                ),
            },
            {
                "number": "02",
                "title": "踊る動物",
                "description": (
                    "官方第二章以第一夜至第十夜组成连续曲序，"
                    "本站不为这些曲目补写未经公开的故事。"
                ),
                "track_slugs": (
                    "first-night",
                    "second-night",
                    "third-night",
                    "fourth-night",
                    "fifth-night",
                    "sixth-night",
                    "seventh-night",
                    "eighth-night",
                    "ninth-night",
                    "tenth-night",
                ),
            },
        ),
        "sources": (
            {
                "label": "Yorushika 官方发行页",
                "url": "https://yorushika.com/discography/detail/30/",
            },
            {
                "label": "Universal Music《幻燈》特设页",
                "url": "https://sp.universal-music.co.jp/yorushika/gentou/",
            },
            {
                "label": "Yorushika 官方发售公告",
                "url": "https://yorushika.com/news/detail/11494",
            },
        ),
    },
    "sousaku": {
        "album_title": "創作",
        "title_en": "Creation",
        "sequence_number": "EP",
        "archive_label": "EP · Spring Theme",
        "source_checked_at": CATALOG_REVIEWED_ON,
        "official_summary": (
            "《創作》是一张以春为主题、与《盗作》保持概念联系的五曲 EP；"
            "它同时通过“有 CD”与“没有 CD”的两种同设计版本，"
            "追问数字聆听时代里实体媒介的意义。"
        ),
        "official_facts": (
            "2021 年 1 月 27 日发行，共收录五首作品。",
            "官方特设页把全作概括为以春为主题，并说明《創作》"
            "与《盗作》在概念上彼此相连。",
            "Type A 内含 CD；Type B 使用相同包装与歌卡，"
            "但不放入音源介质，被官方称为“没有 CD 的 CD”。",
            "曲序包含四首歌曲与器乐作品《創作》。",
        ),
        "editorial_note": (
            "五首曲目很短，却同时放进抢夺、花束、春风、创作行为与余韵。"
            "本站把它分为“取走与生成”和“风与月”两段，"
            "用来观察《盗作》之后的概念如何变得更轻、更开放。"
        ),
        "track_badges": {
            "creation": "器乐作品",
        },
        "secondary_source_label": "EP 特设页",
        "chapters": (
            {
                "number": "01",
                "title": "取走与生成",
                "description": (
                    "从强盗与花束进入春风，再由器乐曲《創作》把问题留在作品中央。"
                ),
                "track_slugs": (
                    "robbery-and-bouquet",
                    "spring-thief",
                    "creation",
                ),
            },
            {
                "number": "02",
                "title": "风与月的余韵",
                "description": (
                    "最后两首从风的移动走向月光，让春日主题在更安静的位置结束。"
                ),
                "track_slugs": (
                    "eat-the-wind",
                    "false-moon",
                ),
            },
        ),
        "sources": (
            {
                "label": "Yorushika 官方发行页",
                "url": "https://yorushika.com/discography/detail/18/",
            },
            {
                "label": "Universal Music《創作》特设页",
                "url": "https://sp.universal-music.co.jp/yorushika/sousaku/",
            },
        ),
    },
    "makeinu-ni-encore-wa-iranai": {
        "album_title": "負け犬にアンコールはいらない",
        "title_en": "Makeinu ni Encore wa Iranai",
        "sequence_number": "M2",
        "archive_label": "2nd Mini Album",
        "source_checked_at": CATALOG_REVIEWED_ON,
        "official_summary": (
            "Yorushika 的第二张 Mini Album 于 2018 年发行，"
            "九首曲目从《前世》展开，在《冬眠》与夏日公交站之间"
            "形成一条关于落下、透明感与季节回返的曲序。"
        ),
        "official_facts": (
            "2018 年 5 月 9 日发行，是 Yorushika 的第二张 Mini Album。",
            "初回生产限定盘与普通盘均收录九首曲目。",
            "初回生产限定盘使用 digipak，并附限定 booklet《生まれ変わり》。",
        ),
        "editorial_note": (
            "官方资料没有把九首曲目划成章节。本站沿着“前世—落下—冬眠”"
            "这些曲名中的动作与时间感分成三段，只作为一种聆听顺序，"
            "不把个人理解写成官方设定。"
        ),
        "track_badges": {
            "previous-life": "开篇",
            "summer-bus-stop-waiting-for-you": "尾声",
        },
        "secondary_source_label": "官方详细公告",
        "chapters": (
            {
                "number": "01",
                "title": "前世与失败者",
                "description": (
                    "前三首从前世进入标题曲与爆弾魔，先建立作品直接、急促的语气。"
                ),
                "track_slugs": (
                    "previous-life",
                    "makeinu-ni-encore-wa-iranai",
                    "bakudanma",
                ),
            },
            {
                "number": "02",
                "title": "提问、落下与透明",
                "description": (
                    "中段把提问、下坠和半透明的形象并置，让情绪从冲撞转向观察。"
                ),
                "track_slugs": (
                    "hitchcock",
                    "falling",
                    "semi-transparent-boy",
                ),
            },
            {
                "number": "03",
                "title": "晴日、冬眠与等待",
                "description": (
                    "最后从晴朗夏日跨到冬眠，再回到公交站的等待，形成季节回环。"
                ),
                "track_slugs": (
                    "just-a-sunny-day-for-you",
                    "hibernation",
                    "summer-bus-stop-waiting-for-you",
                ),
            },
        ),
        "sources": (
            {
                "label": "Yorushika 官方发行页",
                "url": "https://yorushika.com/discography/detail/7/",
            },
            {
                "label": "Yorushika 官方详细公告",
                "url": "https://yorushika.com/news/detail/10227",
            },
        ),
    },
    "natsukusa-ga-jama-wo-suru": {
        "album_title": "夏草が邪魔をする",
        "title_en": "Natsukusa ga Jama wo Suru",
        "sequence_number": "M1",
        "archive_label": "1st Mini Album",
        "source_checked_at": CATALOG_REVIEWED_ON,
        "official_summary": (
            "《夏草が邪魔をする》是 Yorushika 的第一张 Mini Album。"
            "七首曲目从夏日阴影与钢琴出发，经过表达、飞行与花火，"
            "最终停在云与幽灵的景象里。"
        ),
        "official_facts": (
            "2017 年 6 月 28 日发行，是 Yorushika 的第一张 Mini Album。",
            "官方发行页与发售公告均列出完整七首曲序。",
            "作品编号为 DUED-1223；本站只记录公开发行信息，"
            "不补写官方未公开的概念设定。",
        ),
        "editorial_note": (
            "这张早期作品已经能看到后来反复出现的夏、花、云与告别。"
            "下面的三段路径只沿曲名与曲序组织：先进入夏日，"
            "再从表达走向飞行，最后在花火和云层之间停下。"
        ),
        "track_badges": {
            "summer-shadow-playing-piano": "开篇",
            "cloud-and-ghost": "尾声",
        },
        "secondary_source_label": "官方发售公告",
        "chapters": (
            {
                "number": "01",
                "title": "夏阴与花",
                "description": (
                    "前两首用钢琴、夏日阴影与花打开 Yorushika 的第一张作品。"
                ),
                "track_slugs": (
                    "summer-shadow-playing-piano",
                    "cattleya",
                ),
            },
            {
                "number": "02",
                "title": "表达与飞行",
                "description": (
                    "中间三首从一句直接的表达出发，经过盛夏开放的景象走向飞行。"
                ),
                "track_slugs": (
                    "say-it",
                    "bloom-in-that-summer",
                    "flight",
                ),
            },
            {
                "number": "03",
                "title": "花火、云与幽灵",
                "description": (
                    "结尾两首把视线抬向夜空与云层，为整张作品留下悬而未决的余韵。"
                ),
                "track_slugs": (
                    "kutsu-no-hanabi",
                    "cloud-and-ghost",
                ),
            },
        ),
        "sources": (
            {
                "label": "Yorushika 官方发行页",
                "url": "https://yorushika.com/discography/detail/8/",
            },
            {
                "label": "Yorushika 官方发售公告",
                "url": "https://yorushika.com/news/detail/10005",
            },
        ),
    },
    "haru": {
        "album_title": "晴る",
        "title_en": "Sunny",
        "sequence_number": "DS",
        "archive_label": "Digital Single",
        "source_checked_at": CATALOG_REVIEWED_ON,
        "official_summary": (
            "《晴る》于 2024 年 1 月以 Digital Single 发行，"
            "并作为电视动画《葬送的芙莉莲》首季第 2 cour 的片头主题曲；"
            "官方介绍把它写成从尚未放晴之处望向晴空的作品。"
        ),
        "official_facts": (
            "2024 年 1 月 5 日以 Digital Single 形式发行。",
            "Universal Music 商品页将英文标题标注为《Sunny》。",
            "Universal Music 官方公告确认，本曲被采用为"
            "电视动画《葬送的芙莉莲》首季第 2 cour 的片头主题曲。",
        ),
        "editorial_note": (
            "单曲没有专辑式的章节结构。本站保留一个入口，"
            "把注意力放在“尚未放晴”与“正在走向晴朗”之间的变化，"
            "并把所有发行事实与个人感受明确分开。"
        ),
        "track_badges": {
            "haru": "Digital Single",
        },
        "secondary_source_label": "动画主题曲公告",
        "secondary_source_index": 2,
        "chapters": (
            {
                "number": "01",
                "title": "从阴云望向晴空",
                "description": (
                    "这一页只收录一首作品；点击曲名可查看发行资料与已核对影像入口。"
                ),
                "track_slugs": ("haru",),
            },
        ),
        "sources": (
            {
                "label": "Yorushika 官方发行页",
                "url": "https://yorushika.com/discography/detail/37/",
            },
            {
                "label": "Universal Music 数字发行页",
                "url": (
                    "https://www.universal-music.co.jp/yorushika/"
                    "products/up1as-02090/"
                ),
            },
            {
                "label": "Universal Music 动画主题曲公告",
                "url": (
                    "https://www.universal-music.co.jp/yorushika/"
                    "news/2023-12-23/"
                ),
            },
        ),
    },
}
