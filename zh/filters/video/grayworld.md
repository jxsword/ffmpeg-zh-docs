# grayworld

A color constancy filter that applies color correction based on the grayworld assumption

See: <https://www.researchgate.net/publication/275213614_A_New_Color_Correction_Method_for_Underwater_Imaging>

The algorithm uses linear light, so input data should be linearized beforehand (and possibly correctly tagged).

``` text
ffmpeg -i INPUT -vf zscale=transfer=linear,grayworld,zscale=transfer=bt709,format=yuv420p OUTPUT
```
