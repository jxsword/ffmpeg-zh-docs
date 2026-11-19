# ocr

Optical Character Recognition

This filter uses Tesseract for optical character recognition. To enable compilation of this filter, you need to configure FFmpeg with `--enable-libtesseract`.

It accepts the following options:

- **`datapath`** Set datapath to tesseract data. Default is to use whatever was set at installation.

- **`language`** Set language, default is "eng".

- **`whitelist`** Set character whitelist.

- **`blacklist`** Set character blacklist.

The filter exports recognized text as the frame metadata `lavfi.ocr.text`. The filter exports confidence of recognized words as the frame metadata `lavfi.ocr.confidence`.
