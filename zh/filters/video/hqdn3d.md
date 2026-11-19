# hqdn3d

This is a high precision/quality 3d denoise filter. It aims to reduce image noise, producing smooth images and making still images really still. It should enhance compressibility.

It accepts the following optional parameters:

- **`luma_spatial`** A non-negative floating point number which specifies spatial luma strength. It defaults to 4.0.

- **`chroma_spatial`** A non-negative floating point number which specifies spatial chroma strength. It defaults to 3.0\*\<luma_spatial\>/4.0.

- **`luma_tmp`** A floating point number which specifies luma temporal strength. It defaults to 6.0\*\<luma_spatial\>/4.0.

- **`chroma_tmp`** A floating point number which specifies chroma temporal strength. It defaults to \<luma_tmp\>\*\<chroma_spatial\>/\<luma_spatial\>.

## Commands

This filter supports same [commands](#commands) as options. The command accepts the same syntax of the corresponding option.

If the specified expression is not valid, it is kept at its current value.
