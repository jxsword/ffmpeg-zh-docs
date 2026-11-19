# haldclut

Apply a Hald CLUT to a video stream.

First input is the video stream to process, and second one is the Hald CLUT. The Hald CLUT input can be a simple picture or a complete video stream.

The filter accepts the following options:

- **`clut`** Set which CLUT video frames will be processed from second input stream, can be \<first\> or \<all\>. Default is \<all\>.

- **`shortest`** Force termination when the shortest input terminates. Default is `0`.

- **`repeatlast`** Continue applying the last CLUT after the end of the stream. A value of `0` disable the filter after the last frame of the CLUT is reached. Default is `1`.

`haldclut` also has the same interpolation options as [lut3d](lut3d.md#lut3d) (both filters share the same internals).

This filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

More information about the Hald CLUT can be found on Eskil Steenberg's website (Hald CLUT author) at <http://www.quelsolaar.com/technology/clut.html>.

## Commands

This filter supports the `interp` option as [commands](#commands).

## Workflow examples

### Hald CLUT video stream

Generate an identity Hald CLUT stream altered with various effects:

``` text
ffmpeg -f lavfi -i haldclutsrc=8 -vf "hue=H=2*PI*t:s=sin(2*PI*t)+1, curves=cross_process" -t 10 -c:v ffv1 clut.nut
```

Note: make sure you use a lossless codec.

Then use it with `haldclut` to apply it on some random stream:

``` text
ffmpeg -f lavfi -i mandelbrot -i clut.nut -filter_complex '[0][1] haldclut' -t 20 mandelclut.mkv
```

The Hald CLUT will be applied to the 10 first seconds (duration of `clut.nut`), then the latest picture of that CLUT stream will be applied to the remaining frames of the `mandelbrot` stream.

### Hald CLUT with preview

A Hald CLUT is supposed to be a squared image of `Level*Level*Level` by `Level*Level*Level` pixels. For a given Hald CLUT, FFmpeg will select the biggest possible square starting at the top left of the picture. The remaining padding pixels (bottom or right) will be ignored. This area can be used to add a preview of the Hald CLUT.

Typically, the following generated Hald CLUT will be supported by the `haldclut` filter:

``` text
ffmpeg -f lavfi -i haldclutsrc=8 -vf "
   pad=iw+320 [padded_clut];
   smptebars=s=320x256, split [a][b];
   [padded_clut][a] overlay=W-320:h, curves=color_negative [main];
   [main][b] overlay=W-320" -frames:v 1 clut.png
```

It contains the original and a preview of the effect of the CLUT: SMPTE color bars are displayed on the right-top, and below the same color bars processed by the color changes.

Then, the effect of this Hald CLUT can be visualized with:

``` text
ffplay input.mkv -vf "movie=clut.png, [in] haldclut"
```
