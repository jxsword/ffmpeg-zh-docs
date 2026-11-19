# sidedata, asidedata

Delete frame side data, or select frames based on it.

This filter accepts the following options:

- **`mode`** Set mode of operation of the filter.

  Can be one of the following:

  - **`select`** Select every frame with side data of `type`.

  - **`delete`** Delete side data of `type`. If `type` is not set, delete all side data in the frame.

- **`type`** Set side data type used with all modes. Must be set for `select` mode.

  Possible values are:

  - **`PANSCAN`**

  - **`A53_CC`**

  - **`STEREO3D`**

  - **`MATRIXENCODING`**

  - **`DOWNMIX_INFO`**

  - **`REPLAYGAIN`**

  - **`DISPLAYMATRIX`**

  - **`AFD`**

  - **`MOTION_VECTORS`**

  - **`SKIP_SAMPLES`**

  - **`AUDIO_SERVICE_TYPE`**

  - **`MASTERING_DISPLAY_METADATA`**

  - **`GOP_TIMECODE`**

  - **`SPHERICAL`**

  - **`CONTENT_LIGHT_LEVEL`**

  - **`ICC_PROFILE`**

  - **`S12M_TIMECODE`**

  - **`DYNAMIC_HDR_PLUS`**

  - **`REGIONS_OF_INTEREST`**

  - **`VIDEO_ENC_PARAMS`**

  - **`SEI_UNREGISTERED`**

  - **`FILM_GRAIN_PARAMS`**

  - **`DETECTION_BOUNDING_BOXES`**

  - **`DETECTION_BBOXES`**

  - **`DOVI_RPU_BUFFER`**

  - **`DOVI_METADATA`**

  - **`DYNAMIC_HDR_VIVID`**

  - **`AMBIENT_VIEWING_ENVIRONMENT`**

  - **`VIDEO_HINT`**
