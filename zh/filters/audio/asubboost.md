# asubboost

Boost subwoofer frequencies.

The filter accepts the following options:

- **`dry`** Set dry gain, how much of original signal is kept. Allowed range is from 0 to 1. Default value is 1.0.

- **`wet`** Set wet gain, how much of filtered signal is kept. Allowed range is from 0 to 1. Default value is 1.0.

- **`boost`** Set max boost factor. Allowed range is from 1 to 12. Default value is 2.

- **`decay`** Set delay line decay gain value. Allowed range is from 0 to 1. Default value is 0.0.

- **`feedback`** Set delay line feedback gain value. Allowed range is from 0 to 1. Default value is 0.9.

- **`cutoff`** Set cutoff frequency in Hertz. Allowed range is 50 to 900. Default value is 100.

- **`slope`** Set slope amount for cutoff frequency. Allowed range is 0.0001 to 1. Default value is 0.5.

- **`delay`** Set delay. Allowed range is from 1 to 100. Default value is 20.

- **`channels`** Set the channels to process. Default value is all available.

## Commands

This filter supports the all above options as [commands](#commands).
