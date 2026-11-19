# tonemap_vaapi

Perform HDR-to-SDR or HDR-to-HDR tone-mapping. It currently only accepts HDR10 as input.

It accepts the following parameters:

- **`format`** Specify the output pixel format.

  Default is nv12 for HDR-to-SDR tone-mapping and p010 for HDR-to-HDR tone-mapping.

- **`primaries, p`** Set the output color primaries.

  Default is bt709 for HDR-to-SDR tone-mapping and same as input for HDR-to-HDR tone-mapping.

- **`transfer, t`** Set the output transfer characteristics.

  Default is bt709 for HDR-to-SDR tone-mapping and same as input for HDR-to-HDR tone-mapping.

- **`matrix, m`** Set the output colorspace matrix.

  Default is bt709 for HDR-to-SDR tone-mapping and same as input for HDR-to-HDR tone-mapping.

- **`display`** Set the output mastering display colour volume. It is given by a '\|'-separated list of two values, two values are space separated. It set display primaries x & y in G, B, R order, then white point x & y, the nominal minimum & maximum display luminances.

  HDR-to-HDR tone-mapping will be performed when this option is set.

- **`light`** Set the output content light level information. It accepts 2 space-separated values, the first input is the maximum light level and the second input is the maximum average light level.

  It is ignored for HDR-to-SDR tone-mapping, and optional for HDR-to-HDR tone-mapping.

## Example

- Convert HDR(HDR10) video to bt2020-transfer-characteristic p010 format

  ``` text
  tonemap_vaapi=format=p010:t=bt2020-10
  ```

- Convert HDR video to HDR video

  ``` text
  tonemap_vaapi=display=7500\ 3000|34000\ 16000|13250\ 34500|15635\ 16450|500\ 10000000
  ```
