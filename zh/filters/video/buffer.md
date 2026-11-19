# buffer

Buffer video frames, and make them available to the filter chain.

This source is mainly intended for a programmatic use, in particular through the interface defined in `libavfilter/buffersrc.h`.

It accepts the following parameters:

- **`video_size`** Specify the size (width and height) of the buffered video frames. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

- **`width`** The input video width.

- **`height`** The input video height.

- **`pix_fmt`** A string representing the pixel format of the buffered video frames. It may be a number corresponding to a pixel format, or a pixel format name.

- **`time_base`** Specify the timebase assumed by the timestamps of the buffered frames.

- **`frame_rate`** Specify the frame rate expected for the video stream.

- **`colorspace`** A string representing the color space of the buffered video frames. It may be a number corresponding to a color space, or a color space name.

- **`range`** A string representing the color range of the buffered video frames. It may be a number corresponding to a color range, or a color range name.

- **`alpha_mode`** A string representing the alpha mode of the buffered video frames. It may be a number corresponding to an alpha mode, or an alpha mode name.

- **`pixel_aspect, sar`** The sample (pixel) aspect ratio of the input video.

- **`hw_frames_ctx`** When using a hardware pixel format, this should be a reference to an AVHWFramesContext describing input frames.

For example:

``` text
buffer=width=320:height=240:pix_fmt=yuv410p:time_base=1/24:sar=1
```

will instruct the source to accept video frames with size 320x240 and with format "yuv410p", assuming 1/24 as the timestamps timebase and square pixels (1:1 sample aspect ratio). Since the pixel format with name "yuv410p" corresponds to the number 6 (check the enum AVPixelFormat definition in `libavutil/pixfmt.h`), this example corresponds to:

``` text
buffer=size=320x240:pixfmt=6:time_base=1/24:pixel_aspect=1/1
```

Alternatively, the options can be specified as a flat string, but this syntax is deprecated:

\<width\>:\<height\>:\<pix_fmt\>:\<time_base.num\>:\<time_base.den\>:\<pixel_aspect.num\>:\<pixel_aspect.den\>
