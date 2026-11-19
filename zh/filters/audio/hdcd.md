# hdcd

Decodes High Definition Compatible Digital (HDCD) data. A 16-bit PCM stream with embedded HDCD codes is expanded into a 20-bit PCM stream.

The filter supports the Peak Extend and Low-level Gain Adjustment features of HDCD, and detects the Transient Filter flag.

``` text
ffmpeg -i HDCD16.flac -af hdcd OUT24.flac
```

When using the filter with wav, note the default encoding for wav is 16-bit, so the resulting 20-bit stream will be truncated back to 16-bit. Use something like `-acodec pcm_s24le` after the filter to get 24-bit PCM output.

``` text
ffmpeg -i HDCD16.wav -af hdcd OUT16.wav
ffmpeg -i HDCD16.wav -af hdcd -c:a pcm_s24le OUT24.wav
```

The filter accepts the following options:

- **`disable_autoconvert`** Disable any automatic format conversion or resampling in the filter graph.

- **`process_stereo`** Process the stereo channels together. If target_gain does not match between channels, consider it invalid and use the last valid target_gain.

- **`cdt_ms`** Set the code detect timer period in ms.

- **`force_pe`** Always extend peaks above -3dBFS even if PE isn't signaled.

- **`analyze_mode`** Replace audio with a solid tone and adjust the amplitude to signal some specific aspect of the decoding process. The output file can be loaded in an audio editor alongside the original to aid analysis.

  `analyze_mode=pe:force_pe=true` can be used to see all samples above the PE level.

  Modes are:

  | Term       | Description                                                   |
  |------------|---------------------------------------------------------------|
  | `0, off` | Disabled                                                      |
  | `1, lle` | Gain adjustment level at each sample                          |
  | `2, pe`  | Samples where peak extend occurs                              |
  | `3, cdt` | Samples where the code detect timer is active                 |
  | `4, tgm` | Samples where the target gain does not match between channels |
