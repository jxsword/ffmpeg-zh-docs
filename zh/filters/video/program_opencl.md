# program_opencl

Filter video using an OpenCL program.

| Term      | Description                                                     |
|-----------|-----------------------------------------------------------------|
| `source`  | OpenCL program source file.                                     |
| `kernel`  | Kernel name in program.                                         |
| `inputs`  | Number of inputs to the filter. Defaults to 1.                  |
| `size, s` | Size of output frames. Defaults to the same as the first input. |

The `program_opencl` filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

The program source file must contain a kernel function with the given name, which will be run once for each plane of the output. Each run on a plane gets enqueued as a separate 2D global NDRange with one work-item for each pixel to be generated. The global ID offset for each work-item is therefore the coordinates of a pixel in the destination image.

The kernel function needs to take the following arguments:

- Destination image, \<\_\_write_only image2d_t\>.

  This image will become the output; the kernel should write all of it.

- Frame index, \<unsigned int\>.

  This is a counter starting from zero and increasing by one for each frame.

- Source images, \<\_\_read_only image2d_t\>.

  These are the most recent images on each input. The kernel may read from them to generate the output, but they can't be written to.

Example programs:

- Copy the input to the output (output must be the same size as the input).

  ``` c
  __kernel void copy(__write_only image2d_t destination,
                     unsigned int index,
                     __read_only  image2d_t source)
  {
      const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE;

      int2 location = (int2)(get_global_id(0), get_global_id(1));

      float4 value = read_imagef(source, sampler, location);

      write_imagef(destination, location, value);
  }
  ```

- Apply a simple transformation, rotating the input by an amount increasing with the index counter. Pixel values are linearly interpolated by the sampler, and the output need not have the same dimensions as the input.

  ``` c
  __kernel void rotate_image(__write_only image2d_t dst,
                             unsigned int index,
                             __read_only  image2d_t src)
  {
      const sampler_t sampler = (CLK_NORMALIZED_COORDS_FALSE |
                                 CLK_FILTER_LINEAR);

      float angle = (float)index / 100.0f;

      float2 dst_dim = convert_float2(get_image_dim(dst));
      float2 src_dim = convert_float2(get_image_dim(src));

      float2 dst_cen = dst_dim / 2.0f;
      float2 src_cen = src_dim / 2.0f;

      int2   dst_loc = (int2)(get_global_id(0), get_global_id(1));

      float2 dst_pos = convert_float2(dst_loc) - dst_cen;
      float2 src_pos = {
          cos(angle) * dst_pos.x - sin(angle) * dst_pos.y,
          sin(angle) * dst_pos.x + cos(angle) * dst_pos.y
      };
      src_pos = src_pos * src_dim / dst_dim;

      float2 src_loc = src_pos + src_cen;

      if (src_loc.x < 0.0f      || src_loc.y < 0.0f ||
          src_loc.x > src_dim.x || src_loc.y > src_dim.y)
          write_imagef(dst, dst_loc, 0.5f);
      else
          write_imagef(dst, dst_loc, read_imagef(src, sampler, src_loc));
  }
  ```

- Blend two inputs together, with the amount of each input used varying with the index counter.

  ``` c
  __kernel void blend_images(__write_only image2d_t dst,
                             unsigned int index,
                             __read_only  image2d_t src1,
                             __read_only  image2d_t src2)
  {
      const sampler_t sampler = (CLK_NORMALIZED_COORDS_FALSE |
                                 CLK_FILTER_LINEAR);

      float blend = (cos((float)index / 50.0f) + 1.0f) / 2.0f;

      int2  dst_loc = (int2)(get_global_id(0), get_global_id(1));
      int2 src1_loc = dst_loc * get_image_dim(src1) / get_image_dim(dst);
      int2 src2_loc = dst_loc * get_image_dim(src2) / get_image_dim(dst);

      float4 val1 = read_imagef(src1, sampler, src1_loc);
      float4 val2 = read_imagef(src2, sampler, src2_loc);

      write_imagef(dst, dst_loc, val1 * blend + val2 * (1.0f - blend));
  }
  ```
