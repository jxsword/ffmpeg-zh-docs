# sr

Scale the input by applying one of the super-resolution methods based on convolutional neural networks. Supported models:

- Super-Resolution Convolutional Neural Network model (SRCNN). See <https://arxiv.org/abs/1501.00092>.

- Efficient Sub-Pixel Convolutional Neural Network model (ESPCN). See <https://arxiv.org/abs/1609.05158>.

Training scripts as well as scripts for model file (.pb) saving can be found at <https://github.com/XueweiMeng/sr/tree/sr_dnn_native>. Original repository is at <https://github.com/HighVoltageRocknRoll/sr.git>.

The filter accepts the following options:

- **`dnn_backend`** Specify which DNN backend to use for model loading and execution. This option accepts the following values:

  - **`tensorflow`** TensorFlow backend. To enable this backend you need to install the TensorFlow for C library (see <https://www.tensorflow.org/install/lang_c>) and configure FFmpeg with `--enable-libtensorflow`

- **`model`** Set path to model file specifying network architecture and its parameters. Note that different backends use different file formats. TensorFlow, OpenVINO backend can load files for only its format.

- **`scale_factor`** Set scale factor for SRCNN model. Allowed values are `2`, `3` and `4`. Default value is `2`. Scale factor is necessary for SRCNN model, because it accepts input upscaled using bicubic upscaling with proper scale factor.

To get full functionality (such as async execution), please use the [dnn_processing](dnn_detect.md#dnn_detect) filter.
