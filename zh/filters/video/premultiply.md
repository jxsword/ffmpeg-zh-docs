# premultiply

Apply alpha premultiply effect to input video stream using first plane of second stream as alpha.

Both streams must have same dimensions and same pixel format.

The filter accepts the following option:

- **`planes`** Set which planes will be processed, unprocessed planes will be copied. By default value 0xf, all planes will be processed.

- **`inplace`** Do not require 2nd input for processing, instead use alpha plane from input stream.
