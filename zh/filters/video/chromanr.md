# chromanr

Reduce chrominance noise.

The filter accepts the following options:

- **`thres`** Set threshold for averaging chrominance values. Sum of absolute difference of Y, U and V pixel components of current pixel and neighbour pixels lower than this threshold will be used in averaging. Luma component is left unchanged and is copied to output. Default value is 30. Allowed range is from 1 to 200.

- **`sizew`** Set horizontal radius of rectangle used for averaging. Allowed range is from 1 to 100. Default value is 5.

- **`sizeh`** Set vertical radius of rectangle used for averaging. Allowed range is from 1 to 100. Default value is 5.

- **`stepw`** Set horizontal step when averaging. Default value is 1. Allowed range is from 1 to 50. Mostly useful to speed-up filtering.

- **`steph`** Set vertical step when averaging. Default value is 1. Allowed range is from 1 to 50. Mostly useful to speed-up filtering.

- **`threy`** Set Y threshold for averaging chrominance values. Set finer control for max allowed difference between Y components of current pixel and neighbour pixels. Default value is 200. Allowed range is from 1 to 200.

- **`threu`** Set U threshold for averaging chrominance values. Set finer control for max allowed difference between U components of current pixel and neighbour pixels. Default value is 200. Allowed range is from 1 to 200.

- **`threv`** Set V threshold for averaging chrominance values. Set finer control for max allowed difference between V components of current pixel and neighbour pixels. Default value is 200. Allowed range is from 1 to 200.

- **`distance`** Set distance type used in calculations.

  | Term          | Description          |
  |---------------|----------------------|
  | `manhattan` | Absolute difference. |
  | `euclidean` | Difference squared.  |

  Default distance type is manhattan.

## Commands

This filter supports same [commands](#commands) as options. The command accepts the same syntax of the corresponding option.
