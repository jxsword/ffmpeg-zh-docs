# fieldorder

Transform the field order of the input video.

It accepts the following parameters:

- **`order`** The output field order. Valid values are \<tff\> for top field first or \<bff\> for bottom field first.

The default value is `tff`.

The transformation is done by shifting the picture content up or down by one line, and filling the remaining line with appropriate picture content. This method is consistent with most broadcast field order converters.

If the input video is not flagged as being interlaced, or it is already flagged as being of the required output field order, then this filter does not alter the incoming video.

It is very useful when converting to or from PAL DV material, which is bottom field first.

For example:

``` text
ffmpeg -i in.vob -vf "fieldorder=bff" out.dv
```
