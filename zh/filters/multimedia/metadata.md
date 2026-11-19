# metadata, ametadata

Manipulate frame metadata.

This filter accepts the following options:

- **`mode`** Set mode of operation of the filter.

  Can be one of the following:

  - **`select`** If both `value` and `key` is set, select frames which have such metadata. If only `key` is set, select every frame that has such key in metadata.

  - **`add`** Add new metadata `key` and `value`. If key is already available do nothing.

  - **`modify`** Modify value of already present key.

  - **`delete`** If `value` is set, delete only keys that have such value. Otherwise, delete key. If `key` is not set, delete all metadata values in the frame.

  - **`print`** Print key and its value if metadata was found. If `key` is not set print all metadata values available in frame.

- **`key`** Set key used with all modes. Must be set for all modes except `print` and `delete`.

- **`value`** Set metadata value which will be used. This option is mandatory for `modify` and `add` mode.

- **`function`** Which function to use when comparing metadata value and `value`.

  Can be one of following:

  - **`same_str`** Values are interpreted as strings, returns true if metadata value is same as `value`.

  - **`starts_with`** Values are interpreted as strings, returns true if metadata value starts with the `value` option string.

  - **`less`** Values are interpreted as floats, returns true if metadata value is less than `value`.

  - **`equal`** Values are interpreted as floats, returns true if `value` is equal with metadata value.

  - **`greater`** Values are interpreted as floats, returns true if metadata value is greater than `value`.

  - **`expr`** Values are interpreted as floats, returns true if expression from option `expr` evaluates to true.

  - **`ends_with`** Values are interpreted as strings, returns true if metadata value ends with the `value` option string.

- **`expr`** Set expression which is used when `function` is set to `expr`. The expression is evaluated through the eval API and can contain the following constants:

  - **`VALUE1, FRAMEVAL`** Float representation of `value` from metadata key.

  - **`VALUE2, USERVAL`** Float representation of `value` as supplied by user in `value` option.

- **`file`** If specified in `print` mode, output is written to the named file. Instead of plain filename any writable url can be specified. Filename "-" is a shorthand for standard output. If `file` option is not set, output is written to the log with AV_LOG_INFO loglevel.

- **`direct`** Reduces buffering in print mode when output is written to a URL set using \<file\>.

## Examples

- Print all metadata values for frames with key `lavfi.signalstats.YDIF` with values between 0 and 1.

  ``` text
  signalstats,metadata=print:key=lavfi.signalstats.YDIF:value=0:function=expr:expr='between(VALUE1,0,1)'
  ```

- Print silencedetect output to file `metadata.txt`.

  ``` text
  silencedetect,ametadata=mode=print:file=metadata.txt
  ```

- Direct all metadata to a pipe with file descriptor 4.

  ``` text
  metadata=mode=print:file='pipe\:4'
  ```
