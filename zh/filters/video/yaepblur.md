# yaepblur

Apply blur filter while preserving edges ("yaepblur" means "yet another edge preserving blur filter"). The algorithm is described in "J. S. Lee, Digital image enhancement and noise filtering by use of local statistics, IEEE Trans. Pattern Anal. Mach. Intell. PAMI-2, 1980."

It accepts the following parameters:

| Term        | Description                                                  |
|-------------|--------------------------------------------------------------|
| `radius, r` | Set the window radius. Default value is 3.                   |
| `planes, p` | Set which planes to filter. Default is only the first plane. |
| `sigma, s`  | Set blur strength. Default value is 128.                     |

## Commands

This filter supports same [commands](#commands) as options.
