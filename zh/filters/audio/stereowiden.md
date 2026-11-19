# stereowiden

This filter enhance the stereo effect by suppressing signal common to both channels and by delaying the signal of left into right and vice versa, thereby widening the stereo effect.

The filter accepts the following options:

- **`delay`** Time in milliseconds of the delay of left signal into right and vice versa. Default is 20 milliseconds.

- **`feedback`** Amount of gain in delayed signal into right and vice versa. Gives a delay effect of left signal in right output and vice versa which gives widening effect. Default is 0.3.

- **`crossfeed`** Cross feed of left into right with inverted phase. This helps in suppressing the mono. If the value is 1 it will cancel all the signal common to both channels. Default is 0.3.

- **`drymix`** Set level of input signal of original channel. Default is 0.8.

## Commands

This filter supports the all above options except `delay` as [commands](#commands).
