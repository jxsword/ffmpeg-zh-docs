# tile

Tile several successive frames together.

The [untile](untile.md#untile) filter can do the reverse.

The filter accepts the following options:

- **`layout`** Set the grid size in the form `COLUMNSxROWS`. Range is up to UINT_MAX cells. Default is `6x5`.

- **`nb_frames`** Set the maximum number of frames to render in the given area. It must be less than or equal to \<w\>x\<h\>. The default value is `0`, meaning all the area will be used.

- **`margin`** Set the outer border margin in pixels. Range is 0 to 1024. Default is `0`.

- **`padding`** Set the inner border thickness (i.e. the number of pixels between frames). For more advanced padding options (such as having different values for the edges), refer to the pad video filter. Range is 0 to 1024. Default is `0`.

- **`color`** Specify the color of the unused area. For the syntax of this option, check the section ""Color" section in the ffmpeg-utils manual" in `ffmpeg-utils`. The default value of \<color\> is "black".

- **`overlap`** Set the number of frames to overlap when tiling several successive frames together. The value must be between `0` and \<nb_frames - 1\>. Default is `0`.

- **`init_padding`** Set the number of frames to initially be empty before displaying first output frame. This controls how soon will one get first output frame. The value must be between `0` and \<nb_frames - 1\>. Default is `0`.

## Examples

- Produce 8x8 PNG tiles of all keyframes (`-skip_frame nokey`) in a movie:

  ``` text
  ffmpeg -skip_frame nokey -i file.avi -vf 'scale=128:72,tile=8x8' -an -fps_mode passthrough keyframes%03d.png
  ```

  The `-fps_mode passthrough` is necessary to prevent `ffmpeg` from duplicating each output frame to accommodate the originally detected frame rate.

- Display `5` pictures in an area of `3x2` frames, with `7` pixels between them, and `2` pixels of initial margin, using mixed flat and named options:

  ``` text
  tile=3x2:nb_frames=5:padding=7:margin=2
  ```
