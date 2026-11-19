# guided

Apply guided filter for edge-preserving smoothing, dehazing and so on.

The filter accepts the following options:

- **`radius`** Set the box radius in pixels. Allowed range is 1 to 20. Default is 3.

- **`eps`** Set regularization parameter (with square). Allowed range is 0 to 1. Default is 0.01.

- **`mode`** Set filter mode. Can be `basic` or `fast`. Default is `basic`.

- **`sub`** Set subsampling ratio for `fast` mode. Range is 2 to 64. Default is 4. No subsampling occurs in `basic` mode.

- **`guidance`** Set guidance mode. Can be `off` or `on`. Default is `off`. If `off`, single input is required. If `on`, two inputs of the same resolution and pixel format are required. The second input serves as the guidance.

- **`planes`** Set planes to filter. Default is first only.

## Commands

This filter supports the all above options as [commands](#commands).

## Examples

- Edge-preserving smoothing with guided filter:

  ``` text
  ffmpeg -i in.png -vf guided out.png
  ```

- Dehazing, structure-transferring filtering, detail enhancement with guided filter. For the generation of guidance image, refer to paper "Guided Image Filtering". See: <http://kaiminghe.com/publications/pami12guidedfilter.pdf>.

  ``` text
  ffmpeg -i in.png -i guidance.png -filter_complex guided=guidance=on out.png
  ```
