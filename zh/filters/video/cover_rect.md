# cover_rect

Cover a rectangular object

It accepts the following options:

- **`cover`** Filepath of the optional cover image, needs to be in yuv420.

- **`mode`** Set covering mode.

  It accepts the following values:

  | Term      | Description                                      |
  |-----------|--------------------------------------------------|
  | `cover` | cover it by the supplied image                   |
  | `blur`  | cover it by interpolating the surrounding pixels |

  Default value is \<blur\>.

## Examples

- Cover a rectangular object by the supplied image of a given video using `ffmpeg`:

  ``` text
  ffmpeg -i file.ts -vf find_rect=newref.pgm,cover_rect=cover.jpg:mode=cover new.mkv
  ```
