# hue

Modify the hue and/or the saturation of the input.

It accepts the following parameters:

- **`h`** Specify the hue angle as a number of degrees. It accepts an expression, and defaults to "0".

- **`s`** Specify the saturation in the \[-10,10\] range. It accepts an expression and defaults to "1".

- **`H`** Specify the hue angle as a number of radians. It accepts an expression, and defaults to "0".

- **`b`** Specify the brightness in the \[-10,10\] range. It accepts an expression and defaults to "0".

`h` and `H` are mutually exclusive, and can't be specified at the same time.

The `b`, `h`, `H` and `s` option values are expressions containing the following constants:

| Term | Description |
|----|----|
| `n` | frame count of the input frame starting from 0 |
| `pts` | presentation timestamp of the input frame expressed in time base units |
| `r` | frame rate of the input video, NAN if the input frame rate is unknown |
| `t` | timestamp expressed in seconds, NAN if the input timestamp is unknown |
| `tb` | time base of the input video |

## Examples

- Set the hue to 90 degrees and the saturation to 1.0:

  ``` text
  hue=h=90:s=1
  ```

- Same command but expressing the hue in radians:

  ``` text
  hue=H=PI/2:s=1
  ```

- Rotate hue and make the saturation swing between 0 and 2 over a period of 1 second:

  ``` text
  hue="H=2*PI*t: s=sin(2*PI*t)+1"
  ```

- Apply a 3 seconds saturation fade-in effect starting at 0:

  ``` text
  hue="s=min(t/3\,1)"
  ```

  The general fade-in expression can be written as:

  ``` text
  hue="s=min(0\, max((t-START)/DURATION\, 1))"
  ```

- Apply a 3 seconds saturation fade-out effect starting at 5 seconds:

  ``` text
  hue="s=max(0\, min(1\, (8-t)/3))"
  ```

  The general fade-out expression can be written as:

  ``` text
  hue="s=max(0\, min(1\, (START+DURATION-t)/DURATION))"
  ```

## Commands

This filter supports the following commands:

- **`b`**

- **`s`**

- **`h`**

- **`H`** Modify the hue and/or the saturation and/or brightness of the input video. The command accepts the same syntax of the corresponding option.

  If the specified expression is not valid, it is kept at its current value.
