# 简介

FATE 是一个客户端侧的扩展回归测试套件，也是服务端侧进行结果聚合与展示的手段。

本文档第一部分说明如何从您的 FFmpeg 源码目录使用 FATE 测试您的 ffmpeg 二进制。第二部分说明如何运行 FATE 并将结果提交到 FFmpeg 的 FATE 服务器。

无论如何，您都可以访问下面的网站查看公开可见的 FATE 结果：

<http://fate.ffmpeg.org/>

特别推荐所有向 FFmpeg 贡献源码的人查看，因为它能看出您最近的贡献是否破坏了某些平台上的某个测试。这类破坏通常发生在开发者无法实测的平台。

本文档第二部分说明如何运行 FATE 把结果提交到 FFmpeg 的 FATE 服务器。如果您想提交结果，请先确认您的 CPU、OS 与编译器组合尚未列在上文提到的网站上。

第三部分给出 FATE makefile 目标与变量的完整清单。

# 在 FFmpeg 源码目录中使用 FATE

如果您想在您的机器上运行 FATE，需要先配置 FFmpeg。您可以在配置阶段经 `--samples=/path/to/fate-suite` 参数指定样本位置。

``` text
./configure --enable-somelib --samples=/path/to/fate-suite
```

配置成功后，需要就地添加和/或更新样本：

``` text
make fate-rsync
```

现在就可以运行 FATE：

``` text
make fate
```

