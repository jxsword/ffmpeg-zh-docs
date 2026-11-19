# deblock

Remove blocking artifacts from input video.

The filter accepts the following options:

- **`filter`** Set filter type, can be \<weak\> or \<strong\>. Default is \<strong\>. This controls what kind of deblocking is applied.

- **`block`** Set size of block, allowed range is from 4 to 512. Default is \<8\>.

- **`alpha`**

- **`beta`**

- **`gamma`**

- **`delta`** Set blocking detection thresholds. Allowed range is 0 to 1. Defaults are: \<0.098\> for \<alpha\> and \<0.05\> for the rest. Using higher threshold gives more deblocking strength. Setting \<alpha\> controls threshold detection at exact edge of block. Remaining options controls threshold detection near the edge. Each one for below/above or left/right. Setting any of those to \<0\> disables deblocking.

- **`planes`** Set planes to filter. Default is to filter all available planes.

## Examples

- Deblock using weak filter and block size of 4 pixels.

  ``` text
  deblock=filter=weak:block=4
  ```

- Deblock using strong filter, block size of 4 pixels and custom thresholds for deblocking more edges.

  ``` text
  deblock=filter=strong:block=4:alpha=0.12:beta=0.07:gamma=0.06:delta=0.05
  ```

- Similar as above, but filter only first plane.

  ``` text
  deblock=filter=strong:block=4:alpha=0.12:beta=0.07:gamma=0.06:delta=0.05:planes=1
  ```

- Similar as above, but filter only second and third plane.

  ``` text
  deblock=filter=strong:block=4:alpha=0.12:beta=0.07:gamma=0.06:delta=0.05:planes=6
  ```

## Commands

This filter supports the all above options as [commands](#commands).
