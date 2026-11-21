# pptx-stage-slides

**模板可插拔的通用表现层** Skill：给一个 16:9 `.pptx` 模板，先解析成主题规格 theme spec，经确认后复刻为单个自包含、固定舞台、键盘翻页的 HTML 演讲页，并导出同版式 PDF。不写死某一套品牌，换模板即可复用同一套工艺。

## 能力与边界

- 输入仅支持 `.pptx`；当前仅做 **16:9** 画幅（其他比例待后续扩展）。
- 内置**强制确认关**：theme spec（色板/字体/版式/logo）未经用户确认不批量制作。
- 内容拆页先用 [`ppt-content-blueprint`](https://github.com/Valentina-Qiao/ppt-content-blueprint) 出蓝图；本 Skill 不改文案。
- PDF 用 Playwright 逐页 `show(i)` 截 `#stage` + PyMuPDF 合成，禁用浏览器打印与 LibreOffice。

## 目录

- `SKILL.md`：PPTX 解析 → theme spec 确认 → 注入骨架 → 填充 → PDF 的完整流程。
- `references/`：`template-intake.md`（PPTX 结构/spec schema/确认关/16:9 关卡）、`stagecraft.md`（模板无关固定舞台工艺与避坑）、`pdf-export.md`。
- `assets/boilerplate.generic.html`：中性通用骨架，颜色全走 `:root` 变量。
- `scripts/inspect_pptx.py`：标准库解析 pptx 输出 JSON 主题信息。
- `scripts/export_pdf.py`：逐页截图合成 PDF 的参数化脚本。

## 配套 Skill

- 内容层（通用）：[`ppt-content-blueprint`](https://github.com/Valentina-Qiao/ppt-content-blueprint)
- 已知模板快捷通道（广州南方学院）：[`gznf-html-slides`](https://github.com/Valentina-Qiao/gznf-html-slides)
- 导航入口与总览：[`presentation-slides-skills`](https://github.com/Valentina-Qiao/presentation-slides-skills)
