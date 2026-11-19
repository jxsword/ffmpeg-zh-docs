# displace

Displace pixels as indicated by second and third input stream.

It takes three input streams and outputs one stream, the first input is the source, and second and third input are displacement maps.

The second input specifies how much to displace pixels along the x-axis, while the third input specifies how much to displace pixels along the y-axis. If one of displacement map streams terminates, last frame from that displacement map will be used.

Note that once generated, displacements maps can be reused over and over again.

A description of the accepted options follows.

- **`edge`** Set displace behavior for pixels that are out of range.

  Available values are:

  | Term | Description |
  |----|----|
  | `blank` | Missing pixels are replaced by black pixels. |
  | `smear` | Adjacent pixels will spread out to replace missing pixels. |
  | `wrap` | Out of range pixels are wrapped so they point to pixels of other side. |
  | `mirror` | Out of range pixels will be replaced with mirrored pixels. |

  Default is `smear`.

## Examples

- Add ripple effect to rgb input of video size hd720:

  ``` text
  ffmpeg -i INPUT -f lavfi -i nullsrc=s=hd720,lutrgb=128:128:128 -f lavfi -i nullsrc=s=hd720,geq='r=128+30*sin(2*PI*X/400+T):g=128+30*sin(2*PI*X/400+T):b=128+30*sin(2*PI*X/400+T)' -lavfi '[0][1][2]displace' OUTPUT
  ```

- Add wave effect to rgb input of video size hd720:

  ``` text
  ffmpeg -i INPUT -f lavfi -i nullsrc=hd720,geq='r=128+80*(sin(sqrt((X-W/2)*(X-W/2)+(Y-H/2)*(Y-H/2))/220*2*PI+T)):g=128+80*(sin(sqrt((X-W/2)*(X-W/2)+(Y-H/2)*(Y-H/2))/220*2*PI+T)):b=128+80*(sin(sqrt((X-W/2)*(X-W/2)+(Y-H/2)*(Y-H/2))/220*2*PI+T))' -lavfi '[1]split[x][y],[0][x][y]displace' OUTPUT
  ```
