# gfxcapture

Capture windows or monitors using Windows.Graphics.Capture API.

This source provides low overhead capture of application windows or entire monitors. The filter outputs hardware frames in `d3d11` format; use `hwdownload,format=` if system memory frames are required.

The window to be captured can be selected via regular expressions on its title, class name or backing executable name, by explicit native handles, or by monitor index or explicit native handle. A window must match all provided expressions to be selected. The first matching window will be picked, in whatever order Windows returns them.

Explicit handles (`hwnd`, `hmonitor`) override pattern or index based selection. If neither handles nor a monitor index are given, the first window matching the provided regular expressions is captured.

This source does NOT hold a stable FPS. It returns frames at whatever rate the compositor provides them, only capped by the `max_framerate`. If you need a stable rate, you need to add an fps filter to drop/duplicate frames as needed.

If the capture source disappears mid-capture (window closed, monitor disconnected), the filter will return EOF.

This source accepts the following options:

- **`window_title`** ECMAScript regular expression matched against the window title. Supports a PCRE style `(?i)` prefix for case-insensitive matching.

- **`window_class`** As `window_title`, but matched against the window class name.

- **`window_exe`** As `window_title`, but matched against the executable file name of the window's process.

- **`monitor_idx`** Zero-based index of the monitor to capture.

  Can also be set to `window` to capture the monitor the selected window is displayed on at filter initialization time.

- **`hwnd`** Explicit native window handle (HWND).

- **`hmonitor`** Explicit native monitor handle (HMONITOR).

- **`capture_cursor`** Capture the mouse cursor. Enabled by default.

- **`capture_border`** Capture the full area of the window, including its window decorarions/border. Disabled by default.

- **`display_border`** Draw a yellow highlight border around the captured window. Disabled by default.

- **`max_framerate`** Maximum capture frame rate. Accepts a video rate (e.g. `30`, `60/1`, `24000/1001`). The default is `60` FPS. The actual rate is the rate at which the compositor renders the window/monitor, capped by this option.

- **`width`** Force the output canvas width. If zero (default) the initial captured source width is used. If a negative number is provided, the width will be rounded down to the next multiple of that number.

  See `resize_mode`.

- **`height`** Force the output canvas height. If zero (default) the initial captured source height is used. If a negative number is provided, the height will be rounded down to the next multiple of that number.

  See `resize_mode`.

- **`crop_left`** Crop this many pixels from the left side of the captured frames.

- **`crop_top`** Crop this many pixels from the left side of the captured frames.

- **`crop_right`** Crop this many pixels from the left side of the captured frames.

- **`crop_bottom`** Crop this many pixels from the left side of the captured frames.

- **`premultiplied`** If set to 1, return frames with premultiplied alpha. Default is 0 (straight alpha).

- **`resize_mode`** Defines how the captured content is fitted into the output canvas size. Possible values:

  - **`crop`** Crop (or pad with black) to the canvas size. (default)

  - **`scale`** Scale the source to fill the canvas, potentially altering aspect ratio.

  - **`scale_aspect`** Scale the source to fit inside the canvas while preserving aspect ratio. Remaining area is filled with black.

- **`scale_mode`** Scaling algorithm used when resizing is required.

  Possible values:

  - **`point`** Nearest neighbour (pixelated) scaling.

  - **`bilinear`** Bilinear filtering. (default)

  - **`bicubic`** Bicubic filtering. Potentially more blurry, but fewer scaling artifacts depending on contents.

- **`output_fmt`** Desired output pixel format inside the D3D11 hardware frames.

  Possible values:

  - **`bgra`**

  - **`8bit`** 8 bit BGRA output (default)

  - **`x2bgr10`**

  - **`10bit`** 10 bit BGR output

  - **`rgbaf16`**

  - **`16bit`** 16bit float RGBA output

## Examples

- Capture a window by title (case-insensitive) at a maximum of 60 fps:

  ``` text
  ffmpeg -filter_complex gfxcapture=window_title='(?i)My Application':max_framerate=60,hwdownload,format=bgra,format=yuv420p -c:v libx264 -crf 15 capture.mp4
  ```

- Capture monitor 1 at native refresh, 10bit color depth, scale to 1920x1080 preserving aspect:

  ``` text
  ffmpeg -filter_complex gfxcapture=monitor_idx=1:width=1920:height=1080:resize_mode=scale_aspect:output_fmt=10bit -c:v hevc_nvenc -cq 15 capture.mp4
  ```

- Capture a window by executable name, draw border, force point scaling, fixed 60 fps:

  ``` text
  ffmpeg -filter_complex gfxcapture=window_exe='^firefox.exe$':display_border=1:scale_mode=point,fps=60 -rc qvbr -qvbr_quality_level 15 -c:v h264_amf capture.mp4
  ```
