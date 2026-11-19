# concat

Concatenate audio and video streams, joining them together one after the other.

The filter works on segments of synchronized video and audio streams. All segments must have the same number of streams of each type, and that will also be the number of streams at output.

The filter accepts the following options:

- **`n`** Set the number of segments. Default is 2.

- **`v`** Set the number of output video streams, that is also the number of video streams in each segment. Default is 1.

- **`a`** Set the number of output audio streams, that is also the number of audio streams in each segment. Default is 0.

- **`unsafe`** Activate unsafe mode: do not fail if segments have a different format.

The filter has \<v\>+\<a\> outputs: first \<v\> video outputs, then \<a\> audio outputs.

There are \<n\>x(\<v\>+\<a\>) inputs: first the inputs for the first segment, in the same order as the outputs, then the inputs for the second segment, etc.

Related streams do not always have exactly the same duration, for various reasons including codec frame size or sloppy authoring. For that reason, related synchronized streams (e.g. a video and its audio track) should be concatenated at once. The concat filter will use the duration of the longest stream in each segment (except the last one), and if necessary pad shorter audio streams with silence.

For this filter to work correctly, all segments must start at timestamp 0.

All corresponding streams must have the same parameters in all segments; the filtering system will automatically select a common pixel format for video streams, and a common sample format, sample rate and channel layout for audio streams, but other settings, such as resolution, must be converted explicitly by the user.

Different frame rates are acceptable but will result in variable frame rate at output; be sure to configure the output file to handle it.

## Examples

- Concatenate an opening, an episode and an ending, all in bilingual version (video in stream 0, audio in streams 1 and 2):

  ``` text
  ffmpeg -i opening.mkv -i episode.mkv -i ending.mkv -filter_complex \
    '[0:0] [0:1] [0:2] [1:0] [1:1] [1:2] [2:0] [2:1] [2:2]
     concat=n=3:v=1:a=2 [v] [a1] [a2]' \
    -map '[v]' -map '[a1]' -map '[a2]' output.mkv
  ```

- Concatenate two parts, handling audio and video separately, using the (a)movie sources, and adjusting the resolution:

  ``` text
  movie=part1.mp4, scale=512:288 [v1] ; amovie=part1.mp4 [a1] ;
  movie=part2.mp4, scale=512:288 [v2] ; amovie=part2.mp4 [a2] ;
  [v1] [v2] concat [outv] ; [a1] [a2] concat=v=0:a=1 [outa]
  ```

  Note that a desync will happen at the stitch if the audio and video streams do not have exactly the same duration in the first file.

## Commands

This filter supports the following commands:

| Term   | Description                                        |
|--------|----------------------------------------------------|
| `next` | Close the current segment and step to the next one |
