# openclsrc

Generate video using an OpenCL program.

| Term      | Description                                                     |
|-----------|-----------------------------------------------------------------|
| `source`  | OpenCL program source file.                                     |
| `kernel`  | Kernel name in program.                                         |
| `size, s` | Size of frames to generate. This must be set.                   |
| `format`  | Pixel format to use for the generated frames. This must be set. |
| `rate, r` | Number of frames generated every second. Default value is '25'. |

For details of how the program loading works, see the [program_opencl](../overview.md#example) filter.

Example programs:

- Generate a colour ramp by setting pixel values from the position of the pixel in the output image. (Note that this will work with all pixel formats, but the generated output will not be the same.)

  ``` c
  __kernel void ramp(__write_only image2d_t dst,
                     unsigned int index)
  {
      int2 loc = (int2)(get_global_id(0), get_global_id(1));

      float4 val;
      val.xy = val.zw = convert_float2(loc) / convert_float2(get_image_dim(dst));

      write_imagef(dst, loc, val);
  }
  ```

- Generate a Sierpinski carpet pattern, panning by a single pixel each frame.

  ``` c
  __kernel void sierpinski_carpet(__write_only image2d_t dst,
                                  unsigned int index)
  {
      int2 loc = (int2)(get_global_id(0), get_global_id(1));

      float4 value = 0.0f;
      int x = loc.x + index;
      int y = loc.y + index;
      while (x > 0 || y > 0) {
          if (x % 3 == 1 && y % 3 == 1) {
              value = 1.0f;
              break;
          }
          x /= 3;
          y /= 3;
      }

      write_imagef(dst, loc, value);
  }
  ```
