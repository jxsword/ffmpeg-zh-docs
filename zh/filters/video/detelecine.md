# detelecine

Apply an exact inverse of the telecine operation. It requires a predefined pattern specified using the pattern option which must be the same as that passed to the telecine filter.

This filter accepts the following options:

- **`first_field`**

  - **`top, t`** top field first

  - **`bottom, b`** bottom field first The default value is `top`.

- **`pattern`** A string of numbers representing the pulldown pattern you wish to apply. The default value is `23`.

- **`start_frame`** A number representing position of the first frame with respect to the telecine pattern. This is to be used if the stream is cut. The default value is `0`.
