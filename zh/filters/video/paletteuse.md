# paletteuse

Use a palette to downsample an input video stream.

The filter takes two inputs: one video stream and a palette. The palette must be a 256 pixels image.

It accepts the following options:

- **`dither`** Select dithering mode. Available algorithms are:

  - **`bayer`** Ordered 8x8 bayer dithering (deterministic)

  - **`heckbert`** Dithering as defined by Paul Heckbert in 1982 (simple error diffusion). Note: this dithering is sometimes considered "wrong" and is included as a reference.

  - **`floyd_steinberg`** Floyd and Steingberg dithering (error diffusion)

  - **`sierra2`** Frankie Sierra dithering v2 (error diffusion)

  - **`sierra2_4a`** Frankie Sierra dithering v2 "Lite" (error diffusion)

  - **`sierra3`** Frankie Sierra dithering v3 (error diffusion)

  - **`burkes`** Burkes dithering (error diffusion)

  - **`atkinson`** Atkinson dithering by Bill Atkinson at Apple Computer (error diffusion)

  - **`none`** Disable dithering.

  Default is \<sierra2_4a\>.

- **`bayer_scale`** When \<bayer\> dithering is selected, this option defines the scale of the pattern (how much the crosshatch pattern is visible). A low value means more visible pattern for less banding, and higher value means less visible pattern at the cost of more banding.

  The option must be an integer value in the range \[0,5\]. Default is \<2\>.

- **`diff_mode`** If set, define the zone to process

  - **`rectangle`** Only the changing rectangle will be reprocessed. This is similar to GIF cropping/offsetting compression mechanism. This option can be useful for speed if only a part of the image is changing, and has use cases such as limiting the scope of the error diffusal `dither` to the rectangle that bounds the moving scene (it leads to more deterministic output if the scene doesn't change much, and as a result less moving noise and better GIF compression).

  Default is \<none\>.

- **`new`** Take new palette for each output frame.

- **`alpha_threshold`** Sets the alpha threshold for transparency. Alpha values above this threshold will be treated as completely opaque, and values below this threshold will be treated as completely transparent.

  The option must be an integer value in the range \[0,255\]. Default is \<128\>.

## Examples

- Use a palette (generated for example with [palettegen](palettegen.md#palettegen)) to encode a GIF using `ffmpeg`:

  ``` text
  ffmpeg -i input.mkv -i palette.png -lavfi paletteuse output.gif
  ```
