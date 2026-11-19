# qp

Change video quantization parameters (QP).

The filter accepts the following option:

| Term | Description                                |
|------|--------------------------------------------|
| `qp` | Set expression for quantization parameter. |

The expression is evaluated through the eval API and can contain, among others, the following constants:

| Term      | Description                                 |
|-----------|---------------------------------------------|
| \<known\> | 1 if index is not 129, 0 otherwise.         |
| \<qp\>    | Sequential index starting from -129 to 128. |

## Examples

- Some equation like:

  ``` text
  qp=2+2*sin(PI*qp)
  ```