可添加的参数清单参见 [makefile 变量](#makefile-变量)。

如果您在配置阶段没有设置样本路径，或想在启动 FATE 前覆盖它，可以用以下三种方式之一。

要么通过设置 make 变量：

``` text
make fate-rsync SAMPLES=/path/to/fate-suite
make fate       SAMPLES=/path/to/fate-suite
```

或为当前会话设置环境变量：

``` text
export FATE_SAMPLES=/path/to/fate-suite
make fate-rsync
make fate
```

或为单条命令临时前缀设置：

``` text
FATE_SAMPLES=/path/to/fate-suite make fate-rsync
FATE_SAMPLES=/path/to/fate-suite make fate
```

该变量也可以写入您的 shell 配置文件使其永久生效。

不要在样本路径中放 '~' 字符表示主目录。由于 shell 的细微行为差异，这会导致 FATE 失败。另外在 Windows 上，路径必须相对于构建路径——此情形下即 FFmpeg 源码目录。

请注意默认禁用了部分断言，因此请在配置时留意设置 `--assert-level=<level>`，例如追求最高测试覆盖率时：

``` text
./configure --assert-level=2
```

注意提升断言级别可能影响性能。

要获取完整的测试清单，运行命令：

``` text
make fate-list
```

您可以通过指定列表中带 `fate-` 前缀的对应项来选择要运行的测试子集，例如：

``` text
make fate-ffprobe_compact fate-ffprobe_xml
```

这样在出现失败时更容易只跑几个测试，而无需运行完整测试套件。

要用自定义包装器运行测试，向 `configure` 传递 `--target-exec` 或设置 \<TARGET_EXEC\> make 变量。

# 将结果提交到 FFmpeg 结果聚合服务器

要把结果提交到服务器，应当从 FFmpeg 源码经 shell 脚本 `tests/fate.sh` 运行 fate。该脚本需要以配置文件作为第一个参数调用。

``` text
tests/fate.sh /path/to/fate_config
```

带注释的配置文件模板位于 `doc/fate_config.sh.template`，其中描述了各个配置变量。

请基于配置模板创建符合您需求的配置。`slot` 配置变量可以是任意尚未使用的字符串，但建议按 `arch-os-compiler-compiler version` 模式命名。配置文件本身会在 shell 脚本中被 source，因此可以使用所有 shell 特性，便于按构建需要设置环境。

首次试运行时，`fate_recv` 变量应为空或被注释掉。这样除不向服务器提交结果外，一切照常运行。配置文件中指定的 \$workdir 中应出现以下文件：

- configure.log

- compile.log

- test.log

- report

- version

当一切正常后，您可以创建 SSH 密钥对，并把公钥发送给 FATE 服务器管理员，联系邮箱为 <fate-admin@ffmpeg.org>。

配置 SSH 客户端连接 FATE 服务器时使用该密钥做公钥认证。同时别忘了核实服务器身份并接受其主机密钥。通常的做法是手动运行一次 SSH 客户端，接受密钥后终止它。FATE 服务器的指纹为：

| 术语      | 描述                                     |
|-----------|-------------------------------------------------|
| `RSA`   | d3:f1:83:97:a4:75:2b:a6:fb:d6:e8:aa:81:93:97:51 |
| `ECDSA` | 76:9f:68:32:04:1e:d5:d4:ec:47:3f:dc:fc:18:17:86 |

如果连接 FATE 服务器遇到问题，可尝试带一个或多个 `-v` 选项运行 `ssh` 命令。您应当会得到有关 SSH 配置和认证过程的详细输出。

剩下的唯一工作就是自动化 fate.sh 脚本的执行与样本目录的同步。

# 向 fate 套件上传新样本

如果需要上传样本，请发邮件至 samples-request。

这面向在 fate 套件服务器上拥有账户的开发者。上传新样本时，请确保它们尽量小——每个客户端的磁盘空间、网络带宽等都会受益于更小的测试用例。同时请记住较早的检出仍会使用既有样本文件，因此实践中一般不要替换、移除或覆盖文件，否则很可能破坏较早的检出或发布。另外，某次提交所需的全部样本应在其推送前，理想情况下提前 24 小时，完成上传。如果您需要账户以便经常上传样本，或希望以此帮助他人，请发邮件到 ffmpeg-devel。

``` text
#First update your local samples copy:
rsync -vauL --chmod=Dg+s,Duo+x,ug+rw,o+r,o-w,+X fate-suite.ffmpeg.org:/home/samples/fate-suite/ ~/fate-suite

#Then do a dry run checking what would be uploaded:
rsync -vanL --no-g --chmod=Dg+s,Duo+x,ug+rw,o+r,o-w,+X ~/fate-suite/ fate-suite.ffmpeg.org:/home/samples/fate-suite

#Upload the files:
rsync -vaL  --no-g --chmod=Dg+s,Duo+x,ug+rw,o+r,o-w,+X ~/fate-suite/ fate-suite.ffmpeg.org:/home/samples/fate-suite
```

# FATE makefile 目标与变量

## Makefile 目标

- **`fate-rsync`** 下载/同步样本文件到已配置的样本目录。

- **`fate-list`** 会列出所有 fate/回归测试目标。

- **`fate-list-failing`** 列出上次执行时失败的 fate 测试。

- **`fate-clear-reports`** 移除先前测试执行的测试报告（清理掉 fate-list-failing 可能返回的过期结果）。

- **`fate`** 运行 FATE 测试套件（需要 fate-suite 数据集）。

## Makefile 变量

- **`V`** 详细程度，可设为 0、1 或 2。

  - 0：仅显示测试参数

  - 1：仅显示测试中使用的命令

  - 2：显示全部信息

- **`SAMPLES`** 在 make 时指定或覆盖 FATE 样本路径，仅在运行回归测试时有意义。

- **`THREADS`** 指定运行回归测试时使用的线程数，对检测线程相关的回归很有用。

  该变量可设为字符串 "random"，可选地后跟数字（如 "random99"），这将让每个测试使用随机数量的线程。若指定了数字，则作为线程数上限，否则上限为 16。

  若某测试失败，它所用线程数会被写入 errfile。

- **`THREAD_TYPE`** 指定测试哪种线程策略，`slice` 或 `frame`，默认 `slice+frame`。

- **`CPUFLAGS`** 指定 CPU 标志。

- **`TARGET_EXEC`** 指定或覆盖用于运行测试的包装器。`TARGET_EXEC` 选项提供了一种以 `valgrind`、`qemu-user` 或 `wine` 包裹运行 FATE，或经 `ssh` 在远程目标上运行 FATE 的方式。

- **`GEN`** 设为 `1` 以生成缺失或不匹配的参考结果。

- **`HWACCEL`** 指定运行回归测试时使用哪种硬件加速，默认 `none`。

- **`KEEP`** 设为 `1` 可在测试成功时保留 fate 测试生成的临时文件。默认 `0`，即移除这些文件。测试失败时文件总是保留。

## 示例

``` text
make V=1 SAMPLES=/var/fate/samples THREADS=2 CPUFLAGS=mmx fate
```
