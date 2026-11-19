# xfade_opencl

Cross fade two videos with custom transition effect by using OpenCL.

It accepts the following options:

- **`transition`** Set one of possible transition effects.

  - **`custom`** Select custom transition effect, the actual transition description will be picked from source and kernel options.

  - **`fade`**

  - **`wipeleft`**

  - **`wiperight`**

  - **`wipeup`**

  - **`wipedown`**

  - **`slideleft`**

  - **`slideright`**

  - **`slideup`**

  - **`slidedown`** Default transition is fade.

- **`source`** OpenCL program source file for custom transition.

- **`kernel`** Set name of kernel to use for custom transition from program source file.

- **`duration`** Set duration of video transition.

- **`offset`** Set time of start of transition relative to first video.

The program source file must contain a kernel function with the given name, which will be run once for each plane of the output. Each run on a plane gets enqueued as a separate 2D global NDRange with one work-item for each pixel to be generated. The global ID offset for each work-item is therefore the coordinates of a pixel in the destination image.

The kernel function needs to take the following arguments:

- Destination image, \<\_\_write_only image2d_t\>.

  This image will become the output; the kernel should write all of it.

- First Source image, \<\_\_read_only image2d_t\>. Second Source image, \<\_\_read_only image2d_t\>.

  These are the most recent images on each input. The kernel may read from them to generate the output, but they can't be written to.

- Transition progress, \<float\>. This value is always between 0 and 1 inclusive.

Example programs:

- Apply dots curtain transition effect:

  ``` c
  __kernel void blend_images(__write_only image2d_t dst,
                             __read_only  image2d_t src1,
                             __read_only  image2d_t src2,
                             float progress)
  {
      const sampler_t sampler = (CLK_NORMALIZED_COORDS_FALSE |
                                 CLK_FILTER_LINEAR);
      int2  p = (int2)(get_global_id(0), get_global_id(1));
      float2 rp = (float2)(get_global_id(0), get_global_id(1));
      float2 dim = (float2)(get_image_dim(src1).x, get_image_dim(src1).y);
      rp = rp / dim;

      float2 dots = (float2)(20.0, 20.0);
      float2 center = (float2)(0,0);
      float2 unused;

      float4 val1 = read_imagef(src1, sampler, p);
      float4 val2 = read_imagef(src2, sampler, p);
      bool next = distance(fract(rp * dots, &unused), (float2)(0.5, 0.5)) < (progress / distance(rp, center));

      write_imagef(dst, p, next ? val1 : val2);
  }
  ```
