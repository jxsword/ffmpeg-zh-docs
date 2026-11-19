# quirc

Identify and decode a QR code using the libquirc library (see <https://github.com/dlbeer/quirc/>), and print the identified QR codes positions and payload as metadata.

To enable the compilation of this filter, you need to configure FFmpeg with `--enable-libquirc`.

For each found QR code in the input video, some metadata entries are added with the prefix \<lavfi.quirc.N\>, where \<N\> is the index, starting from 0, associated to the QR code.

A description of each metadata value follows:

- **`lavfi.quirc.count`** the number of found QR codes, it is not set in case none was found

- **`lavfi.quirc.N.corner.M.x`**

- **`lavfi.quirc.N.coreer.M.y`** the x/y positions of the four corners of the square containing the QR code, where \<M\> is the index of the corner starting from 0

- **`lavfi.quirc.N.payload`** the payload of the QR code
