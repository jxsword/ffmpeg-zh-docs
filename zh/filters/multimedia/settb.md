# settb, asettb

Set the timebase to use for the output frames timestamps. It is mainly useful for testing timebase configuration.

It accepts the following parameters:

| Term       | Description                                                 |
|------------|-------------------------------------------------------------|
| `expr, tb` | The expression which is evaluated into the output timebase. |

The value for `tb` is an arithmetic expression representing a rational. The expression can contain the constants "AVTB" (the default timebase), "intb" (the input timebase) and "sr" (the sample rate, audio only). Default value is "intb".

## Examples

- Set the timebase to 1/25:

  ``` text
  settb=expr=1/25
  ```

- Set the timebase to 1/10:

  ``` text
  settb=expr=0.1
  ```

- Set the timebase to 1001/1000:

  ``` text
  settb=1+0.001
  ```

- Set the timebase to 2\*intb:

  ``` text
  settb=2*intb
  ```

- Set the default timebase value:

  ``` text
  settb=AVTB
  ```
