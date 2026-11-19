# ddagrab

Captures the Windows Desktop via Desktop Duplication API.

The filter exclusively returns D3D11 Hardware Frames, for on-gpu encoding or processing. So an explicit [hwdownload](hwdownload.md#hwdownload) is needed for any kind of software processing.

It accepts the following options:

- **`output_idx`** DXGI Output Index to capture.

  Usually corresponds to the index Windows has given the screen minus one, so it's starting at 0.

  Defaults to output 0.

- **`draw_mouse`** Whether to draw the mouse cursor.

  Defaults to true.

  Only affects hardware cursors. If a game or application renders its own cursor, it'll always be captured.

- **`framerate`** Maximum framerate at which the desktop will be captured - the interval between successive frames will not be smaller than the inverse of the framerate. When \<dup_frames\> is true (the default) and the desktop is not being updated often enough, the filter will duplicate a previous frame. Note that there is no background buffering going on, so when the filter is not polled often enough then the actual inter-frame interval may be significantly larger.

  Defaults to 30 FPS.

- **`video_size`** Specify the size of the captured video.

  Defaults to the full size of the screen.

  Cropped from the bottom/right if smaller than screen size.

- **`offset_x`** Horizontal offset of the captured video.

- **`offset_y`** Vertical offset of the captured video.

- **`output_fmt`** Desired filter output format. Defaults to 8 Bit BGRA.

  It accepts the following values:

  - **`auto`** Passes all supported output formats to DDA and returns what DDA decides to use.

  - **`8bit`**

  - **`bgra`** 8 Bit formats always work, and DDA will convert to them if necessary.

  - **`10bit`**

  - **`x2bgr10`** Filter initialization will fail if 10 bit format is requested but unavailable.

- **`dup_frames`** When this option is set to true (the default), the filter will duplicate frames when the desktop has not been updated in order to maintain approximately constant target framerate. When this option is set to false, the filter will wait for the desktop to be updated (inter-frame intervals may vary significantly in this case).

## Examples

Capture primary screen and encode using nvenc:

``` text
ffmpeg -f lavfi -i ddagrab -c:v h264_nvenc -cq 18 output.mp4
```

You can also skip the lavfi device and directly use the filter. Also demonstrates downloading the frame and encoding with libx264. Explicit output format specification is required in this case:

``` text
ffmpeg -filter_complex ddagrab=output_idx=1:framerate=60,hwdownload,format=bgra -c:v libx264 -crf 18 output.mp4
```

If you want to capture only a subsection of the desktop, this can be achieved by specifying a smaller size and its offsets into the screen:

``` text
ddagrab=video_size=800x600:offset_x=100:offset_y=100
```
