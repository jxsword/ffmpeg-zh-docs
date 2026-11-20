# 简介

本文档旨在提供一组常用 Git 命令的快速参考。您应始终使用 Git 自带的详尽文档：

``` text
git --help
man git
```

列出可用的子命令，

``` text
git <command> --help
man git-<command>
```

显示有关 \<command\> 子命令的信息。

更多信息可参考 [Git Reference](http://gitref.org) 网站。

想进一步了解 Git 项目，请访问 [Git 网站](http://git-scm.com/)。

遇到问题时请查阅这些资源，它们相当详尽。

接下来是对 Git 的基础介绍，以及一些便于向本项目贡献的 FFmpeg 专属指南。

# 基本用法

## 获取 Git

您可以从 <http://git-scm.com/> 获取 Git。多数发行版和操作系统都提供相应软件包。

## 克隆源码树

``` text
git clone https://git.ffmpeg.org/ffmpeg.git <target>
```

这会把 FFmpeg 源码放入 \<\<target\>\> 目录。

``` text
git clone git@source.ffmpeg.org:ffmpeg <target>
```

这会把 FFmpeg 源码放入 \<\<target\>\> 目录，并允许您将修改推送回远程仓库。

``` text
git clone git@ffmpeg.org:ffmpeg-web <target>
```

这会把 FFmpeg 网站源码放入 \<\<target\>\> 目录，并允许您将修改推送回远程仓库。

如果您对 ffmpeg-web 仓库没有写权限，可以只读克隆 ffmpeg-web 后制作补丁：

``` text
git clone git://ffmpeg.org/ffmpeg-web <target>
```

请确保您的检出中没有 Windows 换行符，否则可能遇到莫名其妙的编译失败。一种做法是运行

``` text
git config --global core.autocrlf false
```

## 将源码树更新到最新版本

``` text
git pull (--rebase)
```

会拉取被跟踪分支的最新变更。被跟踪分支可以是远程分支。默认情况下，master 分支跟踪远程 origin 的 master 分支。

推荐 `--rebase`（见下文）。

## 变基本地分支

``` text
git pull --rebase
```

从主仓库拉取变更并把您的本地提交在其上重放。这是让所有本地修改保持在 FFmpeg master 树顶端的必要操作。master 树会拒绝带合并提交的推送。

## 添加/删除文件/目录

``` text
git add [-A] <filename/dirname>
git rm [-r] <filename/dirname>
```

Git 需要得到通知才能知晓您对工作目录所做的、使文件出现或消失的所有变更。跨文件移动行会被自动跟踪。

## 查看修改

``` text
git diff <filename(s)>
```

会以 unified diff 形式显示工作目录中的所有本地修改。

## 查看变更日志

``` text
git log <filename(s)>
```

您也可以使用 `gitview` 或 `gitk` 等图形工具，或访问 <https://git.ffmpeg.org/ffmpeg.git> 的网页界面。

## 检查源码树状态

``` text
git status
```

检出所有您所做的变更，并列举一旦提交将采取的动作（新增、修改、删除等）。

## 提交

``` text
git diff --check
```

在提交前复查您的修改，避免日后惹上麻烦。所有有经验的开发者在每次提交前都这样做，无论修改多小。

他们每个人都曾多次靠这一步免于闹笑话。杂散的调试输出或外观性修改很容易混进去，请通过这层额外把关避免麻烦。

对于纯外观性提交，以下命令的输出应当（几乎）为空：

``` text
git diff -w -b <filename(s)>
```

另请检查

``` text
git status
```

的输出，确认没有未跟踪文件或删除项。

``` text
git add [-i|-p|-A] <filenames/dirnames>
```

确保已告知 Git 您的姓名、邮箱地址和 GPG 密钥

``` text
git config --global user.name "My Name"
git config --global user.email my@email.invalid
git config --global user.signingkey ABCDEF0123245
```

启用对所有提交签名，或使用 -S

``` text
git config --global commit.gpgsign true
```

使用 `--global` 为您所有的 Git 检出设置全局配置。

Git 会为提交挑选对文件的修改。可选地，您可以用交互模式或补丁模式逐块（hunk）挑选要纳入提交的内容。

``` text
git commit
```

Git 会把选中的修改提交到您当前的本地分支。

您将在编辑器中被提示填写日志信息。编辑器既可在个人配置文件中通过

``` text
git config --global core.editor
```

指定，或由以下环境变量指定：\<GIT_EDITOR\>、\<VISUAL\> 或 \<EDITOR\>。

## 编写提交信息

日志信息应简洁而具有描述性。

首行必须包含上下文、冒号和对其所做修改的极简摘要。必要时可在空一行后补充细节，细节部分每行不超过 60-72 字符（含代码时除外）。

优秀提交信息示例：

``` text
avcodec/cbs: add a helper to read extradata within packet side data

Using ff_cbs_read() on the raw buffer will not parse it as extradata,
resulting in parsing errors for example when handling ISOBMFF avcC.
This helper works around that.
```

``` text
ptr might be NULL
```

如果首行摘要不够，在正文中说明您为什么做该修改——您做了什么，多数时候从修改本身就能看出来。只说"缺陷修复"或"10l"是不好的。要记住：不同水平的读者会阅读并学习您的代码。除上下文外不要在日志信息中包含文件名，Git 会提供该信息。

如果提交修复了已登记的问题，在正文单独一行注明：`Fix Trac ticket #42.`

首行会被 `git format-patch` 用作补丁名。

`git log --oneline` 中常见的首行错误包括：开头缺上下文；描述的是补丁前的旧行为；首行过长或折到第二行。

## 准备补丁集

``` text
git format-patch <commit> [-o directory]
```

会为 \<\<commit\>\> 与当前 \<HEAD\> 之间的每个提交生成一组补丁。例如

``` text
git format-patch origin/master
```

会为当前分支上所有不在上游的提交生成补丁。另一个实用的快捷方式是

``` text
git format-patch -n
```

它会为最近 \<n\> 个提交生成补丁。默认情况下，补丁创建在当前目录。

## 发送补丁供评审

``` text
git send-email <commit list|directory>
```

会发送 `git format-patch` 创建的补丁，或直接生成补丁并发送。所有邮件字段都可在全局/本地配置中设置，或用命令行覆盖。注意该工具通常需要单独安装（如 Debian 系发行版的 \<git-email\> 包）。

## 重命名/移动/复制文件或文件内容

Git 会自动跟踪此类变更，使其成为普通提交。

``` text
mv/cp path/file otherpath/otherfile
git add [-A] .
git commit
```

# Git 配置

为简化若干工作流，建议同时配置您的个人 Git 安装和本地 FFmpeg 仓库。

## 个人 Git 安装

将以下内容加入您的 `~/.gitconfig`，帮助 `git send-email` 和 `git format-patch` 检测重命名：

``` text
[diff]
        renames = copy
```

## 仓库配置

为了让 `git send-email` 自动把补丁发到 ffmpeg-devel 邮件列表，向 `/path/to/ffmpeg/repository/.git/config` 添加以下配置段：

``` text
[sendemail]
        to = ffmpeg-devel@ffmpeg.org
```

# FFmpeg 专属内容

## 回退损坏的提交

``` text
git reset <commit>
```

`git reset` 会撤销直至 \<\<commit\>\> 的提交，并重写当前分支的历史。

``` text
git commit --amend
```

可快速修订最后一次提交的详情。

``` text
git rebase -i origin/master
```

会在主仓库之上重放本地提交，过程中允许编辑、合并或移除其中部分提交。

`git reset`、`git commit --amend` 与 `git rebase` 都会改写历史，因此只应在您的本地分支或主题分支上使用它们。主仓库会拒绝这些修改。

``` text
git revert <commit>
```

`git revert` 会生成一个回退提交。这不会让问题提交从历史中消失。

## 把修改推送到远程树

``` text
git push origin master --dry-run
```

会模拟把本地 master 分支推送到默认远程（\<origin\>），并列出将被推送的分支、范围或提交。本地与远程树不同步时，Git 会阻止推送。参见[将源码树更新到最新版本](#将源码树更新到最新版本)。

``` text
git remote add <name> <url>
```

会添加一个带名称引用的额外远程，若您想把本地分支推送到远程主机供评审，这会很有用。

``` text
git push <remote> <refspec>
```

会把修改推送到 \<\<remote\>\> 仓库。省略 \<\<refspec\>\> 会让 `git push` 更新所有与本地对应的远程分支。

## 查找特定的 svn 版本

自 1.7.1 版起，Git 支持 `:/foo` 语法按正则表达式指定提交。参见 man gitrevisions

``` text
git show :/'as revision 23456'
```

会显示 svn 变更集 `r23456`。更早的 Git 版本在 `git log` 输出中搜索是最简单的办法（尤其在使用支持搜索的分页器时）。

可以用以下命令检出该提交

``` text
git checkout -b svn_23456 :/'as revision 23456'
```

或 Git \< 1.7.1 用

``` text
git checkout -b svn_23456 $SHA1
```

其中 \<\$SHA1\> 是 `git log` 输出中的提交哈希。

# gpg 密钥生成

如果您还没有 gpg 密钥，我们推荐创建基于 ed25519 的密钥，它小、快、安全，尤其能让 git 中的签名很小。

``` text
gpg --default-new-key-algo "ed25519/cert,sign+cv25519/encr" --quick-generate-key "human@server.com"
```

生成密钥时，请确保所指定的邮箱与 git 中使用的一致——GitHub 等站点会把不匹配视为将提交标记为未验证的理由。生成密钥后，您可以将其加入 MAINTAINER 文件并上传到密钥服务器。

# 推送前检查清单

一旦您准备好一组可以推送的提交，请过一遍以下检查清单，确认一切就绪。本清单力求全面。若您只是推一个注释里的错字，其中某些步骤可能不必要。请运用常识，但拿不准时宁可谨慎。

首先，确保将推送的提交和分支与您想推送的内容一致，没有缺漏、多余或错误。可先运行 git push 命令加 `--dry-run` 查看将要推送的内容，然后用 `git log -p 1234567..987654` 查看列出的提交。`git status` 命令有助于发现遗漏添加的本地修改。

接下来让代码完整跑一遍我们的测试套件。

- `make distclean`

- `/path/to/ffmpeg/configure`

- `make fate`

- 若 fate 因缺少样本而失败，运行 `make fate-rsync` 并重试

推送前请确认所有修改都已检查过——测试套件只检查回归，且也只是一定程度上。它显然不会检查新添加的功能/代码是否真的可用，除非您为它加了测试（推荐）。

另请注意，系列中的每个提交都应能通过测试套件，而不只是补丁系列的最终结果。

一切通过后，把修改推送到您的公开 ffmpeg 克隆，并向 ffmpeg-devel 发合并请求。也可以直接推，但不推荐。

# 服务器问题

如果 Git 服务器遇到技术问题，请通过 <root@ffmpeg.org> 联系项目管理员。
