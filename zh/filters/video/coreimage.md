# coreimage

Video filtering on GPU using Apple's CoreImage API on OSX.

Hardware acceleration is based on an OpenGL context. Usually, this means it is processed by video hardware. However, software-based OpenGL implementations exist which means there is no guarantee for hardware processing. It depends on the respective OSX.

There are many filters and image generators provided by Apple that come with a large variety of options. The filter has to be referenced by its name along with its options.

The coreimage filter accepts the following options:

- **`list_filters`** List all available filters and generators along with all their respective options as well as possible minimum and maximum values along with the default values.

  ``` text
  list_filters=true
  ```

- **`filter`** Specify all filters by their respective name and options. Use \<list_filters\> to determine all valid filter names and options. Numerical options are specified by a float value and are automatically clamped to their respective value range. Vector and color options have to be specified by a list of space separated float values. Character escaping has to be done. A special option name `default` is available to use default options for a filter.

  It is required to specify either `default` or at least one of the filter options. All omitted options are used with their default values. The syntax of the filter string is as follows:

  ``` text
  filter=<NAME>@<OPTION>=<VALUE>[@<OPTION>=<VALUE>][@...][#<NAME>@<OPTION>=<VALUE>[@<OPTION>=<VALUE>][@...]][#...]
  ```

- **`output_rect`** Specify a rectangle where the output of the filter chain is copied into the input image. It is given by a list of space separated float values:

  ``` text
  output_rect=x\ y\ width\ height
  ```

  If not given, the output rectangle equals the dimensions of the input image. The output rectangle is automatically cropped at the borders of the input image. Negative values are valid for each component.

  ``` text
  output_rect=25\ 25\ 100\ 100
  ```

Several filters can be chained for successive processing without GPU-HOST transfers allowing for fast processing of complex filter chains. Currently, only filters with zero (generators) or exactly one (filters) input image and one output image are supported. Also, transition filters are not yet usable as intended.

Some filters generate output images with additional padding depending on the respective filter kernel. The padding is automatically removed to ensure the filter output has the same size as the input image.

For image generators, the size of the output image is determined by the previous output image of the filter chain or the input image of the whole filterchain, respectively. The generators do not use the pixel information of this image to generate their output. However, the generated output is blended onto this image, resulting in partial or complete coverage of the output image.

The [coreimagesrc](coreimagesrc.md#coreimagesrc) video source can be used for generating input images which are directly fed into the filter chain. By using it, providing input images by another video source or an input video is not required.

## Examples

- List all filters available:

  ``` text
  coreimage=list_filters=true
  ```

- Use the CIBoxBlur filter with default options to blur an image:

  ``` text
  coreimage=filter=CIBoxBlur@default
  ```

- Use a filter chain with CISepiaTone at default values and CIVignetteEffect with its center at 100x100 and a radius of 50 pixels:

  ``` text
  coreimage=filter=CIBoxBlur@default#CIVignetteEffect@inputCenter=100\ 100@inputRadius=50
  ```

- Use nullsrc and CIQRCodeGenerator to create a QR code for the FFmpeg homepage, given as complete and escaped command-line for Apple's standard bash shell:

  ``` text
  ffmpeg -f lavfi -i nullsrc=s=100x100,coreimage=filter=CIQRCodeGenerator@inputMessage=https\\\\\://FFmpeg.org/@inputCorrectionLevel=H -frames:v 1 QRCode.png
  ```
