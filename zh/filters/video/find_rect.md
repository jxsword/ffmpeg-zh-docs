# find_rect

Find a rectangular object in the input video.

The object to search for must be specified as a gray8 image specified with the `object` option.

For each possible match, a score is computed. If the score reaches the specified threshold, the object is considered found.

If the input video contains multiple instances of the object, the filter will find only one of them.

When an object is found, the following metadata entries are set in the matching frame:

| Term               | Description                     |
|--------------------|---------------------------------|
| `lavfi.rect.w`     | width of object                 |
| `lavfi.rect.h`     | height of object                |
| `lavfi.rect.x`     | x position of object            |
| `lavfi.rect.y`     | y position of object            |
| `lavfi.rect.score` | match score of the found object |

It accepts the following options:

- **`object`** Filepath of the object image, needs to be in gray8.

- **`threshold`** Detection threshold, expressed as a decimal number in the range 0-1.

  A threshold value of 0.01 means only exact matches, a threshold of 0.99 means almost everything matches.

  Default value is 0.5.

- **`mipmaps`** Number of mipmaps, default is 3.

- **`xmin, ymin, xmax, ymax`** Specifies the rectangle in which to search.

- **`discard`** Discard frames where object is not detected. Default is disabled.

## Examples

- Cover a rectangular object by the supplied image of a given video using `ffmpeg`:

  ``` text
  ffmpeg -i file.ts -vf find_rect=newref.pgm,cover_rect=cover.jpg:mode=cover new.mkv
  ```

- Find the position of an object in each frame using `ffprobe` and write it to a log file:

  ``` text
  ffprobe -f lavfi movie=test.mp4,find_rect=object=object.pgm:threshold=0.3 \
    -show_entries frame=pkt_pts_time:frame_tags=lavfi.rect.x,lavfi.rect.y \
    -of csv -o find_rect.csv
  ```
