# despill

Remove unwanted contamination of foreground colors, caused by reflected color of greenscreen or bluescreen.

This filter accepts the following options:

| Term | Description |
|----|----|
| `type` | Set what type of despill to use. |
| `mix` | Set how spillmap will be generated. |
| `expand` | Set how much to get rid of still remaining spill. |
| `red` | Controls amount of red in spill area. |
| `green` | Controls amount of green in spill area. Should be -1 for greenscreen. |
| `blue` | Controls amount of blue in spill area. Should be -1 for bluescreen. |
| `brightness` | Controls brightness of spill area, preserving colors. |
| `alpha` | Modify alpha from generated spillmap. |

## Commands

This filter supports the all above options as [commands](#commands).
