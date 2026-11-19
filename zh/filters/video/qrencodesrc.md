# qrencodesrc

Generate a QR code using the libqrencode library (see <https://fukuchi.org/works/qrencode/>).

To enable the compilation of this source, you need to configure FFmpeg with `--enable-libqrencode`.

The QR code is generated from the provided text or text pattern. The corresponding QR code is scaled and put in the video output according to the specified output size options.

In case no text is specified, the QR code is not generated, but an empty colored output is returned instead.

This source accepts the following options:

- **`qrcode_width, q`**

- **`padded_qrcode_width, Q`** Specify an expression for the width of the rendered QR code, with and without padding. The \<qrcode_width\> expression can reference the value set by the \<padded_qrcode_width\> expression, and vice versa. By default \<padded_qrcode_width\> is set to \<qrcode_width\>, meaning that there is no padding.

  These expressions are evaluated only once, when initializing the source. See the [qrencode Expressions](qrencode.md#qrencode) section for details.

  Note that some of the constants are missing for the source (for example the \<x\> or \<t\> or ¸\<n\>), since they only makes sense when evaluating the expression for each frame rather than at initialization time.

- **`rate, r`** Specify the frame rate of the sourced video, as the number of frames generated per second. It has to be a string in the format \<frame_rate_num\>/\<frame_rate_den\>, an integer number, a floating point number or a valid video frame rate abbreviation. The default value is "25".

- **`case_sensitive, cs`** Instruct libqrencode to use case sensitive encoding. This is enabled by default. This can be disabled to reduce the QR encoding size.

- **`level, l`** Specify the QR encoding error correction level. With an higher correction level, the encoding size will increase but the code will be more robust to corruption. Lower level is \<L\>.

  It accepts the following values:

  - **`L`**

  - **`M`**

  - **`Q`**

  - **`H`**

- **`expansion`** Select how the input text is expanded. Can be either `none`, or `normal` (default). See the [qrencode Text expansion](../overview.md#qrencode-expressions) section for details.

- **`text`**

- **`textfile`** Define the text to be rendered. In case neither is specified, no QR is encoded (just an empty colored frame).

  In case expansion is enabled, the text is treated as a text template, using the qrencode expansion mechanism. See the [qrencode Text expansion](../overview.md#qrencode-expressions) section for details.

- **`background_color, bc`**

- **`foreground_color, fc`** Set the QR code and background color. The default value of \<foreground_color\> is "black", the default value of \<background_color\> is "white".

  For the syntax of the color options, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`.

## Examples

- Generate a QR code encoding the specified text with the default size:

  ``` text
  qrencodesrc=text=www.ffmpeg.org
  ```

- Same as below, but select blue on pink colors:

  ``` text
  qrencodesrc=text=www.ffmpeg.org:bc=pink:fc=blue
  ```

- Generate a QR code with width of 200 pixels and padding, making the padded width 4/3 of the QR code width:

  ``` text
  qrencodesrc=text=www.ffmpeg.org:q=200:Q=4/3*q
  ```

- Generate a QR code with padded width of 200 pixels and padding, making the QR code width 3/4 of the padded width:

  ``` text
  qrencodesrc=text=www.ffmpeg.org:Q=200:q=3/4*Q
  ```

- Generate a QR code encoding the frame number:

  ``` text
  qrencodesrc=text=%{n}
  ```

- Generate a QR code encoding the GMT timestamp:

  ``` text
  qrencodesrc=text=%{gmtime}
  ```

- Generate a QR code encoding the timestamp expressed as a float:

  ``` text
  qrencodesrc=text=%{pts}
  ```
