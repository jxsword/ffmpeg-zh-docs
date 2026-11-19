# alphamerge

Add or replace the alpha component of the primary input with the grayscale value of a second input. This is intended for use with \<alphaextract\> to allow the transmission or storage of frame sequences that have alpha in a format that doesn't support an alpha channel.

For example, to reconstruct full frames from a normal YUV-encoded video and a separate video created with \<alphaextract\>, you might use:

``` text
movie=in_alpha.mkv [alpha]; [in][alpha] alphamerge [out]
```
