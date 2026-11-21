# pptx-stage-slides

> 表现层 Skill（模板可插拔）：给它一个 16:9 `.pptx` 模板，先确定性解析成**主题规格 theme spec 并经你确认**，再复刻成单个自包含、固定舞台、键盘翻页的 HTML 演讲页，确认后导出同版式 PDF。不写死任何品牌，换模板只换规格。

- 导航入口：[presentation-slides-skills](https://github.com/Valentina-Qiao/presentation-slides-skills)
- 内容拆页先用 [ppt-content-blueprint](https://github.com/Valentina-Qiao/ppt-content-blueprint)
- 若模板就是广州南方学院，用更快捷的特化版 [gznf-html-slides](https://github.com/Valentina-Qiao/gznf-html-slides)

## 它的特长

- **模板可插拔、不硬编码**：颜色字体全部走 `:root` CSS 变量，通用骨架 `boilerplate.generic.html` 按确认后的 theme spec 注入换肤。
- **确定性解析、不靠目测**：`scripts/inspect_pptx.py`（仅标准库）直接输出画幅/比例/是否 16:9、幻灯片数、主题色板、主次中英字体、媒体素材清单 JSON。
- **强制确认关**：制作前先把色板、字体、版式、素材形成 theme spec 给用户确认，避免方向错了大面积返工。
- **沉淀通用固定舞台工艺**：显隐铁规则、防溢出、翻页接口契约、关系箭头、编码页码、PDF 导出全部模板无关，换皮肤不换工艺。

## 负责解决什么问题

当你要套用的不是某一套固定模板，而是“每次一个新 PPTX”，靠肉眼取色、猜字体、对版式既慢又不准；本 Skill 把“解压 PPTX → 提取客观规格 → 人工确认 → 注入骨架 → 守工艺出页 → 导 PDF”做成标准流水线，保证新模板也能稳定复刻且不溢出、不裂图、不重影。

## 适用边界（本期硬性约束）

- 输入**仅支持 `.pptx`**；参考图片、手绘稿、现成 HTML 不在范围，遇到请用户提供 pptx。
- 画幅**仅做 16:9**：`inspect_pptx.py` 返回 `is_16_9=false` 时停止并告知，不自行拉伸；其他比例待后续版本。
- 内容结构来自 ppt-content-blueprint 的逐页蓝图，没有蓝图先做蓝图；本 Skill 不擅改文案。
- 广州南方学院这一已知模板优先用 gznf-html-slides，本 Skill 面向新模板。

## 工作流（7 步）

1. **解析模板**：`python3 scripts/inspect_pptx.py 模板.pptx` 取客观 JSON，再 unzip 看 slideMasters/slideLayouts 辨识封面/导航/章节/页码版式与 logo。
2. **生成 theme spec 并强制确认（不可跳过）**：按 `references/template-intake.md` schema 填色板/字体/舞台/各页型组件/素材，先呈现给用户确认；信息不足按提问清单问清，不猜。
3. **准备素材**：导出 logo/图片；云电脑用 `lark-cli drive +html-image-upload` 换不过期 URL，禁用 FileBatchUpload。
4. **注入规格搭骨架**：复制通用骨架，把确认后的色板/字体填入 `:root`，调整组件外观，保留舞台、显隐与翻页接口不变。
5. **按蓝图填充并守工艺**：遵循 `references/stagecraft.md`（安全高约 580px、并列禁箭头、虚线表未来、不删文案、对称等高、数据带口径）。
6. **交付前核对**：无重影、不超舞台、无裂图、页码连续、section 配平、UTF-8，只交付一个 `.html`。
7. **用户确认后导 PDF**：运行 `scripts/export_pdf.py`。

## 常用命令

```bash
# 1) 解析模板主题信息
python3 scripts/inspect_pptx.py template.pptx

# 2) 安装 PDF 依赖（另需系统 chromium、中文字体）
pip install pymupdf playwright

# 3) 确认 HTML 后导出 16:9 PDF；离线图片用 --map 替换
python3 scripts/export_pdf.py --html slides.html --out slides.pdf
python3 scripts/export_pdf.py --html s.html --out s.pdf \
  --map "https://host/logo.png|/abs/assets/logo.png"
```

## 常见问题与解决方案

- **模板不是 16:9 怎么办？** 脚本 `is_16_9=false` 时直接停下告知当前不支持，绝不拉伸变形；等后续支持其他画幅。
- **只有设计图/截图/现成 HTML，没有 pptx？** 本期不支持，请先拿到源 `.pptx` 再开工。
- **脚本提取不到某些颜色或字体？** 机器提取覆盖主题层，特殊版式需结合 unzip 看 slideLayouts；仍有歧义按 template-intake 的提问清单向用户确认，不凭感觉取值。
- **担心配色字体方向做错？** 这正是强制确认关的作用：theme spec 未经用户确认不进入制作，确认后颜色字体只允许来自 spec，不临时换色。
- **章节页/目录叠加重影？** 遵守显隐铁规则：`.slide.chapter{display:none}` + `.slide.chapter.active{display:grid}` + `.toc .chapter{display:grid}`；新增特殊 display 页型同步补非激活 `display:none`。
- **内容或流程图超舞台？** 按约 580px 安全高预算并留余量；复杂竖图用固定高容器 + `object-fit:contain` 锁高等比；超量拆页，不缩字号、不裁切、不删字。
- **图片裂图？** 云电脑用 lark-cli 换不过期 URL 且只用 `src` 引用；导 PDF 时可用 `--map` 临时换本地 file 资源，交付 HTML 仍保留在线 URL。
- **PDF 只出当前页/排版走样？** 不用浏览器打印或 LibreOffice，统一用 export_pdf.py（Playwright 逐页截图 + PyMuPDF 合成）；脚本依赖全局 `slides`/`show(i)`/`id=stage`，勿改名。
- **和 gznf-html-slides 怎么选？** 南院模板选 B（内置规格、跳过解析确认）；其他任意 16:9 pptx 选 C。

## 目录结构

```
pptx-stage-slides/
├─ SKILL.md
├─ assets/boilerplate.generic.html   # 中性通用骨架，颜色走 CSS 变量
├─ scripts/
│  ├─ inspect_pptx.py                # 解析 pptx 输出主题 JSON（标准库，已实测）
│  └─ export_pdf.py                  # 逐页截图合成 PDF（已实测，支持 --map）
└─ references/
   ├─ template-intake.md             # PPTX 结构、theme spec schema、确认话术、16:9 关卡
   ├─ stagecraft.md                  # 模板无关固定舞台工艺与避坑、交付检查清单
   └─ pdf-export.md                  # HTML→PDF 工艺、依赖与故障排查
```

## 边界

单文件自包含、原生 JS 无框架；仅 `.pptx` 输入、仅 16:9；theme spec 必须先确认；只交付一个最终 `.html`，用户确认后才导 PDF。
