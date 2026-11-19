# bilateral

Apply bilateral filter, spatial smoothing while preserving edges.

The filter accepts the following options:

- **`sigmaS`** Set sigma of gaussian function to calculate spatial weight. Allowed range is 0 to 512. Default is 0.1.

- **`sigmaR`** Set sigma of gaussian function to calculate range weight. Allowed range is 0 to 1. Default is 0.1.

- **`planes`** Set planes to filter. Default is first only.

## Commands

This filter supports the all above options as [commands](#commands).
