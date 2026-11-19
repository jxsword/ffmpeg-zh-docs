# 翻译作品许可声明

> 本仓库（ffmpeg-zh-docs）包含两类不同许可的翻译内容，**分区标注、不混许可**。
> 工程代码（`scripts/`、`tests/`、CI 配置等）按仓库根 [LICENSE](LICENSE)（MIT）授权。

## 一、正文与 API 注释译本：LGPL-2.1-or-later

### 原作品许可

FFmpeg 官方文档（源码树 `doc/*.texi` 及 `libav*/`、`libswscale/`、`libswresample/` 公开头文件中的 Doxygen 注释）随 FFmpeg 源码树分发。官方 `.texi` 文件无单独许可声明（n9.0.2 全树核查，2026-11-19 实测），按 FFmpeg 源码树主许可 [LICENSE.md](https://github.com/FFmpeg/FFmpeg/blob/master/LICENSE.md) 的说明，推定适用 **GNU Lesser General Public License version 2.1 or later**（LGPL 2.1+）。

该推定的唯一开放确认项：已列为本项目 M4 动作——由维护者向 ffmpeg-devel 邮件列表书面询问官方文档许可意图，结论到达后回填决策记录（如有变更将更新本声明）。许可全文见仓库根 [COPYING.LGPLv2.1](COPYING.LGPLv2.1)。

### 翻译作品许可

本中文译本作为原作品的衍生作品，按 **LGPL-2.1-or-later** 提供：

- 译自 **FFmpeg n9.0.2 官方文档**（tag 日期 2026-09-18），各页面页脚与导航均注明翻译状态与基线版本；
- 保留原作品版权与许可声明；翻译贡献者按 LGPL-2.1-or-later 授权其翻译贡献；
- 再分发时须附带 LGPL 2.1 许可文本副本（或其链接）与翻译状态声明。

### API 注释译本的分区许可

API 注释随各源码文件的许可：绝大多数为 LGPL 2.1+；**libavfilter 有 40 个文件为 GPL**、`doc/examples` 下 24 个示例为 MIT——API 译本许可页将逐文件列明清单，各文件译文保留原许可，不统一改标。

## 二、wiki 精选页：CC BY-SA 3.0

社区精选页（站点 `/wiki/` 目录）译自 [FFmpeg Community Documentation Wiki](https://trac.ffmpeg.org/wiki)（Trac wiki），该 wiki 明示以 **[Creative Commons Attribution-ShareAlike 3.0](https://creativecommons.org/licenses/by-sa/3.0/)**（CC BY-SA 3.0）授权。

- 每页页脚固定标注：原文链接、快照日期、页面版本号，署名 **"Contributors to the FFmpeg Community Documentation Wiki"**；
- wiki 精选页与 LGPL 译本**分离标注**，再分发 wiki 译文须同样遵循 CC BY-SA 3.0 并给出署名与许可链接。

## 三、禁止与未触碰项

- **不搬运** [ffmpeg-web](https://git.ffmpeg.org/ffmpeg-web.git)（官网网站源码仓）的文案与设计资产——该仓无任何许可声明，本仓库不复制其内容；
- `doc/t2h.pm`、`doc/texi2pod.pl`（FFmpeg 源码树内 GPL 文件）：本仓库**未衍生、未修改、未再分发**，仅原样调用其所在构建环境；
- 官网生成页（如 `ffmpeg-all.html` 合集）以外部链接方式引用，不复制入站。

## 四、署名要求

使用本翻译作品时需包含：

1. **原作品声明**：FFmpeg 官方文档（FFmpeg contributors），基线版本 n9.0.2；
2. **译本许可声明**：本文件（或等效声明）与对应许可全文链接；
3. **翻译贡献者列表**：见 [AUTHORS_TRANSLATION.md](AUTHORS_TRANSLATION.md)；
4. **原文链接**：正文与 API 页每页页脚提供英文原文链接；wiki 页提供 Trac 原文链接与快照信息。

## 五、免责声明

本翻译仅供参考，**不保证完全准确**。如有歧义，**以英文原版为准**。翻译贡献者不对因使用本翻译造成的任何直接或间接损失负责。

## 贡献者授权

通过提交翻译 PR，贡献者同意：

1. 其翻译贡献按对应内容分区许可（正文/API 为 LGPL-2.1-or-later，wiki 页为 CC BY-SA 3.0）授权；
2. 授权本项目在上述许可下分发翻译作品；
3. 授权本项目维护者根据需要修改、整合翻译内容。

---

*声明版本：2026-11-20（M1 建仓）；基线：FFmpeg n9.0.2。如有法律疑问，请咨询专业法律顾问。*
