# transpose

Transpose rows with columns in the input video and optionally flip it.

It accepts the following parameters:

- **`dir`** Specify the transposition direction.

  Can assume the following values:

  - **`0, 4, cclock_flip`** Rotate by 90 degrees counterclockwise and vertically flip (default), that is:

    ``` text
    L.R     L.l
    . . ->  . .
    l.r     R.r
    ```

  - **`1, 5, clock`** Rotate by 90 degrees clockwise, that is:

    ``` text
    L.R     l.L
    . . ->  . .
    l.r     r.R
    ```

  - **`2, 6, cclock`** Rotate by 90 degrees counterclockwise, that is:

    ``` text
    L.R     R.r
    . . ->  . .
    l.r     L.l
    ```

  - **`3, 7, clock_flip`** Rotate by 90 degrees clockwise and vertically flip, that is:

    ``` text
    L.R     r.R
    . . ->  . .
    l.r     l.L
    ```

  For values between 4-7, the transposition is only done if the input video geometry is portrait and not landscape. These values are deprecated, the `passthrough` option should be used instead.

  Numerical values are deprecated, and should be dropped in favor of symbolic constants.

- **`passthrough`** Do not apply the transposition if the input geometry matches the one specified by the specified value. It accepts the following values:

  - **`none`** Always apply transposition.

  - **`portrait`** Preserve portrait geometry (when \<height\> \>= \<width\>).

  - **`landscape`** Preserve landscape geometry (when \<width\> \>= \<height\>).

  Default value is `none`.

For example to rotate by 90 degrees clockwise and preserve portrait layout:

``` text
transpose=dir=1:passthrough=portrait
```

The command above can also be specified as:

``` text
transpose=1:portrait
```
