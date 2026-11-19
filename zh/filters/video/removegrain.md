# removegrain

The removegrain filter is a spatial denoiser for progressive video.

| Term | Description                    |
|------|--------------------------------|
| `m0` | Set mode for the first plane.  |
| `m1` | Set mode for the second plane. |
| `m2` | Set mode for the third plane.  |
| `m3` | Set mode for the fourth plane. |

Range of mode is from 0 to 24. Description of each mode follows:

- **\<0\>** Leave input plane unchanged. Default.

- **\<1\>** Clips the pixel with the minimum and maximum of the 8 neighbour pixels.

- **\<2\>** Clips the pixel with the second minimum and maximum of the 8 neighbour pixels.

- **\<3\>** Clips the pixel with the third minimum and maximum of the 8 neighbour pixels.

- **\<4\>** Clips the pixel with the fourth minimum and maximum of the 8 neighbour pixels. This is equivalent to a median filter.

- **\<5\>** Line-sensitive clipping giving the minimal change.

- **\<6\>** Line-sensitive clipping, intermediate.

- **\<7\>** Line-sensitive clipping, intermediate.

- **\<8\>** Line-sensitive clipping, intermediate.

- **\<9\>** Line-sensitive clipping on a line where the neighbours pixels are the closest.

- **\<10\>** Replaces the target pixel with the closest neighbour.

- **\<11\>** \[1 2 1\] horizontal and vertical kernel blur.

- **\<12\>** Same as mode 11.

- **\<13\>** Bob mode, interpolates top field from the line where the neighbours pixels are the closest.

- **\<14\>** Bob mode, interpolates bottom field from the line where the neighbours pixels are the closest.

- **\<15\>** Bob mode, interpolates top field. Same as 13 but with a more complicated interpolation formula.

- **\<16\>** Bob mode, interpolates bottom field. Same as 14 but with a more complicated interpolation formula.

- **\<17\>** Clips the pixel with the minimum and maximum of respectively the maximum and minimum of each pair of opposite neighbour pixels.

- **\<18\>** Line-sensitive clipping using opposite neighbours whose greatest distance from the current pixel is minimal.

- **\<19\>** Replaces the pixel with the average of its 8 neighbours.

- **\<20\>** Averages the 9 pixels (\[1 1 1\] horizontal and vertical blur).

- **\<21\>** Clips pixels using the averages of opposite neighbour.

- **\<22\>** Same as mode 21 but simpler and faster.

- **\<23\>** Small edge and halo removal, but reputed useless.

- **\<24\>** Similar as 23.
