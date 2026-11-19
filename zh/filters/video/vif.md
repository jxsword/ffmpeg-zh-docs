# vif

Obtain the average VIF (Visual Information Fidelity) between two input videos.

This filter takes two input videos.

Both input videos must have the same resolution and pixel format for this filter to work correctly. Also it assumes that both inputs have the same number of frames, which are compared one by one.

The obtained average VIF score is printed through the logging system.

The filter stores the calculated VIF score of each frame.

This filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.

In the below example the input file `main.mpg` being processed is compared with the reference file `ref.mpg`.

``` text
ffmpeg -i main.mpg -i ref.mpg -lavfi vif -f null -
```
