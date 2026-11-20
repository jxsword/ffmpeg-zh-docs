# 描述

libavutil 库是一个帮助可移植多媒体编程的实用工具库。它包含安全可移植的字符串函数、随机数生成器、数据结构、附加数学函数、密码学以及多媒体相关功能（如像素格式与采样格式的枚举）。它并不是用来存放 libavcodec 与 libavformat 共同所需代码的库。

本库的目标是：

- ****模块化**** 各部分之间应尽量少互相依赖，并且可以在 `./configure` 期间禁用单个部分。

- ****小巧**** 源码与目标文件都应当小巧。

- ****高效**** 它应具有较低的 CPU 与内存占用。

- ****实用**** 它应避免提供几乎无人需要的无用特性。

# 另请参见

ffmpeg(1), ffplay(1), ffprobe(1), ffmpeg-utils(1)

# 作者

FFmpeg 开发者。

有关作者身份的详情，请参阅项目的 Git 历史 (https://git.ffmpeg.org/ffmpeg)，例如在 FFmpeg 源码目录中键入 `git log` 命令，或浏览 <https://git.ffmpeg.org/ffmpeg> 上的在线仓库。

各具体组件的维护者列表见源码树中的 `MAINTAINERS` 文件。
