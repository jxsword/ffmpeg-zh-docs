# flite

Synthesize a voice utterance using the libflite library.

To enable compilation of this filter you need to configure FFmpeg with `--enable-libflite`.

Note that versions of the flite library prior to 2.0 are not thread-safe.

The filter accepts the following options:

- **`list_voices`** If set to 1, list the names of the available voices and exit immediately. Default value is 0.

- **`nb_samples, n`** Set the maximum number of samples per frame. Default value is 512.

- **`textfile`** Set the filename containing the text to speak.

- **`text`** Set the text to speak.

- **`voice, v`** Set the voice to use for the speech synthesis. Default value is `kal`. See also the \<list_voices\> option.

## Examples

- Read from file `speech.txt`, and synthesize the text using the standard flite voice:

  ``` text
  flite=textfile=speech.txt
  ```

- Read the specified text selecting the `slt` voice:

  ``` text
  flite=text='So fare thee well, poor devil of a Sub-Sub, whose commentator I am':voice=slt
  ```

- Input text to ffmpeg:

  ``` text
  ffmpeg -f lavfi -i flite=text='So fare thee well, poor devil of a Sub-Sub, whose commentator I am':voice=slt
  ```

- Make `ffplay` speak the specified text, using `flite` and the `lavfi` device:

  ``` text
  ffplay -f lavfi flite=text='No more be grieved for which that thou hast done.'
  ```

For more information about libflite, check: <http://www.festvox.org/flite/>
