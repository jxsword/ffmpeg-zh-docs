# frc_amf

Double the frame rate, using Frame Rate Converter (FRC) provided by AMD Advanced Media Framework library for hardware acceleration.

The filter accepts the following options:

- **`engine_type`** Specify the engine used to run shaders.

  | Term     | Description                 |
  |----------|-----------------------------|
  | `dx11` | DirectX 11.                 |
  | `dx12` | DirectX 12 (Default value). |

- **`enable`** Boolean value: enable/disable FRC. Dynamic value, can be altered at a runtime without re-initializing the filter. (Default value: enabled).

- **`fallback_mode`** Fallback behavior in case of low interpolation confidence.

  | Term          | Description                                |
  |---------------|--------------------------------------------|
  | `duplicate` | Duplicate frame.                           |
  | `blend`     | Blend two frames together (Default value). |

- **`indicator`** Boolean value: show FRC indicator square in the top left corner of the video (Default value: disabled).

- **`profile`** Level of hierarchical motion search.

  - **`low`** Less levels of hierarchical motion search. Only recommended for extremely low resolutions.

  - **`high`** Recommended for any resolution up to 1440p. (Default value)

  - **`super`** More levels of hierarchical motion search. Recommended for resolutions 1440p or higher.

- **`mv_search_mode`** Performance mode of the motion search.

  - **`native`** Conduct motion search on the full resolution of source images.

  - **`performance`** Conduct motion search on the down scaled source images. Recommended for APU or low end GPU for better performance.

- **`use_future_frame`** Boolean value: enable dependency on future frame, improves quality for the cost of latency (Default value: enabled).
