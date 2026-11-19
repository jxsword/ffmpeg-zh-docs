# libvmaf

Calculate the VMAF (Video Multi-Method Assessment Fusion) score for a reference/distorted pair of input videos.

The first input is the distorted video, and the second input is the reference video.

The obtained VMAF score is printed through the logging system.

It requires Netflix's vmaf library (libvmaf) as a pre-requisite. After installing the library it can be enabled using: `./configure --enable-libvmaf`.

The filter has following options:

- **`model`** A '\|' delimited list of vmaf models. Each model can be configured with a number of parameters. Default value: `"version=vmaf_v0.6.1"`

- **`feature`** A '\|' delimited list of features. Each feature can be configured with a number of parameters.

- **`log_path`** Set the file path to be used to store log files.

- **`log_fmt`** Set the format of the log file (xml, json, csv, or sub).

- **`pool`** Set the pool method to be used for computing vmaf. Options are `min`, `harmonic_mean` or `mean` (default).

- **`n_threads`** Set number of threads to be used when initializing libvmaf. Default value: `0`, no threads.

- **`n_subsample`** Set frame subsampling interval to be used.

This filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

## Examples

- In the examples below, a distorted video `distorted.mpg` is compared with a reference file `reference.mpg`.

- Basic usage:

  ``` text
  ffmpeg -i distorted.mpg -i reference.mpg -lavfi libvmaf=log_path=output.xml -f null -
  ```

- Example with multiple models:

  ``` text
  ffmpeg -i distorted.mpg -i reference.mpg -lavfi libvmaf='model=version=vmaf_v0.6.1\\:name=vmaf|version=vmaf_v0.6.1neg\\:name=vmaf_neg' -f null -
  ```

- Example with multiple additional features:

  ``` text
  ffmpeg -i distorted.mpg -i reference.mpg -lavfi libvmaf='feature=name=psnr|name=ciede' -f null -
  ```

- Example with options and different containers:

  ``` text
  ffmpeg -i distorted.mpg -i reference.mkv -lavfi "[0:v]settb=AVTB,setpts=PTS-STARTPTS[main];[1:v]settb=AVTB,setpts=PTS-STARTPTS[ref];[main][ref]libvmaf=log_fmt=json:log_path=output.json" -f null -
  ```
