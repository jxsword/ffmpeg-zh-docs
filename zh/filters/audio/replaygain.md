# replaygain

ReplayGain scanner filter. This filter takes an audio stream as an input and outputs it unchanged. At end of filtering it displays `track_gain` and `track_peak`.

The filter accepts the following exported read-only options:

| Term         | Description                                 |
|--------------|---------------------------------------------|
| `track_gain` | Exported track gain in dB at end of stream. |
| `track_peak` | Exported track peak at end of stream.       |
