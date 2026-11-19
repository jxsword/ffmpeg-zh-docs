# xpsnr

Obtain the average (across all input frames) and minimum (across all color plane averages) eXtended Perceptually weighted peak Signal-to-Noise Ratio (XPSNR) between two input videos.

The XPSNR is a low-complexity psychovisually motivated distortion measurement algorithm for assessing the difference between two video streams or images. This is especially useful for objectively quantifying the distortions caused by video and image codecs, as an alternative to a formal subjective test. The logarithmic XPSNR output values are in a similar range as those of traditional [psnr](psnr.md#psnr) assessments but better reflect human impressions of visual coding quality. More details on the XPSNR measure, which essentially represents a blockwise weighted variant of the PSNR measure, can be found in the following freely available papers:

- C. R. Helmrich, M. Siekmann, S. Becker, S. Bosse, D. Marpe, and T. Wiegand, "XPSNR: A Low-Complexity Extension of the Perceptually Weighted Peak Signal-to-Noise Ratio for High-Resolution Video Quality Assessment," in Proc. IEEE Int. Conf. Acoustics, Speech, Sig. Process. (ICASSP), virt./online, May 2020. [www.ecodis.de/xpsnr.htm](https://www.ecodis.de/xpsnr.htm)

- C. R. Helmrich, S. Bosse, H. Schwarz, D. Marpe, and T. Wiegand, "A Study of the Extended Perceptually Weighted Peak Signal-to-Noise Ratio (XPSNR) for Video Compression with Different Resolutions and Bit Depths," ITU Journal: ICT Discoveries, vol. 3, no. 1, pp. 65 - 72, May 2020. <http://handle.itu.int/11.1002/pub/8153d78b-en>

When publishing the results of XPSNR assessments obtained using, e.g., this FFmpeg filter, a reference to the above papers as a means of documentation is strongly encouraged. The filter requires two input videos. The first input is considered a (usually not distorted) reference source and is passed unchanged to the output, whereas the second input is a (distorted) test signal. Except for the bit depth, these two video inputs must have the same pixel format. In addition, for best performance, both compared input videos should be in YCbCr color format.

The obtained overall XPSNR values mentioned above are printed through the logging system. In case of input with multiple color planes, we suggest reporting of the minimum XPSNR average.

The following parameter, which behaves like the one for the [psnr](psnr.md#psnr) filter, is accepted:

- **`stats_file, f`** If specified, the filter will use the named file to save the XPSNR value of each individual frame and color plane. When the file name equals "-", that data is sent to standard output.

This filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

## Examples

- XPSNR analysis of two 1080p HD videos, ref_source.yuv and test_video.yuv, both at 24 frames per second, with color format 4:2:0, bit depth 8, and output of a logfile named "xpsnr.log":

  ``` text
  ffmpeg -s 1920x1080 -framerate 24 -pix_fmt yuv420p -i ref_source.yuv -s 1920x1080 -framerate
  24 -pix_fmt yuv420p -i test_video.yuv -lavfi xpsnr="stats_file=xpsnr.log" -f null -
  ```

- XPSNR analysis of two 2160p UHD videos, ref_source.yuv with bit depth 8 and test_video.yuv with bit depth 10, both at 60 frames per second with color format 4:2:0, no logfile output:

  ``` text
  ffmpeg -s 3840x2160 -framerate 60 -pix_fmt yuv420p -i ref_source.yuv -s 3840x2160 -framerate
  60 -pix_fmt yuv420p10le -i test_video.yuv -lavfi xpsnr="stats_file=-" -f null -
  ```
