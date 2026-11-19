# signalstats

Evaluate various visual metrics that assist in determining issues associated with the digitization of analog video media.

By default the filter will log these metadata values:

- **`YMIN`** Display the minimal Y value contained within the input frame. Expressed in range of \[0-255\].

- **`YLOW`** Display the Y value at the 10% percentile within the input frame. Expressed in range of \[0-255\].

- **`YAVG`** Display the average Y value within the input frame. Expressed in range of \[0-255\].

- **`YHIGH`** Display the Y value at the 90% percentile within the input frame. Expressed in range of \[0-255\].

- **`YMAX`** Display the maximum Y value contained within the input frame. Expressed in range of \[0-255\].

- **`UMIN`** Display the minimal U value contained within the input frame. Expressed in range of \[0-255\].

- **`ULOW`** Display the U value at the 10% percentile within the input frame. Expressed in range of \[0-255\].

- **`UAVG`** Display the average U value within the input frame. Expressed in range of \[0-255\].

- **`UHIGH`** Display the U value at the 90% percentile within the input frame. Expressed in range of \[0-255\].

- **`UMAX`** Display the maximum U value contained within the input frame. Expressed in range of \[0-255\].

- **`VMIN`** Display the minimal V value contained within the input frame. Expressed in range of \[0-255\].

- **`VLOW`** Display the V value at the 10% percentile within the input frame. Expressed in range of \[0-255\].

- **`VAVG`** Display the average V value within the input frame. Expressed in range of \[0-255\].

- **`VHIGH`** Display the V value at the 90% percentile within the input frame. Expressed in range of \[0-255\].

- **`VMAX`** Display the maximum V value contained within the input frame. Expressed in range of \[0-255\].

- **`SATMIN`** Display the minimal saturation value contained within the input frame. Expressed in range of \[0-~181.02\].

- **`SATLOW`** Display the saturation value at the 10% percentile within the input frame. Expressed in range of \[0-~181.02\].

- **`SATAVG`** Display the average saturation value within the input frame. Expressed in range of \[0-~181.02\].

- **`SATHIGH`** Display the saturation value at the 90% percentile within the input frame. Expressed in range of \[0-~181.02\].

- **`SATMAX`** Display the maximum saturation value contained within the input frame. Expressed in range of \[0-~181.02\].

- **`HUEMED`** Display the median value for hue within the input frame. Expressed in range of \[0-360\].

- **`HUEAVG`** Display the average value for hue within the input frame. Expressed in range of \[0-360\].

- **`YDIF`** Display the average of sample value difference between all values of the Y plane in the current frame and corresponding values of the previous input frame. Expressed in range of \[0-255\].

- **`UDIF`** Display the average of sample value difference between all values of the U plane in the current frame and corresponding values of the previous input frame. Expressed in range of \[0-255\].

- **`VDIF`** Display the average of sample value difference between all values of the V plane in the current frame and corresponding values of the previous input frame. Expressed in range of \[0-255\].

- **`YBITDEPTH`** Display bit depth of Y plane in current frame. Expressed in range of \[0-16\].

- **`UBITDEPTH`** Display bit depth of U plane in current frame. Expressed in range of \[0-16\].

- **`VBITDEPTH`** Display bit depth of V plane in current frame. Expressed in range of \[0-16\].

The filter accepts the following options:

- **`stat`**

- **`out`** `stat` specify an additional form of image analysis. `out` output video with the specified type of pixel highlighted.

  Both options accept the following values:

  - **`tout`** Identify \<temporal outliers\> pixels. A \<temporal outlier\> is a pixel unlike the neighboring pixels of the same field. Examples of temporal outliers include the results of video dropouts, head clogs, or tape tracking issues.

  - **`vrep`** Identify \<vertical line repetition\>. Vertical line repetition includes similar rows of pixels within a frame. In born-digital video vertical line repetition is common, but this pattern is uncommon in video digitized from an analog source. When it occurs in video that results from the digitization of an analog source it can indicate concealment from a dropout compensator.

  - **`brng`** Identify pixels that fall outside of legal broadcast range.

- **`color, c`** Set the highlight color for the `out` option. The default color is yellow.

## Examples

- Output data of various video metrics:

  ``` text
  ffprobe -f lavfi movie=example.mov,signalstats="stat=tout+vrep+brng" -show_frames
  ```

- Output specific data about the minimum and maximum values of the Y plane per frame:

  ``` text
  ffprobe -f lavfi movie=example.mov,signalstats -show_entries frame_tags=lavfi.signalstats.YMAX,lavfi.signalstats.YMIN
  ```

- Playback video while highlighting pixels that are outside of broadcast range in red.

  ``` text
  ffplay example.mov -vf signalstats="out=brng:color=red"
  ```

- Playback video with signalstats metadata drawn over the frame.

  ``` text
  ffplay example.mov -vf signalstats=stat=brng+vrep+tout,drawtext=fontfile=FreeSerif.ttf:textfile=signalstat_drawtext.txt
  ```

  The contents of signalstat_drawtext.txt used in the command are:

  ``` text
  time %{pts:hms}
  Y (%{metadata:lavfi.signalstats.YMIN}-%{metadata:lavfi.signalstats.YMAX})
  U (%{metadata:lavfi.signalstats.UMIN}-%{metadata:lavfi.signalstats.UMAX})
  V (%{metadata:lavfi.signalstats.VMIN}-%{metadata:lavfi.signalstats.VMAX})
  saturation maximum: %{metadata:lavfi.signalstats.SATMAX}
  ```
