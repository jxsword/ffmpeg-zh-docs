# Synopsis

ffplay \[\<options\>\] \[`input_url`\]

# Description

FFplay is a very simple and portable media player using the FFmpeg libraries and the SDL library. It is mostly used as a testbed for the various FFmpeg APIs.

# Options

## Main options

- **`-x width`** Force displayed width.

- **`-y height`** Force displayed height.

- **`-fs`** Start in fullscreen mode.

- **`-an`** Disable audio.

- **`-vn`** Disable video.

- **`-sn`** Disable subtitles.

- **`-ss pos`** Seek to \<pos\>. Note that in most formats it is not possible to seek exactly, so `ffplay` will seek to the nearest seek point to \<pos\>.

  \<pos\> must be a time duration specification, see section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils`.

- **`-t duration`** Play \<duration\> seconds of audio/video.

  \<duration\> must be a time duration specification, see section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils`.

- **`-bytes`** Seek by bytes.

- **`-seek_interval`** Set custom interval, in seconds, for seeking using left/right keys. Default is 10 seconds.

- **`-nodisp`** Disable graphical display.

- **`-noborder`** Borderless window.

- **`-alwaysontop`** Window always on top. Available on: X11 with SDL \>= 2.0.5, Windows SDL \>= 2.0.6.

- **`-volume`** Set the startup volume. 0 means silence, 100 means no volume reduction or amplification. Negative values are treated as 0, values above 100 are treated as 100.

- **`-f fmt`** Force format.

- **`-window_title title`** Set window title (default is the input filename).

- **`-left title`** Set the x position for the left of the window (default is a centered window).

- **`-top title`** Set the y position for the top of the window (default is a centered window).

- **`-loop number`** Loops movie playback \<number\> times. 0 means forever.

- **`-showmode mode`** Set the show mode to use. Available values for \<mode\> are:

  | Term | Description |
  |----|----|
  | `0, video` | show video |
  | `1, waves` | show audio waves |
  | `2, rdft` | show audio frequency band using RDFT ((Inverse) Real Discrete Fourier Transform) |

  Default value is "video", if video is not present or cannot be played "rdft" is automatically selected.

  You can interactively cycle through the available show modes by pressing the key w.

- **`-vf filtergraph`** Create the filtergraph specified by \<filtergraph\> and use it to filter the video stream.

  \<filtergraph\> is a description of the filtergraph to apply to the stream, and must have a single video input and a single video output. In the filtergraph, the input is associated to the label `in`, and the output to the label `out`. See the ffmpeg-filters manual for more information about the filtergraph syntax.

  You can specify this parameter multiple times and cycle through the specified filtergraphs along with the show modes by pressing the key w.

- **`-af filtergraph`** \<filtergraph\> is a description of the filtergraph to apply to the input audio. Use the option "-filters" to show all the available filters (including sources and sinks).

- **`-i input_url`** Read \<input_url\>.

## Advanced options

- **`-stats`** Print several playback statistics, in particular show the stream duration, the codec parameters, the current position in the stream and the audio/video synchronisation drift. It is shown by default, unless the log level is lower than `info`. Its display can be forced by manually specifying this option. To disable it, you need to specify `-nostats`.

- **`-fast`** Non-spec-compliant optimizations.

- **`-genpts`** Generate pts.

- **`-sync type`** Set the master clock to audio (`type=audio`), video (`type=video`) or external (`type=ext`). Default is audio. The master clock is used to control audio-video synchronization. Most media players use audio as master clock, but in some cases (streaming or high quality broadcast) it is necessary to change that. This option is mainly used for debugging purposes.

- **`-ast audio_stream_specifier`** Select the desired audio stream using the given stream specifier. The stream specifiers are described in the [Stream specifiers](#Stream-specifiers) chapter. If this option is not specified, the "best" audio stream is selected in the program of the already selected video stream.

- **`-vst video_stream_specifier`** Select the desired video stream using the given stream specifier. The stream specifiers are described in the [Stream specifiers](#Stream-specifiers) chapter. If this option is not specified, the "best" video stream is selected.

- **`-sst subtitle_stream_specifier`** Select the desired subtitle stream using the given stream specifier. The stream specifiers are described in the [Stream specifiers](#Stream-specifiers) chapter. If this option is not specified, the "best" subtitle stream is selected in the program of the already selected video or audio stream.

- **`-autoexit`** Exit when video is done playing.

- **`-exitonkeydown`** Exit if any key is pressed.

- **`-exitonmousedown`** Exit if any mouse button is pressed.

- **`-codec:media_specifier codec_name`** Force a specific decoder implementation for the stream identified by \<media_specifier\>, which can assume the values `a` (audio), `v` (video), and `s` subtitle.

- **`-acodec codec_name`** Force a specific audio decoder.

- **`-vcodec codec_name`** Force a specific video decoder.

- **`-scodec codec_name`** Force a specific subtitle decoder.

- **`-autorotate`** Automatically rotate the video according to file metadata. Enabled by default, use `-noautorotate` to disable it.

- **`-framedrop`** Drop video frames if video is out of sync. Enabled by default if the master clock is not set to video. Use this option to enable frame dropping for all master clock sources, use `-noframedrop` to disable it.

- **`-infbuf`** Do not limit the input buffer size, read as much data as possible from the input as soon as possible. Enabled by default for realtime streams, where data may be dropped if not read in time. Use this option to enable infinite buffers for all inputs, use `-noinfbuf` to disable it.

- **`-filter_threads nb_threads`** Defines how many threads are used to process a filter pipeline. Each pipeline will produce a thread pool with this many threads available for parallel processing. The default is 0 which means that the thread count will be determined by the number of available CPUs.

- **`-enable_vulkan`** Use vulkan renderer rather than SDL builtin renderer. Depends on libplacebo.

- **`-vulkan_params`** Vulkan configuration using a list of \<key\>=\<value\> pairs separated by ":".

- **`-hwaccel`** Use HW accelerated decoding. Enable this option will enable vulkan renderer automatically.

- **`-video_bg pattern`** Set the video background pattern used for transparent videos. For solid color patterns you can use the color name or color code as specified in the section "Color section in the ffmpeg-utils(1) manual" in `ffmpeg-utils`. You can also use the special `tiles` keyword for a checker board style pattern. This is also the default. The `none` pattern does rendering without alpha blending effectively ignoring alpha channel.

## While playing

- **q, ESC** Quit.

- **f** Toggle full screen.

- **p, SPC** Pause.

- **m** Toggle mute.

- **9, 0**

- **/, \*** Decrease and increase volume respectively.

- **a** Cycle audio channel in the current program.

- **v** Cycle video channel.

- **t** Cycle subtitle channel in the current program.

- **c** Cycle program.

- **w** Cycle video filters or show modes.

- **s** Step to the next frame.

  Pause if the stream is not already paused, step to the next video frame, and pause.

- **left/right** Seek backward/forward by 10 seconds or a custom interval if -seek_interval is set.

- **down/up** Seek backward/forward 1 minute.

- **page down/page up** Seek to previous/next chapter or backward/forward 10 minutes if no chapters.

- **right mouse click** Seek to percentage in file corresponding to fraction of width.

- **left mouse double-click** Toggle full screen.

# See Also

ffmpeg(1), ffprobe(1), ffmpeg-utils(1), ffmpeg-scaler(1), ffmpeg-resampler(1), ffmpeg-codecs(1), ffmpeg-bitstream-filters(1), ffmpeg-formats(1), ffmpeg-devices(1), ffmpeg-protocols(1), ffmpeg-filters(1)
