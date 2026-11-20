# 类 Unix 系统

FFmpeg 的某些部分无法用部分 AMD64 发行版仍在提供的 GNU 汇编器 2.15 版构建。为确保 binutils 升级后您的编译器确实使用所需版本的 gas，请运行：

``` text
$(gcc -print-prog-name=as) --version
```

如果不是，则您应当安装一个没有硬编码 gas 路径的其他编译器。最坏情况下，向 configure 传入 `--disable-asm`。

## 高级链接配置

如果您静态编译了 FFmpeg 库并想用它们来构建自己的共享库，您可能需要强制 PIC 支持（在 FFmpeg configure 时加 `--enable-pic`），并在项目的 LDFLAGS 中加入以下选项：

``` text
-Wl,-Bsymbolic
```

如果您的目标平台要求位置无关二进制文件，您应当把正确的链接标志（如 `-pie`）传给 `--extra-ldexeflags`。

## BSD

BSD make 无法构建 FFmpeg，您需要安装并使用 GNU Make（`gmake`）。

## (Open)Solaris

构建 FFmpeg 需要 GNU Make，因此您必须调用 `gmake`，标准的 Solaris Make 无法工作。使用非 c99 前端（gcc、generic suncc）构建时，向 configure 选项添加 `--extra-libs=/usr/lib/values-xpg6.o` 或 `--extra-libs=/usr/lib/64/values-xpg6.o`，因为 libc 默认不符合 c99。configure 执行的探测可能因系统 shell 的一个缺陷而抛出异常，导致 configure 自身终止；直接改用 bash 等 shell 即可绕开：

``` text
bash ./configure
```

## Darwin (Mac OS X, iPhone)

Xcode 提供的工具链足以构建基础的未加速代码。

PowerPC 或 ARM (iPhone) 平台的 Mac OS X 需要 <https://github.com/FFmpeg/gas-preprocessor> 或 <https://github.com/yuvi/gas-preprocessor>（现已过时）提供的预处理器来构建优化汇编函数。把该 Perl 脚本放到 PATH 中的某个位置，FFmpeg 的 configure 会自动拾取它。

