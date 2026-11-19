# hstack_qsv

Stack input videos horizontally.

This is the QSV variant of the [hstack](hstack.md#hstack) filter, each input stream may have different height, this filter will scale down/up each input stream while keeping the original aspect.

It accepts the following options:

- **`inputs`** See [hstack](hstack.md#hstack).

- **`shortest`** See [hstack](hstack.md#hstack).

- **`height`** Set height of output. If set to 0, this filter will set height of output to height of the first input stream. Default value is 0.
