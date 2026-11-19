# lensfun

Apply lens correction via the lensfun library (<http://lensfun.sourceforge.net/>).

The `lensfun` filter requires the camera make, camera model, and lens model to apply the lens correction. The filter will load the lensfun database and query it to find the corresponding camera and lens entries in the database. As long as these entries can be found with the given options, the filter can perform corrections on frames. Note that incomplete strings will result in the filter choosing the best match with the given options, and the filter will output the chosen camera and lens models (logged with level "info"). You must provide the make, camera model, and lens model as they are required.

To obtain a list of available makes and models, leave out one or both of `make` and `model` options. The filter will send the full list to the log with level `INFO`. The first column is the make and the second column is the model. To obtain a list of available lenses, set any values for make and model and leave out the `lens_model` option. The filter will send the full list of lenses in the log with level `INFO`. The ffmpeg tool will exit after the list is printed.

The filter accepts the following options:

- **`make`** The make of the camera (for example, "Canon"). This option is required.

- **`model`** The model of the camera (for example, "Canon EOS 100D"). This option is required.

- **`lens_model`** The model of the lens (for example, "Canon EF-S 18-55mm f/3.5-5.6 IS STM"). This option is required.

- **`db_path`** The full path to the lens database folder. If not set, the filter will attempt to load the database from the install path when the library was built. Default is unset.

- **`mode`** The type of correction to apply. The following values are valid options:

  | Term | Description |
  |----|----|
  | `vignetting` | Enables fixing lens vignetting. |
  | `geometry` | Enables fixing lens geometry. This is the default. |
  | `subpixel` | Enables fixing chromatic aberrations. |
  | `vig_geo` | Enables fixing lens vignetting and lens geometry. |
  | `vig_subpixel` | Enables fixing lens vignetting and chromatic aberrations. |
  | `distortion` | Enables fixing both lens geometry and chromatic aberrations. |
  | `all` | Enables all possible corrections. |

- **`focal_length`** The focal length of the image/video (zoom; expected constant for video). For example, a 18–55mm lens has focal length range of \[18–55\], so a value in that range should be chosen when using that lens. Default 18.

- **`aperture`** The aperture of the image/video (expected constant for video). Note that aperture is only used for vignetting correction. Default 3.5.

- **`focus_distance`** The focus distance of the image/video (expected constant for video). Note that focus distance is only used for vignetting and only slightly affects the vignetting correction process. If unknown, leave it at the default value (which is 1000).

- **`scale`** The scale factor which is applied after transformation. After correction the video is no longer necessarily rectangular. This parameter controls how much of the resulting image is visible. The value 0 means that a value will be chosen automatically such that there is little or no unmapped area in the output image. 1.0 means that no additional scaling is done. Lower values may result in more of the corrected image being visible, while higher values may avoid unmapped areas in the output.

- **`target_geometry`** The target geometry of the output image/video. The following values are valid options:

  - **`rectilinear (default)`**

  - **`fisheye`**

  - **`panoramic`**

  - **`equirectangular`**

  - **`fisheye_orthographic`**

  - **`fisheye_stereographic`**

  - **`fisheye_equisolid`**

  - **`fisheye_thoby`**

- **`reverse`** Apply the reverse of image correction (instead of correcting distortion, apply it).

- **`interpolation`** The type of interpolation used when correcting distortion. The following values are valid options:

  - **`nearest`**

  - **`linear (default)`**

  - **`lanczos`**

## Examples

- Apply lens correction with make "Canon", camera model "Canon EOS 100D", and lens model "Canon EF-S 18-55mm f/3.5-5.6 IS STM" with focal length of "18" and aperture of "8.0".

  ``` text
  ffmpeg -i input.mov -vf lensfun=make=Canon:model="Canon EOS 100D":lens_model="Canon EF-S 18-55mm f/3.5-5.6 IS STM":focal_length=18:aperture=8 -c:v h264 -b:v 8000k output.mov
  ```

- Apply the same as before, but only for the first 5 seconds of video.

  ``` text
  ffmpeg -i input.mov -vf lensfun=make=Canon:model="Canon EOS 100D":lens_model="Canon EF-S 18-55mm f/3.5-5.6 IS STM":focal_length=18:aperture=8:enable='lte(t\,5)' -c:v h264 -b:v 8000k output.mov
  ```
