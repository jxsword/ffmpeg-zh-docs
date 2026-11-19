# blockdetect

Determines blockiness of frames without altering the input frames.

Based on Remco Muijs and Ihor Kirenko: "A no-reference blocking artifact measure for adaptive video processing." 2005 13th European signal processing conference.

The filter accepts the following options:

- **`period_min`**

- **`period_max`** Set minimum and maximum values for determining pixel grids (periods). Default values are \[3,24\].

- **`planes`** Set planes to filter. Default is first only.

## Examples

- Determine blockiness for the first plane and search for periods within \[8,32\]:

  ``` text
  blockdetect=period_min=8:period_max=32:planes=1
  ```
