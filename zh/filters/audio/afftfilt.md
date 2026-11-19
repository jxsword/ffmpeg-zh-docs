# afftfilt

Apply arbitrary expressions to samples in frequency domain.

- **`real`** Set frequency domain real expression for each separate channel separated by '\|'. Default is "re". If the number of input channels is greater than the number of expressions, the last specified expression is used for the remaining output channels.

- **`imag`** Set frequency domain imaginary expression for each separate channel separated by '\|'. Default is "im".

  Each expression in \<real\> and \<imag\> can contain the following constants and functions:

  - **`sr`** sample rate

  - **`b`** current frequency bin number

  - **`nb`** number of available bins

  - **`ch`** channel number of the current expression

  - **`chs`** number of channels

  - **`pts`** current frame pts

  - **`re`** current real part of frequency bin of current channel

  - **`im`** current imaginary part of frequency bin of current channel

  - **`real(b, ch)`** Return the value of real part of frequency bin at location (\<bin\>,\<channel\>)

  - **`imag(b, ch)`** Return the value of imaginary part of frequency bin at location (\<bin\>,\<channel\>)

- **`win_size`** Set window size. Allowed range is from 16 to 131072. Default is `4096`

- **`win_func`** Set window function.

  It accepts the following values:

  - **`rect`**

  - **`bartlett`**

  - **`hann, hanning`**

  - **`hamming`**

  - **`blackman`**

  - **`welch`**

  - **`flattop`**

  - **`bharris`**

  - **`bnuttall`**

  - **`bhann`**

  - **`sine`**

  - **`nuttall`**

  - **`lanczos`**

  - **`gauss`**

  - **`tukey`**

  - **`dolph`**

  - **`cauchy`**

  - **`parzen`**

  - **`poisson`**

  - **`bohman`**

  - **`kaiser`**

  Default is `hann`.

- **`overlap`** Set window overlap. If set to 1, the recommended overlap for selected window function will be picked. Default is `0.75`.

## Examples

- Leave almost only low frequencies in audio:

  ``` text
  afftfilt="'real=re * (1-clip((b/nb)*b,0,1))':imag='im * (1-clip((b/nb)*b,0,1))'"
  ```

- Apply robotize effect:

  ``` text
  afftfilt="real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75"
  ```

- Apply whisper effect:

  ``` text
  afftfilt="real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8"
  ```

- Apply phase shift:

  ``` text
  afftfilt="real=re*cos(1)-im*sin(1):imag=re*sin(1)+im*cos(1)"
  ```
