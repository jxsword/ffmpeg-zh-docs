# adrc

Apply spectral dynamic range controller filter to input audio stream.

A description of the accepted options follows.

- **`transfer`** Set the transfer expression.

  The expression can contain the following constants:

  | Term          | Description                          |
  |---------------|--------------------------------------|
  | `ch`          | current channel number               |
  | `sn`          | current sample number                |
  | `nb_channels` | number of channels                   |
  | `t`           | timestamp expressed in seconds       |
  | `sr`          | sample rate                          |
  | `p`           | current frequency power value, in dB |
  | `f`           | current frequency in Hz              |

  Default value is `p`.

- **`attack`** Set the attack in milliseconds. Default is `50` milliseconds. Allowed range is from 1 to 1000 milliseconds.

- **`release`** Set the release in milliseconds. Default is `100` milliseconds. Allowed range is from 5 to 2000 milliseconds.

- **`channels`** Set which channels to filter, by default `all` channels in audio stream are filtered.

## Commands

This filter supports the all above options as [commands](#commands).

## Examples

- Apply spectral compression to all frequencies with threshold of -50 dB and 1:6 ratio:

  ``` text
  adrc=transfer='if(gt(p,-50),-50+(p-(-50))/6,p)':attack=50:release=100
  ```

- Similar to above but with 1:2 ratio and filtering only front center channel:

  ``` text
  adrc=transfer='if(gt(p,-50),-50+(p-(-50))/2,p)':attack=50:release=100:channels=FC
  ```

- Apply spectral noise gate to all frequencies with threshold of -85 dB and with short attack time and short release time:

  ``` text
  adrc=transfer='if(lte(p,-85),p-800,p)':attack=1:release=5
  ```

- Apply spectral expansion to all frequencies with threshold of -10 dB and 1:2 ratio:

  ``` text
  adrc=transfer='if(lt(p,-10),-10+(p-(-10))*2,p)':attack=50:release=100
  ```

- Apply limiter to max -60 dB to all frequencies, with attack of 2 ms and release of 10 ms:

  ``` text
  adrc=transfer='min(p,-60)':attack=2:release=10
  ```
