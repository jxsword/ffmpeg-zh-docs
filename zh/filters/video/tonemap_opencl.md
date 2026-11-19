# tonemap_opencl

Perform HDR(PQ/HLG) to SDR conversion with tone-mapping.

It accepts the following parameters:

- **`tonemap`** Specify the tone-mapping operator to be used. Same as tonemap option in [tonemap](tonemap.md#tonemap).

- **`param`** Tune the tone mapping algorithm. same as param option in [tonemap](tonemap.md#tonemap).

- **`desat`** Apply desaturation for highlights that exceed this level of brightness. The higher the parameter, the more color information will be preserved. This setting helps prevent unnaturally blown-out colors for super-highlights, by (smoothly) turning into white instead. This makes images feel more natural, at the cost of reducing information about out-of-range colors.

  The default value is 0.5, and the algorithm here is a little different from the cpu version tonemap currently. A setting of 0.0 disables this option.

- **`threshold`** The tonemapping algorithm parameters is fine-tuned per each scene. And a threshold is used to detect whether the scene has changed or not. If the distance between the current frame average brightness and the current running average exceeds a threshold value, we would re-calculate scene average and peak brightness. The default value is 0.2.

- **`format`** Specify the output pixel format.

  Currently supported formats are:

  - **\<p010\>**

  - **\<nv12\>**

- **`range, r`** Set the output color range.

  Possible values are:

  - **\<tv/mpeg\>**

  - **\<pc/jpeg\>**

  Default is same as input.

- **`primaries, p`** Set the output color primaries.

  Possible values are:

  - **\<bt709\>**

  - **\<bt2020\>**

  Default is same as input.

- **`transfer, t`** Set the output transfer characteristics.

  Possible values are:

  - **\<bt709\>**

  - **\<bt2020\>**

  Default is bt709.

- **`matrix, m`** Set the output colorspace matrix.

  Possible value are:

  - **\<bt709\>**

  - **\<bt2020\>**

  Default is same as input.

## Example

- Convert HDR(PQ/HLG) video to bt2020-transfer-characteristic p010 format using linear operator.

  ``` text
  -i INPUT -vf "format=p010,hwupload,tonemap_opencl=t=bt2020:tonemap=linear:format=p010,hwdownload,format=p010" OUTPUT
  ```
