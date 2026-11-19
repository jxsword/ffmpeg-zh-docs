# movie

Read audio and/or video stream(s) from a movie container.

It accepts the following parameters:

- **`filename`** The name of the resource to read (not necessarily a file; it can also be a device or a stream accessed through some protocol).

- **`format_name, f`** Specifies the format assumed for the movie to read, and can be either the name of a container or an input device. If not specified, the format is guessed from \<movie_name\> or by probing.

- **`seek_point, sp`** Specifies the seek point in seconds. The frames will be output starting from this seek point. The parameter is evaluated with `av_strtod`, so the numerical value may be suffixed by an IS postfix. The default value is "0".

- **`streams, s`** Specifies the streams to read. Several streams can be specified, separated by "+". The source will then have as many outputs, in the same order. The syntax is explained in the section ""Stream specifiers" section in the ffmpeg manual" in `ffmpeg`. Two special names, "dv" and "da" specify respectively the default (best suited) video and audio stream. Default is "dv", or "da" if the filter is called as "amovie".

- **`stream_index, si`** Specifies the index of the video stream to read. If the value is -1, the most suitable video stream will be automatically selected. The default value is "-1". Deprecated. If the filter is called "amovie", it will select audio instead of video.

- **`loop`** Specifies how many times to read the stream in sequence. If the value is 0, the stream will be looped infinitely. Default value is "1".

  Note that when the movie is looped the source timestamps are not changed, so it will generate non monotonically increasing timestamps.

- **`discontinuity`** Specifies the time difference between frames above which the point is considered a timestamp discontinuity which is removed by adjusting the later timestamps.

- **`dec_threads`** Specifies the number of threads for decoding

- **`format_opts`** Specify format options for the opened file. Format options can be specified as a list of \<key\>=\<value\> pairs separated by ':'. The following example shows how to add protocol_whitelist and protocol_blacklist options:

  ``` text
  ffplay -f lavfi
  "movie=filename='1.sdp':format_opts='protocol_whitelist=file,rtp,udp\:protocol_blacklist=http'"
  ```

It allows overlaying a second video on top of the main input of a filtergraph, as shown in this graph:

``` text
input -----------> deltapts0 --> overlay --> output
                                    ^
                                    |
movie --> scale--> deltapts1 -------+
```

## Examples

- Skip 3.2 seconds from the start of the AVI file in.avi, and overlay it on top of the input labelled "in":

  ``` text
  movie=in.avi:seek_point=3.2, scale=180:-1, setpts=PTS-STARTPTS [over];
  [in] setpts=PTS-STARTPTS [main];
  [main][over] overlay=16:16 [out]
  ```

- Read from a video4linux2 device, and overlay it on top of the input labelled "in":

  ``` text
  movie=/dev/video0:f=video4linux2, scale=180:-1, setpts=PTS-STARTPTS [over];
  [in] setpts=PTS-STARTPTS [main];
  [main][over] overlay=16:16 [out]
  ```

- Read the first video stream and the audio stream with id 0x81 from dvd.vob; the video is connected to the pad named "video" and the audio is connected to the pad named "audio":

  ``` text
  movie=dvd.vob:s=v:0+#0x81 [video] [audio]
  ```

## Commands

Both movie and amovie support the following commands:

- **`seek`** Perform seek using "av_seek_frame". The syntax is: seek \<stream_index\>\|\<timestamp\>\|\<flags\>

  - \<stream_index\>: If stream_index is -1, a default stream is selected, and \<timestamp\> is automatically converted from AV_TIME_BASE units to the stream specific time_base.

  - \<timestamp\>: Timestamp in AVStream.time_base units or, if no stream is specified, in AV_TIME_BASE units.

  - \<flags\>: Flags which select direction and seeking mode.

- **`get_duration`** Get movie duration in AV_TIME_BASE units.
