# atempo

Adjust audio tempo.

The filter accepts exactly one parameter, the audio tempo. If not specified then the filter will assume nominal 1.0 tempo. Tempo must be in the \[0.5, 100.0\] range.

Note that tempo greater than 2 will skip some samples rather than blend them in. If for any reason this is a concern it is always possible to daisy-chain several instances of atempo to achieve the desired product tempo.

## Examples

- Slow down audio to 80% tempo:

  ``` text
  atempo=0.8
  ```

- To speed up audio to 300% tempo:

  ``` text
  atempo=3
  ```

- To speed up audio to 300% tempo by daisy-chaining two atempo instances:

  ``` text
  atempo=sqrt(3),atempo=sqrt(3)
  ```

## Commands

This filter supports the following commands:

- **`tempo`** Change filter tempo scale factor. Syntax for the command is : "\<tempo\>"
