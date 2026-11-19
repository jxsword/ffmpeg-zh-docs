# roberts

Apply roberts cross operator to input video stream.

The filter accepts the following option:

- **`planes`** Set which planes will be processed, unprocessed planes will be copied. By default value 0xf, all planes will be processed.

- **`scale`** Set value which will be multiplied with filtered result.

- **`delta`** Set value which will be added to filtered result.

## Commands

This filter supports the all above options as [commands](#commands).
