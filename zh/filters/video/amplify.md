# amplify

Amplify differences between current pixel and pixels of adjacent frames in same pixel location.

This filter accepts the following options:

- **`radius`** Set frame radius. Default is 2. Allowed range is from 1 to 63. For example radius of 3 will instruct filter to calculate average of 7 frames.

- **`factor`** Set factor to amplify difference. Default is 2. Allowed range is from 0 to 65535.

- **`threshold`** Set threshold for difference amplification. Any difference greater or equal to this value will not alter source pixel. Default is 10. Allowed range is from 0 to 65535.

- **`tolerance`** Set tolerance for difference amplification. Any difference lower to this value will not alter source pixel. Default is 0. Allowed range is from 0 to 65535.

- **`low`** Set lower limit for changing source pixel. Default is 65535. Allowed range is from 0 to 65535. This option controls maximum possible value that will decrease source pixel value.

- **`high`** Set high limit for changing source pixel. Default is 65535. Allowed range is from 0 to 65535. This option controls maximum possible value that will increase source pixel value.

- **`planes`** Set which planes to filter. Default is all. Allowed range is from 0 to 15.

## Commands

This filter supports the following [commands](#commands) that corresponds to option of same name:

- **`factor`**

- **`threshold`**

- **`tolerance`**

- **`low`**

- **`high`**

- **`planes`**
