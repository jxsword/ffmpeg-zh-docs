# mestimate_d3d12

Estimate and export motion vectors using D3D12 hardware-accelerated motion estimation. This filter uses GPU hardware motion estimation capabilities available in DirectX 12 Video APIs to achieve significant performance improvements over the software-based `mestimate` filter.

Motion vectors are stored in frame side data to be used by other filters.

This filter requires the input to be in `d3d12` hardware pixel format. The filter uses quarter-pixel precision for motion vector estimation.

This filter accepts the following options:

- **`mb_size`** Macroblock size. Only `8` and `16` are supported. Default `16`.

## Examples

Estimate motion vectors using D3D12 hardware acceleration with 16x16 blocks, and visualize them:

``` text
ffmpeg -hwaccel d3d12va -hwaccel_output_format d3d12 -i input.mp4 \
        -vf mestimate_d3d12=mb_size=16,hwdownload,format=nv12,codecview=mv=pf \
        -c:v libx264 -preset fast -b:v 5M output.mp4
```
