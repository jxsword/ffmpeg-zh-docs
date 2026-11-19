# acrusher

Reduce audio bit resolution.

This filter is bit crusher with enhanced functionality. A bit crusher is used to audibly reduce number of bits an audio signal is sampled with. This doesn't change the bit depth at all, it just produces the effect. Material reduced in bit depth sounds more harsh and "digital". This filter is able to even round to continuous values instead of discrete bit depths. Additionally it has a D/C offset which results in different crushing of the lower and the upper half of the signal. An Anti-Aliasing setting is able to produce "softer" crushing sounds.

Another feature of this filter is the logarithmic mode. This setting switches from linear distances between bits to logarithmic ones. The result is a much more "natural" sounding crusher which doesn't gate low signals for example. The human ear has a logarithmic perception, so this kind of crushing is much more pleasant. Logarithmic crushing is also able to get anti-aliased.

The filter accepts the following options:

- **`level_in`** Set level in.

- **`level_out`** Set level out.

- **`bits`** Set bit reduction.

- **`mix`** Set mixing amount.

- **`mode`** Can be linear: `lin` or logarithmic: `log`.

- **`dc`** Set DC.

- **`aa`** Set anti-aliasing.

- **`samples`** Set sample reduction.

- **`lfo`** Enable LFO. By default disabled.

- **`lforange`** Set LFO range.

- **`lforate`** Set LFO rate.

## Commands

This filter supports the all above options as [commands](#commands).
