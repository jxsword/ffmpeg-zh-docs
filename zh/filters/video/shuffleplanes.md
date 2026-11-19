# shuffleplanes

Reorder and/or duplicate video planes.

It accepts the following parameters:

| Term | Description |
|----|----|
| `map0` | The index of the input plane to be used as the first output plane. |
| `map1` | The index of the input plane to be used as the second output plane. |
| `map2` | The index of the input plane to be used as the third output plane. |
| `map3` | The index of the input plane to be used as the fourth output plane. |

The first plane has the index 0. The default is to keep the input unchanged.

## Examples

- Swap the second and third planes of the input:

  ``` text
  ffmpeg -i INPUT -vf shuffleplanes=0:2:1:3 OUTPUT
  ```
