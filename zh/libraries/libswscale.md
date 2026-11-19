!!! warning "翻译占位页"
    本页为英文原文占位（翻译进行中，进度见[翻译看板](https://github.com/jxsword/ffmpeg-zh-docs/blob/main/docs/translation-board.md)）。
    术语与示例以英文原文为准。

# Description

The libswscale library performs highly optimized image scaling and colorspace and pixel format conversion operations.

Specifically, this library performs the following conversions:

- *Rescaling*: is the process of changing the video size. Several rescaling options and algorithms are available. This is usually a lossy process.

- *Pixel format conversion*: is the process of converting the image format and colorspace of the image, for example from planar YUV420P to RGB24 packed. It also handles packing conversion, that is converts from packed layout (all pixels belonging to distinct planes interleaved in the same buffer), to planar layout (all samples belonging to the same plane stored in a dedicated buffer or "plane").

  This is usually a lossy process in case the source and destination colorspaces differ.

# See Also

ffmpeg(1), ffplay(1), ffprobe(1), ffmpeg-scaler(1), libavutil(3)

# Authors

The FFmpeg developers.

For details about the authorship, see the Git history of the project (https://git.ffmpeg.org/ffmpeg), e.g. by typing the command `git log` in the FFmpeg source directory, or browsing the online repository at <https://git.ffmpeg.org/ffmpeg>.

Maintainers for the specific components are listed in the file `MAINTAINERS` in the source code tree.
