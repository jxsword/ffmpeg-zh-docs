# 简介

本文关注的是 FFmpeg *本身*的开发。关于在其他程序中使用 FFmpeg 库的信息可在别处找到，例如：

- 已安装的头文件

- 由这些头文件生成的 [Doxygen 文档](http://ffmpeg.org/doxygen/trunk/index.html)

- `doc/examples` 下的示例

关于在外部程序中使用 FFmpeg 的更详细法律信息，请阅读源码树中的 `LICENSE` 文件，并查阅 <https://ffmpeg.org/legal.html>。

如果您为自己的使用场景修改了 FFmpeg 代码，我们强烈鼓励您*将修改提交回来*，并以本文档作为指南。这样做既有现实层面的理由，也有理念层面的理由：

- 在主线开发之外维护自己的改动以跟上上游开发既耗时又容易出错。而您的代码进入主代码树后，将由 FFmpeg 开发者代为维护。

- FFmpeg 开发者中有该领域的顶尖专家，他们能发现您代码中的缺陷或设计问题。

- 支持您觉得有用的项目，才能确保它持续得到维护和发展。

所有拟议的代码修改都应提交到 [Forgejo](https://code.ffmpeg.org/FFmpeg/FFmpeg/pulls) 或[开发邮件列表](mailto:ffmpeg-devel@ffmpeg.org)接受评审，详见[提交补丁](#提交补丁)一章。代码应符合[开发政策](#开发政策)，并遵循[编码规则](#编码规则)。执行提交的开发者与补丁作者都要对自己的修改负责，并应尽力修复其提交引发的问题。

# 编码规则

## 语言

FFmpeg 主要使用 ISO C11 语言编写，但公共头文件必须保持 C99 兼容。

出于充分理由可以使用编译器专属扩展，但不得形成依赖，即代码在缺少该扩展的编译器上仍必须能够编译并正常工作。

代码库中任何地方都不得使用以下 C99 特性：

- 变长数组；

- 复数；

### SIMD/DSP

由于现代编译器无法从纯 C 代码生成高效的 SIMD 或其他性能关键的 DSP 代码，因此需要手写汇编。这类代码通常被隔离在单独的函数中。标准做法是为该函数编写多个版本——一个到处可用、也便于调试的纯 C 版本，以及可能的多个架构专属优化实现。初始化代码随后在运行时挑选最优的可用版本并装入函数指针；此后该函数始终通过这个指针调用。

编写汇编所用的具体语法为：

- x86 上使用 NASM；

- ARM 与 RISC-V 上使用 GAS。

汇编单元测试框架 `checkasm` 位于 `tests/checkasm`。所有新增汇编都应附带 `checkasm` 测试；也强烈鼓励为缺少测试的既有汇编补充测试。

### 其他语言

特殊情况下可以使用 C 以外的语言：

- 当相关代码无法按 [SIMD/DSP](#simddsp) 一节所述的标准方式编写时，可使用编译器内建函数（intrinsics）或内联汇编。这通常适用于需要内联的代码。

- 需要与 macOS 专属接口交互时，可使用 Objective-C。

## 代码排版约定

关于源文件中的代码风格，有以下准则：

- 缩进宽度为 4。

- 制表符（TAB）在 Makefile 之外禁止使用，任何形式的行尾空白同样禁止。含两者的提交会被 git 仓库拒绝。

- 您应尽量将代码行控制在 80 个字符以内；但仅在此举确实能提升可读性时才这样做。

- 采用 K&R 代码风格。

本排版风格受 'indent -i4 -kr -nut' 启发。

### 示例

以下是一些值得注意的示例，用于说明 FFmpeg 的常见代码风格：

- 赋值号两侧以及 `if`/`do`/`while`/`for` 关键字之后留空格：

  ``` c
  // Good
  if (condition)
      av_foo();
  ```

  ``` c
  // Good
  for (size_t i = 0; i < len; i++)
      av_bar(i);
  ```

  ``` text
  // Good
  size_t size = 0;
  ```

  但圆括号与条件之间不要留空格，除非这样有助于阅读复杂条件，因此不应写成下面这样：

  ``` c
  // Bad style
  if ( condition )
      av_foo();
  ```

- 不加多余的圆括号，除非有助于可读性：

  ``` text
  // Good
  int fields = ilace ? 2 : 1;
  ```

- 不要给单行语句块套花括号。仅当存在配套的 else 语句时才使用花括号。这样便于日后跟踪代码变更。

  ``` c
  // Good
  if (bits_pixel == 24) {
      avctx->pix_fmt = AV_PIX_FMT_BGR24;
  } else if (bits_pixel == 8) {
      avctx->pix_fmt = AV_PIX_FMT_GRAY8;
  } else
      return AVERROR_INVALIDDATA;
  ```

- 在合理的情况下避免在条件表达式中进行赋值：

  ``` c
  // Good
  video_enc->chroma_intra_matrix = av_mallocz(sizeof(*video_enc->chroma_intra_matrix) * 64)
  if (!video_enc->chroma_intra_matrix)
      return AVERROR(ENOMEM);
  ```

  ``` c
  // Bad style
  if (!(video_enc->chroma_intra_matrix = av_mallocz(sizeof(*video_enc->chroma_intra_matrix) * 64)))
      return AVERROR(ENOMEM);
  ```

  ``` c
  // Ok
  while ((entry = av_dict_iterate(options, entry)))
      av_log(ctx, AV_LOG_INFO, "Item '%s': '%s'\n", entry->key, entry->value);
  ```

- 声明指针变量时，`*` 靠近变量名而不是类型：

  ``` text
  // Good
  AVStream *stream;
  ```

  ``` text
  // Bad style
  AVStream* stream;
  ```

- 在合理的情况下优先使用尽量小的变量作用域，for 循环尤甚：

  ``` c
  // Good
  for (unsigned i = 0; i < submix->nb_elements; i++) {
      // Do something...
  }
  ```

  ``` c
  // Bad style
  unsigned i;
  //...
  for (i = 0; i < submix->nb_elements; i++) {
      // Do something...
  }
  ```

如果您处理的文件并未一贯遵循这些准则，请将您正在编辑的部分改为遵循这些准则，但不要为了迎合它们而在文件中做无关的修改。

### Vim 配置

要让 Vim 遵循 FFmpeg 的排版约定，请将以下片段粘贴到您的 `.vimrc` 中：

``` text
" indentation rules for FFmpeg: 4 spaces, no tabs
set expandtab
set shiftwidth=4
set softtabstop=4
set cindent
set cinoptions=(0
" Allow tabs in Makefiles.
autocmd FileType make,automake set noexpandtab shiftwidth=8 softtabstop=8
" Trailing whitespace and tabs are forbidden, so highlight them.
highlight ForbiddenWhitespace ctermbg=red guibg=red
match ForbiddenWhitespace /\s\+$\|\t/
" Do not highlight spaces at the end of line while typing on that line.
autocmd InsertEnter * match ForbiddenWhitespace /\t\|\s\+\%#\@<!$/
```

### Emacs 配置

对于 Emacs，请将下面这些大致等效的行添加到您的 `.emacs.d/init.el`：

``` text
(c-add-style "ffmpeg"
             '("k&r"
               (c-basic-offset . 4)
               (indent-tabs-mode . nil)
               (show-trailing-whitespace . t)
               (c-offsets-alist
                (statement-cont . (c-lineup-assignments +)))
               )
             )
(setq c-default-style "ffmpeg")
```

## 注释

请使用 JavaDoc/Doxygen 格式（见下文示例），以便自动生成代码文档。所有非平凡函数的上方都应有注释说明其功能，哪怕只有一句话。所有结构体及其成员变量也都应有文档说明。

避免使用 Qt 风格及其他含 `!` 的 Doxygen 语法，即用 `///` 取代 `//!` 等。标记命令也应采用 @ 语法，即使用 `@param` 而不是 `\param`。

``` c
/**
 * @file
 * MPEG codec.
 * @author ...
 */

/**
 * Summary sentence.
 * more text ...
 * ...
 */
typedef struct Foobar {
    int var1; /**< var1 description */
    int var2; ///< var2 description
    /** var3 description */
    int var3;
} Foobar;

/**
 * Summary sentence.
 * more text ...
 * ...
 * @param my_parameter description of my_parameter
 * @return return value description
 */
int myfunc(int my_parameter)
...
```

## 命名约定

函数、变量和结构体成员的名称必须小写，使用下划线（\_）分隔单词。例如 `avfilter_get_video_buffer` 是可接受的函数名，而 `AVFilterGetVideo` 则不是。

struct、union、enum 以及经 typedef 定义的类型名必须使用 CamelCase。所有 struct 与 union 都应通过 typedef 定义为与其标签相同的名字，例如 `typedef struct AVFoo { ... } AVFoo;`。enum 通常不做 typedef。

枚举常量和宏必须全部大写，但伪装成函数的宏除外，这类宏应遵循函数命名约定。

库中所有标识符应按如下方式做命名空间隔离：

- 文件及更小作用域的标识符（如局部变量、静态函数）以及 struct 和 union 成员不做命名空间隔离；

- 作用域超出文件、但仅在单个库内部使用的变量与函数必须使用 `ff_` 前缀，例如 `ff_w64_demuxer`。这可避免 FFmpeg 被静态链接时的命名冲突。

- 作用域超出文件、且在多个库内部跨库使用的变量与函数，使用 `avpriv_` 前缀，例如 `avpriv_report_missing_feature`。

- 其余内部标识符（如私有类型名或宏名）只需做命名空间隔离以避免可能的内部冲突，例如 `H264_NAL_SPS` 与 `HEVC_NAL_SPS`。

- 除通用的 `av_` 之外，每个库的公共符号还有各自的前缀（libavformat 用 `avformat_`，libavcodec 用 `avcodec_`，libswresample 用 `swr_` 等）。请查看现有代码并据此选择名称。

- 其他公共标识符（struct、union、enum、宏、类型名）必须使用所属库的公共前缀（`AV`、`Sws` 或 `Swr`）。

此外，不得侵入系统保留的命名空间。以 `_t` 结尾的标识符由 [POSIX](http://pubs.opengroup.org/onlinepubs/007904975/functions/xsh_chap02_02.html#tag_02_02_02) 保留。同时避免以 `__` 开头、或以 `_` 后跟大写字母开头的名称，它们由 C 标准保留。以 `_` 开头的名称在文件作用域级别被保留，不得用于外部可见的符号。拿不准时，干脆避免一切以 `_` 开头的名称。

## 其他约定

- 仅在必要时使用强制类型转换。无助于理解代码的多余圆括号也应避免。

- 适用之处应使用 SI 单位。例如超时时长应以秒而非微秒为基本单位，即 `1.0` 这样的裸值必须表示 1 秒，`50m` 表示 50 毫秒。重量则以克为单位。

# 开发政策

## 代码行为

**正确性**

代码必须正确有效。不得崩溃、中止、访问无效指针、泄漏内存、引发数据竞争或有符号整数溢出，也不得以其他方式造成未定义行为。错误码应予检查，并在适用时向上传给调用者。

**线程与库安全**

同一进程中的多个独立调用者都可能调用我们的库。这些调用可能来自任意数量的线程，且不同调用点彼此可能并不知晓——例如用户程序直接调用我们的库，同时又使用一个或多个同样会调用我们库的其他库。代码必须在这些条件下表现正确。

**健壮性**

代码必须将从调用者接收或从文件、网络等读取的任何字节流视为不可信数据。收到任意数据时不得行为失常——通常应在遇到无效输入数据时打印错误消息并返回 `AVERROR_INVALIDDATA`。

**内存分配**

代码必须使用 `libavutil/mem.h` 中的 `av_malloc()` 系列函数进行所有内存分配，特殊情况除外（例如与要求使用特定分配器的外部库交互时）。

所有分配都应检查，失败时返回 `AVERROR(ENOMEM)`。常见错误是错误处理路径泄漏内存——请务必避免。

**stdio**

我们的库不得直接访问 stdio 流 stdin/stdout/stderr（例如通过 `printf()` 系列函数），因为这不符合库安全要求。日志请使用 `av_log()`。

## 补丁与提交

**补丁的许可证必须与 FFmpeg 兼容。**

贡献代码应采用 [LGPL 2.1](http://www.gnu.org/licenses/lgpl-2.1.html) 许可（含"或任意后续版本"条款）；如果您偏好赠予式许可，可采用 [ISC](http://opensource.org/licenses/isc-license.txt) 或 [MIT](http://mit-license.org/) 许可。含"或任意后续版本"条款的 [GPL 2](http://www.gnu.org/licenses/gpl-2.0.html) 也可接受，但首选 LGPL。新增文件时请为其添加规范的许可证头，不要从随机的地方复制粘贴，应使用现有文件作为模板。

**严禁提交会破坏 FFmpeg 的代码！**

这是指启用后会导致编译失败、或虽能编译但无法工作/破坏回归测试的未完成代码。未完成但被禁用的代码在特定情况下可以允许，例如缺少样本或仅实现了小部分功能。推送前务必到邮件列表确认没有评审人提出异议，并测试 FATE。

**提交信息**

提交信息是告知其他开发者某项修改做了什么、为什么这样改的重要工具。每个提交都必须始终附带填写规范的提交信息，格式如下：

``` text
area changed: short 1 line description

details describing what and why and giving references.
```

如果提交修复了错误跟踪器上已知的缺陷或其他外部问题（如 CVE），提交信息中应包含相关的缺陷 ID 或其他外部标识符。注意这是在规范说明之外的额外要求，而非替代。诸如"fixed!"或"Changed it."之类的注释不可接受。

应用邮件列表上经过深入讨论的补丁时，请在该提交信息中引用相应的讨论串。

**测试要充分但不过度。**

如果代码对您和对他人都工作正常并通过 FATE，那么只要符合其他提交标准，就可以提交。您不必担心测试过度。如果您的代码有问题（可移植性、触发编译器缺陷、异常环境等），问题会被报告并最终得到修复。

**不要把不相关的修改合并提交。**

应将它们拆分为各自独立的部分。同时别忘了：若部分 B 依赖部分 A，而 A 不依赖 B，那么 A 可以且应当先于 B 单独提交。把修改妥善拆分成自成一体的部分，便于在提交日志邮件列表上评审和理解，也有助于日后的调试。如果您对拆与不拆拿不准，尽管到开发邮件列表上询问或讨论。

**打算回迁的缺陷修复应保持聚焦。**

缺陷修复应在完整修复所报问题的前提下尽量小。正确性或健壮性并不需要的修改应单独提交，尤其是会增加复杂度或影响回迁的修改。

**外观性修改应放入单独的补丁。**

若源码缩进及其他外观性修改与功能性修改混在一起，我们会拒绝此类提交并予以移除。但 `git diff --ignore-all-space` 可以忽略的缩进变化（如空白量增减、行首/行尾空格）可以与功能性修改混合，因为评审者可以用 `git diff -w` 或 `git log -p --ignore-all-space` 只评审功能部分。Forgejo 的拉取请求界面也为此提供"隐藏空白变化"选项。每位开发者都有自己的缩进风格，您不应改动它。当然，如果您（重新）编写某段代码，可以使用自己的风格，尽管我们更希望 FFmpeg 全库的缩进保持一致（许多项目强制统一的缩进风格——我们不这样）。如果您确实需要做非空白的外观性修改，请将其与真正的修改严格分开。

注意：如果您不得不给一大段（\> 5 行）代码套上 if(){ .. }，那么要么不要改动其中内部部分的缩进（不要整体右移），要么把缩进调整放进单独的提交

**注明补丁作者。**

确保提交的作者信息设置正确。（参见 git commit –author）如果您应用了某个补丁，请向 ffmpeg-devel（或您获取补丁的地方）回信说明您已应用该补丁。

**致谢相关研究人员**

如果某个提交/补丁修复了研究人员发现的问题，请始终在提交信息中致谢发现/报告该问题的人。

**推送修改前总要等待足够长的时间**

未经许可，不要提交他人积极维护的代码。请把补丁发到 ffmpeg-devel。如果在合理时间内无人回应（构建失败和安全修复为 12 小时，小修改为 3 天，大补丁为 1 周），且您认为补丁没有问题，即可提交。另外请注意，维护者可以简单地向您请求更多评审时间！

## 代码

**若无其他选择，可以禁用针对正确代码的编译警告。**

编译器警告预示潜在缺陷或风格不良的代码。如果某类警告总是指向正确且干净的代码，那么应禁用的是警告本身，而不是去改代码。这样剩余的警告要么是缺陷，要么对应正确的代码。若是缺陷，就必须修复；若不是，则应改写代码使其不再产生警告，除非这样会导致性能下降或使代码晦涩难懂。

## 库的公共接口

FFmpeg 的每个库都在其安装头文件中提供一组公共 API，即该库 `Makefile` 中 `HEADERS` 变量所列的头文件。这些头文件中定义的所有标识符（明确另行说明者除外）以及编译产物（共享库或静态库）导出的对应符号，均视为公共接口，必须遵守本节所述的 API 与 ABI 兼容性规则。

公共 API 在同一主版本内必须保持向后兼容。也就是说，只要主版本号不变，任何能编译并与某版本库正常配合的用户代码，都必须仍能编译并与之后任何版本正常配合。此处"有效用户代码"指以有文档记载和/或预期的方式调用我们 API、且不依赖任何未定义行为的代码。提升主版本号可能破坏向后兼容，但仅限于[主版本号提升](#主版本号提升)一节所述的范围。

我们还为共享库和静态库保证向后 ABI 兼容。也就是说，只要主版本号保持不变，就应当能够把我们的库替换为任意更高版本的构建产物（静态库情形需重新链接用户二进制），而不会破坏任何有效的用户二进制。

### 添加新接口

安装头文件中的任何新公共标识符都视为新 API——包括新函数、struct、宏、枚举值、typedef、现有 struct 的新字段、新安装头文件等。添加新 API 时请考虑以下准则。

**动机**

新 API 的添加相对容易，但由于上述兼容性要求，修改或移除它们要困难得多。因此您应仔细斟酌：要添加的功能是否真的需要作为新的公共 API 暴露给我们的调用者。

您的新 API 应至少有一个库外部的成熟用例，且该用例无法用现有 API 轻松实现。FFmpeg 的每个库都有明确的职责范围——新 API 必须落在其内。

**替换既有 API**

如果新 API 要取代既有 API，它必须严格优于后者，使新 API 带来的好处超过调用者改代码的代价。添加新 API 后，您应弃用旧 API 并安排其移除，如[移除接口](#移除接口)一节所述。

如果您认为某个既有 API 有缺陷并想修复它，多数情况下的首选做法是新增一个不同名称的替代 API 并弃用既有 API，而不是直接修改它。要让调用者切实感知这些变化（例如通过编译期或运行期弃用警告），并说明清楚如何迁移到新 API（例如在 Doxygen 文档或 wiki 中）。

**API 设计**

FFmpeg 库被各种各样的调用者用于执行广泛的多媒体处理任务。因此，您应在合理范围内尽量面向最广的可行用例集合来设计新 API，避免不必要地把它局限于某类调用者（如仅媒体播放或仅转码）。

**一致性**

检查 FFmpeg 中是否已有类似的 API。若有，尽量以它们为蓝本设计新成员，以获得更好的整体一致性。

新标识符的命名应遵循[命名约定](#命名约定)，并在适用时与其他类似 API 保持一致。

**可扩展性**

您还应考虑 API 未来如何以向后兼容的方式扩展。若要添加新 struct `AVFoo`，标准做法是要求调用者始终通过构造函数分配它，该函数通常命名为 `av_foo_alloc()`。这样便可在 struct 末尾追加新字段而不破坏 ABI 兼容。通常还需要一个析构函数——`av_foo_free(AVFoo**)`，释放间接传入的对象（及其内容，如适用）并向传入的指针写入 `NULL`，从而消除调用者内存中潜在的悬空指针。

如果添加新函数，考虑将来是否可能需要调整其行为——或许应增加一个 flags 参数，即便最初用不上。

**文档**

所有新 API 都必须在公共头文件中所添加标识符的上方以 Doxygen 格式注释写明文档。您还应在 `doc/APIchanges` 中简要提及该变化。

**提升版本号**

破坏向后兼容的 API 或 ABI 变更需要提升（bump）主版本号，如[主版本号提升](#主版本号提升)一节所述。主版本提升是按计划发生的重大事件——因此如果您的修改确需如此，应将其置于 `#if` 预处理卫兵之下先行禁用，待下一次主版本提升时再启用。

能在不破坏 API 与 ABI 兼容的前提下添加的新 API，需要提升次版本号。

提升第三段（micro，微）版本号意味着一次值得注意的二进制兼容变更（例如对解码器有影响的编码器缺陷修复）。第三段版本号总是从 100 起始，以区别于 Libav。

### 移除接口

由于上述兼容性保证，移除 API 是一个复杂的过程，只应有充分理由时才进行。通常是有缺陷、受限或以其他方式不敷使用的 API 被更优秀者取代；但偶尔我们也会在没有任何替代的情况下移除某个 API（例如其提供的功能被认为不值得维护投入、超出项目范围、存在根本性缺陷等）。

移除分两步——第一步先将 API 弃用并列入移除计划，此期间它仍然存在且可用；第二步才真正移除 API，这在[主版本号提升](#主版本号提升)一节有述。

要弃用某个 API，您应向用户发出停止使用的信号。例如若要移除 struct 成员或函数，应为其标注 `attribute_deprecated`。当无法如此标注时，或许可以在运行期检测到已弃用 API 的使用并打印警告（注意不要打印得太频繁）。您还应在相应的 Doxygen 文档块中写明弃用（及替代方案，如适用）。

最后，您应按 `#define FF_API_<FOO> (LIBAVBAR_VERSION_MAJOR < XX)` 的形式定义弃用保护宏（其中 XX 为该 API 将被移除的主版本号），位置在 `libavbar/version_major.h`（`libavutil` 为 `version.h`）。然后，用 `#if FF_API_<FOO> .... #endif` 包裹已弃用 API 的所有使用处，使代码在主版本达到 XX 时自动禁用。您还可以在这些卫兵内使用 `FF_DISABLE_DEPRECATION_WARNINGS` 和 `FF_ENABLE_DEPRECATION_WARNINGS` 来抑制编译器弃用警告。您应测试代码在保护宏取真与取假两种情况下都能编译并正常工作。

### 主版本号提升

主版本号提升意味着 API 和/或 ABI 兼容性破坏。为减轻调用者（他们必须适配自己的代码）受到的负面影响，主版本提升期间的不兼容变更应仅限于：

- 移除此前已弃用的 API。

- 执行破坏 ABI 但不破坏 API 的变更，例如重排 struct 成员顺序。

## 文档与其他

**订阅 ffmpeg-devel 邮件列表。**

订阅 [ffmpeg-devel](https://lists.ffmpeg.org/mailman/listinfo/ffmpeg-devel) 邮件列表很重要。几乎所有非平凡补丁都应发到该列表接受评审。其他开发者可能对您的贡献提出意见，我们期望您看到这些意见，并在被要求时加以改进。（注意：有经验的提交者另有渠道，对琐碎修复有时可跳过评审。）此外，其他开发者在这里讨论的缺陷修复与 FFmpeg 改进对您也可能是很有用的信息。最后，作为列表订阅者，您的贡献会立即投递到列表，而不会经历非订阅者消息所受的审核滞留。

不过，对项目而言，收到您的补丁比您订阅 ffmpeg-devel 列表更重要。如果您手头有补丁，又不想订阅并讨论它，也请照样发到列表。

**订阅 ffmpeg-cvslog 邮件列表。**

所有提交的 diff 都会发送到 [ffmpeg-cvslog](https://lists.ffmpeg.org/mailman/listinfo/ffmpeg-cvslog) 邮件列表。一些开发者阅读该列表以评审来自所有来源的全部代码库变更。是否订阅该列表不做强制要求。

**保持文档同步更新。**

如果您更改了行为或添加了功能，请更新文档。若不确定怎样写最好，请把补丁发到 ffmpeg-devel，文档维护者会评审并提交您的内容。

**重要讨论应让所有人都能看到。**

尽量把重要的讨论和请求（也）放在公开的开发邮件列表上，让所有开发者都能从中受益。

**检查您在 MAINTAINERS 中的条目。**

确保您维护的代码库部分没有遗漏于 `MAINTAINERS` 文件。若您想维护的内容尚未列出，请将您的名字附在其后加入。若某个时候您不再想维护某些代码，请协助寻找新的维护者，并且别忘了更新 `MAINTAINERS` 文件。

我们认为这些规则并不苛刻。如有意见，欢迎联系我们。

# 提交补丁

首先，如果您还没有读过前文的[编码规则](#编码规则)，请先阅读它，尤其是有关补丁提交的规则。

提交补丁时，请使用 `git format-patch` 或 `git send-email`。我们读不了其他格式的 diff :-)。

另外请不要提交包含多个不相关修改的补丁。请将其拆分为各自独立的部分。这不是按文件拆分，而是让补丁在仍保持为一个包含单项修改的逻辑单元的前提下尽量小，即便它横跨多个文件。这会让我们评审您的补丁轻松得多，也大大提高补丁被采纳的机会。

请使用 FFmpeg 的 patcheck 工具检查您的补丁，该工具位于 tools 目录。

提交补丁前请运行[回归测试](#回归测试)，以验证补丁不会造成意外问题。

如果您能说明补丁做了什么（例如"用 lrintf 替换 lrint"）以及为什么（例如"\*BSD 不符合 C99、没有 lrint()"），也会很有帮助。

另外，若发送多个补丁，请每个补丁单独一封邮件，不要把多个不相关补丁附加在同一封邮件里。

补丁应发布到 [Forgejo](https://code.ffmpeg.org/FFmpeg/FFmpeg/pulls) 或 [ffmpeg-devel](https://lists.ffmpeg.org/mailman/listinfo/ffmpeg-devel) 邮件列表。尽可能使用 `git send-email`，它能正确发送补丁而无需额外操心。若无法使用，请将补丁作为 base64 编码的附件发送，以免补丁在传输中被破坏。同时确保使用正确的 MIME 类型（text/x-diff 或 text/x-patch，至少为 text/plain），且每封邮件内嵌或附件只含一个补丁。您可以到 <https://patchwork.ffmpeg.org> 查看；如果补丁没有出现，很可能是 MIME 类型不对。

**如何配置 git send-email？**

请参见 <https://git-send-email.io/>。Gmail 用户另见 <https://shallowsky.com/blog/tech/email/gmail-app-passwds.html>。

**从邮件客户端发送补丁**

并非人人都适合用 `git send-email`。下面的技巧允许以安全的方式经邮件客户端发送补丁。它已在 Outlook 和 Thunderbird（借助 X-Unsent 扩展）上测试通过，可能也适用于其他应用。

像这样创建补丁：

``` text
git format-patch -s -o "outputfolder" --add-header "X-Unsent: 1" --suffix .eml --to ffmpeg-devel@ffmpeg.org -1 1a2b3c4d
```

之后只需用邮件应用打开该 eml 文件并执行"发送"即可。

**评审**

您的补丁或拉取请求将在邮件列表或 code.ffmpeg.org 上评审。您很可能会被要求做一些修改，并应在修改后提交采纳了评审意见的改进版本。此过程可能历经数轮。补丁一旦被认为足够好，某位开发者会接手并将其提交到官方 FFmpeg 代码树。如果您想要基于 LLM 的评审，可将 [Forgejo Fairy](https://code.ffmpeg.org/Forgejo_Fairy) 加为您拉取请求的评审人。Fairy 本身的问题可报告到她的[仓库](https://code.ffmpeg.org/michaelni/Fairies)。

给我们几天反应时间。若一段时间过去仍无反应，请发邮件提醒。您的补丁终会得到处理。

# 新编解码器或格式检查清单

1.  编解码器的初始化与关闭函数是否使用了 av_cold？

2.  是否在 NULL_IF_CONFIG_SMALL 之下为 AVCodec 或 AVInputFormat/AVOutputFormat 结构体添加了 long_name？

3.  是否在 `libavcodec/version.h` 或 `libavformat/version.h` 中提升了次版本号（并重置微版本号）？

4.  是否已在 `allcodecs.c` 或 `allformats.c` 中注册？

5.  是否已把 AVCodecID 添加到 `codec_id.h`？添加新编解码器 ID 时，还应向 `libavcodec/codec_desc.c` 的编解码器描述符列表添加条目。

6.  若它有 FourCC，是否已将其添加到 `libavformat/riff.c`，即便它只是个解码器？

7.  是否在 Makefile 中添加了编译相应文件的规则？即使只是向某个已由其他规则编译的文件（如裸 demuxer）添加一种格式，也记得要做这一步。

8.  是否已向 `doc/general_contents.texi` 的受支持格式或编解码器表添加条目？

9.  是否已在 Changelog 中添加条目？

10. 若它依赖某个解析器或库，是否已在 configure 中添加该依赖？

11. 提交前是否已 `git add` 相应文件？

12. 是否已确认它能独立编译，即用 `configure --disable-everything --enable-decoder=foo`（或 `--enable-demuxer` 或您的组件对应的选项）验证过？

# 补丁提交检查清单

1.  应用补丁后 `make fate` 是否通过？

2.  补丁是否用 git format-patch 或 send-email 生成？

3.  是否已为补丁签署（sign-off）？（`git commit -s`）签署的含义见 [Sign your work](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/process/submitting-patches.rst)。

4.  是否提供了清晰的 git 提交日志信息？

5.  补丁是否基于最新的 FFmpeg git master 分支？

6.  您是否订阅了 ffmpeg-devel？（因垃圾邮件问题，该列表仅限订阅者发帖）

7.  是否已确认修改足够精简，同样的效果无法用更小的补丁和/或更简单的最终代码实现？

8.  若改动涉及速度关键代码，是否做过基准测试？

9.  若做过基准测试，是否已在邮件中提供结果？

10. 是否已确认补丁不引入缓冲区溢出或其他安全问题？

11. 是否用损坏数据测试过您的解码器或解复用器？若没有，请参见 tools/trasher、noise 比特流滤镜以及 [zzuf](http://caca.zoy.org/wiki/zzuf)。喂入损坏数据时，解码器或解复用器不应崩溃、陷入（近乎）无限循环或分配荒谬数量的内存。

12. 是否用样本文件测试过您的解码器或解复用器？样本可从 <https://samples.ffmpeg.org> 获取。

13. 补丁是否没有把功能性与外观性修改混在一起？

14. 是否向代码中添加了制表符或行尾空白？两者都在禁止之列。

15. 补丁是否随您发送的邮件附上？

16. 补丁的 MIME 类型是否正确？应为 text/x-diff 或 text/x-patch，至少是 text/plain，而不能是 application/octet-stream。

17. 若补丁修复缺陷，是否提供了对该缺陷的详尽分析？

18. 若补丁修复缺陷，是否提供了包括样本在内的足够信息，使缺陷可复现、修复可验证？注意请勿向邮件附加大于 \>100k 的样本，而应提供 URL，可上传至 <https://streams.videolan.org/upload/>。

19. 是否提供了关于补丁所做修改的详尽摘要？

20. 是否提供了为什么这样修改的详尽解释？

21. 若应用补丁，是否提供了对用户可见的优缺点的详尽总结？

22. 是否提供了便于我们验证补丁新增功能的示例？

23. 若新增了文件，是否插入了许可证头？应取自 FFmpeg，而不是随意从别处复制粘贴。

24. 在按字母序排列的列表中，只要不破坏 API/ABI 兼容，就应保持字母序。

25. 内容相近的行若纵向对齐能提升可读性，就应纵向对齐。

26. 考虑为您的代码添加回归测试。所有新模块都应有测试覆盖，包括解复用器、复用器、解码器、编码器、滤镜、比特流滤镜、解析器。若确实无法覆盖，请在补丁集中说明原因；有理由不做测试是可以接受的。

27. 若添加了 NASM 代码，请检查在 –disable-x86asm 下一切仍正常工作。

28. 用 valgrind 和/或 Address Sanitizer 测试您的代码，确保其不存在内存泄漏、越界访问等问题。

# 补丁评审流程

发布到 ffmpeg-devel 的所有补丁都会被评审，除非补丁中明确注明不适用于 git master 分支。评审与意见将作为对补丁的回复张贴在邮件列表上。补丁提交者必须处理每一条意见，方式可以是重新提交修改后的补丁，也可以是讨论。重新提交的补丁将像其他补丁一样再次评审。若某补丁在评审中未收到任何意见而通过，即为获批；简单的小补丁可能立即通过，而大补丁通常要经过多轮修改与评审方能获批。补丁获批后将被提交进仓库。

我们会评审所有提交的补丁，但有时相当繁忙，因此对大补丁而言这可能耗费数周。

如果您觉得评审流程太慢，并愿意尝试接手您所改代码区域的维护工作，那么直接克隆 git master 并在该处维护该代码区域即可。我们会从维护得最好的地方合并每个区域。

重新提交补丁时，请不要夹带与评审意见无关的重大改动。此类补丁将被拒绝。重大改动或新功能应作为单独的补丁提交。

欢迎所有人评审补丁。如果您正在等待自己的补丁被评审，也请考虑帮忙评审其他人的补丁——这是让大家的补丁都更快得到评审的好办法。

# 回归测试

在提交补丁（或向仓库提交代码）之前，您至少应测试确认没有破坏任何东西。

运行 'make fate' 即可完成此项检查，详情请参见 [FATE](fate.md)。

\[当然，某些补丁可能会改变回归测试的结果。这种情况下，应相应修改回归测试的参考结果\]。

## 向 fate-suite 数据集添加文件

如果需要上传样本，请发邮件至 samples-request。

当没有可用来生成某个测试所需测试媒体的复用器或编码器时，该媒体就必须纳入 fate-suite。首先请确保样本文件在足以充分测试相应解码器或解复用器的前提下尽量小。大文件会增加网络带宽和磁盘空间开销。当您有了可用的 fate 测试和 fate 样本后，请在提交信息中，或在其发布到 ffmpeg-devel 邮件列表的补丁系列的说明信中，给出样本媒体的直接下载链接。

## 可视化测试覆盖率

FFmpeg 构建系统支持用覆盖率工具 `gcov`/`lcov` 以简便方式可视化测试覆盖率，包含以下步骤：

1.  以启用插桩的方式配置编译：`configure --toolchain=gcov`。

2.  手动或经 FATE 运行您的测试用例。可以是完整的 FATE 回归测试套件，也可以是对 FFmpeg 提供的任何前端工具的任意调用的任意组合。

3.  运行 `make lcov` 生成 HTML 格式的覆盖率数据。

4.  在您惯用的 HTML 查看器中查看 `lcov/index.html`。

可用命令 `make lcov-reset` 重置覆盖率测量结果。运行新测试后需重新执行 `make lcov`。

## 使用 Valgrind

configure 脚本为用 valgrind 发现内存处理相关缺陷提供了快捷方式：只需在 configure 命令行加上选项 `--toolchain=valgrind-memcheck` 或 `--toolchain=valgrind-massif`，即可为在 valgrind 套件的 **memcheck** 或 **massif** 工具监督下运行 FATE 设置合理的默认值。

如需对 valgrind 的调用方式做更细的控制，请改用 configure 命令行中的 `--target-exec='valgrind <your_custom_valgrind_options>` 选项。

# 维护流程

## MAINTAINERS

维护代码库各部分的开发者名单收录于 `MAINTAINERS`。被列入 `MAINTAINERS` 即意味着获得相应仓库的 git 写权限。

## 成为维护者

人们像提交其他代码修改一样，通过发送补丁把自己加入 `MAINTAINERS`。这类补丁会像其他补丁一样接受社区评审。如果有人反对新增维护者，我们期望其愿意公开以真名提出反对，并愿意接手该区域的维护工作。

# 发布流程

FFmpeg 维护一组**发布分支**，它们是面向系统集成方与发行方（如各 Linux 发行版等）推荐的交付物。**发布负责人**会定期准备、测试并在 <https://ffmpeg.org> 网站上发布 tarball。

发布分为两类：

1.  **主版本发布**总是包含最新最强的特性与功能。

2.  **点版本发布**从**发布**分支切出，分支命名为 `release/X`，其中 `X` 为发布版本号。

请注意，我们向用户承诺：任何 FFmpeg 发布中的共享库在任何情况下都不会破坏**针对同一发布系列**先前版本**编译**的程序！

不过，我们不时会做出需要应用程序适配的 API 变更。此类变更只允许出现在（新的）主版本发布中，并需要进一步的操作，如提升库版本号和/或调整符号版本文件。请及时在 **ffmpeg-devel** 长列表上讨论此类变更，以便提前规划。

## 点版本发布的标准

符合以下标准的修改可以作为纳入点版本发布的候选：

1.  修复安全问题，最好是 <http://cve.mitre.org/> 颁发的 **CVE 编号**所标识的问题。

2.  修复 <https://trac.ffmpeg.org> 上有记载的缺陷。

3.  改进随附文档。

4.  与同一发布分支先前点版本发布保持源码与二进制两方面的兼容。

规则的判定顺序为（1 或 2 或 3）且 4。

## 发布检查清单

发布流程包含以下步骤：

1.  确保 `RELEASE` 文件包含即将发布版本的版本号。

2.  在 <https://trac.ffmpeg.org/admin/ticket/versions> 添加该发布。

3.  向邮件列表宣布发布意向。

4.  确保所有相关的安全修复都已回迁。参见 <https://ffmpeg.org/security.html>。

5.  确保 FATE 回归测试套件在发布分支上至少于 **i386** 和 **amd64** 上通过（参见[回归测试](#回归测试)）。

6.  准备 `bz2` 与 `gz` 两种格式的发布 tarball，以及包含 `gpg` 签名的补充文件

7.  在 <https://ffmpeg.org/releases> 发布 tarball。创建并推送形如 `nX` 的附注标签，`X` 为版本号。

8.  向 **ffmpeg-devel** 邮件列表提交并发送一份带有网站新闻条目的补丁。

9.  发布该新闻条目。

10. 向邮件列表发送公告。
