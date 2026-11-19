# deesser

Apply de-essing to the audio samples.

- **`i`** Set intensity for triggering de-essing. Allowed range is from 0 to 1. Default is 0.

- **`m`** Set amount of ducking on treble part of sound. Allowed range is from 0 to 1. Default is 0.5.

- **`f`** How much of original frequency content to keep when de-essing. Allowed range is from 0 to 1. Default is 0.5.

- **`s`** Set the output mode.

  It accepts the following values:

  - **`i`** Pass input unchanged.

  - **`o`** Pass ess filtered out.

  - **`e`** Pass only ess.

    Default value is \<o\>.
