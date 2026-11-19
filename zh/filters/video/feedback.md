# feedback

Apply feedback video filter.

This filter pass cropped input frames to 2nd output. From there it can be filtered with other video filters. After filter receives frame from 2nd input, that frame is combined on top of original frame from 1st input and passed to 1st output.

The typical usage is filter only part of frame.

The filter accepts the following options:

- **`x`**

- **`y`** Set the top left crop position.

- **`w`**

- **`h`** Set the crop size.

## Examples

- Blur only top left rectangular part of video frame size 100x100 with gblur filter.

  ``` text
  [in][blurin]feedback=x=0:y=0:w=100:h=100[out][blurout];[blurout]gblur=8[blurin]
  ```

- Draw black box on top left part of video frame of size 100x100 with drawbox filter.

  ``` text
  [in][blurin]feedback=x=0:y=0:w=100:h=100[out][blurout];[blurout]drawbox=x=0:y=0:w=100:h=100:t=100[blurin]
  ```

- Pixelize rectangular part of video frame of size 100x100 with pixelize filter.

  ``` text
  [in][blurin]feedback=x=320:y=240:w=100:h=100[out][blurout];[blurout]pixelize[blurin]
  ```
