# scale_vt

Scale and convert the color parameters using VTPixelTransferSession.

The filter accepts the following options:

- **`w`**

- **`h`** Set the output video dimension expression. Default value is the input dimension.

- **`color_matrix`** Set the output colorspace matrix.

- **`color_primaries`** Set the output color primaries.

- **`color_transfer`** Set the output transfer characteristics.

## Examples

- Perform HDR to SDR conversion, and scale to half size of input

  ``` text
  ffmpeg -hwaccel videotoolbox \
          -hwaccel_output_format videotoolbox_vld \
          -i hdr.mov \
          -c:v hevc_videotoolbox \
          -profile:v main \
          -b:v 3M \
          -vf scale_vt=w=iw/2:h=ih/2:color_matrix=bt709:color_primaries=bt709:color_transfer=bt709 \
          -c:a copy \
          -tag:v hvc1 \
          sdr.mp4
  ```
