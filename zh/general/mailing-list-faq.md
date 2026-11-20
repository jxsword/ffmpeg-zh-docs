# 一般问题

## 什么是邮件列表？

邮件列表与给某人发电子邮件没有太大区别，主要区别在于您的消息会被订阅该列表的每个人收到。它有点像论坛，只是以电子邮件形式存在。

例子可参见 [ffmpeg-user 存档](https://lists.ffmpeg.org/pipermail/ffmpeg-user/)。

## 我可以问哪类问题？

- [ffmpeg-user](https://lists.ffmpeg.org/mailman/listinfo/ffmpeg-user/)：涉及 FFmpeg 命令行工具（`ffmpeg`、`ffprobe`、`ffplay`）的非脚本化使用或编译问题。

- [libav-user](https://lists.ffmpeg.org/mailman/listinfo/libav-user/)：涉及 FFmpeg libav\* 库（libavcodec、libavformat、libavfilter 等）的问题。

- [ffmpeg-devel](https://lists.ffmpeg.org/mailman/listinfo/ffmpeg-devel/)：讨论 FFmpeg 的开发并提交补丁。用户问题请到 ffmpeg-user 或 libav-user。

报告缺陷请参见 <https://ffmpeg.org/bugreports.html>。

我们无法为脚本和/或第三方工具提供帮助。

## 如何向邮件列表提问或发送消息？

首先您必须[订阅](#如何订阅)。之后只需发送一封邮件：

- 向 <ffmpeg-user@ffmpeg.org> 发送邮件即可向 ffmpeg-user 邮件列表发消息。

- 向 <libav-user@ffmpeg.org> 发送邮件即可向 libav-user 邮件列表发消息。

- 向 <ffmpeg-devel@ffmpeg.org> 发送邮件即可向 ffmpeg-devel 邮件列表发消息。

# 订阅与退订

## 如何订阅？

向 <ffmpeg-user-request@ffmpeg.org> 发送主题为 *subscribe* 的邮件。

或访问 [ffmpeg-user 邮件列表信息页](https://lists.ffmpeg.org/mailman/listinfo/ffmpeg-user/)，参见 *Subscribing to ffmpeg-user* 一节。

其他邮件列表流程相同。

## 如何退订？

向 <ffmpeg-user-request@ffmpeg.org> 发送主题为 *unsubscribe* 的邮件。

或访问 [ffmpeg-user 邮件列表信息页](https://lists.ffmpeg.org/mailman/listinfo/ffmpeg-user/)，滚动到页面底部，在输入框中填入您的邮箱地址，并点击 *Unsubscribe or edit options* 按钮。

其他邮件列表流程相同。

除非您完全无法自行操作，否则请避免让邮件列表管理员帮您退订。参见[邮件列表出问题该联系谁？](#邮件列表出问题该联系谁)

注意可以临时暂停消息投递（度假模式）。参见[如何在不退订的情况下停止邮件投递？](#如何在不退订的情况下停止邮件投递)

# 审核队列

## 为什么我的消息在等待审核人批准？

有些消息会被自动扣留在 *审核队列* 中，必须由邮件列表管理员人工批准：

这些情况是：

- 超过[消息大小上限](#消息大小上限是多少)的消息。

- 账户被设置了 *审核标记* 的用户的消息（极少发生，但可能发生在反复无视规则或对他人恶言相向的用户身上）。

## 审核队列中我的消息要多久才会被批准？

队列并非定期检查。您可以到 Libera Chat 的 `#ffmpeg-devel` IRC 频道请人批准您的消息。

## 如何删除审核队列中我的消息？

您应该收到过主题为 *Your message to \<mailing list name\> awaits moderator approval* 的邮件。消息中有一个链接，除非管理员已批准或拒绝该消息，否则您可以经此链接删除您的消息。

# 存档

## 存档在哪里？

请参见 [FFmpeg Contact](https://ffmpeg.org/contact.html) 页面上的 *Archives* 一节，获取所有 FFmpeg 邮件列表存档的链接。

注意存档按月分卷。跨月讨论在存档中会按月分开。

## 如何回复存档中的消息？

点击消息顶部、主题标题正下方的邮件链接。该链接会带上把消息保持在原讨论串内的正确邮件头。

注意您必须订阅后才能向 ffmpeg-user 或 libav-user 邮件列表发消息。

## 如何搜索存档？

用您惯用的搜索引擎做站点搜索。示例：

`site:lists.ffmpeg.org/pipermail/ffmpeg-user/ "search term"`

# 其他

## 有邮件列表的替代方案吗？

您可以在 Libera Chat 的官方 `#ffmpeg` IRC 频道求助。

另有许多第三方求助站点，如 [Super User](https://superuser.com/tags/ffmpeg) 和 [r/ffmpeg on reddit](https://www.reddit.com/r/ffmpeg/)。

## 什么是 top-posting？

参见 <https://en.wikipedia.org/wiki/Posting_style#Top-posting>。

作为替代，请使用修剪整齐的交错式/行内回复（[示例](https://lists.ffmpeg.org/pipermail/ffmpeg-user/2017-April/035849.html)）。

## 消息大小上限是多少？

消息大小上限为 1000 千字节。较大的文件请提供链接而不是附件。

## 我可以在哪里上传样本文件？

任何不会让我们用起来太麻烦的地方都可以。

如果需要文件托管，Google Drive 和 Dropbox 都可以接受；小于 256 MiB 的文件用 [0x0.st](https://0x0.st/) 很方便。

可能的话，小而短的样本更受欢迎。

## 发送或订阅邮件列表会收到垃圾邮件吗？

可能性极低。

- 订阅用户名单不公开。

- 存档中的邮箱地址已做混淆处理。

- 我们曾使用多个专用测试邮箱账户进行测试，至今没有收到过任何垃圾邮件。

不过，偶尔您可能会在邮件列表里见到垃圾邮件：

- 审核队列中的垃圾邮件可能因人为失误被误批准。

- 有订阅用户的邮箱账户被黑，来自（或看似来自）被黑账户的垃圾邮件被发给了其联系人（邮件列表也在其联系人之列）。

- 如果您订阅了缺陷跟踪器邮件列表（ffmpeg-trac），可能偶尔会看到作为虚假缺陷报告出现的垃圾邮件，但我们会采取措施尽量防止。

## 如何过滤邮件列表消息？

使用 *List-Id*。例如 ffmpeg-user 邮件列表的 List-Id 为 `ffmpeg-user.ffmpeg.org`。您可以在原始邮件或邮件头中查看 List-Id。

之后您就可以把邮件列表消息过滤到各自的文件夹。

## 如何在不退订的情况下停止邮件投递？

有时您可能想临时停止接收所有邮件列表消息。这个"度假模式"做起来很简单：

1.  前往 [ffmpeg-user 邮件列表信息页](https://lists.ffmpeg.org/mailman/listinfo/ffmpeg-user/)

2.  在页面最底部的输入框中填入您的邮箱地址，点击 *Unsubscribe or edit options* 按钮。

3.  输入您的密码并点击 *Log in* 按钮。

4.  找到 *Mail delivery* 选项。在此可禁用/启用邮件投递。若勾选 *Set globally*，您的选择将应用于您订阅的所有其他 FFmpeg 邮件列表。

另外，也可以从您订阅所用的邮箱向 <ffmpeg-user-request@ffmpeg.org> 发送主题为 *set delivery off* 的邮件；要恢复邮件投递，向 <ffmpeg-user-request@ffmpeg.org> 发送主题为 *set delivery on* 的邮件。

## 为什么邮件列表要改写我的地址？

这是由于部分订阅者使用的邮件服务商执行 DMARC 拒收策略，给邮件列表运营者带来了麻烦。

邮件列表必须为这类用户改写（munge）*From:* 头部；否则其邮件服务商会拒收并退回消息，导致其被邮件列表自动退订。

发送消息时，这类用户会看到自己的名字后附加 *via \<mailing list name\>*，且 *From:* 地址被改写为相应邮件列表的地址。

如果想避免这种情况，请换用其他邮件服务。

注意 ffmpeg-devel 不做任何改写，因为改写会干扰补丁作者信息。因此使用带 DMARC 拒收策略邮件服务的用户可能因消息被拒收/退回而被自动退订。

# 规则与礼仪

## 规则和正确的礼仪是什么？

需要记住的东西看起来很多，但我们是想帮您：遵循这些准则能让您更快得到回答，也有助于避免被忽视。

- 始终展示您实际运行的、非脚本化的 `ffmpeg` 命令，以及该命令完整、未经剪裁的控制台输出。

- 使用仍能展示您所遇问题的最简单、最精简的命令。

- 提供所有必要信息，让他人能够尝试复现您的问题。这包括实际命令、完整未经剪裁的控制台输出，以及复现该问题所需的任何输入。

- 使用您能获取的最新 `ffmpeg` 构建。Linux、macOS 与 Windows 最新构建的链接见 [FFmpeg Download](https://ffmpeg.org/download.html) 页面，或从当前 git master 分支自行编译。

- 避免 [top-posting](https://en.wikipedia.org/wiki/Posting_style#Top-posting)。另见[什么是 top-posting？](#什么是-top-posting)

- 避免劫持讨论串。讨论串劫持指回复某消息时把主题行改成与原讨论串无关的内容。多数邮件客户端仍会把改名后的消息显示在原讨论串下，这容易造成混淆，这类消息常被忽视。

- 不要发截图。请复制粘贴控制台文本，而不是对文本截图。

- 这是公开列表，如无必要请避免发送邮件免责声明和法律措辞（legalese）。

- 如未被要求，避免使用 `-loglevel debug`、`-loglevel quiet` 和 `-hide_banner` 选项。

- 附文件时不要压缩小文件。首选不压缩。

- 请勿发送纯 HTML 消息。邮件列表会忽略消息的 HTML 成分。多数邮件客户端会自动附带文本成分：邮件列表使用的就是文本成分。

- 建议配置您的邮件客户端在约 70 个字符处换行。

- 避免向多个邮件列表发送同一消息。

- 请遵循我们的 [Code of Conduct](https://ffmpeg.org/community.html#Code-of-Conduct)。

# 帮助

## 为什么我收不到任何消息？

一些邮箱服务商把邮件列表消息拉黑或在垃圾邮件过滤器中标记为误报。遗憾的是，用户往往对此不知情，且通常无能为力。

条件允许时，我们会设法通知服务商将邮件列表移出黑名单或过滤器。

## 为什么我发出的消息没有显示？

除[被扣留在审核队列中的消息](#为什么我的消息在等待审核人批准)外，您的消息没有出现还可能有以下原因：

- 邮件列表忽略纯 HTML 邮件。多数邮件客户端发送 HTML 邮件时会自动附带文本成分：邮件列表使用的就是文本成分。若没有附带，请认定您的客户端有问题——邮件标准本身就建议随 HTML 成分附带文本成分以构成多部分消息。

- 检查您的垃圾邮件文件夹。

## 为什么我总是被 ffmpeg-devel 退订？

使用带 DMARC 拒收或隔离策略邮件服务的用户，可能因邮件列表消息持续被拒收/退回而被自动移出 ffmpeg-devel 邮件列表。

考虑换用其他邮件服务。

## 邮件列表出问题该联系谁？

向 <ffmpeg-user-owner@ffmpeg.org> 发送消息。
