# hysteresis

Grow first stream into second stream by connecting components. This makes it possible to build more robust edge masks.

This filter accepts the following options:

- **`planes`** Set which planes will be processed as bitmap, unprocessed planes will be copied from first stream. By default value 0xf, all planes will be processed.

- **`threshold`** Set threshold which is used in filtering. If pixel component value is higher than this value filter algorithm for connecting components is activated. By default value is 0.

The `hysteresis` filter also supports the [framesync](../overview.md#changing-options-at-runtime-with-a-command) options.
