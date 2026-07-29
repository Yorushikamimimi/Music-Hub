"""Source-backed release stories kept separate from database catalog facts."""

from catalog_data import CATALOG_REVIEWED_ON


def _single_release_story(
    *,
    album_title,
    title_en,
    track_slug,
    official_summary,
    official_facts,
    editorial_note,
    chapter_title,
    chapter_description,
    official_release_url,
    context_sources=(),
    secondary_source_label=None,
    track_badge="Digital Single",
):
    """Build the shared archive shape without inventing album-style chapters."""
    story = {
        "album_title": album_title,
        "title_en": title_en,
        "sequence_number": "DS",
        "archive_label": "Digital Single",
        "source_checked_at": CATALOG_REVIEWED_ON,
        "official_summary": official_summary,
        "official_facts": official_facts,
        "editorial_note": editorial_note,
        "track_badges": {track_slug: track_badge},
        "chapters": (
            {
                "number": "01",
                "title": chapter_title,
                "description": chapter_description,
                "track_slugs": (track_slug,),
            },
        ),
        "sources": (
            {
                "label": "Yorushika 官方发行页",
                "url": official_release_url,
            },
            *context_sources,
        ),
    }
    if secondary_source_label:
        story["secondary_source_label"] = secondary_source_label
    return story


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
    "nininsyou": {
        "album_title": "二人称",
        "title_en": "Second Person",
        "sequence_number": "DA",
        "archive_label": "Digital Album · 22 Tracks",
        "source_checked_at": CATALOG_REVIEWED_ON,
        "official_summary": (
            "《二人称》是与同名书简型小说联动的 Digital Album。"
            "官方发售公告列出二十二首完整曲序：两首器乐作品分别位于"
            "开头与结尾，其间收录二十首歌曲。"
        ),
        "official_facts": (
            "2026 年 3 月 4 日以 Digital Album 形式发行。",
            "官方发售公告列出二十二首曲目，并说明作品与"
            "2026 年 2 月 26 日发行的书简型小说《二人称》联动。",
            "《早朝、郵便受け》与《海へ》是专辑开头和结尾的器乐作品；"
            "官方乐谱公告也明确区分这两首器乐与中间二十首歌曲。",
            "《プレイシック》在专辑发行前于 2025 年 12 月 22 日先行配信。",
        ),
        "editorial_note": (
            "本站把二十二首曲序完整保留，不把两首器乐从专辑中删掉。"
            "下面四段只是一条个人聆听路径：从投递与来信进入，"
            "经过明亮和冲撞，再沿着犹疑、动物与旧作回声走向海边。"
        ),
        "track_badges": {
            "early-morning-mailbox": "器乐序章",
            "play-sick": "先行单曲",
            "hitchcock": "再录音版",
            "to-the-sea": "器乐尾声",
        },
        "secondary_source_label": "完整曲序公告",
        "secondary_source_index": 1,
        "chapters": (
            {
                "number": "01",
                "title": "投递、云与春后",
                "description": (
                    "从清晨的邮筒声景进入，以云、花、魔性与春后的空气"
                    "建立这部作品最初的距离。"
                ),
                "track_slugs": (
                    "early-morning-mailbox",
                    "kumo-ni-naru",
                    "hana-mo-zawameku",
                    "mashou",
                    "play-sick",
                    "post-haru",
                ),
            },
            {
                "number": "02",
                "title": "太阳、遗忘与修罗",
                "description": (
                    "第二段把明亮、遗忘、紧张推进与陌生视角放在一起，"
                    "让情绪从晴朗表面转向更锋利的位置。"
                ),
                "track_slugs": (
                    "taiyou",
                    "haru",
                    "wasurete-kudasai",
                    "shura",
                    "kaseijin",
                ),
            },
            {
                "number": "03",
                "title": "速度、火与未解",
                "description": (
                    "从自由速度走向火葬、无解与蛇的形象，"
                    "最后在一声低沉的《うめき》中停顿。"
                ),
                "track_slugs": (
                    "rubato",
                    "kasou",
                    "aporia",
                    "hebi",
                    "umeki",
                ),
            },
            {
                "number": "04",
                "title": "旧歌、月光与海",
                "description": (
                    "尾段经过啄木鸟、再录音版《ヒッチコック》与月光，"
                    "再由《千鳥》《櫂》把专辑送向器乐尾声《海へ》。"
                ),
                "track_slugs": (
                    "kitsutsuki",
                    "hitchcock",
                    "gekkouyoku",
                    "chidori",
                    "kai",
                    "to-the-sea",
                ),
            },
        ),
        "sources": (
            {
                "label": "Yorushika 官方发行页",
                "url": "https://yorushika.com/discography/artist/2/detail/75/",
            },
            {
                "label": "Yorushika 二十二首完整曲序公告",
                "url": "https://yorushika.com/news/detail/11729",
            },
            {
                "label": "Yorushika 官方乐谱公告",
                "url": "https://yorushika.com/news/detail/11816",
            },
            {
                "label": "Universal Music《二人称》特设页",
                "url": "https://sp.universal-music.co.jp/yorushika/nininshou/",
            },
        ),
    },
    "abuku": _single_release_story(
        album_title="あぶく",
        title_en="Abuku",
        track_slug="abuku",
        official_summary=(
            "《あぶく》于 2026 年 4 月 22 日以 Digital Single 发行，"
            "并被采用为电视动画《LIAR GAME》的片头主题曲。"
        ),
        official_facts=(
            "2026 年 4 月 22 日以 Digital Single 形式发行。",
            "Yorushika 官方公告确认，本曲是电视动画"
            "《LIAR GAME》的片头主题曲。",
            "官方发行页只列出同名单曲一首。",
        ),
        editorial_note=(
            "本站把“浮起又消散”的轻盈感作为进入这首歌的个人入口，"
            "但不把曲名联想扩写成官方剧情。页面只保留公开发行信息、"
            "主题曲关系与一条聆听路径。"
        ),
        chapter_title="从浮起与消散之间进入",
        chapter_description=(
            "这一页只收录一首作品；点击曲名可继续查看发行资料与"
            "已经核对的影像入口。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/76/"
        ),
        context_sources=(
            {
                "label": "Yorushika 动画主题曲公告",
                "url": "https://yorushika.com/news/detail/11771",
            },
        ),
        secondary_source_label="动画主题曲公告",
    ),
    "akane": _single_release_story(
        album_title="茜",
        title_en="Akane",
        track_slug="akane",
        official_summary=(
            "《茜》于 2026 年 2 月 4 日以 Digital Single 发行，"
            "并作为剧场版《僕の心のヤバイやつ》的主题曲。"
        ),
        official_facts=(
            "2026 年 2 月 4 日以 Digital Single 形式发行。",
            "Yorushika 官方公告确认，本曲是剧场版"
            "《僕の心のヤバイやつ》的主题曲。",
            "官方发行页只列出同名单曲一首。",
        ),
        editorial_note=(
            "个人聆听时，可以把《茜》放在暮色刚刚改变颜色的时刻。"
            "本站只把这种色温感作为入口，不为电影或歌词补写"
            "未经官方公开的情节解释。"
        ),
        chapter_title="从暮色的色温进入",
        chapter_description=(
            "这一页只收录一首作品；官方主题曲关系与本站个人感受"
            "分别呈现。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/74/"
        ),
        context_sources=(
            {
                "label": "Yorushika 剧场版主题曲公告",
                "url": "https://yorushika.com/news/detail/11734",
            },
        ),
        secondary_source_label="剧场版主题曲公告",
    ),
    "play-sick": _single_release_story(
        album_title="プレイシック",
        title_en="Play Sick",
        track_slug="play-sick",
        official_summary=(
            "《プレイシック》于 2025 年 12 月 22 日先行配信，"
            "之后收录于 Digital Album《二人称》；"
            "官方公告同时标注其为 Daihatsu Move Canbus Stripes 的电视广告曲。"
        ),
        official_facts=(
            "2025 年 12 月 22 日以 Digital Single 形式先行发行。",
            "本曲后来收录于 2026 年 3 月 4 日发行的《二人称》。",
            "Yorushika 官方公告将其标注为 Daihatsu Move Canbus "
            "Stripes 的电视广告曲。",
        ),
        editorial_note=(
            "这首歌既可以作为单曲进入，也可以回到《二人称》的完整曲序。"
            "本站在单曲页只保留它作为先行入口的身份，"
            "不让广告合作信息取代作品本身。"
        ),
        chapter_title="从先行单曲回到整张作品",
        chapter_description=(
            "先单独听这一首，再从“收录作品”入口进入《二人称》的"
            "二十二首完整曲序。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/73/"
        ),
        context_sources=(
            {
                "label": "Yorushika《二人称》与先行配信公告",
                "url": "https://yorushika.com/news/detail/11729",
            },
        ),
        secondary_source_label="先行配信公告",
        track_badge="《二人称》先行单曲",
    ),
    "shura": _single_release_story(
        album_title="修羅",
        title_en="Shura",
        track_slug="shura",
        official_summary=(
            "《修羅》于 2025 年 8 月 8 日以 Digital Single 发行，"
            "并作为关西电视台月十剧《僕達はまだその星の校則を知らない》"
            "的主题曲。"
        ),
        official_facts=(
            "2025 年 8 月 8 日以 Digital Single 形式发行。",
            "Yorushika 官方公告确认，本曲是电视剧"
            "《僕達はまだその星の校則を知らない》的主题曲。",
            "官方发行页只列出同名单曲一首。",
        ),
        editorial_note=(
            "个人聆听时，这是一首适合从紧张推进感进入的作品。"
            "本站不借电视剧背景替歌曲下结论，只把合作信息"
            "作为可核对的公开事实。"
        ),
        chapter_title="从紧张推进的位置进入",
        chapter_description=(
            "这一页只收录一首作品；先听完整首歌，再回看它的"
            "电视剧主题曲背景。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/65/"
        ),
        context_sources=(
            {
                "label": "Yorushika 电视剧主题曲与配信公告",
                "url": "https://yorushika.com/news/detail/11697",
            },
        ),
        secondary_source_label="电视剧主题曲公告",
    ),
    "kaseijin": _single_release_story(
        album_title="火星人",
        title_en="Kaseijin",
        track_slug="kaseijin",
        official_summary=(
            "《火星人》于 2025 年 5 月 9 日以 Digital Single 发行，"
            "并被采用为电视动画《小市民シリーズ》第 2 季的片头主题曲。"
        ),
        official_facts=(
            "2025 年 5 月 9 日以 Digital Single 形式发行。",
            "Yorushika 官方公告确认，本曲是电视动画"
            "《小市民シリーズ》第 2 季的片头主题曲。",
            "官方发行页只列出同名单曲一首。",
        ),
        editorial_note=(
            "本站把“陌生人如何观看熟悉世界”当作一个个人聆听问题，"
            "而不是官方给出的答案。动画合作与发行日期仍单独列在"
            "可核对的事实区。"
        ),
        chapter_title="从陌生视角进入",
        chapter_description=(
            "这一页只收录一首作品；先从曲名带来的距离感开始，"
            "再查看官方动画合作信息。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/63/"
        ),
        context_sources=(
            {
                "label": "Yorushika 动画片头主题曲公告",
                "url": "https://yorushika.com/news/detail/11670",
            },
        ),
        secondary_source_label="动画片头主题曲公告",
    ),
    "hebi": _single_release_story(
        album_title="へび",
        title_en="Hebi",
        track_slug="hebi",
        official_summary=(
            "《へび》于 2025 年 1 月 17 日以 Digital Single 发行，"
            "并作为电视动画《チ。―地球の運動について―》的片尾曲。"
        ),
        official_facts=(
            "2025 年 1 月 17 日以 Digital Single 形式发行。",
            "Yorushika 官方公告确认，本曲是电视动画"
            "《チ。―地球の運動について―》的片尾曲。",
            "官方发行页只列出同名单曲一首。",
        ),
        editorial_note=(
            "个人聆听时，可以先注意歌曲留下的蜿蜒与悬置感。"
            "本站不把这种感受解释成动画剧情，只保留一条"
            "与《アポリア》并置聆听的入口。"
        ),
        chapter_title="沿着悬置感进入",
        chapter_description=(
            "这一页只收录一首作品；它也可以与同为该动画片尾曲的"
            "《アポリア》前后对照。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/61/"
        ),
        context_sources=(
            {
                "label": "Yorushika 动画片尾曲与配信公告",
                "url": "https://yorushika.com/news/detail/11659",
            },
        ),
        secondary_source_label="动画片尾曲公告",
    ),
    "taiyou": _single_release_story(
        album_title="太陽",
        title_en="Sun",
        track_slug="taiyou",
        official_summary=(
            "《太陽》于 2024 年 11 月 22 日以 Digital Single 发行，"
            "是电影《正体》的主题曲；其视觉企划与艺术总监永戸鉄也"
            "围绕同一主题分别创作，再在完成后汇合。"
        ),
        official_facts=(
            "2024 年 11 月 22 日以 Digital Single 形式发行。",
            "Yorushika 官方公告确认，本曲是电影《正体》的主题曲。",
            "官方展览说明记载，永戸鉄也与 Yorushika 先共享“太陽”主题，"
            "在不提前观看对方成品的情况下分别完成图像与音乐。",
        ),
        editorial_note=(
            "这首歌适合把“同一个主题如何生成不同作品”当作入口。"
            "本站把电影合作和联合视觉企划视作官方背景，"
            "而对声音明暗的感受仍明确属于个人笔记。"
        ),
        chapter_title="从同一主题的两种创作进入",
        chapter_description=(
            "先听歌曲，再查看官方展览记录中音乐与视觉各自生成、"
            "最后汇合的创作方式。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/57/"
        ),
        context_sources=(
            {
                "label": "Yorushika 电影主题曲与配信公告",
                "url": "https://yorushika.com/news/detail/11642",
            },
            {
                "label": "永戸鉄也 + Yorushika《太陽》官方特设页",
                "url": "https://yorushika.com/feature/exhibition_sun",
            },
        ),
        secondary_source_label="电影主题曲公告",
    ),
    "aporia": _single_release_story(
        album_title="アポリア",
        title_en="Aporia",
        track_slug="aporia",
        official_summary=(
            "《アポリア》于 2024 年 10 月 7 日以 Digital Single 发行，"
            "并作为电视动画《チ。―地球の運動について―》的片尾曲。"
        ),
        official_facts=(
            "2024 年 10 月 7 日以 Digital Single 形式发行。",
            "Yorushika 官方公告确认，本曲是电视动画"
            "《チ。―地球の運動について―》的片尾曲。",
            "官方发行页只列出同名单曲一首。",
        ),
        editorial_note=(
            "“Aporia”指向一个难以直接解开的困境。本站把这种"
            "悬而未决的状态当作个人聆听入口，不延伸为"
            "动画设定或歌词的唯一解释。"
        ),
        chapter_title="从未解的停顿进入",
        chapter_description=(
            "这一页只收录一首作品；可以继续与后来的片尾曲"
            "《へび》并置聆听。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/56/"
        ),
        context_sources=(
            {
                "label": "Yorushika 动画片尾曲公告",
                "url": "https://yorushika.com/news/detail/11625",
            },
        ),
        secondary_source_label="动画片尾曲公告",
    ),
    "wasurete-kudasai": _single_release_story(
        album_title="忘れてください",
        title_en="Wasurete Kudasai",
        track_slug="wasurete-kudasai",
        official_summary=(
            "《忘れてください》于 2024 年 7 月 13 日以 Digital Single "
            "形式发行；官方发行页只列出同名单曲一首。"
        ),
        official_facts=(
            "2024 年 7 月 13 日以 Digital Single 形式发行。",
            "Yorushika 官方发行页只列出同名单曲一首。",
            "当前官方发行资料没有为本曲附加专辑式章节或故事说明，"
            "本站因此不补写未经公开的背景设定。",
        ),
        editorial_note=(
            "本站把这首歌放在“如何面对被要求遗忘”这一私人问题旁边，"
            "而不把个人理解冒充成官方故事。它也可以回到"
            "《二人称》的完整曲序中重新聆听。"
        ),
        chapter_title="从克制的告别进入",
        chapter_description=(
            "这一页只收录一首作品；先保留一句标题的空白，"
            "再从收录作品入口回到《二人称》。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/52/"
        ),
        track_badge="后收录于《二人称》",
    ),
    "rubato": _single_release_story(
        album_title="ルバート",
        title_en="Rubato",
        track_slug="rubato",
        official_summary=(
            "《ルバート》于 2024 年 5 月 29 日以 Digital Single 发行；"
            "官方配信公告与发行页均把它作为同名单曲单独列出。"
        ),
        official_facts=(
            "2024 年 5 月 29 日以 Digital Single 形式发行。",
            "Yorushika 官方配信公告提供了 Apple Music 与 Spotify "
            "的预存入口。",
            "官方发行页只列出同名单曲一首。",
        ),
        editorial_note=(
            "Rubato 是速度可以自由伸缩的音乐术语。本站只把"
            "“速度如何呼吸”当作个人聆听入口，不据此断言"
            "歌曲存在官方概念设定。"
        ),
        chapter_title="从速度的伸缩进入",
        chapter_description=(
            "这一页只收录一首作品；先注意推进与停顿，"
            "再回到公开发行资料。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/50/"
        ),
        context_sources=(
            {
                "label": "Yorushika 官方配信公告",
                "url": "https://yorushika.com/news/detail/11598",
            },
        ),
        secondary_source_label="官方配信公告",
        track_badge="后收录于《二人称》",
    ),
    "gekkouyoku": _single_release_story(
        album_title="月光浴",
        title_en="Moonbath",
        track_slug="gekkouyoku",
        official_summary=(
            "《月光浴》于 2023 年 10 月 13 日以 Digital Single 发行，"
            "并作为剧场动画《大雪海のカイナ ほしのけんじゃ》的主题曲。"
        ),
        official_facts=(
            "2023 年 10 月 13 日以 Digital Single 形式发行。",
            "Yorushika 官方公告确认，本曲是剧场动画"
            "《大雪海のカイナ ほしのけんじゃ》的主题曲。",
            "本曲延续了 Yorushika 与《大雪海のカイナ》"
            "电视动画阶段的合作。",
        ),
        editorial_note=(
            "个人聆听时，可以把月光理解成一种照亮而不刺眼的距离。"
            "本站保留这一感受，同时把电影主题曲关系"
            "清楚放在官方事实区。"
        ),
        chapter_title="从月光照亮的距离进入",
        chapter_description=(
            "这一页只收录一首作品；也可以先听电视动画片头曲"
            "《テレパス》，再回到这首剧场版主题曲。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/47/"
        ),
        context_sources=(
            {
                "label": "Yorushika 剧场动画主题曲与配信公告",
                "url": "https://yorushika.com/news/detail/11552",
            },
        ),
        secondary_source_label="剧场动画主题曲公告",
        track_badge="剧场动画主题曲",
    ),
    "shayou": _single_release_story(
        album_title="斜陽",
        title_en="Shayou",
        track_slug="shayou",
        official_summary=(
            "《斜陽》于 2023 年 5 月 8 日以 Digital Single 发行，"
            "并作为电视动画《僕の心のヤバイやつ》的片头主题曲。"
        ),
        official_facts=(
            "2023 年 5 月 8 日以 Digital Single 形式发行。",
            "Yorushika 官方公告确认，本曲是电视动画"
            "《僕の心のヤバイやつ》的片头主题曲。",
            "官方发行页只列出同名单曲一首。",
        ),
        editorial_note=(
            "个人聆听时，斜阳既是明确的时间与光线，也会留下"
            "快要结束的感觉。本站只把这种暮色感作为入口，"
            "不把它写成动画剧情的标准答案。"
        ),
        chapter_title="从倾斜的暮光进入",
        chapter_description=(
            "这一页只收录一首作品；可以继续与剧场版主题曲"
            "《茜》形成前后对照。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/48/"
        ),
        context_sources=(
            {
                "label": "Yorushika 动画片头主题曲与配信公告",
                "url": "https://yorushika.com/news/detail/11520",
            },
        ),
        secondary_source_label="动画片头主题曲公告",
    ),
    "telepath": _single_release_story(
        album_title="テレパス",
        title_en="Telepath",
        track_slug="telepath",
        official_summary=(
            "《テレパス》于 2023 年 1 月 12 日以 Digital Single 发行，"
            "并作为电视动画《大雪海のカイナ》的片头主题曲。"
        ),
        official_facts=(
            "2023 年 1 月 12 日以 Digital Single 形式发行。",
            "Yorushika 官方公告确认，本曲是电视动画"
            "《大雪海のカイナ》的片头主题曲。",
            "官方发行页只列出同名单曲一首。",
        ),
        editorial_note=(
            "本站把“无法直接说出，却仍想传达到”的距离"
            "作为个人聆听入口。动画主题曲身份是公开事实，"
            "而这条理解路径不代表官方对歌曲的唯一说明。"
        ),
        chapter_title="从无法直说的距离进入",
        chapter_description=(
            "这一页只收录一首作品；之后可以继续进入"
            "同系列剧场动画主题曲《月光浴》。"
        ),
        official_release_url=(
            "https://yorushika.com/discography/artist/2/detail/46/"
        ),
        context_sources=(
            {
                "label": "Yorushika 动画片头主题曲与配信公告",
                "url": "https://yorushika.com/news/detail/11440",
            },
        ),
        secondary_source_label="动画片头主题曲公告",
    ),
}
