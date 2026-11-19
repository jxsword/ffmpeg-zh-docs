# zoompan

Apply Zoom & Pan effect.

This filter accepts the following options:

- **`zoom, z`** Set the zoom expression. Range is 1-10. Default is 1.

- **`x`**

- **`y`** Set the x and y expression. Default is 0.

- **`d`** Set the duration expression in number of frames. This sets for how many number of frames effect will last for single input image. Default is 90.

- **`s`** Set the output image size, default is 'hd720'.

- **`fps`** Set the output frame rate, default is '25'.

Each expression can contain the following constants:

- **`in_w, iw`** Input width.

- **`in_h, ih`** Input height.

- **`out_w, ow`** Output width.

- **`out_h, oh`** Output height.

- **`in`** Input frame count.

- **`on`** Output frame count.

- **`in_time, it`** The input timestamp expressed in seconds. It's NAN if the input timestamp is unknown.

- **`out_time, time, ot`** The output timestamp expressed in seconds.

- **`x`**

- **`y`** Last calculated 'x' and 'y' position from 'x' and 'y' expression for current input frame.

- **`px`**

- **`py`** 'x' and 'y' of last output frame of previous input frame or 0 when there was not yet such frame (first input frame).

- **`zoom`** Last calculated zoom from 'z' expression for current input frame.

- **`pzoom`** Last calculated zoom of last output frame of previous input frame.

- **`duration`** Number of output frames for current input frame. Calculated from 'd' expression for each input frame.

- **`pduration`** number of output frames created for previous input frame

- **`a`** Rational number: input width / input height

- **`sar`** sample aspect ratio

- **`dar`** display aspect ratio

## Examples

- Zoom in up to 1.5x and pan at same time to some spot near center of picture:

  ``` text
  zoompan=z='min(zoom+0.0015,1.5)':d=700:x='if(gte(zoom,1.5),x,x+1/a)':y='if(gte(zoom,1.5),y,y+1)':s=640x360
  ```

- Zoom in up to 1.5x and pan always at center of picture:

  ``` text
  zoompan=z='min(zoom+0.0015,1.5)':d=700:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'
  ```

- Same as above but without pausing:

  ``` text
  zoompan=z='min(max(zoom,pzoom)+0.0015,1.5)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'
  ```

- Zoom in 2x into center of picture only for the first second of the input video:

  ``` text
  zoompan=z='if(between(in_time,0,1),2,1)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'
  ```
