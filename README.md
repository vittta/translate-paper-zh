# Translate Paper ZH · 论文全文中文翻译

**让 Agent 把英文学术论文做成可检索的中文 PDF，并尽量保留原论文的双栏结构、公式、图表与引用。**

[English](README.en.md) · [skills.sh 页面](https://skills.sh/vittta/translate-paper-zh/translate-paper-zh) · [Skill instructions](SKILL.md) · [Layout guide](references/layout.md) · [Audit schema](references/manifest.md)

面向想认真读论文的研究者：正文、图注、表头、图内标注、脚注和附录都纳入翻译范围。优先使用原论文的 LaTeX 源码和会议模板；只有 PDF 时，由 Agent 规划文本区域或重建版面。最终交付包含可复制、可搜索的中文文字。

## 特点

- **双栏与学术版式**：优先保留论文实际使用的模板、标题层级、浮动图表和公式结构。
- **全文覆盖**：用源文清单逐项跟踪译文，图中的文字也进入检查范围。
- **数据与数学保真**：保留公式含义、实验数值、单位和引文，记录必要的保留项。
- **可检查的成品**：输出逐页预览、字体嵌入检查、遗漏候选、残留英文和审阅记录。
- **本地辅助工具**：四个 Python 工具不联网，不依赖外部翻译 API；译文由执行 Skill 的 Agent 完成。

这是一个由 Agent 执行的翻译、排版与审阅流程。原始模板和素材、可用工具以及实际审阅会影响结果；它允许增加页数来容纳中文，避免靠删减内容或缩小到难以阅读来强凑原页数。

## 成品展示

作者提供的 TTT（ICML 2020）中文译本：17 页，约 4.4 MB。下图是实际 PDF 页面，展示双栏正文、公式和中文图表标注。

[打开中文成品](examples/ttt-2020/chinese.pdf) · [原论文与署名](examples/ttt-2020/README.md)

![中文双栏首页](examples/ttt-2020/page-01.png)

![方法与公式](examples/ttt-2020/page-02.png)

![图表与中文标注](examples/ttt-2020/page-04.png)

本次发布查看了这些代表页并检查了全文件的文字可提取性。成品由作者提供，未在本次发布中重新运行全文翻译，也未据此声称所有内容经过独立语义复核。

## 安装

通过 Agent Skills CLI 安装：

```bash
npx skills add vittta/translate-paper-zh --skill translate-paper-zh
```

或者下载 [GitHub Releases](https://github.com/vittta/translate-paper-zh/releases) 中的 `translate-paper-zh.zip`，按所用 Agent 的 Skill 安装方式导入。

手动安装到 Codex 的示例：

```bash
git clone https://github.com/vittta/translate-paper-zh.git ~/.codex/skills/translate-paper-zh
```

此命令适用于目标目录尚不存在的情况。重新打开 Agent 或刷新 Skill 列表后使用。

## 环境

运行辅助工具需要 Python 3.10+：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

排版需要可嵌入的简体中文字体，例如 Noto Sans CJK SC 或 Noto Serif CJK SC。采用原始 LaTeX 路线时还需要 XeLaTeX 或 LuaLaTeX 及论文模板依赖；扫描件可能需要 OCR。字体、TeX 和 OCR 工具不随本包提供。

Skill 采用标准 `SKILL.md` 结构，包含 Codex 界面元数据。其他支持 Agent Skills 的环境可读取同一工作流程，但仍需具备本地文件、PDF 检查与排版能力；本仓库不声称完成了所有 Agent 的端到端验证。

## 使用

把论文 PDF 交给 Agent，并输入：

> 使用 $translate-paper-zh，把这篇论文全文翻译成简体中文 PDF。尽量保留原来的双栏排版、公式、图表、引用和附录；图内文字也要翻译。请逐页检查最终 PDF，确保中文可搜索、可复制，没有遮挡或溢出。

如果同时有对应版本的 LaTeX 源码，一并提供，可以帮助保留原论文模板。可在请求中指定术语表、保留哪些英文缩写、目标字体或附加源译对照。

输入是论文和必要素材；输出是中文 PDF，以及工作目录中的覆盖清单、审阅报告和逐页预览。把个人论文提供给 Agent 时，按该 Agent 的数据处理设置和自己的授权范围使用；辅助脚本自身不上传文件。

## 工具

| 工具 | 用途 |
| --- | --- |
| `scripts/paper_inventory.py` | 提取文本块、记录来源校验值并渲染源文页面 |
| `scripts/overlay_regions.py` | 将规划好的中文区域写入 PDF，保留图像与矢量图形；拒绝已检测到的区域冲突或溢出 |
| `scripts/audit_translation.py` | 检查译文覆盖、可检索文字、字体、残留英文和绑定当前文件的逐页审阅记录 |
| `scripts/optimize_pdf_fonts.py` | 仅在检查分辨率下逐页文字与像素保持一致、且文件变小时保存字体优化结果 |

使用参数和清单字段见 [manifest.md](references/manifest.md)。脚本不会自动翻译文字，也不会自动识别所有图内标注；译文忠实度和视觉审阅需要实际完成。

## 验证与反馈

公开版本附带辅助工具的冒烟检查，验证清单生成和未完成译文被审计拒绝等行为。它们检验工具行为，不替代真实论文的语义和视觉评测。

欢迎在 [Issues](https://github.com/vittta/translate-paper-zh/issues) 分享使用情况。报告排版问题时，请附上可公开的最小样例、Agent 环境、处理路线和问题页；分享成功案例时，请注明源文版本及有权公开的范围。

## 项目来源

该 Skill 来自作者对英文学术论文中文阅读与排版的实际需求，由 Agent 协作整理。调研过程中参考了 [academic-pdf-translation](https://github.com/ezra-y/academic-pdf-translation) 等公开项目，保留对它们的致谢；本项目的具体流程与辅助工具以此仓库内容为准。

论文的原作者、出版信息和素材权利属于各自权利人。Skill 的发布不改变论文和字体的授权范围。

## 许可证

Skill 指令和工具采用 [MIT](LICENSE)。论文示例及其译文按 examples 中的署名与 CC BY 4.0 说明单独处理，不适用代码的 MIT 许可。
