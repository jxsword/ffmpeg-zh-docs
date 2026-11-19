# hwupload

Upload system memory frames to hardware surfaces.

The device to upload to must be supplied when the filter is initialised. If using ffmpeg, select the appropriate device with the `-filter_hw_device` option or with the `derive_device` option. The input and output devices must be of different types and compatible - the exact meaning of this is system-dependent, but typically it means that they must refer to the same underlying hardware context (for example, refer to the same graphics card).

The following additional parameters are accepted:

- **`derive_device type`** Rather than using the device supplied at initialisation, instead derive a new device of type \<type\> from the device the input frames exist on.
