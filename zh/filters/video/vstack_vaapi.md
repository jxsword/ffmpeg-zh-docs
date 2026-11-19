# vstack_vaapi

Stack input videos vertically.

This is the VA-API variant of the [vstack](vstack.md#vstack) filter, each input stream may have different width, this filter will scale down/up each input stream while keeping the original aspect.

It accepts the following options:

- **`inputs`** See [vstack](vstack.md#vstack).

- **`shortest`** See [vstack](vstack.md#vstack).

- **`width`** Set width of output. If set to 0, this filter will set width of output to width of the first input stream. Default value is 0.
