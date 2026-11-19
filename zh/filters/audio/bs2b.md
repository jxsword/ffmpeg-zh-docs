# bs2b

Bauer stereo to binaural transformation, which improves headphone listening of stereo audio records.

To enable compilation of this filter you need to configure FFmpeg with `--enable-libbs2b`.

It accepts the following parameters:

- **`profile`** Pre-defined crossfeed level.

  | Term      | Description                            |
  |-----------|----------------------------------------|
  | `default` | Default level (fcut=700, feed=50).     |
  | `cmoy`    | Chu Moy circuit (fcut=700, feed=60).   |
  | `jmeier`  | Jan Meier circuit (fcut=650, feed=95). |

- **`fcut`** Cut frequency (in Hz).

- **`feed`** Feed level (in Hz).
