# dnn_classify

Do classification with deep neural networks based on bounding boxes.

The filter accepts the following options:

- **`dnn_backend`** Specify which DNN backend to use for model loading and execution. This option accepts only openvino now, tensorflow backends will be added.

- **`model`** Set path to model file specifying network architecture and its parameters. Note that different backends use different file formats.

- **`input`** Set the input name of the dnn network.

- **`output`** Set the output name of the dnn network.

- **`confidence`** Set the confidence threshold (default: 0.5).

- **`labels`** Set path to label file specifying the mapping between label id and name. Each label name is written in one line, tailing spaces and empty lines are skipped. The first line is the name of label id 0, and the second line is the name of label id 1, etc. The label id is considered as name if the label file is not provided.

- **`backend_configs`** Set the configs to be passed into backend

  For tensorflow backend, you can set its configs with `sess_config` options, please use tools/python/tf_sess_config.py to get the configs for your system.
