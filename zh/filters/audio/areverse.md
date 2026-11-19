# areverse

Reverse an audio clip.

Warning: This filter requires memory to buffer the entire clip, so trimming is suggested.

## Examples

- Take the first 5 seconds of a clip, and reverse it.

  ``` text
  atrim=end=5,areverse
  ```