amd64 与 x86 平台的 Mac OS X 需要 `nasm` 来构建大多数优化汇编函数。[Fink](http://www.finkproject.org/)、[Gentoo Prefix](https://wiki.gentoo.org/wiki/Project:Prefix)、[Homebrew](https://mxcl.github.com/homebrew/) 或 [MacPorts](http://www.macports.org) 都能轻松提供它。

# DOS

出于多种原因，优先使用交叉编译器。<http://www.delorie.com/howto/djgpp/linux-x-djgpp.html>

# OS/2

关于在 OS/2 上编译 FFmpeg 的信息，参见 <http://www.edm2.com/index.php/FFmpeg>。

# Windows

## 使用 MinGW 或 MinGW-w64 的 Windows 原生编译

可以用 MinGW-w64 工具链把 FFmpeg 构建为原生运行于 Windows 的程序。请从 <http://msys2.github.io/> 和/或 <http://mingw-w64.sourceforge.net/> 安装最新版本的 MSYS2 与 MinGW-w64。您可以在下载区和 FAQ 中找到详细的安装说明。

注意：

- 不建议为 MSYS 环境构建；MSYS2 通过 `mingw64_shell.bat` 或 `mingw32_shell.bat` 提供完整的 MinGW-w64 环境，应当使用它而不是 `msys2_shell.bat` 提供的环境。

- 用 MSYS2 构建可以通过禁用 Makefile 的隐式规则来提速：调用 `make -r` 而非单纯的 `make`。这一提速对普通的一次性构建几乎不存在，只在第二次运行 make 时（例如 `make install` 期间）才能察觉。

- 要编译 FFplay，您必须已安装 [SDL](http://www.libsdl.org/) 的 MinGW 开发库和 `pkg-config`。

- 在配置 FFmpeg 时使用 `./configure --enable-shared`，您可以把 FFmpeg 库（如 libavutil、libavcodec、libavformat）构建为 DLL。

### 使用 MSYS2 的 Windows 原生编译

MSYS2 MinGW-w64 环境通过 `pacman` 提供开箱即用的工具链与依赖。

请确保使用 `mingw64_shell.bat` 或 `mingw32_shell.bat` 以获得正确的 MinGW-w64 环境。默认安装会在 `MinGW-w64 Win64 Shell` 与 `MinGW-w64 Win32 Shell` 下提供它们的快捷方式。

``` text
# normal msys2 packages
pacman -S make pkgconf diffutils

# mingw-w64 packages and toolchains
pacman -S mingw-w64-x86_64-nasm mingw-w64-x86_64-gcc mingw-w64-x86_64-SDL2
```

若目标是 32 位，把上述命令中的 `x86_64` 替换为 `i686`。

## Microsoft Visual C++ 或 Intel C++ 编译器（Windows）

FFmpeg 可以用 MSVC 2013 或更高版本构建。

您需要以下前提条件：

- [MSYS2](http://msys2.github.io/)

- [NASM](http://www.nasm.us/)（也可经 MSYS2 的包管理器获取。）

要在 MSYS2 中设置妥当的环境，您需要从 Visual Studio 或 Intel 编译器命令提示符运行 `msys_shell.bat`。

把 `nasm.exe` 放到 `PATH` 中的某个位置。

接下来，确保您想用的其他头文件和库（如 zlib）位于编译器可见的位置。做法是修改 `LIB` 与 `INCLUDE` 环境变量，把这些目录的 **Windows 风格** 路径加进去。或者，您也可以尝试 `--extra-cflags`/`--extra-ldflags` configure 选项。

最后，运行：

``` text
For MSVC:
./configure --toolchain=msvc

For ICL:
./configure --toolchain=icl

make
make install
```

如果您想编译共享库，请在 configure 选项中加入 `--enable-shared`。注意，由于 MSVC 与 ICL 处理 DLL 导入/导出的方式，您无法同时编译静态库与共享库；启用共享库会自动禁用静态库。

注意：

- 如果您想构建带 zlib 支持的版本，您需要从某处获取带 MSVC 导入库的兼容 zlib 二进制文件；或者，如果想静态链接，可按下面的步骤用 MSVC 构建兼容的 `zlib.lib`。无论采用哪种方法，都必须遵循第 3 步，否则编译将失败。

  1.  获取 [zlib 源码](http://zlib.net/)。

  2.  编辑 `win32/Makefile.msc`，使其使用 -MT 而非 -MD，因为 FFmpeg 也是这样构建的。

  3.  编辑 `zconf.h`，移除它对 `unistd.h` 的包含。构建 FFmpeg 时该头会被错误地包含进来。

  4.  运行 `nmake -f win32/Makefile.msc`。

  5.  把 `zlib.lib`、`zconf.h` 与 `zlib.h` 移到 MSVC 可见的位置。

- FFmpeg 已在 i686 与 x86_64 上用下列组合测试过：

  - Visual Studio 2013 Pro 与 Express 版

  - Intel Composer XE 2013

  - Intel Composer XE 2013 SP1

  其他组合均不受官方支持。

### 使用 Microsoft Visual C++ 链接 FFmpeg

如果您计划链接 MSVC 构建的静态库，需要确保项目设置中 `Runtime Library` 已设为 `Multi-threaded (/MT)`。

您需要把 `inline` 定义为 MSVC 能理解的形式：

``` text
#define inline __inline
```

另请注意，如 **Microsoft Visual C++** 一节所述，您需要一个与 MSVC 兼容的 [inttypes.h](http://code.google.com/p/msinttypes/)。

如果您打算使用 dlltool 创建的导入库，必须在链接器优化设置中把 `References` 设为 `No (/OPT:NOREF)`，否则得到的二进制文件在运行时会失败。使用 `lib.exe` 生成的导入库则无此要求。该问题已上报上游：<http://sourceware.org/bugzilla/show_bug.cgi?id=12633>。

要创建与 `/OPT:REF` 选项（Release 模式默认启用）兼容工作的导入库，请遵循以下步骤：

1.  打开 *Visual Studio Command Prompt*。

    或者，在普通命令行提示符中调用 `vcvars32.bat`，它为 Visual C++ 工具设置环境变量（该文件的标准位置类似 `C:\Program Files (x86_\Microsoft Visual Studio 10.0\VC\bin\vcvars32.bat`）。

2.  进入存放所生成 LIB 与 DLL 文件的 `bin` 目录。

3.  用 `lib.exe` 生成新的导入库：

    ``` text
    lib /machine:i386 /def:..\lib\foo-version.def  /out:foo.lib
    ```

    把 `foo-version` 与 `foo` 替换为相应的库名。

## 使用 Linux 交叉编译 Windows 版本

您必须使用 <http://www.mingw.org/> 提供的 MinGW 交叉编译工具。

然后用以下选项配置 FFmpeg：

``` text
./configure --target-os=mingw32 --cross-prefix=i386-mingw32msvc-
```

（您可以按为 MinGW 工具选择的前缀更改 cross-prefix。）

然后您可以轻松地用 [Wine](http://www.winehq.com/) 测试 FFmpeg。

## 在 Cygwin 下编译

请使用 Cygwin 1.7.x，因为已过时的 Cygwin 1.5.x 的 C 库缺少 llrint()。

安装 Cygwin 时请带上全部 "Base" 包，再加上以下 "Devel" 包：

``` text
binutils, gcc4-core, make, git, mingw-runtime, texinfo
```

为了运行 FATE，您还需要以下 "Utils" 包：

``` text
diffutils
```

如果您想构建带额外库的 FFmpeg，请从任意 Cygwin 软件包仓库下载 Ogg 与 Vorbis 的 Cygwin "Devel" 包：

``` text
libogg-devel, libvorbis-devel
```

这些库包只能从 [Cygwin Ports](http://sourceware.org/cygwinports/) 获取：

``` text
libSDL-devel, libgsm-devel, libmp3lame-devel,
speex-devel, libtheora-devel, libxvidcore-devel
```

对 x264 的建议是从源码构建，因为其演进速度太快，Cygwin Ports 来不及更新。

## 在 Cygwin 下为 Windows 交叉编译

使用 Cygwin，您可以创建不需要 cygwin1.dll 的 Windows 二进制文件。

只需按前文所述安装 Cygwin，再加上这些额外的 "Devel" 包：

``` text
gcc-mingw-core, mingw-runtime, mingw-zlib
```

并向 configure 调用添加一些特殊标志。

静态构建运行

``` text
./configure --target-os=mingw32 --extra-cflags=-mno-cygwin --extra-libs=-mno-cygwin
```

若要构建共享库版本则运行

``` text
./configure --target-os=mingw32 --enable-shared --disable-static --extra-cflags=-mno-cygwin --extra-libs=-mno-cygwin
```

## ARM64EC

FFmpeg 无意支持 Windows 的 ARM64EC 构建配置；为 ARM64EC 改动各个库的补丁将不被接受。

在此构建配置下仍有可能构建出 FFmpeg；这样的构建可能在某种程度上看似可用，但可能存在一定程度的 ABI 不一致——我们不愿修复它。

（将 aarch64 汇编代码改为严格支持 ARM64EC 需要对几乎所有此类汇编代码进行 ifdeffing/改动，将是巨大的维护负担。此外，修改库的 ABI 表面来修复 ABI 不一致可能需要大量侵入式更改。）
