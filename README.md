# Overseas AIRP Hotspot Cards

将美国、英国、加拿大、澳大利亚、德国、新西兰和俄罗斯的真实高热事件，转换为原创英文 AIRP Bot 卡，并把热点证据、候选事件和完整制卡资产写入同一个 Excel 总表。

## 这个仓库包含什么

```text
skills/overseas-airp-hotspot-cards/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── research-and-heat.md
│   ├── card-design.md
│   └── workbook-schema.md
└── scripts/build_workbook.py

templates/海外AIRP热点制卡总表-空白.xlsx
examples/sample-run.json
dist/overseas-airp-hotspot-cards.zip
```

`skills/overseas-airp-hotspot-cards/` 是真正需要安装的 Skill。Word 或 PDF 说明文档不能代替这个目录。

## Codex 安装

### 方式一：从 GitHub 安装（推荐）

在 Codex 中发送：

```text
$skill-installer

请从这个 GitHub 地址安装 Skill：
https://github.com/kkky-ai/overseas-airp-hotspot-cards/tree/main/skills/overseas-airp-hotspot-cards
```

仓库为 Private 时，安装者必须拥有仓库访问权限，并在本机配置 GitHub 凭据。安装成功后，新开一个对话即可使用。

### 方式二：ZIP 安装

1. 下载 `dist/overseas-airp-hotspot-cards.zip`。
2. 解压后，将 `overseas-airp-hotspot-cards` 整个文件夹放入：
   - Codex 默认：`~/.codex/skills/`
   - 其他支持 Agent Skills 的工具：放入该工具指定的 Skill 目录。
3. 重启 Codex，或重新打开会话。

安装后应存在：

```text
~/.codex/skills/overseas-airp-hotspot-cards/SKILL.md
```

## 使用

在新对话中输入：

```text
$overseas-airp-hotspot-cards

搜索截至今天最近 7 天真正热门的海外事件，制作 5 个 AIRP Bot。
不要为了凑数降低热度门槛。将所有候选、证据和卡片资产追加到：
/Users/你的用户名/Desktop/海外AIRP热点制卡总表.xlsx
```

也可以指定国家、题材、时间范围或现有总表：

```text
$overseas-airp-hotspot-cards

只研究最近 72 小时美国和英国真正破圈的娱乐与社交媒体热点，
制作最多 3 个恋爱向 Bot，追加到现有 Excel，避免重复 Event ID。
```

## 热度门槛

正式制卡要求同时满足：

- 加权热度分至少 70；
- 有可靠事实来源；
- 至少两类独立热度证据；
- 满足跨媒体、社媒、搜索、榜单或相对市场破圈模式之一；
- 小众单篇报道、无数字的“viral”宣传和无法核实的截图不进入正式制卡池。

如果合格事件不足，宁可少产出，也不以小众内容凑数。

## Excel 输出

Skill 生成的工作簿包含：

- `Bots`：一行一个 Bot；
- `热点候选`：合格、观察和淘汰事件；
- `热度证据`：媒体、社媒、搜索和榜单证据；
- `卡片视图`：按照字段纵排、Bot 横向扩展；
- `运行记录`：每批执行记录；
- `字段说明`：数据口径。

生成脚本需要 Python 3 和 `openpyxl`：

```bash
python3 -m pip install -r requirements.txt
python3 skills/overseas-airp-hotspot-cards/scripts/build_workbook.py \
  --input examples/sample-run.json \
  --output output.xlsx
```

## 在其他 Agent 中使用

只有支持 Agent Skills 或能够读取目录、联网研究并执行 Python 的 Agent，才能完整运行此项目。若目标 Agent 不支持 Skill 安装，可以把 `SKILL.md` 和 `references/` 提供给它作为工作流指令，但它可能无法自动运行 Excel 脚本，也不会出现 `$overseas-airp-hotspot-cards` 调用入口。

## 更新与版本

GitHub 仓库是唯一源码。修改后重新生成 ZIP，不要直接编辑 `dist/` 中的副本。正式业务生成的 Excel 不提交到仓库，避免把数据和 Skill 源码混在一起。
