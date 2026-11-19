# shufflepixels

Reorder pixels in video frames.

This filter accepts the following options:

- **`direction, d`** Set shuffle direction. Can be forward or inverse direction. Default direction is forward.

- **`mode, m`** Set shuffle mode. Can be horizontal, vertical or block mode.

- **`width, w`**

- **`height, h`** Set shuffle block_size. In case of horizontal shuffle mode only width part of size is used, and in case of vertical shuffle mode only height part of size is used.

- **`seed, s`** Set random seed used with shuffling pixels. Mainly useful to set to be able to reverse filtering process to get original input. For example, to reverse forward shuffle you need to use same parameters and exact same seed and to set direction to inverse.
