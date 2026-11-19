# FFmpeg 中文文档翻译贡献指南

感谢您对 FFmpeg 中文文档翻译项目的关注！本文档说明如何参与翻译贡献。

> 项目定位：跟随 FFmpeg release 节奏的**增量翻译体系**（当前基线 n9.0.2）。与一次性全册翻译不同，我们的核心机制是段落级 hash 对比 + 滤镜级拆页——上游出新版本后，只翻译变更内容。

## 角色与权限

| 角色 | 权限 | 获取方式 |
|------|------|----------|
| 翻译贡献者 | 认领段落/滤镜、提交翻译 PR | 任何人均可 |
| 审校员 | 审批翻译、合并 PR、维护术语表 | 连续 3 个 PR 通过后邀请 |
| 维护者 | 发布版本、管理 CI、处理增量同步 | 核心团队指定 |

## 快速开始

### 1. 环境准备

```bash
# Fork 仓库到您的 GitHub 账号后克隆
git clone https://github.com/YOUR_USERNAME/ffmpeg-zh-docs.git
cd ffmpeg-zh-docs

# 工具链（版本须与 source/UPSTREAM.json 记录一致，CI 会锁定比对）
#   texinfo >= 5（基线实测 7.2）、pandoc 3.7.0.2、doxygen 1.15.0、Python 3.11+
pip install -r requirements.txt
```

### 2. 认领翻译任务

1. 查看 [翻译任务看板](docs/translation-board.md)（按批次组织，批次粒度=单会话/单 PR 可完成）；
2. 评论认领："我来翻译 B3 批 filters/video 下的 `<滤镜名>` 小节"；
3. 创建分支：`git checkout -b translate/b3-filters-<名字>`；
4. 翻译对象 = `source/` 英文 md → `zh/` 对应中文 md（保持段落结构与 hash 对应）。

### 3. 翻译流程

```bash
# 1. 同步上游文档（通常由 CI 自动完成，手动重放）
python scripts/sync_docs.py --tag n9.0.2

# 2. 翻译（对照 style-guide.md 与 glossary.yml）
#    - 术语表未收录的术语：首次出现括注原文，并在 PR 中讨论入表
#    - 代码块/选项名/滤镜名/协议名/命令行示例整块保留英文

# 3. 本地校验
python scripts/validate_translation.py
python scripts/validate_structure.py

# 4. 提交 PR
git add zh/ && git commit -m "translate: B3 filters video 批次（<滤镜名列表>）"
```

### 4. 提交 PR 前自检清单

- [ ] 术语与 `config/glossary.yml` 一致（校验器 0 告警）
- [ ] 代码块、内联代码、选项名、命令行示例未翻译未改动
- [ ] 中文标点、语气符合 `config/style-guide.md`
- [ ] 段落结构与英文原文对应（无合并/拆分段落）
- [ ] PR 标题注明批次号与范围

## 翻译内容分区（许可注意）

| 内容区 | 位置 | 许可 |
|---|---|---|
| 正文（manual/components/filters/libraries/general） | `zh/` | LGPL-2.1-or-later（见 [LICENSE_TRANSLATION.md](LICENSE_TRANSLATION.md)） |
| API 注释 | `api/zh/` | 随源文件（LGPL 为主，libavfilter 部分 GPL） |
| wiki 精选页 | `zh/wiki/` | **CC BY-SA 3.0**（页脚署名块不可删改） |

wiki 页的页脚署名块是许可合规要求，贡献时不得删除或改写。

## 增量同步与冲突

- CI 每周一检测上游新稳定 tag；新版本进入站点新版本目录，未变段落自动保留译文；
- 您的 PR 期间上游若发布新基线：维护者会 rebase 您的分支，hash 未变的段落译文自动迁移，仅变更段需重译——请在 PR 中留意 reviewer 标注的 `changed` 段落；
- 大版本（major）发布时按分级响应：<10% 结构变化自动迁移 / 10-30% 半自动 / >30% 冻结+冲刺。

## 行为规范

- 讨论对事不对人；术语分歧以 glossary 评审结论为准；
- 不在译文 PR 中夹带无关改动（格式化、脚本修改请分开提）；
- 尊重上游：报告原文错误请到 [FFmpeg Trac](https://trac.ffmpeg.org/) 而非在译文里"顺手修正"。

---

*本指南随项目演进更新；重大变更会在 GitHub Discussions 公告。*
