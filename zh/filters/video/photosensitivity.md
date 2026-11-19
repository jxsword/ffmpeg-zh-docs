# photosensitivity

Reduce various flashes in video, so to help users with epilepsy.

It accepts the following options:

- **`frames, f`** Set how many frames to use when filtering. Default is 30.

- **`threshold, t`** Set detection threshold factor. Default is 1. Lower is stricter.

- **`skip`** Set how many pixels to skip when sampling frames. Default is 1. Allowed range is from 1 to 1024.

- **`bypass`** Leave frames unchanged. Default is disabled.
