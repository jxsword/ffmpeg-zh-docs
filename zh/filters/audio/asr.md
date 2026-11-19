# asr

Automatic Speech Recognition

This filter uses PocketSphinx for speech recognition. To enable compilation of this filter, you need to configure FFmpeg with `--enable-pocketsphinx`.

It accepts the following options:

- **`rate`** Set sampling rate of input audio. Defaults is `16000`. This need to match speech models, otherwise one will get poor results.

- **`hmm`** Set dictionary containing acoustic model files.

- **`dict`** Set pronunciation dictionary.

- **`lm`** Set language model file.

- **`lmctl`** Set language model set.

- **`lmname`** Set which language model to use.

- **`logfn`** Set output for log messages.

The filter exports recognized speech as the frame metadata `lavfi.asr.text`.
