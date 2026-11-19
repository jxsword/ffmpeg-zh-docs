# anlmdn

Reduce broadband noise in audio samples using Non-Local Means algorithm.

Each sample is adjusted by looking for other samples with similar contexts. This context similarity is defined by comparing their surrounding patches of size `p`. Patches are searched in an area of `r` around the sample.

The filter accepts the following options:

- **`strength, s`** Set denoising strength. Allowed range is from 0.00001 to 10000. Default value is 0.00001.

- **`patch, p`** Set patch radius duration. Allowed range is from 1 to 100 milliseconds. Default value is 2 milliseconds.

- **`research, r`** Set research radius duration. Allowed range is from 2 to 300 milliseconds. Default value is 6 milliseconds.

- **`output, o`** Set the output mode.

  It accepts the following values:

  - **`i`** Pass input unchanged.

  - **`o`** Pass noise filtered out.

  - **`n`** Pass only noise.

    Default value is \<o\>.

- **`smooth, m`** Set smooth factor. Default value is \<11\>. Allowed range is from \<1\> to \<1000\>.

## Commands

This filter supports the all above options as [commands](#commands).
