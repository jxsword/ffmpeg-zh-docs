# fspp

Apply fast and simple postprocessing. It is a faster version of [spp](spp.md#spp).

It splits (I)DCT into horizontal/vertical passes. Unlike the simple post- processing filter, one of them is performed once per block, not per pixel. This allows for much higher speed.

The filter accepts the following options:

- **`quality`** Set quality. This option defines the number of levels for averaging. It accepts an integer in the range 4-5. Default value is `4`.

- **`qp`** Force a constant quantization parameter. It accepts an integer in range 0-63. If not set, the filter will use the QP from the video stream (if available).

- **`strength`** Set filter strength. It accepts an integer in range -15 to 32. Lower values mean more details but also more artifacts, while higher values make the image smoother but also blurrier. Default value is `0` − PSNR optimal.

- **`use_bframe_qp`** Enable the use of the QP from the B-Frames if set to `1`. Using this option may cause flicker since the B-Frames have often larger QP. Default is `0` (not enabled).
