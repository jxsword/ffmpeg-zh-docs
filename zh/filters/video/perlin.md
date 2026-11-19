# perlin

Generate Perlin noise.

Perlin noise is a kind of noise with local continuity in space. This can be used to generate patterns with continuity in space and time, e.g. to simulate smoke, fluids, or terrain.

In case more than one octave is specified through the `octaves` option, Perlin noise is generated as a sum of components, each one with doubled frequency. In this case the `persistence` option specify the ratio of the amplitude with respect to the previous component. More octave components enable to specify more high frequency details in the generated noise (e.g. small size variations due to boulders in a generated terrain).

## Options

- **`size, s`** Specify the size (width and height) of the buffered video frames. For the syntax of this option, check the section ""Video size" section in the ffmpeg-utils manual" in `ffmpeg-utils`. Default value is `320x240`.

- **`rate, r`** Specify the frame rate expected for the video stream, expressed as a number of frames per second. Default value is `25`.

- **`octaves`** Specify the total number of components making up the noise, each one with doubled frequency. Default value is `1`.

- **`persistence`** Set the ratio used to compute the amplitude of the next octave component with respect to the previous component amplitude. Default value is `1`.

- **`xscale`**

- **`yscale`** Define a scale factor used to multiple the x, y coordinates. This can be useful to define an effect with a pattern stretched along the x or y axis. Default value is `1`.

- **`tscale`** Define a scale factor used to multiple the time coordinate. This can be useful to change the time variation speed. Default value is `1`.

- **`random_mode`** Set random mode used to compute initial pattern.

  Supported values are:

  - **`random`** Compute and use random seed.

  - **`ken`** Use the predefined initial pattern defined by Ken Perlin in the original article, can be useful to compare the output with other sources.

  - **`seed`** Use the value specified by `random_seed` option.

  Default value is `random`.

- **`random_seed, seed`** When `random_mode` is set to \<random_seed\>, use this value to compute the initial pattern. Default value is `0`.

## Examples

- Generate single component:

  ``` text
  perlin
  ```

- Use Perlin noise with 7 components, each one with a halved contribution to total amplitude:

  ``` text
  perlin=octaves=7:persistence=0.5
  ```

- Chain Perlin noise with the [lutyuv](../overview.md#commands) to generate a black&white effect:

  ``` text
  perlin=octaves=3:tscale=0.3,lutyuv=y='if(lt(val\,128)\,255\,0)'
  ```

- Stretch noise along the y axis, and convert gray level to red-only signal:

  ``` text
  perlin=octaves=7:tscale=0.4:yscale=0.3,lutrgb=r=val:b=0:g=0
  ```
