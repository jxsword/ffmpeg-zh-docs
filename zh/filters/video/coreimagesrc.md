# coreimagesrc

Video source generated on GPU using Apple's CoreImage API on OSX.

This video source is a specialized version of the [coreimage](coreimage.md#coreimage) video filter. Use a core image generator at the beginning of the applied filterchain to generate the content.

The coreimagesrc video source accepts the following options:

- **`list_generators`** List all available generators along with all their respective options as well as possible minimum and maximum values along with the default values.

  ``` text
  list_generators=true
  ```

- **`size, s`** Specify the size of the sourced video. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. The default value is `320x240`.

- **`rate, r`** Specify the frame rate of the sourced video, as the number of frames generated per second. It has to be a string in the format \<frame_rate_num\>/\<frame_rate_den\>, an integer number, a floating point number or a valid video frame rate abbreviation. The default value is "25".

- **`sar`** Set the sample aspect ratio of the sourced video.

- **`duration, d`** Set the duration of the sourced video. See section "the Time duration section in the ffmpeg-utils(1) manual" in `ffmpeg-utils` for the accepted syntax.

  If not specified, or the expressed duration is negative, the video is supposed to be generated forever.

Additionally, all options of the [coreimage](coreimage.md#coreimage) video filter are accepted. A complete filterchain can be used for further processing of the generated input without CPU-HOST transfer. See [coreimage](coreimage.md#coreimage) documentation and examples for details.

## Examples

- Use CIQRCodeGenerator to create a QR code for the FFmpeg homepage, given as complete and escaped command-line for Apple's standard bash shell:

  ``` text
  ffmpeg -f lavfi -i coreimagesrc=s=100x100:filter=CIQRCodeGenerator@inputMessage=https\\\\\://FFmpeg.org/@inputCorrectionLevel=H -frames:v 1 QRCode.png
  ```

  This example is equivalent to the QRCode example of [coreimage](coreimage.md#coreimage) without the need for a nullsrc video source.
