# mergeplanes

Merge color channel components from several video streams.

The filter accepts up to 4 input streams, and merge selected input planes to the output video.

This filter accepts the following options:

- **`mapping`** Set input to output plane mapping. Default is `0`.

  The mappings is specified as a bitmap. It should be specified as a hexadecimal number in the form 0xAa\[Bb\[Cc\[Dd\]\]\]. 'Aa' describes the mapping for the first plane of the output stream. 'A' sets the number of the input stream to use (from 0 to 3), and 'a' the plane number of the corresponding input to use (from 0 to 3). The rest of the mappings is similar, 'Bb' describes the mapping for the output stream second plane, 'Cc' describes the mapping for the output stream third plane and 'Dd' describes the mapping for the output stream fourth plane.

- **`format`** Set output pixel format. Default is `yuva444p`.

- **`map0s`**

- **`map1s`**

- **`map2s`**

- **`map3s`** Set input to output stream mapping for output Nth plane. Default is `0`.

- **`map0p`**

- **`map1p`**

- **`map2p`**

- **`map3p`** Set input to output plane mapping for output Nth plane. Default is `0`.

## Examples

- Merge three gray video streams of same width and height into single video stream:

  ``` text
  [a0][a1][a2]mergeplanes=0x001020:yuv444p
  ```

- Merge 1st yuv444p stream and 2nd gray video stream into yuva444p video stream:

  ``` text
  [a0][a1]mergeplanes=0x00010210:yuva444p
  ```

- Swap Y and A plane in yuva444p stream:

  ``` text
  format=yuva444p,mergeplanes=0x03010200:yuva444p
  ```

- Swap U and V plane in yuv420p stream:

  ``` text
  format=yuv420p,mergeplanes=0x000201:yuv420p
  ```

- Cast a rgb24 clip to yuv444p:

  ``` text
  format=rgb24,mergeplanes=0x000102:yuv444p
  ```
