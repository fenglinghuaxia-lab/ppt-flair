# ppt-flair · 高层汇报金句页视觉 Skill

> 书法大字 + 纯 AI 底图 + 蒙版校色 —— 一条流水线产出高管级演示视觉。

`ppt-flair` 是一个 [WorkBuddy](https://www.workbuddy.cn) Skill，把「高层汇报封面 / 大会视觉 / 页内金句页」的设计流程固化为**六阶段可执行工作流**：需求解析自动选书风 → AI 书法标题生成 → 纯 AI 底图生成 → 抠图与水印清理 → 调色合成 → HTML 画廊交付。

**English**: A WorkBuddy skill that turns executive-deck quote pages into a repeatable pipeline — AI calligraphy titles × AI-generated backgrounds, 6 visual candidates per request.

## 核心交付规则（v1.0.0 定稿）

- **≥3 种书风 × ≥2 张底图 = 6 张视觉候选**，HTML 画廊一次交付
- 底图**纯 AI 生成**，版权干净、可安全公开分发；上暗下亮构图给标题让位
- 标题墨迹垂直中心位于画面 **36%** 高度（四轮实测校准定稿）
- 内置**墨迹 bbox 自动裁切**，规避 AI 导出 PNG 透明 padding 导致字位下沉的陷阱
- 铁律：定稿前必须多风格对比迭代

## 六阶段工作流

| 阶段 | 内容 | 产出 |
|------|------|------|
| 0 需求解析 | 按场合/情绪匹配书风矩阵（5 种书法风格库） | 书风推荐 ≥3 种 |
| A 标题生成 | 图生图锚定 + 书体硬锚点提示词 + 错字检查硬关卡 | ≥3 种书风标题 PNG |
| B 底图生成 | 纯 AI 生成，≥2 种风格方向，上暗下亮构图 | ≥2 张底图 |
| C 抠图清理 | 亮度抠图出透明标题 + 清理 AI 水印 | 透明 PNG + 干净底图 |
| D 调色合成 | 统一配方：饱和度 0.92 / 对比 1.06 / 蓝叠加 0.22 / 亮度 0.97 | 合成候选 |
| E 画廊交付 | 3×2 全组合 + HTML 画廊 | 6 张候选一次交付 |

## 工具链脚本

| 脚本 | 用途 |
|------|------|
| `scripts/keyout_title.py` | 黑底白字标题 → 透明 PNG（亮度抠图） |
| `scripts/compose_cover.py` | 合成：墨迹自动裁切 + 36% 定位 + 统一调色 |
| `scripts/build_gallery.py` | 多 PNG → 单文件 HTML 画廊（base64 内嵌） |

```bash
# 典型用法
python -X utf8 compose_cover.py --bg 底图.png --title 标题.png --out 成品.png
```

## 目录结构

```
ppt-flair/
├── SKILL.md                      # 主入口：六阶段工作流 + 全部规则
├── README.md
├── LICENSE                       # MIT
├── icon.png                      # 512×512 技能图标
├── references/                   # 决策清单 / 书风参考 / 底图提示词方向
├── assets/
│   ├── calligraphy-ref/          # 书风锚定参考图（图生图用）
│   └── examples/                 # 真实交付案例基准
└── scripts/                      # 工具链脚本
```

> `assets/backgrounds/` 素材库为本地可选组件，**公开版不含**（版权与体积考量），Stage B 一律纯 AI 生成底图。

## 安装

方式一：克隆本仓库到 WorkBuddy skills 目录

- 用户级（个人所有项目可用）：`~/.workbuddy/skills/ppt-flair/`
- 项目级（团队共享，随仓库分发）：`<workspace>/.workbuddy/skills/ppt-flair/`

方式二：下载 [Release](../../releases) 中的 `ppt-flair.zip`，解压到上述任一目录。

## 触发场景

说这些词自动启用：PPT汇报风格 / 总经理大会封面 / 书法字标题 / 高层汇报底版 / 金句页 / 领导汇报视觉 / 高级商务视觉

## 风格内核

- 深蓝黑底 + 低饱和暖/冷色叠加，禁霓虹色
- 书法大字标题（白色透明 PNG），墨迹中心位于画面 36% 高度
- 单视觉焦点，留白 ≥15%，强对比电影感

## License

MIT
