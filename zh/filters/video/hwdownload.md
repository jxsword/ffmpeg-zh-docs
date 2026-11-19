# hwdownload

Download hardware frames to system memory.

The input must be in hardware frames, and the output a non-hardware format. Not all formats will be supported on the output - it may be necessary to insert an additional `format` filter immediately following in the graph to get the output in a supported format.
