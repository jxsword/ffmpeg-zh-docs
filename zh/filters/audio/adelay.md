# adelay

Delay one or more audio channels.

Samples in delayed channel are filled with silence.

The filter accepts the following option:

- **`delays`** Set list of delays in milliseconds for each channel separated by '\|'. Unused delays will be silently ignored. If number of given delays is smaller than number of channels all remaining channels will not be delayed. If you want to delay exact number of samples, append 'S' to number. If you want instead to delay in seconds, append 's' to number.

- **`all`** Use last set delay for all remaining channels. By default is disabled. This option if enabled changes how option `delays` is interpreted.

## Examples

- Delay first channel by 1.5 seconds, the third channel by 0.5 seconds and leave the second channel (and any other channels that may be present) unchanged.

  ``` text
  adelay=1500|0|500
  ```

- Delay second channel by 500 samples, the third channel by 700 samples and leave the first channel (and any other channels that may be present) unchanged.

  ``` text
  adelay=0|500S|700S
  ```

- Delay all channels by same number of samples:

  ``` text
  adelay=delays=64S:all=1
  ```
