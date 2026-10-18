# 第三方代码、字体与图像

本仓库的 MIT [LICENSE](LICENSE) 只覆盖维护者有权许可的原创程序代码，不把字体、图标、Bootstrap、专辑封面、艺人标识、歌词或音频改授为 MIT。依赖包继续遵守各自许可证；本仓库不包含私人音频库及生产数据库。本文不构成对第三方素材的授权。

## 随仓库分发的字体与样式

| 文件 | 实际版本证据 | 上游与完整原许可 |
| --- | --- | --- |
| `static/fonts/Outfit-{Light,Regular,SemiBold,Bold}.ttf` | 四份 name 表均为 `Version 1.100;gftools[0.9.27]`；版权为 Copyright 2021 The Outfit Project Authors | [Outfit 上游](https://github.com/Outfitio/Outfit-Fonts)，SIL OFL 1.1：[完整正文](static/fonts/OFL-Outfit.txt) |
| `static/fonts/bootstrap-icons.woff`、`.woff2` 及 `static/css/bootstrap-icons.css` | CSS 头标记 1.11.1；两个字体与上游 v1.11.1 逐字节一致 | [Bootstrap Icons v1.11.1](https://github.com/twbs/icons/tree/v1.11.1)，MIT：[原许可](static/fonts/LICENSE-bootstrap-icons.txt) |
| `static/css/bootstrap.min.css` | CSS 头标记 Bootstrap 5.3.0，保留原版权头 | [Bootstrap v5.3.0](https://github.com/twbs/bootstrap/tree/v5.3.0)，MIT：[原许可](static/css/LICENSE-bootstrap.txt) |

Outfit 的 OFL 文本取自上游提交 `902773808eb372f70fb34e8946dd1ffe604efc79` 的 `OFL.txt`，其版权行与本仓库字体内嵌版权一致。字体本身保留原字节；未证明这四份静态字体的具体生成批次与上游某一二进制发行逐字节相同，不能将字体版本号当成构建来源证明。OFL 允许使用和随软件分发，但须保留版权及许可、遵守独立销售与字体名称等条件，字体不能随应用改授 MIT。

字体文件 SHA-256（用于确认本次检查对象）：

- `Outfit-Light.ttf`：`643f64e9bfc140a9352ebf1b33958d5d5e0548ddc1bf7dc439e8da3df482473a`
- `Outfit-Regular.ttf`：`6a8c9be856a6b9e09c66615634904616152c9de5e44db343a3ced240479c586a`
- `Outfit-SemiBold.ttf`：`8900df5726b5a6f23e723594f11d5ea27e695bd85c884f18d88ed080544fe205`
- `Outfit-Bold.ttf`：`49dcdf653a004a2575b3de649f5e4c549d774fecddf317812330edd0ad70685a`
- `bootstrap-icons.woff`：`4d4572ef314e1b734cdd6485f913b0396d81bedf4d216a47cfde0cdf32a9316e`
- `bootstrap-icons.woff2`：`bacd70afda7da1deac2bbd49b5717a4dd133bcd59c379525d705b8492f678e95`

## 封面和艺人相关图像

用途仅为登录保护的个人非官方作品索引及聆听记录；这说明项目用途，不等于版权人授予使用或再分发许可。封面、名称与艺人相关标识的相关权利归原权利人，本项目 MIT 不覆盖它们。

本次核对 `static/images/` 的全部 42 份 WebP 和 2 份 SVG，未修改或删除原件。42 份 WebP 已作缩略图视觉检查，未见私人聊天、账号或个人文档；本地元数据检查未检出 EXIF 字段，仅有 WebP 容器的 loop/background 信息。这不是版权授权证明。

下表中的“官方资料页”来自源码 `catalog_data.py` 中的发行目录，是作品关联证据，不是图片原始下载 URL、逐像素来源验证或许可凭证。未保存可复核来源的历史图片保留未知。所有封面的公开再分发许可均**待核**；复用代码时应自行取得适用许可或换成有权使用的素材，不把 Public 仓库或官方网页可访问解释为授权。本轮只新增说明和许可文本，不新增封面或扩大私人站点访问。

| 文件（位于 `static/images/`） | 已有来源证据 | 许可 / 待核项 |
| --- | --- | --- |
| `algernon.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `deep_indigo.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `elma.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `flower_badger.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `gave_up_music.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `ghost_flower.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `hitchcock.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `hole_heart.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `left_right.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `nautilus.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `night_journey.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `parade.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `plagiarism.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `rain_cappuccino.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `release_abuku.webp` | [あぶく 官方资料页](https://yorushika.com/discography/artist/2/detail/76/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_akane.webp` | [茜 官方资料页](https://yorushika.com/discography/artist/2/detail/74/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_aporia.webp` | [アポリア 官方资料页](https://yorushika.com/discography/artist/2/detail/56/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_dakara_boku.webp` | [だから僕は音楽を辞めた 官方资料页](https://yorushika.com/discography/detail/6/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_elma.webp` | [エルマ 官方资料页](https://yorushika.com/discography/detail/2/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_gekkouyoku.webp` | [月光浴 官方资料页](https://yorushika.com/discography/artist/2/detail/47/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_gentou.webp` | [幻燈 官方资料页](https://yorushika.com/discography/detail/30/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_haru.webp` | [晴る 官方资料页](https://yorushika.com/discography/detail/37/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_hebi.webp` | [へび 官方资料页](https://yorushika.com/discography/artist/2/detail/61/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_kaseijin.webp` | [火星人 官方资料页](https://yorushika.com/discography/artist/2/detail/63/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_makeinu.webp` | [負け犬にアンコールはいらない 官方资料页](https://yorushika.com/discography/detail/7/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_natsukusa.webp` | [夏草が邪魔をする 官方资料页](https://yorushika.com/discography/detail/8/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_nininsyou.webp` | [二人称 官方资料页](https://yorushika.com/discography/artist/2/detail/75/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_play_sick.webp` | [プレイシック 官方资料页](https://yorushika.com/discography/artist/2/detail/73/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_rubato.webp` | [ルバート 官方资料页](https://yorushika.com/discography/artist/2/detail/50/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_shayou.webp` | [斜陽 官方资料页](https://yorushika.com/discography/artist/2/detail/48/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_shura.webp` | [修羅 官方资料页](https://yorushika.com/discography/artist/2/detail/65/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_sousaku.webp` | [創作 官方资料页](https://yorushika.com/discography/detail/18/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_taiyou.webp` | [太陽 官方资料页](https://yorushika.com/discography/artist/2/detail/57/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_telepath.webp` | [テレパス 官方资料页](https://yorushika.com/discography/artist/2/detail/46/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_tousaku.webp` | [盗作 官方资料页](https://yorushika.com/discography/detail/15/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `release_wasurete_kudasai.webp` | [忘れてください 官方资料页](https://yorushika.com/discography/artist/2/detail/52/)；源码关联 | 图像获取链与公开再分发许可待核 |
| `say_it.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `spring_thief.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `sunny.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `sunny_day.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `thoughtcrime.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `walking.webp` | 历史素材；未找到独立可复核的获取记录 | 图像获取链与公开再分发许可待核 |
| `yorushika-eye.svg` | 标题为 Yorushika eye mark；是艺人相关标识，未找到权利人许可凭证 | 原创/衍生归属和商标等使用范围待核；不纳入项目 MIT |
| `avatar-placeholder.svg` | 仓库历史中的通用头像占位矢量；未找到独立原始来源记录 | 来源待核，保守不纳入项目 MIT |

## 发布边界

本次许可维护只新增文本，不提供公开在线音乐演示、不提供歌曲下载、不把现有封面声明为可自由复用，也不把链接可达当作官方授权。若要发布含这些图片、音频的新下载包，或扩大为公开服务，应先补足对应素材来源与权利凭证；未核清部分保持 HOLD。
