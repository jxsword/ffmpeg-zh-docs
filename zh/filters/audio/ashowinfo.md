# ashowinfo

Show a line containing various information for each input audio frame. The input audio is not modified.

The shown line contains a sequence of key/value pairs of the form \<key\>:\<value\>.

The following values are shown in the output:

- **`n`** The (sequential) number of the input frame, starting from 0.

- **`pts`** The presentation timestamp of the input frame, in time base units; the time base depends on the filter input pad, and is usually 1/\<sample_rate\>.

- **`pts_time`** The presentation timestamp of the input frame in seconds.

- **`fmt`** The sample format.

- **`chlayout`** The channel layout.

- **`rate`** The sample rate for the audio frame.

- **`nb_samples`** The number of samples (per channel) in the frame.

- **`checksum`** The Adler-32 checksum (printed in hexadecimal) of the audio data. For planar audio, the data is treated as if all the planes were concatenated.

- **`plane_checksums`** A list of Adler-32 checksums for each data plane.
