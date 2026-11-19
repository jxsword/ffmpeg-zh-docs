# showinfo

Show a line containing various information for each input video frame. The input video is not modified.

This filter supports the following options:

- **`checksum`** Calculate checksums of each plane. By default enabled.

- **`udu_sei_as_ascii`** Try to print user data unregistered SEI as ascii character when possible, in hex format otherwise.

The shown line contains a sequence of key/value pairs of the form \<key\>:\<value\>.

The following values are shown in the output:

- **`n`** The (sequential) number of the input frame, starting from 0.

- **`pts`** The Presentation TimeStamp of the input frame, expressed as a number of time base units. The time base unit depends on the filter input pad.

- **`pts_time`** The Presentation TimeStamp of the input frame, expressed as a number of seconds.

- **`fmt`** The pixel format name.

- **`sar`** The sample aspect ratio of the input frame, expressed in the form \<num\>/\<den\>.

- **`s`** The size of the input frame. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

- **`i`** The type of interlaced mode ("P" for "progressive", "T" for top field first, "B" for bottom field first).

- **`iskey`** This is 1 if the frame is a key frame, 0 otherwise.

- **`type`** The picture type of the input frame ("I" for an I-frame, "P" for a P-frame, "B" for a B-frame, or "?" for an unknown type). Also refer to the documentation of the `AVPictureType` enum and of the `av_get_picture_type_char` function defined in `libavutil/avutil.h`.

- **`checksum`** The Adler-32 checksum (printed in hexadecimal) of all the planes of the input frame.

- **`plane_checksum`** The Adler-32 checksum (printed in hexadecimal) of each plane of the input frame, expressed in the form "\[\<c0\> \<c1\> \<c2\> \<c3\>\]".

- **`mean`** The mean value of pixels in each plane of the input frame, expressed in the form "\[\<mean0\> \<mean1\> \<mean2\> \<mean3\>\]".

- **`stdev`** The standard deviation of pixel values in each plane of the input frame, expressed in the form "\[\<stdev0\> \<stdev1\> \<stdev2\> \<stdev3\>\]".
