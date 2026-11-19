# dnn_processing

Do image processing with deep neural networks. It works together with another filter which converts the pixel format of the Frame to what the dnn network requires.

The filter accepts the following options:

- **`dnn_backend`** Specify which DNN backend to use for model loading and execution. This option accepts the following values:

  - **`tensorflow`** TensorFlow backend. To enable this backend you need to install the TensorFlow for C library (see <https://www.tensorflow.org/install/lang_c>) and configure FFmpeg with `--enable-libtensorflow`

  - **`openvino`** OpenVINO backend. To enable this backend you need to build and install the OpenVINO for C library (see <https://github.com/openvinotoolkit/openvino/blob/master/build-instruction.md>) and configure FFmpeg with `--enable-libopenvino` (–extra-cflags=-I... –extra-ldflags=-L... might be needed if the header files and libraries are not installed into system path)

  - **`torch`** Libtorch backend. To enable this backend you need to build and install Libtroch for C++ library. Please download cxx11 ABI version (see <https://pytorch.org/get-started/locally>) and configure FFmpeg with `--enable-libtorch --extra-cflags=-I/libtorch_root/libtorch/include --extra-cflags=-I/libtorch_root/libtorch/include/torch/csrc/api/include --extra-ldflags=-L/libtorch_root/libtorch/lib/`

  - **`onnx`** ONNX Runtime backend. To enable this backend you need to install the ONNX Runtime library (see <https://onnxruntime.ai/>) and configure FFmpeg with `--enable-libonnxruntime`.

    The current ONNX Runtime backend expects 4-D input and output tensors with NCHW layout and 32-bit floating-point element type (ONNX `FLOAT`); models with integer or other element types (e.g. `UINT8`) are not supported and will be rejected at load time. Models using NHWC layout or other ranks are not yet supported. Only single-input models are supported; the backend binds exactly one input tensor when running the model.

    The `input` and `output` options are optional for the ONNX Runtime backend; when they are omitted the backend resolves the tensor names from the session.

    The ONNX Runtime backend runs inference synchronously using a single inference request. The shared `async` and `nireq` options therefore have no effect for `dnn_backend=onnx`; inference always runs synchronously regardless of their values.

- **`model`** Set path to model file specifying network architecture and its parameters. Note that different backends use different file formats. TensorFlow, OpenVINO, Libtorch, and ONNX Runtime backends can load files for only their respective formats.

- **`input`** Set the input name of the dnn network. Required for the TensorFlow backend; optional for the ONNX Runtime backend.

- **`output`** Set the output name of the dnn network. Required for the TensorFlow backend; optional for the ONNX Runtime backend.

- **`backend_configs`** Set the configs to be passed into backend. To use async execution, set async (default: set). Roll back to sync execution if the backend does not support async.

  For tensorflow backend, you can set its configs with `sess_config` options, please use tools/python/tf_sess_config.py to get the configs of TensorFlow backend for your system.

- **`device`** Set the device to run the model. For the ONNX Runtime backend this selects the execution provider: `cpu` (default), `cuda` (NVIDIA GPU), `dml` (DirectML, Windows only) or `vitisai` (AMD Ryzen AI NPU).

- **`device_id`** Set the device index used by GPU execution providers (e.g. `cuda` or `dml`) for the ONNX Runtime backend. Default is 0.

- **`threads_per_operation`** ONNX Runtime backend only. Set the number of CPU threads used per ONNX Runtime operator when running with `device=cpu`. Default is 0 (let ONNX Runtime choose automatically). Has no effect for GPU/NPU providers.

## Examples

- Remove rain in rgb24 frame with can.pb (see [derain](derain.md#derain) filter):

  ``` text
  ./ffmpeg -i rain.jpg -vf format=rgb24,dnn_processing=dnn_backend=tensorflow:model=can.pb:input=x:output=y derain.jpg
  ```

- Handle the Y channel with srcnn.pb (see [sr](sr.md#sr) filter) for frame with yuv420p (planar YUV formats supported):

  ``` text
  ./ffmpeg -i 480p.jpg -vf format=yuv420p,scale=w=iw*2:h=ih*2,dnn_processing=dnn_backend=tensorflow:model=srcnn.pb:input=x:output=y -y srcnn.jpg
  ```

- Handle the Y channel with espcn.pb (see [sr](sr.md#sr) filter), which changes frame size, for format yuv420p (planar YUV formats supported), please use tools/python/tf_sess_config.py to get the configs of TensorFlow backend for your system.

  ``` text
  ./ffmpeg -i 480p.jpg -vf format=yuv420p,dnn_processing=dnn_backend=tensorflow:model=espcn.pb:input=x:output=y:backend_configs=sess_config=0x10022805320e09cdccccccccccec3f20012a01303801 -y tmp.espcn.jpg
  ```
