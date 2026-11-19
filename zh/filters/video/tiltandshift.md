# tiltandshift

Apply tilt-and-shift effect.

What happens when you invert time and space?

Normally a video is composed of several frames that represent a different instant of time and shows a scene that evolves in the space captured by the frame. This filter is the antipode of that concept, taking inspiration from tilt and shift photography.

A filtered frame contains the whole timeline of events composing the sequence, and this is obtained by placing a slice of pixels from each frame into a single one. However, since there are no infinite-width frames, this is done up the width of the input frame, and a video is recomposed by shifting away one column for each subsequent frame. In order to map space to time, the filter tilts each input frame as well, so that motion is preserved. This is accomplished by progressively selecting a different column from each input frame.

The end result is a sort of inverted parallax, so that far away objects move much faster that the ones in the front. The ideal conditions for this video effect are when there is either very little motion and the background is static, or when there is a lot of motion and a very wide depth of field (e.g. wide panorama, while moving on a train).

The filter accepts the following parameters:

- **`tilt`** Tilt video while shifting (default). When unset, video will be sliding a static image, composed of the first column of each frame.

- **`start`** What to do at the start of filtering (see below).

- **`end`** What to do at the end of filtering (see below).

- **`hold`** How many columns should pass through before start of filtering.

- **`pad`** How many columns should be inserted before end of filtering.

Normally the filter shifts and tilts from the very first frame, and stops when the last one is received. However, before filtering starts, normal video may be preserved, so that the effect is slowly shifted in its place. Similarly, the last video frame may be reconstructed at the end. Alternatively it is possible to just start and end with black.

| Term | Description |
|----|----|
| `none` | Filtering starts immediately and ends when the last frame is received. |
| `frame` | The first frames or the very last frame are kept intact during processing. |
| `black` | Black is padded at the beginning or at the end of filtering. |
