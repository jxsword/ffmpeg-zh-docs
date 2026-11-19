# siti

Calculate Spatial Information (SI) and Temporal Information (TI) scores for a video, as defined in ITU-T Rec. P.910 (11/21): Subjective video quality assessment methods for multimedia applications. Available PDF at <https://www.itu.int/rec/T-REC-P.910-202111-S/en>. Note that this is a legacy implementation that corresponds to a superseded recommendation. Refer to ITU-T Rec. P.910 (07/22) for the latest version: <https://www.itu.int/rec/T-REC-P.910-202207-I/en>

It accepts the following option:

| Term | Description |
|----|----|
| `print_summary` | If set to 1, Summary statistics will be printed to the console. Default 0. |

## Examples

- To calculate SI/TI metrics and print summary:

  ``` text
  ffmpeg -i input.mp4 -vf siti=print_summary=1 -f null -
  ```
