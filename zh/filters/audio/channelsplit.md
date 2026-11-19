# channelsplit

Split each channel from an input audio stream into a separate output stream.

It accepts the following parameters:

- **`channel_layout`** The channel layout of the input stream. The default is "stereo".

- **`channels`** A channel layout describing the channels to be extracted as separate output streams or "all" to extract each input channel as a separate stream. The default is "all".

  Choosing channels not present in channel layout in the input will result in an error.

## Examples

- For example, assuming a stereo input MP3 file,

  ``` text
  ffmpeg -i in.mp3 -filter_complex channelsplit out.mkv
  ```

  will create an output Matroska file with two audio streams, one containing only the left channel and the other the right channel.

- Split a 5.1 WAV file into per-channel files:

  ``` text
  ffmpeg -i in.wav -filter_complex
  'channelsplit=channel_layout=5.1[FL][FR][FC][LFE][SL][SR]'
  -map '[FL]' front_left.wav -map '[FR]' front_right.wav -map '[FC]'
  front_center.wav -map '[LFE]' lfe.wav -map '[SL]' side_left.wav -map '[SR]'
  side_right.wav
  ```

- Extract only LFE from a 5.1 WAV file:

  ``` text
  ffmpeg -i in.wav -filter_complex 'channelsplit=channel_layout=5.1:channels=LFE[LFE]'
  -map '[LFE]' lfe.wav
  ```
