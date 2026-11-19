# derain

Remove the rain in the input image/video by applying the derain methods based on convolutional neural networks. Supported models:

- Recurrent Squeeze-and-Excitation Context Aggregation Net (RESCAN). See <http://openaccess.thecvf.com/content_ECCV_2018/papers/Xia_Li_Recurrent_Squeeze-and-Excitation_Context_ECCV_2018_paper.pdf>.

Training as well as model generation scripts are provided in the repository at <https://github.com/XueweiMeng/derain_filter.git>.

The filter accepts the following options:

- **`filter_type`** Specify which filter to use. This option accepts the following values:

  | Term | Description |
  |----|----|
  | `derain` | Derain filter. To conduct derain filter, you need to use a derain model. |
  | `dehaze` | Dehaze filter. To conduct dehaze filter, you need to use a dehaze model. |

  Default value is `derain`.

- **`dnn_backend`** Specify which DNN backend to use for model loading and execution. This option accepts the following values:

  - **`tensorflow`** TensorFlow backend. To enable this backend you need to install the TensorFlow for C library (see <https://www.tensorflow.org/install/lang_c>) and configure FFmpeg with `--enable-libtensorflow`

- **`model`** Set path to model file specifying network architecture and its parameters. Note that different backends use different file formats. TensorFlow can load files for only its format.

To get full functionality (such as async execution), please use the [dnn_processing](dnn_detect.md#dnn_detect) filter.
