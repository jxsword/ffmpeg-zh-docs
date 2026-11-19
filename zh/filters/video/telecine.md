# telecine

Apply telecine process to the video.

This filter accepts the following options:

- **`first_field`**

  - **`top, t`** top field first

  - **`bottom, b`** bottom field first The default value is `top`.

- **`pattern`** A string of numbers representing the pulldown pattern you wish to apply. The default value is `23`.

``` text
Some typical patterns:

NTSC output (30i):
27.5p: 32222
24p: 23 (classic)
24p: 2332 (preferred)
20p: 33
18p: 334
16p: 3444

PAL output (25i):
27.5p: 12222
24p: 222222222223 ("Euro pulldown")
16.67p: 33
16p: 33333334
```
