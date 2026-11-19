# dcshift

Apply a DC shift to the audio.

This can be useful to remove a DC offset (caused perhaps by a hardware problem in the recording chain) from the audio. The effect of a DC offset is reduced headroom and hence volume. The [astats](astats.md#astats) filter can be used to determine if a signal has a DC offset.

- **`shift`** Set the DC shift, allowed range is \[-1, 1\]. It indicates the amount to shift the audio.

- **`limitergain`** Optional. It should have a value much less than 1 (e.g. 0.05 or 0.02) and is used to prevent clipping.
