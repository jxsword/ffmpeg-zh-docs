# API 注释翻译提取范围（api/meta/scope.md）

> M1 实测落盘（PLAN §5 验证项）：Doxyfile EXTRACT_ALL/INPUT 配置 + 公开 API
> 提取清单。基线 FFmpeg n9.0.2（tag 日期 2026-09-18）；doxygen 1.15.0 本机实测。
> 查证日期：2026-11-20（本地源码树 /tmp 浅克隆实测，通道=代理克隆）。

## 一、Doxygen 配置实测结论

| 配置项 | 实测值 | 出处 |
|---|---|---|
| EXTRACT_ALL | **YES**（doc/Doxyfile:412） | 未注释实体也进输出——提取器须以注释块存在为过滤条件 |
| INPUT | **空**（Doxyfile:756），构建期由 `doc/doxy-wrapper.sh` 注入 `INPUT = $@` | wrapper 机制实测 |
| 构建注入内容 | `DOXY_INPUT = $(INSTHEADERS)`（doc/Makefile:105）+ `doc/examples` 24 个 .c（examples/Makefile:43 累加） | Makefile 实测 |
| EXCLUDE_PATTERNS | `*.git`、`*.d`（不排除任何源码目录） | Doxyfile:807 |
| make -n 空跑展开 | **143 个公开头文件 + 19 个 examples .c**（configure 后 `make -n doc/doxy/html` 实测展开，2026-11-20） | 本文件第二节 |
| 本机 doxygen 重建 | `./doc/doxy-wrapper.sh /tmp/doxy-out ... doxygen` 实测跑通（1.15.0） | M1 验证项 |

## 二、公开头文件清单（逐库计数，make -n 展开）

| 库 | 公开头数 | 说明 |
|---|---|---|
| libavutil | 100 | 含 hwcontext_*.h 系列（8 平台）与 halffloat/tea/rc 等 |
| libavcodec | 25 | avcodec.h/codec*.h/vdpau.h/videotoolbox.h 等 |
| libavformat | 4 | avformat.h/avio.h/url.h/version.h |
| libavfilter | 5 | avfilter.h/buffersrc.h/buffersink.h/version.h/dnn.h |
| libavdevice | 3 | avdevice.h/version.h |
| libswscale | 3 | version.h/swscale.h/version_major.h |
| libswresample | 3 | version.h/swresample.h/version_major.h |
| **合计** | **143** | 完整文件名清单：`make -n doc/doxy/html` 可重放 |
| doc/examples | 19 | 构建期并入 DOXY_INPUT（MIT，随示例处理，不进注释翻译主线） |

> S2 调研报告中的 "libavcodec 1695/libavformat 690 个标准头" 为该子报告对
> 目录内全部 .h 文件的口径（含私有头）；本清单按构建系统 INSTHEADERS
> （安装的公开头）口径实测为准——**DR-005 只译公开 API**。

## 三、许可分区（DR-006 API 译本许可页输入）

- 绝大多数公开头：**LGPL 2.1+**（文件头实测惯例）；
- **libavfilter 40 个文件为 GPL**（S2 逐文件头实测）：其中公开头涉及
  `libavfilter/dnn/` 子树等，M2 提取时逐文件核对许可头并在 API 译本许可页列明；
- `doc/examples/*.c`：MIT（24 个构建目标 / DOXY_INPUT 含 19 个 .c）；
- 提取器（M2 `extract_api_comments.py`）须把文件许可头一并写入
  `api/en/<库>/<头文件>.md` 元数据，供回填与许可页使用。

## 四、提取范围（DR-005 口径）

1. **对象**：上述 143 个公开头的 Doxygen 注释块（`/** ... */`）；
2. **保序**：@param/@return/@note/@deprecated 结构逐字段保留；
3. **不译**：.c 内部注释、私有头、`@file` 之外的实现注释；
4. **回填**：validate_backfill.py 校验 @param 数量/顺序、非注释区零改动；
5. **分支隔离**：API 翻译在 `api-baseline/n9.0.2` 分支进行（PLAN §7.2）。

## 五、复现命令

```bash
# 1) 浅克隆 + configure（见 sync_docs.py）
git clone --depth 1 --branch n9.0.2 https://github.com/FFmpeg/FFmpeg.git /tmp/ff
cd /tmp/ff && ./configure --disable-x86asm

# 2) 展开公开头清单（make -n 不执行任何构建动作）
make -n doc/doxy/html | grep -o "libav[a-z]*/[a-zA-Z0-9_.]*\.h" | sort -u

# 3) 实测 doxygen 重建
./doc/doxy-wrapper.sh /tmp/doxy-out /tmp/ff doc/Doxyfile doxygen
```
