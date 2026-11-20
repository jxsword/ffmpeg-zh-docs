# 描述

本文档描述 libavformat 库提供的输入和输出协议。

# 协议选项

libavformat 库提供一些通用全局选项，可以在所有协议上设置。此外，每个协议还可以支持所谓的私有选项，即特定于该组件的选项。

选项可以通过在 FFmpeg 工具中指定 -\<option\> \<value\> 来设置，或通过在 `AVFormatContext` 选项中显式设置值，或使用 `libavutil/opt.h` API 以编程方式设置。

支持的选项列表如下：

- **`protocol_whitelist list (input)`** 设置一个以 "," 分隔的允许协议列表。"ALL" 匹配所有协议。前缀为 "-" 的协议被禁用。默认允许所有协议，但被另一个协议使用的协议（嵌套协议）会被限制为每协议子集。

# 协议

协议是 FFmpeg 中的可配置元素，用于启用对需要特定协议的资源的访问。

配置 FFmpeg 构建时，所有支持的协议默认启用。可以使用 configure 选项 "–list-protocols" 列出所有可用的协议。

可以使用 configure 选项 "–disable-protocols" 禁用所有协议，使用选项 "–enable-protocol=\<PROTOCOL\>" 选择性启用某个协议，或者使用选项 "–disable-protocol=\<PROTOCOL\>" 禁用特定协议。

ff\* 工具的选项 "-protocols" 将显示支持的协议列表。

所有协议都接受以下选项：

- **`rw_timeout`** 等待（网络）读写操作完成的最长时间，单位为微秒。

以下是对当前可用协议的描述。

## amqp

高级消息队列协议 (Advanced Message Queueing Protocol, AMQP) 0-9-1 版是一种基于代理 (broker) 的发布-订阅通信协议。

FFmpeg 必须以 –enable-librabbitmq 编译才能支持 AMQP。还必须运行一个单独的 AMQP 代理。RabbitMQ 是一个开源 AMQP 代理的例子。

启动代理后，FFmpeg 客户端可以使用以下命令向代理推流：

``` text
ffmpeg -re -i input -f mpegts amqp://[[user]:[password]@]hostname[:port][/vhost]
```

其中 hostname 和 port（默认为 5672）是代理的地址。客户端还可以设置用户/密码进行身份验证。这两个字段的默认值均为 "guest"。可以使用 vhost 设置代理上虚拟主机的名称。默认值为 "/"。

多个订阅者可以使用以下命令从代理拉流：

``` text
ffplay amqp://[[user]:[password]@]hostname[:port][/vhost]
```

在 RabbitMQ 中，所有发布到代理的数据都流经一个特定的交换机 (exchange)，每个订阅客户端都有一个分配的队列/缓冲区。当数据包到达交换机时，可能根据 exchange 和 routing_key 字段将其复制到客户端的队列。

支持以下选项：

- **`exchange`** 设置要在代理上使用的交换机。RabbitMQ 有几个预定义的交换机："amq.direct" 是默认交换机，发布者和订阅者必须具有匹配的 routing_key；"amq.fanout" 等同于广播操作（即数据被转发到 fanout 交换机上的所有队列，与 routing_key 无关）；"amq.topic" 与 "amq.direct" 类似，但允许更复杂的模式匹配（参见 RabbitMQ 文档）。

- **`routing_key`** 设置路由键。默认值为 "amqp"。该路由键在 "amq.direct" 和 "amq.topic" 交换机上用于决定是否将数据包写入订阅者的队列。

- **`pkt_size`** 向代理发送/从代理接收的每个数据包的最大大小。默认值为 131072。最小值为 4096，最大值为任意大的值（int 可表示的值）。接收数据包时，此选项设置 FFmpeg 中的内部缓冲区大小。它应当等于或大于发布到代理的数据包的大小，否则接收到的消息可能被截断从而导致解码错误。

- **`connection_timeout`** 与代理建立初始连接期间的超时（秒）。默认值为 rw_timeout，若未设置 rw_timeout 则为 5 秒。

- **`delivery_mode mode`** 设置发送到代理的每条消息的投递模式。接受以下值：

  - **`persistent`** 投递模式设为 "persistent" (2)。这是默认值。根据代理的配置，消息可能会写入代理的磁盘。

  - **`non-persistent`** 投递模式设为 "non-persistent" (1)。除非代理内存吃紧，否则消息将保留在代理的内存中。

## async

输入流的异步数据填充包装器。

在后台线程中填充数据，使 I/O 操作与解复用线程解耦。

``` text
async:URL
async:http://host/resource
async:cache:http://host/resource
```

## bluray

读取 BluRay 播放列表。

可接受的选项有：

| Term       | Description                                 |
|------------|---------------------------------------------|
| `angle`    | BluRay 角度                                  |
| `chapter`  | 起始章节 (1...N)                             |
| `playlist` | 要读取的播放列表 (BDMV/PLAYLIST/?????.mpls) |

示例：

从挂载到 /mnt/bluray 的 BluRay 读取最长的播放列表：

``` text
bluray:/mnt/bluray
```

从挂载到 /mnt/bluray 的 BluRay 读取播放列表 4 的角度 2，从章节 2 开始：

``` text
-playlist 4 -angle 2 -chapter 2 bluray:/mnt/bluray
```

## cache

输入流的缓存包装器。

将输入流缓存到临时文件。它为直播流带来了定位 (seek) 能力。

可接受的选项有：

- **`read_ahead_limit`** 在不支持定位时可以预读的字节数。范围为 -1 到 INT_MAX。-1 表示无限制。默认值为 65536。

URL 语法为

``` text
cache:URL
```

## concat

物理拼接协议。

按顺序从多个资源读取和定位，就像它们是单一资源一样。

此协议接受的 URL 具有如下语法：

``` text
concat:URL1|URL2|...|URLN
```

其中 \<URL1\>、\<URL2\>、...、\<URLN\> 是要拼接的资源的 url，每个资源都可以指定不同的协议。

例如要用 `ffplay` 读取文件序列 `split1.mpeg`、`split2.mpeg`、`split3.mpeg`，可使用命令：

``` text
ffplay concat:split1.mpeg\|split2.mpeg\|split3.mpeg
```

注意，可能需要转义字符 "\|"，该字符对许多 shell 而言是特殊字符。

## concatf

使用以换行符分隔的资源列表的物理拼接协议。

按顺序从多个资源读取和定位，就像它们是单一资源一样。

此协议接受的 URL 具有如下语法：

``` text
concatf:URL
```

其中 \<URL\> 是包含以换行符分隔的待拼接资源列表的 url，每个资源都可以指定不同的协议。特殊字符必须用反斜杠或单引号转义。参见 `ffmpeg-utils` 手册中的 "Quoting and escaping"（引用与转义）章节。

例如要读取在文件 `split.txt` 中以单独行列出的文件序列 `split1.mpeg`、`split2.mpeg`、`split3.mpeg`，用 `ffplay` 可使用命令：

``` text
ffplay concatf:split.txt
```

其中 `split.txt` 包含以下行：

``` text
split1.mpeg
split2.mpeg
split3.mpeg
```

## crypto

AES 加密流读取协议。

可接受的选项有：

- **`key`** 根据给定的十六进制表示设置 AES 解密密钥二进制块。

- **`iv`** 根据给定的十六进制表示设置 AES 解密初始化向量二进制块。

可接受的 URL 格式：

``` text
crypto:URL
crypto+URL
```

## data

URI 内嵌数据。参见 <http://en.wikipedia.org/wiki/Data_URI_scheme>。

例如，要用 `ffmpeg` 转换以内嵌形式给出的 GIF 文件：

``` text
ffmpeg -i "data:image/gif;base64,R0lGODdhCAAIAMIEAAAAAAAA//8AAP//AP///////////////ywAAAAACAAIAAADF0gEDLojDgdGiJdJqUX02iB4E8Q9jUMkADs=" smiley.png
```

## fd

文件描述符访问协议。

可接受的语法为：

``` text
fd: -fd file_descriptor
```

如果未指定 `fd`，默认情况下写入时使用 stdout 文件描述符，读取时使用 stdin。与 pipe 协议不同，若 fd 协议对应常规文件则支持定位。出于安全考虑，fd 协议不支持通过 URL 传递文件描述符。

此协议接受以下选项：

- **`blocksize`** 设置 I/O 操作的最大块大小（字节）。默认值为 `INT_MAX`，即不限制请求的块大小。将该值设置得足够低可以改善用户终止请求的响应时间，这在数据传输缓慢时很有价值。

- **`fd`** 设置文件描述符。

## file

文件访问协议。

从文件读取或写入文件。

文件 URL 可以具有如下形式：

``` text
file:filename
```

其中 \<filename\> 是要读取的文件的路径。

没有协议前缀的 URL 将被视为文件 URL。根据构建配置，开头带有盘符、形如 Windows 路径的 URL 也会被视为文件 URL（在类 unix 系统的构建中通常不是这种情况）。

例如要用 `ffmpeg` 从文件 `input.mpeg` 读取，可使用命令：

``` text
ffmpeg -i file:input.mpeg output.mpeg
```

此协议接受以下选项：

- **`truncate`** 若设为 1，写入时截断已有文件。值为 0 时禁止截断。默认值为 1。

- **`blocksize`** 设置 I/O 操作的最大块大小（字节）。默认值为 `INT_MAX`，即不限制请求的块大小。将该值设置得足够低可以改善用户终止请求的响应时间，这对慢速介质上的文件很有价值。

- **`follow`** 若设为 1，协议将在文件末尾重试读取，从而允许读取仍在写入中的文件。为使其能够终止，需使用 rw_timeout 选项，或使用中断回调（针对 API 用户）。设置此选项还会忽略文件系统报告的文件大小。

- **`seekable`** 控制是否在文件上声明可定位性。0 表示不可定位，-1 表示自动（常规文件可定位，命名管道不可定位）。

  许多解复用器对可定位与不可定位资源的处理方式不同，覆盖此设置可能会加快某些文件的打开速度，但会损失一些特性（例如精确定位）。

- **`pkt_size`** 设置用于文件 I/O 的最大数据包大小。较小的值可以减少内存占用。较大的值可以提高吞吐量，对网络文件系统尤其如此。

  对于读取，如果显式设置，它将覆盖默认的内部缓冲区大小 (32 KB)，并限制每次操作读取的最大数据量。

  对于写入，此选项设置每次写入操作的大小。常规文件默认为 256 KB，其他情况为 32 KB。

## ftp

FTP（文件传输协议）。

使用 FTP 协议从远程资源读取或向其写入。

所需语法如下。

``` text
ftp://[user[:password]@]server[:port]/path/to/remote/resource.mpeg
```

此协议接受以下选项。

- **`timeout`** 设置底层低层操作所用套接字 I/O 操作的超时（微秒）。默认设置为 -1，表示未指定超时。

- **`ftp-user`** 设置用于向 FTP 服务器进行身份验证的用户。FTP URL 中的用户会覆盖此设置。

- **`ftp-password`** 设置用于向 FTP 服务器进行身份验证的密码。FTP URL 中的密码会覆盖此设置；若未设置用户，则由 `ftp-anonymous-password` 覆盖。

- **`ftp-anonymous-password`** 以匿名用户登录时使用的密码。通常应使用电子邮件地址。

- **`ftp-write-seekable`** 控制编码期间连接的可定位性。若设为 1，则假定资源可定位；若设为 0，则假定不可定位。默认值为 0。

注意：该协议可以用作输出，但不建议这样做，除非采取特殊的预防措施（测试、自定义服务器配置等）。不同的 FTP 服务器在定位操作期间表现不同。受服务器限制，ff\* 工具可能产生不完整的内容。

## gopher

Gopher 协议。

## gophers

Gophers 协议。

带 TLS 封装的 Gopher 协议。

## http

HTTP（超文本传输协议）。

此协议接受以下选项：

- **`seekable`** 控制连接的可定位性。若设为 1，则假定资源可定位；若设为 0，则假定不可定位；若设为 -1，将尝试自动检测其是否可定位。默认值为 -1。

- **`chunked_post`** 若设为 1，对 POST 使用分块传输编码 (chunked Transfer-Encoding)，默认值为 1。

- **`http_proxy`** 设置要穿隧道使用的 HTTP 代理，例如 http://example.com:1234

- **`headers`** 设置自定义 HTTP 头，可以覆盖内建的默认头。该值必须是编码这些头的字符串。

- **`content_type`** 为 POST 消息或监听模式设置特定的内容类型。

- **`user_agent`** 覆盖 User-Agent 头。若未指定，协议将使用一个描述 libavformat 构建的字符串（"Lavf/\<version\>"）。

- **`referer`** 设置 Referer 头。在 HTTP 请求中包含 'Referer: URL' 头。

- **`multiple_requests`** 若设为 1 则使用持久连接，默认值为 0。

- **`request_size`** 限制所发起请求的大小。这对某些对无边界范围请求限流的病态服务器很有用，也适用于预期频繁定位的情况。默认禁用（设为 0）。

  注意，如果启用此选项，强烈建议同时启用 `multiple_requests` 选项，并将 `short_seek_size` 设置为相同或更大的值。这样做可以让 FFmpeg 尽可能复用单个 HTTP 连接。

- **`initial_request_size`** 限制初始请求的大小。与 `request_size` 类似，但仅用于初始格式解析期间。对 MXF 或 MOV 这类在头部解析期间需要频繁定位的格式很有用。在解复用器发出大于此大小的读取请求（中间没有定位）之后，实现将继续照常使用请求。默认禁用（设为 0）。

  注意，如果启用此选项，强烈建议同时启用 `multiple_requests` 选项，并将 `short_seek_size` 设置为相同或更大的值。

- **`post_data`** 设置自定义 HTTP POST 数据。

- **`mime_type`** 导出 MIME 类型。

- **`http_version`** 导出 HTTP 响应版本号。通常为 "1.0" 或 "1.1"。

- **`cookies`** 设置要在后续请求中发送的 cookie。每个 cookie 的格式与 Set-Cookie HTTP 响应字段的值相同。多个 cookie 可以用换行符分隔。

- **`icy`** 若设为 1，向服务器请求 ICY (SHOUTcast) 元数据。如果服务器支持，应用程序必须通过读取 `icy_metadata_headers` 和 `icy_metadata_packet` 选项来获取元数据。默认值为 1。

- **`icy_metadata_headers`** 如果服务器支持 ICY 元数据，此选项包含 ICY 特有的 HTTP 应答头，以换行符分隔。

- **`icy_metadata_packet`** 如果服务器支持 ICY 元数据且 `icy` 被设为 1，此选项包含服务器发送的最后一个非空元数据包。对流中元数据更新感兴趣的应用程序应以固定间隔轮询它。

- **`metadata`** 设置一个导出的字典，包含来自比特流的 Icecast 元数据（如果存在）。仅对 C API 有用。

- **`auth_type`** 设置 HTTP 身份验证类型。没有针对 Digest 的选项，因为该方法需要先从服务器获取 nonce 参数，无法像 Basic 那样直接使用。

  - **`none`** 自动选择 HTTP 身份验证类型。这是默认值。

  - **`basic`** 选择 HTTP basic 身份验证。

    Basic 身份验证发送一个包含用户名和密码的 Base64 编码字符串。Base64 不是一种加密形式，应视为与明文发送用户名和密码相同（Base64 是一种可逆编码）。如果资源需要保护，强烈建议考虑使用 basic 身份验证以外的身份验证方案。HTTPS/TLS 应与 basic 身份验证配合使用。若没有这些额外的安全增强措施，不应使用 basic 身份验证来保护敏感或有价值的信息。

- **`send_expect_100`** 为 POST 发送 Expect: 100-continue 头。若设为 1 则发送，若设为 0 则不发送，若设为 -1 则在适用时尝试发送。默认值为 -1。

- **`location`** 包含内容位置的导出字典。仅对 C API 有用。

- **`offset`** 设置初始字节偏移量。

- **`end_offset`** 尝试将请求限制在此偏移量之前的字节范围内。

- **`method`** 用作客户端选项时，它设置请求的 HTTP 方法。

  用作服务器选项时，它设置预期来自客户端的 HTTP 方法。如果预期的与收到的 HTTP 方法不匹配，客户端将收到 Bad Request 响应。目前未设置时不检查 HTTP 方法。将来会被自动检测取代。

- **`reconnect`** 在到达 EOF 之前断开连接时自动重连。

- **`reconnect_at_eof`** 如果设置了此选项，eof 将被视为错误并触发重连，这对直播/无尽流很有用。

- **`reconnect_on_network_error`** 在连接期间发生 TCP/TLS 错误时自动重连。

- **`reconnect_on_http_error`** 触发重连的 HTTP 状态码列表（以逗号分隔）。列表可以包含具体的状态码（例如 '503'）或字符串 '4xx' / '5xx'。

- **`reconnect_streamed`** 如果设置了此选项，即使是流式/不可定位的流也会在出错时重连。

- **`reconnect_delay_max`** 设置放弃重连前的最大延迟（秒）。

- **`reconnect_max_retries`** 设置重试连接的最大次数。默认未设置。

- **`reconnect_delay_total_max`** 设置放弃重连前的最大总延迟（秒）。

- **`respect_retry_after`** 如果启用此选项，并且在遇到 Retry-After 头时，将遵循其请求的重连延迟，而不是使用指数退避。对 429 和 503 错误有用。默认启用。

- **`listen`** 若设为 1，启用实验性 HTTP 服务器。用作输出选项时可用于发送数据；用作输入选项时，可通过 HTTP POST 从客户端读取数据。若设为 2，启用实验性多客户端 HTTP 服务器。此功能尚未在 ffmpeg.c 中实现，因此不得用作命令行选项。

  ``` text
  # Server side (sending):
  ffmpeg -i somefile.ogg -c copy -listen 1 -f ogg http://server:port

  # Client side (receiving):
  ffmpeg -i http://server:port -c copy somefile.ogg

  # Client can also be done with wget:
  wget http://server:port -O somefile.ogg

  # Server side (receiving):
  ffmpeg -listen 1 -i http://server:port -c copy somefile.ogg

  # Client side (sending):
  ffmpeg -i somefile.ogg -chunked_post 0 -c copy -f ogg http://server:port

  # Client can also be done with wget:
  wget --post-file=somefile.ogg http://server:port
  ```

- **`resource`** 使用实验性 HTTP 服务器时，客户端请求的资源。

- **`reply_code`** 使用实验性 HTTP 服务器时，返回给客户端的 HTTP 代码。

- **`short_seek_size`** 设置预读优先于定位并发起新 HTTP 请求的字节阈值。例如，这有助于确保在读取大视频数据包、其间夹杂小音频数据包时使用同一连接。

### HTTP Cookie

某些 HTTP 请求如果不随请求传入 cookie 值，将会被拒绝。`cookies` 选项允许指定这些 cookie。每个 cookie 至少必须指定一个值以及路径和域。同时匹配域和路径的 HTTP 请求将自动在 HTTP Cookie 头字段中包含该 cookie 值。多个 cookie 可以用换行符分隔。

播放流时指定 cookie 所需的语法为：

``` text
ffplay -cookies "nlqptid=nltid=tsn; path=/; domain=somedomain.com;" http://somedomain.com/somestream.m3u8
```

## Icecast

Icecast 协议（向 Icecast 服务器推流）

此协议接受以下选项：

- **`ice_genre`** 设置流的流派 (genre)。

- **`ice_name`** 设置流的名称。

- **`ice_description`** 设置流的描述。

- **`ice_url`** 设置流的网站 URL。

- **`ice_public`** 设置流是否应为公开的。默认值为 0（不公开）。

- **`user_agent`** 覆盖 User-Agent 头。若未指定，将使用形如 "Lavf/\<version\>" 的字符串。

- **`password`** 设置 Icecast 挂载点 (mountpoint) 密码。

- **`content_type`** 设置流的内容类型。如果与 audio/mpeg 不同，则必须设置此项。

- **`legacy_icecast`** 此选项启用对 Icecast 版本 \< 2.4.0 的支持，这些版本不支持 HTTP PUT 方法，而使用 SOURCE 方法。

- **`tls`** 建立到 Icecast 的 TLS (HTTPS) 连接。

``` text
icecast://[username[:password]@]server:port/mountpoint
```

## ipfs

行星际文件系统 (InterPlanetary File System, IPFS) 协议支持。可以通过所谓的网关 (gateway) 访问存储在 IPFS 网络上的文件。这些是 http(s) 端点。此协议包装 IPFS 原生协议（ipfs:// 和 ipns://）以发送到此类网关。用户可以（并且应该）托管自己的节点，这意味着此协议将使用本地网关访问 IPFS 网络上的文件。

此协议接受以下选项：

- **`gateway`** 定义要使用的网关。未设置时，协议将首先按顺序查看 `$IPFS_GATEWAY`、`$IPFS_PATH` 和 `$HOME/.ipfs/` 来尝试定位本地网关。

此协议有两种使用方式。使用 IPFS：

``` text
ffplay ipfs://<hash>
```

或使用 IPNS 协议（IPNS 是可变的 IPFS）：

``` text
ffplay ipns://<hash>
```

## mmst

TCP 上的 MMS (Microsoft Media Server) 协议。

## mmsh

HTTP 上的 MMS (Microsoft Media Server) 协议。

必需的语法为：

``` text
mmsh://server[:port][/app][/playpath]
```

## md5

MD5 输出协议。

计算要写入数据的 MD5 哈希，并在关闭时将其写入指定的输出；若未指定输出，则写入 stdout。它可用于在不写入实际文件的情况下测试复用器。

下面给出一些示例。

``` text
# Write the MD5 hash of the encoded AVI file to the file output.avi.md5.
ffmpeg -i input.flv -f avi -y md5:output.avi.md5

# Write the MD5 hash of the encoded AVI file to stdout.
ffmpeg -i input.flv -f avi -y md5:
```

注意，某些格式（典型如 MOV）要求输出协议可定位，因此它们在 MD5 输出协议上会失败。

## pipe

UNIX 管道访问协议。

从 UNIX 管道读取和写入。

可接受的语法为：

``` text
pipe:[number]
```

如果未指定 `fd`，\<number\> 是与管道的文件描述符对应的编号（例如 stdin 为 0，stdout 为 1，stderr 为 2）。如果未指定 \<number\>，默认情况下写入时使用 stdout 文件描述符，读取时使用 stdin。

例如要用 `ffmpeg` 从 stdin 读取：

``` text
cat test.wav | ffmpeg -i pipe:0
# ...this is the same as...
cat test.wav | ffmpeg -i pipe:
```

例如要用 `ffmpeg` 写入 stdout：

``` text
ffmpeg -i test.wav -f avi pipe:1 | cat > test.avi
# ...this is the same as...
ffmpeg -i test.wav -f avi pipe: | cat > test.avi
```

此协议接受以下选项：

- **`blocksize`** 设置 I/O 操作的最大块大小（字节）。默认值为 `INT_MAX`，即不限制请求的块大小。将该值设置得足够低可以改善用户终止请求的响应时间，这在数据传输缓慢时很有价值。

- **`fd`** 设置文件描述符。

注意，某些格式（典型如 MOV）要求输出协议可定位，因此它们在 pipe 输出协议上会失败。

## prompeg

Pro-MPEG 实践准则 (Code of Practice) \#3 第 2 版 FEC 协议。

Pro-MPEG CoP#3 FEC 是一种针对经 RTP 发送的 MPEG-2 传输流的二维奇偶校验前向纠错机制。

此协议必须与 `rtp_mpegts` 复用器和 `rtp` 协议配合使用。

必需的语法为：

``` text
-f rtp_mpegts -fec prompeg=option=val... rtp://hostname:port
```

列 FEC 流的目的 UDP 端口为 `port + 2`，行 FEC 流为 `port + 4`。

此协议接受以下选项：

| Term  | Description                               |
|-------|-------------------------------------------|
| `l=n` | 列数 (4-20, LxD \<= 100) |
| `d=n` | 行数 (4-20, LxD \<= 100)    |

用法示例：

``` text
-f rtp_mpegts -fec prompeg=l=8:d=4 rtp://hostname:port
```

## rist

可靠互联网流传输协议 (Reliable Internet Streaming Transport)

可接受的选项有：

- **`rist_profile`** 支持的值：

  - **`simple`**

  - **`main`** 此值为默认值。

  - **`advanced`**

- **`buffer_size`** 设置用于数据重传的内部 RIST 缓冲区大小（毫秒）。默认值为 0，表示使用 librist 默认值（1 秒）。最大值为 30 秒。

- **`fifo_size`** librist 接收器输出 fifo 的大小（以数据包数计）。必须是 2 的幂。默认值为 8192（librist 默认值为 1024）。

- **`overrun_nonfatal=1|0`** 在 librist fifo 缓冲区溢出时继续存活。默认值为 0。

- **`pkt_size`** 设置发送数据的最大数据包大小。默认为 1316。

- **`log_level`** 设置 RIST 日志消息的日志级别。只有当您明确希望启用调试级别消息或丢包模拟时才需要设置此项，否则将遵循常规日志级别。

- **`secret`** 设置加密密钥的覆盖值，默认未设置。

- **`encryption`** 设置加密类型，默认禁用。可接受的值为 128 和 256。

## rtmp

实时消息协议 (Real-Time Messaging Protocol)。

实时消息协议 (RTMP) 用于跨 TCP/IP 网络传输流媒体内容。

必需的语法为：

``` text
rtmp://[username:password@]server[:port][/app][/instance][/playpath]
```

可接受的参数有：

- **`username`** 可选的用户名（主要用于发布）。

- **`password`** 可选的密码（主要用于发布）。

- **`server`** RTMP 服务器的地址。

- **`port`** 要使用的 TCP 端口号（默认为 1935）。

- **`app`** 要访问的应用程序的名称。它通常对应于应用程序在 RTMP 服务器上的安装路径（例如 `/ondemand/`、`/flash/live/` 等）。也可以通过 `rtmp_app` 选项覆盖从 URI 解析出的值。

- **`playpath`** 相对于 \<app\> 中指定的应用程序，要播放的资源的路径或名称，可以以 "mp4:" 为前缀。也可以通过 `rtmp_playpath` 选项覆盖从 URI 解析出的值。

- **`listen`** 充当服务器，监听传入连接。

- **`timeout`** 等待传入连接的最长时间。隐含 listen。

此外，以下参数可以通过命令行选项设置（或在代码中通过 `AVOption` 设置）：

- **`rtmp_app`** 要在 RTMP 服务器上连接的应用程序的名称。此选项覆盖 URI 中指定的参数。

- **`rtmp_buffer`** 设置客户端缓冲时间（毫秒）。默认值为 3000。

- **`rtmp_conn`** 额外的任意 AMF 连接参数，从字符串解析，例如 `B:1 S:authMe O:1 NN:code:1.23 NS:flag:ok O:0`。每个值都以单个字符为前缀表示类型：B 表示布尔值，N 表示数字，S 表示字符串，O 表示对象，Z 表示 null，后跟冒号。对于布尔值，数据必须分别为 0 或 1（对应 FALSE 或 TRUE）。同样，对于对象，数据必须分别为 0 或 1（对应结束或开始一个对象）。子对象中的数据项可以命名，方法是在类型前加 'N' 并在值之前指定名称（即 `NB:myFlag:1`）。此选项可以多次使用以构造任意 AMF 序列。

- **`rtmp_enhanced_codecs`** 指定客户端在增强 RTMP 流中声明支持的编解码器列表。此选项应设置为以逗号分隔的 fourcc 值列表，例如多编解码器时为 `hvc1,av01,vp09`，单个编解码器时为 `hvc1`。指定的列表将显示在 Connect 命令消息的 "fourCcLive" 属性中。

- **`rtmp_flashver`** 用于运行 SWF 播放器的 Flash 插件版本。默认值为 LNX 9,0,124,2。（发布时，默认值为 FMLE/3.0 (compatible; \<libavformat version\>)。）

- **`rtmp_flush_interval`** 同一请求中刷新的数据包数量（仅限 RTMPT）。默认值为 10。

- **`rtmp_live`** 指定媒体为直播流。直播流无法恢复播放或定位。默认值为 `any`，表示订阅者首先尝试播放 playpath 中指定的直播流；如果未找到该名称的直播流，则播放录制的流。其他可能的值为 `live` 和 `recorded`。

- **`rtmp_pageurl`** 嵌入媒体的网页的 URL。默认不发送任何值。

- **`rtmp_playpath`** 要播放或发布的流标识符。此选项覆盖 URI 中指定的参数。

- **`rtmp_subscribe`** 要订阅的直播流的名称。默认不发送任何值。仅当指定了此选项或 rtmp_live 被设为 live 时才会发送。

- **`rtmp_swfhash`** 解压缩后的 SWF 文件的 SHA256 哈希值（32 字节）。

- **`rtmp_swfsize`** 解压缩后的 SWF 文件的大小，SWFVerification 所需。

- **`rtmp_swfurl`** 媒体的 SWF 播放器的 URL。默认不发送任何值。

- **`rtmp_swfverify`** 播放器 swf 文件的 URL，自动计算哈希/大小。

- **`rtmp_tcurl`** 目标流的 URL。默认值为 proto://host\[:port\]/app。

- **`tcp_nodelay=1|0`** 设置 TCP_NODELAY 以禁用 Nagle 算法。默认值为 0。

  *注：目前对套接字的写入未针对最小化系统调用进行优化，这会降低 TCP_NODELAY 的效率/效果。*

- **`tcp_keepalive=1|0`** 启用 TCP keepalive 机制以检测失效的对等端，并帮助维持长期空闲的连接。默认值为 0。

  只有基本的 keepalive 选项 (SO_KEEPALIVE) 可以启用或禁用。平台特定的调优参数（如 TCP_KEEPIDLE、TCP_KEEPINTVL 或 TCP_KEEPCNT）不可配置，将使用操作系统的默认值。

例如要用 `ffplay` 从 RTMP 服务器 "myserver" 上的应用程序 "vod" 读取名为 "sample" 的多媒体资源：

``` text
ffplay rtmp://myserver/vod/sample
```

要发布到受密码保护的服务器，并分别传递 playpath 和 app 名称：

``` text
ffmpeg -re -i <input> -f flv -rtmp_playpath some/long/path -rtmp_app long/app/name rtmp://username:password@myserver/
```

## rtmpe

加密实时消息协议。

加密实时消息协议 (RTMPE) 用于在标准密码学原语（由 Diffie-Hellman 密钥交换和 HMACSHA256 组成，生成一对 RC4 密钥）内传输流媒体内容。

## rtmps

经安全 SSL 连接的实时消息协议。

实时消息协议 (RTMPS) 用于跨加密连接传输流媒体内容。

## rtmpt

经 HTTP 隧道的实时消息协议。

经 HTTP 隧道的实时消息协议 (RTMPT) 用于在 HTTP 请求内传输流媒体内容以穿越防火墙。

## rtmpte

经 HTTP 隧道的加密实时消息协议。

经 HTTP 隧道的加密实时消息协议 (RTMPTE) 用于在 HTTP 请求内传输流媒体内容以穿越防火墙。

## rtmpts

经 HTTPS 隧道的实时消息协议。

经 HTTPS 隧道的实时消息协议 (RTMPTS) 用于在 HTTPS 请求内传输流媒体内容以穿越防火墙。

## libsmbclient

libsmbclient 允许操纵 CIFS/SMB 网络资源。

所需语法如下。

``` text
smb://[[domain:]user[:password@]]server[/share[/path[/file]]]
```

此协议接受以下选项。

- **`timeout`** 设置底层低层操作所用套接字 I/O 操作的超时（毫秒）。默认设置为 -1，表示未指定超时。

- **`truncate`** 若设为 1，写入时截断已有文件。值为 0 时禁止截断。默认值为 1。

- **`workgroup`** 设置用于建立连接的工作组。默认不指定工作组。

更多信息参见：<http://www.samba.org/>。

## libssh

经 libssh 的安全文件传输协议

使用 SFTP 协议从远程资源读取或向其写入。

所需语法如下。

``` text
sftp://[user[:password]@]server[:port]/path/to/remote/resource.mpeg
```

此协议接受以下选项。

- **`timeout`** 设置底层低层操作所用套接字 I/O 操作的超时。默认设置为 -1，表示未指定超时。

- **`truncate`** 若设为 1，写入时截断已有文件。值为 0 时禁止截断。默认值为 1。

- **`private_key`** 指定授权期间使用的私钥文件的路径。默认情况下，libssh 在 `~/.ssh/` 目录中搜索密钥。

示例：播放存储在远程服务器上的文件。

``` text
ffplay sftp://user:password@server_address:22/home/user/resource.mpeg
```

## librtmp rtmp, rtmpe, rtmps, rtmpt, rtmpte

通过 librtmp 支持的实时消息协议及其变体。

在配置期间需要 librtmp 头文件和库。需要通过 "–enable-librtmp" 显式配置构建。启用后，它将替换原生 RTMP 协议。

此协议提供支持 RTMP、HTTP 内隧道 RTMP (RTMPT)、加密 RTMP (RTMPE)、SSL/TLS 上的 RTMP (RTMPS) 以及这些加密类型的隧道变体 (RTMPTE、RTMPTS) 所需的大多数客户端函数和少量服务器函数。

必需的语法为：

``` text
rtmp_proto://server[:port][/app][/playpath] options
```

其中 \<rtmp_proto\> 是字符串 "rtmp"、"rtmpt"、"rtmpe"、"rtmps"、"rtmpte"、"rtmpts" 之一，对应各个 RTMP 变体；\<server\>、\<port\>、\<app\> 和 \<playpath\> 的含义与 RTMP 原生协议中指定的相同。\<options\> 包含一个以空格分隔的选项列表，选项形如 \<key\>=\<val\>。

更多信息参见 librtmp 手册页 (man 3 librtmp)。

例如，要用 `ffmpeg` 将文件实时推流到 RTMP 服务器：

``` text
ffmpeg -re -i myfile -f flv rtmp://myserver/live/mystream
```

要用 `ffplay` 播放同一流：

``` text
ffplay "rtmp://myserver/live/mystream live=1"
```

## rtp

实时传输协议 (Real-time Transport Protocol)。

RTP URL 的必需语法为：

``` text
rtp://hostname[:port][?options]
```

\<port\> 指定要使用的 RTP 端口。

\<options\> 包含一个以 & 分隔的选项列表，选项形如 \<key\>=\<val\>。可使用标准百分号编码（以及用加号表示空格）来转义键和值。

选项也可以通过命令行选项指定（或在代码中通过 `AVOption` 指定）。

支持的选项列表如下。

- **`ttl=n`** 设置 TTL (Time-To-Live) 值（仅限组播）。

- **`rtcpport=n`** 将远端 RTCP 端口设置为 \<n\>。

- **`localport, local_rtpport, localrtpport=n`** 将本地 RTP 端口设置为 \<n\>。

  使用 localport 这一选项名已弃用，不应再使用。

- **`local_rtcpport, localrtcpport=n'`** 将本地 RTCP 端口设置为 \<n\>。

- **`pkt_size=n`** 将最大数据包大小（字节）设置为 \<n\>。

- **`buffer_size=size`** 设置最大 UDP 套接字缓冲区大小（字节）。

- **`connect=0|1`** 在 UDP 套接字上执行（设为 1 时）或不执行（设为 0 时）`connect()`。

- **`sources=ip[,ip]`** 列出允许的源 IP 地址。

- **`block=ip[,ip]`** 列出禁止（阻止）的源 IP 地址。

- **`write_to_source=0|1`** 将数据包发送到最近收到的数据包的源地址（设为 1 时）或发送到默认远端地址（设为 0 时）。

- **`localaddr=addr`** 用于发送数据包或加入组播组的网络接口的本地 IP 地址。

- **`timeout=n`** 将套接字 I/O 操作的超时（微秒）设置为 \<n\>。

重要说明：

1.  如果未设置 `rtcpport`，RTCP 端口将设置为 RTP 端口的值加 1。

2.  如果未设置 `localrtpport`（本地 RTP 端口），本地 RTP 和 RTCP 端口将使用任意可用端口。

3.  如果未设置 `localrtcpport`（本地 RTCP 端口），它将设置为本地 RTP 端口的值加 1。

## rtsp

实时流协议 (Real-Time Streaming Protocol)。

从技术上讲，RTSP 不是 libavformat 中的协议处理器，而是一个解复用器和复用器。该解复用器同时支持常规 RTSP（数据经 RTP 传输；Apple 和 Microsoft 等使用此方式）和 Real-RTSP（数据经 RDT 传输）。

该复用器可用于使用 RTSP ANNOUNCE 向支持它的服务器发送流（当前支持 Darwin Streaming Server 和 Mischa Spiegelmock 的 [RTSP server](https://github.com/revmischa/rtsp-server)）。

RTSP url 的必需语法为：

``` text
rtsp://hostname[:port]/path
```

选项可以在 `ffmpeg`/`ffplay` 命令行上设置，或在代码中通过 `AVOption` 设置，或在 `avformat_open_input` 中设置。

### 复用器

支持以下选项。

- **`rtsp_transport`** 设置 RTSP 传输协议。

  它接受以下值：

  - **`udp`** 使用 UDP 作为底层传输协议。

  - **`tcp`** 使用 TCP（在 RTSP 控制信道内交错传输）作为底层传输协议。

  默认值为 `0`。

- **`rtsp_flags`** 设置 RTSP 标志。

  接受以下值：

  | Term | Description |
  |----|----|
  | `latm` | 对 AAC 使用 MP4A-LATM 打包方式而不是 MPEG4-GENERIC。 |
  | `rfc2190` | 对 H.263 使用 RFC 2190 打包方式而不是 RFC 4629。 |
  | `skip_rtcp` | 不发送 RTCP 发送方报告。 |
  | `h264_mode0` | 在 RTP 中对 H.264 使用 mode 0。 |
  | `send_bye` | 结束时发送 RTCP BYE 数据包。 |

  默认值为 `0`。

- **`min_port`** 设置最小本地 UDP 端口。默认值为 5000。

- **`max_port`** 设置最大本地 UDP 端口。默认值为 65000。

- **`buffer_size`** 设置最大套接字缓冲区大小（字节）。

- **`pkt_size`** 设置最大发送数据包大小（字节）。默认值为 1472。

### 解复用器

支持以下选项。

- **`initial_pause`** 若设为 1，则不立即开始播放流。默认值为 0。

- **`rtsp_transport`** 设置 RTSP 传输协议。

  它接受以下值：

  - **`udp`** 使用 UDP 作为底层传输协议。

  - **`tcp`** 使用 TCP（在 RTSP 控制信道内交错传输）作为底层传输协议。

  - **`udp_multicast`** 使用 UDP 组播作为底层传输协议。

  - **`http`** 使用 HTTP 隧道作为底层传输协议，这有助于穿越代理。

  - **`https`** 使用 HTTPs 隧道作为底层传输协议，这有助于穿越代理，且出于安全考虑被广泛使用。

  可以指定多个底层传输协议，此时将逐个尝试（如果其中一个设置失败，则尝试下一个）。对于复用器，仅支持 `tcp` 和 `udp` 选项。

- **`rtsp_flags`** 设置 RTSP 标志。

  接受以下值：

  - **`filter_src`** 仅接受来自协商的对等端地址和端口的数据包。

  - **`listen`** 充当服务器，监听传入连接。

  - **`prefer_tcp`** 若 TCP 可用作 RTSP RTP 传输，则优先尝试以 TCP 进行 RTP 传输。

  - **`satip_raw`** 导出原始 MPEG-TS 流而不是进行解复用。该标志将直接写出原始流，保持原始的 PAT/PMT/PID 不变。

  默认值为 `none`。

- **`allowed_media_types`** 设置从服务器接受的媒体类型。

  接受以下标志：

  - **`video`**

  - **`audio`**

  - **`data`**

  - **`subtitle`**

  默认接受所有媒体类型。

- **`min_port`** 设置最小本地 UDP 端口。默认值为 5000。

- **`max_port`** 设置最大本地 UDP 端口。默认值为 65000。

- **`listen_timeout`** 设置建立初始连接的最大超时（秒）。将 `listen_timeout` 设置为 \> 0 会将 `rtsp_flags` 设为 `listen`。默认值为 -1，表示在设置了 `listen` 模式时超时为无限。

- **`reorder_queue_size`** 设置为处理乱序数据包而缓冲的数据包数量。

- **`timeout`** 设置套接字 TCP I/O 超时（微秒）。

- **`user_agent`** 覆盖 User-Agent 头。若未指定，默认为 libavformat 标识字符串。

- **`buffer_size`** 设置最大套接字缓冲区大小（字节）。

通过 UDP 接收数据时，解复用器会尝试对接收到的数据包重新排序（因为它们可能乱序到达，或者可能完全丢失）。可以通过将最大解复用延迟设为零（通过 AVFormatContext 的 `max_delay` 字段）来禁用此行为。

使用 `ffplay` 观看多码率 Real-RTSP 流时，可以用 `-vst` \<n\> 和 `-ast` \<n\> 分别选择要显示的视频和音频流，并可以通过按 `v` 和 `a` 实时切换。

### 示例

以下示例均使用 `ffplay` 和 `ffmpeg` 工具。

- 观看 UDP 上的流，最大重排序延迟为 0.5 秒：

  ``` text
  ffplay -max_delay 500000 -rtsp_transport udp rtsp://server/video.mp4
  ```

- 观看经 HTTP 隧道传输的流：

  ``` text
  ffplay -rtsp_transport http rtsp://server/video.mp4
  ```

- 向 RTSP 服务器实时发送流，供其他人观看：

  ``` text
  ffmpeg -re -i input -f rtsp -muxdelay 0.1 rtsp://server/live.sdp
  ```

- 实时接收流：

  ``` text
  ffmpeg -rtsp_flags listen -i rtsp://ownaddress/live.sdp output
  ```

## sap

会话通告协议 (Session Announcement Protocol, RFC 2974)。从技术上讲，它不是 libavformat 中的协议处理器，而是一个复用器和解复用器。它用于 RTP 流的信令，通过在单独的端口上定期通告这些流的 SDP。

### 复用器

提供给复用器的 SAP url 的语法为：

``` text
sap://destination[:port][?options]
```

RTP 数据包被发送到端口 \<port\> 上的 \<destination\>；若未指定端口，则发送到端口 5004。\<options\> 是一个以 `&` 分隔的列表。支持以下选项：

- **`announce_addr=address`** 指定发送通告的目的 IP 地址。若省略，通告将发送到常用的 SAP 通告组播地址 224.2.127.254 (sap.mcast.net)；若 \<destination\> 是 IPv6 地址，则发送到 ff0e::2:7ffe。

- **`announce_port=port`** 指定发送通告的端口，若未指定，默认为 9875。

- **`ttl=ttl`** 指定通告和 RTP 数据包的生存时间 (time to live) 值，默认为 255。

- **`same_port=0|1`** 若设为 1，则在同一端口对上发送所有 RTP 流。若为零（默认值），所有流都发送到唯一的端口，每个流的端口比前一个高 2 个数字。VLC/Live555 要求将此设置为 1 才能接收流。libavformat 中用于接收的 RTP 协议栈要求所有流都发送到唯一的端口。

下面给出一些示例命令行。

要在本地子网上广播流以供 VLC 观看：

``` text
ffmpeg -re -i input -f sap sap://224.0.0.255?same_port=1
```

类似地，要用 `ffplay` 观看：

``` text
ffmpeg -re -i input -f sap sap://224.0.0.255
```

要用 `ffplay` 经 IPv6 观看：

``` text
ffmpeg -re -i input -f sap sap://[ff0e::1:2:3:4]
```

### 解复用器

提供给解复用器的 SAP url 的语法为：

``` text
sap://[address][:port]
```

\<address\> 是监听通告的组播地址；若省略，则使用默认值 224.2.127.254 (sap.mcast.net)。\<port\> 是监听的端口；若省略，则为 9875。

解复用器在给定的地址和端口上监听通告。收到通告后，它会尝试接收该特定流。

下面给出一些示例命令行。

要播放从常规 SAP 组播地址通告的第一个流：

``` text
ffplay sap://
```

要播放从默认 IPv6 SAP 组播地址通告的第一个流：

``` text
ffplay sap://[ff0e::2:7ffe]
```

## sctp

流控制传输协议 (Stream Control Transmission Protocol)。

可接受的 URL 语法为：

``` text
sctp://host:port[?options]
```

\<options\> 包含一个以 & 分隔的选项列表，选项形如 \<key\>=\<val\>。可使用标准百分号编码（以及用加号表示空格）来转义键和值。

选项也可以通过命令行选项指定（或在代码中通过 `AVOption` 指定）。

支持的选项列表如下。

- **`listen`** 若设为任意值，则监听传入连接。默认执行向外连接。

- **`max_streams`** 设置最大流数量。默认不设限制。

## shared

线程安全、持久化、跨进程的输入流缓存包装器。将输入流缓存到指定目录中的文件。这与 [cache](#cache) 类似，但使用磁盘上的持久缓存，可以在多个进程或解复用器之间共享，甚至可以并发共享。

缓存文件名通过对输入 URL 进行哈希得到，因此如果同一 URL 被用于不同内容（例如由于使用额外的 POST 数据来选择流 ID），则存在冲突风险。为避免这种情况，请确保仅将此协议用于能唯一标识内容的 URL；否则可能会得到来源混杂的乱码内容。

可接受的选项有：

- **`cache_dir`** 存储缓存文件的目录路径。此选项是必需的。

- **`block_shift`** 内部读/写所用块大小的移位因子 (log2)。默认值为 15，即 32KB 块。如果与创建现有缓存文件时指定的值不匹配，将改用先前指定的值。

- **`read_only`** 若为 true，则将共享缓存用于读取，但不向其写入任何新块。默认值为 false。请注意，即使启用了此选项，缓存文件在不存在时仍会被初始化。

- **`cache_verify`** 若为 true，将从缓存读取的任何数据与底层输入流进行核对，并报告任何不匹配。请注意，这会使缓存层实际上失去作用。这纯粹是一个调试选项。

- **`cache_timeout`** 若设为非零值，则指定等待数据变为可用的最长时间（微秒），适用于另一个进程当前正试图同时获取并缓存同一块的情况。如果此超时已过，则假定另一个进程可能已卡住或在此期间已终止。

  如果设为零，则不进行任何等待，所有进程将立即竞争自行获取相同的缺失块。默认值为 10000 (10 ms)。

- **`retry_errors`** 若为 true（默认值），则忽略来自底层输入流的瞬时读取错误并再次重试。若为 false，则先前读取失败的任何块都将被视为永久不可访问。

URL 语法为

``` text
shared:URL
```

## srt

经 libsrt 的 Haivision 安全可靠传输协议。

SRT URL 支持的语法为：

``` text
srt://hostname:port[?options]
```

\<options\> 包含一个以 & 分隔的选项列表，选项形如 \<key\>=\<val\>。可使用标准百分号编码（以及用加号表示空格）来转义键和值。

选项也可以通过命令行选项指定（或在代码中通过 `AVOption` 指定）。

支持的选项列表如下。

- **`connect_timeout=milliseconds`** 连接超时；在默认连接超时为 3 秒的情况下，RTT \> 1500 毫秒（2 次握手交互）时 SRT 无法连接。此选项适用于 caller 和 rendezvous 连接模式。rendezvous 模式的连接超时是所设值的 10 倍（对于使用早期版本时的这一连接问题，可用作变通方法）。

- **`ffs=bytes`** 飞行标志大小 (Flight Flag Size，窗口大小)，以字节为单位。FFS 实际上是一个内部参数，应将其设置为不小于 `recv_buffer_size` 和 `mss`。默认值相对较大，因此除非设置了非常大的接收缓冲区，否则无需更改此选项。默认值为 25600。

- **`inputbw=bytes/seconds`** 发送方的标称输入速率，以字节/秒为单位。当 `maxbw` 设为相对值 (0) 时，与 `oheadbw` 一起使用，用于计算在随主媒体流一起发送恢复数据包时的最大发送速率：若未设置 `inputbw` 而 `maxbw` 设为相对值 (0)，则发送速率为 `inputbw` \* (100 + `oheadbw`) / 100，实际输入速率将在库内部估算。默认值为 0。

- **`iptos=tos`** IP 服务类型 (Type of Service)。仅适用于发送方。默认值为 0xB8。

- **`ipttl=ttl`** IP 生存时间 (Time To Live)。仅适用于发送方。默认值为 64。

- **`latency=microseconds`** 基于时间戳的数据包交付延迟。用于吸收丢失数据包重传的突发。此标志将 `rcvlatency` 和 `peerlatency` 设置为相同的值。请注意，在 1.3.0 版本之前，这是设置延迟的唯一标志，但其实际效果等价于：发送方设置 `peerlatency`、接收方设置 `rcvlatency`，且不支持双向流发送。

- **`listen_timeout=microseconds`** 设置套接字监听超时。

- **`maxbw=bytes/seconds`** 最大发送带宽，以字节/秒为单位。-1 表示无限（CSRTCC 限制为 30mbps），0 表示相对于输入速率（参见 `inputbw`），\>0 表示绝对限制值。默认值为 0（相对）。

- **`mode=caller|listener|rendezvous`** 连接模式。`caller` 打开客户端连接。`listener` 启动服务器以监听传入连接。`rendezvous` 使用 Rendez-Vous 连接模式。默认值为 caller。

- **`mss=bytes`** 最大分段大小 (Maximum Segment Size)，以字节为单位。用于缓冲区分配，并使用假定数据包被完全填充的数据包计数器进行速率计算。使用对等端之间较小的 MSS。在整个互联网上默认为 1500。这是 UDP 数据包的最大大小，只能调低，除非您有一些不常用的专用网络设置。默认值为 1500。

- **`nakreport=1|0`** 若设为 1，接收方将定期发送 'UMSG_LOSSREPORT' 消息，直到丢失的数据包被重传或被有意丢弃。默认值为 1。

- **`oheadbw=percents`** 输入速率之上的恢复带宽开销，以百分比表示。参见 `inputbw`。默认值为 25%。

- **`passphrase=string`** HaiCrypt 加密/解密口令字符串，长度为 10 到 79 个字符。该口令是发送方和接收方之间的共享密钥。它用于通过 PBKDF2 (Password-Based Key Derivation Function) 生成密钥加密密钥 (Key Encrypting Key)。仅在 `pbkeylen` 非零时使用。仅在接收到的数据已加密时才在接收方使用。所配置的口令无法恢复（只写）。

- **`enforced_encryption=1|0`** 若为 true，则连接双方必须设置相同的密码（包括空密码，即不加密）。如果密码不匹配或只有一方未加密，连接将被拒绝。默认值为 true。

- **`kmrefreshrate=packets`** 在传输这么多数据包之后，加密密钥切换为新密钥。默认值为 -1。-1 表示自动（srt 库中为 0x1000000）。此选项的范围为 0 - `INT_MAX` 内的整数。

- **`kmpreannounce=packets`** 从发送新加密密钥到发生切换之间的间隔。此值也适用于从发生切换到旧加密密钥退役之间的后续间隔。默认值为 -1。-1 表示自动（srt 库中为 0x1000）。此选项的范围为 0 - `INT_MAX` 内的整数。

- **`snddropdelay=microseconds`** 发送方在丢弃数据包之前的额外延迟。此延迟会加到默认的丢弃延迟时间间隔值上。

  特殊值 -1：发送方完全不丢弃数据包。

- **`payload_size=bytes`** 设置在 Live 模式下单次调用发送函数时传输的数据包的最大声明大小。如果不使用该值，则设为 0（这是文件模式下的默认值）。默认值为 -1（自动），通常表示 MPEG-TS；如果要使用 SRT 发送任何其他类型的载荷，例如将直播流包装在非常小的帧中，则可以使用更大的最大帧大小，但不得超过 1456 字节。

- **`pkt_size=bytes`** `payload_size` 的别名。

- **`peerlatency=microseconds`** 由发送方设置为接收方最小值的延迟值（如 `rcvlatency` 中所述）。

- **`pbkeylen=bytes`** 发送方加密密钥长度，以字节为单位。只能设置为 0、16、24 和 32。若不为 0 则启用发送方加密。接收方不需要（设为 0），密钥大小在 HaiCrypt 握手期间从发送方获取。默认值为 0。

- **`rcvlatency=microseconds`** 从数据包被发送的时刻到接收函数将其交付给接收方应用程序的时刻之间应经过的时间。该时间应当是足够大的缓冲时间，以覆盖发送所花的时间、意外延长的 RTT 时间以及重传丢失 UDP 数据包所需的时间。有效延迟值将是此选项值与对等端设置的 `peerlatency` 值中的最大者。在 1.3.0 版本之前，此选项仅以 `latency` 形式提供。

- **`recv_buffer_size=bytes`** 设置 UDP 接收缓冲区大小，以字节表示。

- **`send_buffer_size=bytes`** 设置 UDP 发送缓冲区大小，以字节表示。

- **`timeout=microseconds`** 设置读、写和连接操作引发错误的超时。请注意，SRT 库具有可单独控制的内部超时，此处设置的值只是这些内部超时的上限。

- **`tlpktdrop=1|0`** 过迟数据包丢弃 (Too-late Packet Drop)。在接收方启用时，它会跳过未能及时交付的缺失数据包，并在后续数据包的播放时间到达时将其交付给应用程序。它还会向发送方发送虚假 ACK。在发送方及其接收对等端都启用时，发送方会丢弃已无机会按时交付的较旧数据包。如果接收方支持，它会在发送方自动启用。

- **`sndbuf=bytes`** 设置发送缓冲区大小，以字节表示。

- **`rcvbuf=bytes`** 设置接收缓冲区大小，以字节表示。

  接收缓冲区不得大于 `ffs`。

- **`lossmaxttl=packets`** 重排序容忍度 (Reorder Tolerance) 可以增长到的值。当重排序容忍度 \> 0 时，丢包报告将延迟到该数量的数据包到达为止。每当一个"迟到"的数据包到达且并非由重传所致（即 UDP 数据包往往乱序到达的情况）时，重排序容忍度都会以最新序列号与此数据包序列号之差增加，但不超过此选项的值。默认值为 0，表示此机制关闭，遇到序列"间隙"时总是立即发送丢包报告。

- **`minversion`** 对等端所需的最低 SRT 版本。与不满足最低版本要求的对等端的连接将被拒绝。

  十六进制版本格式为 0xXXYYZZ，对应人类可读形式 x.y.z。

- **`streamid=string`** 一个限制为 512 个字符的字符串，可以在连接之前在套接字上设置。监听方将能够从 srt_accept 返回的套接字中检索此流 ID，该套接字由设置了此流 ID 的套接字连接。SRT 不强制对此字符串的内容做任何特殊解释。此选项在 Rendezvous 连接中没有意义；结果可能只是一方覆盖另一方的值，至于哪一方获胜则纯属运气。

- **`srt_streamid=string`** `streamid` 的别名，用于避免与 ffmpeg 命令行选项冲突。

- **`smoother=live|file`** 用于该套接字传输的 Smoother 类型，负责传输和拥塞控制。连接双方的 Smoother 类型必须完全相同，否则连接将被拒绝。

- **`messageapi=1|0`** 设置后，此套接字使用消息 API (Message API)，否则使用缓冲 API (Buffer API)。请注意，在 live 模式（参见 `transtype`）下只有消息 API 可用。在文件模式下，可以选择以下两种模式之一：

  流 API（默认，此选项为 false 时）。在此模式下，您可以在一次发送指令中发送任意多的数据，甚至可以使用直接从文件读取的专用函数。内部机制将处理速度和拥塞控制。接收时，您也可以按需接收任意多的数据，未提取的数据将等待下一次调用。流模式下数据部分之间没有边界。

  消息 API。在此模式下，您的单次发送指令恰好传递一条有边界（一个消息）的数据。与 Live 模式相反，此消息可以跨越多个 UDP 数据包，唯一的大小限制是它必须整体适合发送缓冲区。接收方应使用足够大的缓冲区来接收消息，否则消息不会被放弃。当消息不完整（未收到所有数据包或有数据包丢失）时，它不会被放弃。

- **`transtype=live|file`** 设置套接字的传输类型；特别是，设置此选项会将多个其他参数设置为特定传输类型所需的默认值。

  live：按直播传输设置选项。在此模式下，单次发送指令只应发送适合一个 UDP 数据包的数据，并受 `payload_size` 首先定义的值限制（此模式下默认为 1316）。此模式下没有速度控制，只有带宽控制（如果已配置），以免传输开销（重传和控制数据包）超出带宽。

  file：按非直播传输设置选项。进一步说明参见 `messageapi`。

- **`linger=seconds`** 关闭时套接字等待未发送数据的秒数。默认值为 -1。-1 表示自动（live 模式下关闭，为 0 秒；文件模式下开启，为 180 秒）。此选项的范围为 0 - `INT_MAX` 内的整数。

- **`tsbpd=1|0`** 若为 true，则使用基于时间戳的数据包交付 (Timestamp-based Packet Delivery) 模式。默认行为取决于传输类型：live 模式下启用，文件模式下禁用。

- **`ipv6only=1|0`** 使用 IPv6 通配地址时是否接受 IPv4。在 IPv6 通配地址上监听时应设置此项。

更多信息参见：<https://github.com/Haivision/srt>。

## srtp

安全实时传输协议 (Secure Real-time Transport Protocol)。

可接受的选项有：

- **`srtp_in_suite`**

- **`srtp_out_suite`** 选择输入和输出加密套件。

  支持的值：

  - **`AES_CM_128_HMAC_SHA1_80`**

  - **`SRTP_AES128_CM_HMAC_SHA1_80`**

  - **`AES_CM_128_HMAC_SHA1_32`**

  - **`SRTP_AES128_CM_HMAC_SHA1_32`**

- **`srtp_in_params`**

- **`srtp_out_params`** 设置输入和输出加密参数，以二进制块的 base64 编码表示形式表达。该二进制块的前 16 字节用作主密钥 (master key)，随后的 14 字节用作主盐值 (master salt)。

## subfile

从文件或另一个流中虚拟提取一段。底层流必须可定位。

可接受的选项：

- **`start`** 所提取段的起始偏移量，以字节为单位。

- **`end`** 所提取段的结束偏移量，以字节为单位。若设为 0，则提取到文件末尾。

示例：

从 DVD VOB 文件中提取一个章节（起始和结束扇区从外部获取并乘以 2048）：

``` text
subfile,,start,153391104,end,268142592,,:/media/dvd/VIDEO_TS/VTS_08_1.VOB
```

直接从 TAR 归档播放 AVI 文件：

``` text
subfile,,start,183241728,end,366490624,,:archive.tar
```

从起始偏移量播放 MPEG-TS 文件直至结尾：

``` text
subfile,,start,32815239,end,0,,:video.ts
```

## tee

将输出写入多个协议。各个输出以 \| 分隔

``` text
tee:file://path/to/local/this.avi|file://path/to/local/that.avi
```

## tcp

传输控制协议 (Transmission Control Protocol)。

TCP url 的必需语法为：

``` text
tcp://hostname:port[?options]
```

\<options\> 包含一个以 & 分隔的选项列表，选项形如 \<key\>=\<val\>。可使用标准百分号编码（以及用加号表示空格）来转义键和值。

选项也可以通过命令行选项指定（或在代码中通过 `AVOption` 指定）。

支持的选项列表如下。

- **`listen=2|1|0`** 监听传入连接。0 禁用监听，1 启用单客户端模式监听，2 启用多客户端模式监听。默认值为 0。

- **`local_addr=addr`** 用于 tcp 套接字连接的网络接口的本地 IP 地址。

- **`local_port=port`** 用于 tcp 套接字连接的本地端口。

- **`timeout=microseconds`** 设置引发错误的超时，以微秒表示。

  此选项仅在读取模式下相关：如果在此时间间隔内没有数据到达，则引发错误。

- **`listen_timeout=milliseconds`** 设置监听超时，以毫秒表示。

- **`recv_buffer_size=bytes`** 设置接收缓冲区大小，以字节表示。

- **`send_buffer_size=bytes`** 设置发送缓冲区大小，以字节表示。

- **`tcp_nodelay=1|0`** 设置 TCP_NODELAY 以禁用 Nagle 算法。默认值为 0。

  *注：目前对套接字的写入未针对最小化系统调用进行优化，这会降低 TCP_NODELAY 的效率/效果。*

- **`tcp_mss=bytes`** 设置传出 TCP 数据包的最大分段大小，以字节表示。

以下示例展示如何用 `ffmpeg` 建立监听中的 TCP 连接，然后用 `ffplay` 访问它：

``` text
ffmpeg -i input -f format tcp://hostname:port?listen
ffplay tcp://hostname:port
```

## tls

传输层安全 (Transport Layer Security, TLS) / 安全套接字层 (Secure Sockets Layer, SSL)

TLS/SSL url 的必需语法为：

``` text
tls://hostname:port[?options]
```

\<options\> 包含一个以 & 分隔的选项列表，选项形如 \<key\>=\<val\>。可使用标准百分号编码（以及用加号表示空格）来转义键和值。

选项也可以通过命令行选项指定（或在代码中通过 `AVOption` 指定）。

支持的选项列表如下。

- **`ca_file, cafile=filename`** 包含视为受信任的证书颁发机构 (CA) 根证书的文件。如果所链接的 TLS 库包含默认值，则验证可能无需指定此项，但并非所有库和设置都内建了默认值。该文件必须为 OpenSSL PEM 格式。

- **`tls_verify, verify=1|0`** 如果启用，尝试验证我们正在与之通信的对等端。注意，如果使用 OpenSSL，目前这只确保对等端证书由 CA 数据库中的根证书之一签名，但不会验证该证书是否确实与我们尝试连接的主机名匹配。（使用其他后端时，主机名也会被验证。）

  默认启用此项。验证对等端需要 CA 数据库，某些情况下必须由调用方提供。

- **`cert_file, cert=filename`** 包含要在与对等端握手时使用的证书的文件。（作为服务器在监听模式下运行时，对等端通常更常要求此项，而客户端证书只在某些设置下才强制要求。）

- **`key_file, key=filename`** 包含证书私钥的文件。

- **`listen=1|0`** 如果启用，在提供的端口上监听连接，并在握手中假定服务器角色而不是客户端角色。

- **`http_proxy`** 要穿隧道使用的 HTTP 代理，例如 `http://example.com:1234`。该代理必须支持 CONNECT 方法。

示例命令行：

创建一个提供输入流服务的 TLS/SSL 服务器。

``` text
ffmpeg -i input -f format tls://hostname:port?listen&cert=server.crt&key=server.key
```

使用 `ffplay` 从 TLS/SSL 服务器播放流：

``` text
ffplay tls://hostname:port
```

## dtls

数据报传输层安全 (Datagram Transport Layer Security, DTLS)

DTLS URL 的必需语法为：

``` text
dtls://hostname:port[?options]
```

\<options\> 包含一个以 & 分隔的选项列表，选项形如 \<key\>=\<val\>。可使用标准百分号编码（以及用加号表示空格）来转义键和值。

选项也可以通过命令行选项指定（或在代码中通过 `AVOption` 指定）。

DTLS 与 TLS 共享大多数选项，但通过 UDP 而不是 TCP 运行。

支持的选项列表如下。

- **`ca_file, cafile=filename`** 包含视为受信任的证书颁发机构 (CA) 根证书的文件。如果所链接的 TLS 库包含默认值，则验证可能无需指定此项，但并非所有库和设置都内建了默认值。该文件必须为 OpenSSL PEM 格式。

- **`tls_verify, verify=1|0`** 如果启用，尝试验证我们正在与之通信的对等端。注意，如果使用 OpenSSL，目前这只确保对等端证书由 CA 数据库中的根证书之一签名，但不会验证该证书是否确实与我们尝试连接的主机名匹配。

  默认启用此项。验证对等端需要 CA 数据库，某些情况下必须由调用方提供。

- **`cert_file, cert=filename`** 包含要在与对等端握手时使用的证书的文件。（作为服务器在监听模式下运行时，对等端通常更常要求此项，而客户端证书只在某些设置下才强制要求。）

- **`key_file, key=filename`** 包含证书私钥的文件。

- **`cert_pem=string`** 证书 PEM 字符串

- **`key_pem=string`** 私钥 PEM 字符串

- **`listen=1|0`** 如果启用，在提供的端口上监听连接，并在握手中假定服务器角色而不是客户端角色。

- **`mtu=size`** 设置 DTLS 数据包的最大传输单元 (MTU)。

- **`use_srtp=1|0`** 启用 use_srtp DTLS 扩展。这在 WebRTC 应用程序中用于通过 DTLS 握手建立 SRTP 加密密钥。默认禁用。

- **`external_sock=1|0`** 使用外部套接字而不是创建新的套接字。仅在与代码通过 API 交互时传递此选项才有意义，从 CLI 启用将导致立即失败。默认禁用。

示例命令行：

创建一个 DTLS 服务器：

``` text
ffmpeg -listen 1 -i dtls://hostname:port output
```

创建一个 DTLS 客户端并向服务器发送数据：

``` text
ffmpeg -i input -f format dtls://hostname:port
```

## udp

用户数据报协议 (User Datagram Protocol)。

UDP URL 的必需语法为：

``` text
udp://hostname:port[?options]
```

\<options\> 包含一个以 & 分隔的选项列表，选项形如 \<key\>=\<val\>。可使用标准百分号编码（以及用加号表示空格）来转义键和值。

选项也可以通过命令行选项指定（或在代码中通过 `AVOption` 指定）。

在系统上启用线程的情况下，将使用循环缓冲区存储传入数据，这可以减少因 UDP 套接字缓冲区溢出导致的数据丢失。\<fifo_size\> 和 \<overrun_nonfatal\> 选项与此缓冲区相关。

支持的选项列表如下。

- **`buffer_size=size`** 设置 UDP 最大套接字缓冲区大小（字节）。这用于设置接收或发送缓冲区大小，具体取决于套接字的用途。输出默认为 32 KB，输入默认为 384 KB。另请参见 \<fifo_size\>。

- **`bitrate=bitrate`** 若设为非零值，且输入有足够的数据包来维持，则输出将具有指定的恒定码率。

- **`burst_bits=bits`** 使用 \<bitrate\> 时，此选项指定数据包突发中的最大位数。

- **`localport=port`** 覆盖要绑定的本地 UDP 端口。

- **`localaddr=addr`** 用于发送数据包或加入组播组的网络接口的本地 IP 地址。

- **`pkt_size=size`** 设置 UDP 数据包的大小（字节）。

- **`reuse=1|0`** 显式允许或禁止重用 UDP 套接字。

- **`ttl=ttl`** 设置生存时间 (time to live) 值（仅限组播）。

- **`dscp=dscp`** 为传出数据包设置 6 位 DSCP 字段。

- **`connect=1|0`** 用 `connect()` 初始化 UDP 套接字。在这种情况下，之后无法使用 ff_udp_set_remote_url 更改目标地址。如果开始时不知道目标地址，也可以在 ff_udp_set_remote_url 中指定此选项。这允许通过 getsockname 获取数据包的源地址，并且在收到"目标不可达"时使写入返回 AVERROR(ECONNREFUSED)。对于接收，这带来仅接收来自指定对等端地址/端口的数据包的好处。

- **`sources=address[,address]`** 仅接收从指定地址发送的数据包。对于组播，也仅订阅来自这些地址的组播流量。

- **`block=address[,address]`** 忽略从指定地址发送的数据包。对于组播，也在组播订阅中排除这些源地址。

- **`fifo_size=units`** 设置 UDP 接收循环缓冲区的大小，表示为大小为 188 字节的数据包数量。若未指定，默认为 7\*4096。

- **`overrun_nonfatal=1|0`** 在 UDP 接收循环缓冲区溢出时继续存活。默认值为 0。

- **`timeout=microseconds`** 设置引发错误的超时，以微秒表示。

  此选项仅在读取模式下相关：如果在此时间间隔内没有数据到达，则引发错误。

- **`broadcast=1|0`** 显式允许或禁止 UDP 广播。

  请注意，在具有广播风暴防护的网络上，广播可能无法正常工作。

### 示例

- 使用 `ffmpeg` 通过 UDP 向远端端点推流：

  ``` text
  ffmpeg -i input -f format udp://hostname:port
  ```

- 使用 `ffmpeg` 通过 UDP 以 mpegts 格式推流，使用 188 字节大小的 UDP 数据包，并使用较大的输入缓冲区：

  ``` text
  ffmpeg -i input -f mpegts udp://hostname:port?pkt_size=188&buffer_size=65535
  ```

- 使用 `ffmpeg` 从远端端点通过 UDP 接收：

  ``` text
  ffmpeg -i udp://[multicast-address]:port ...
  ```

## unix

Unix 本地套接字

Unix 套接字 URL 的必需语法为：

``` text
unix://filepath
```

以下参数可以通过命令行选项设置（或在代码中通过 `AVOption` 设置）：

- **`timeout`** 超时（毫秒）。

- **`listen`** 以监听模式创建 Unix 套接字。

- **`type`** 选择套接字类型。

  - **`stream Corresponds to SOCK_STREAM (reliable stream-oriented)`**

  - **`datagram Corresponds to SOCK_DGRAM (unreliable packet-oriented)`**

  - **`seqpacket Corresponds to SOCK_SEQPACKET (reliable packet-oriented)`**

- **`pkt_size`** 面向数据包的套接字 (SOCK_DGRAM 和 SOCK_SEQPACKET) 的最大数据包大小。若大于零，此值将用作 `max_packet_size`。对 SOCK_STREAM 忽略。默认值为 `0`。

## zmq

使用 libzmq 库的 ZeroMQ 异步消息传递。

此库支持不依赖外部服务器向多个客户端进行单播推流。

推流或连接到流的必需语法为：

``` text
zmq:tcp://ip-address:port
```

示例：在端口 5555 上创建 localhost 流：

``` text
ffmpeg -re -i input -f mpegts zmq:tcp://127.0.0.1:5555
```

多个客户端可以使用以下命令连接到该流：

``` text
ffplay zmq:tcp://127.0.0.1:5555
```

向多个客户端推流通过 ZeroMQ 发布-订阅 (Pub-Sub) 模式实现。服务器端绑定到一个端口并发布数据。客户端连接到服务器（通过 IP 地址/端口）并订阅该流。服务器和客户端启动的先后顺序通常无关紧要。

ffmpeg 必须以 –enable-libzmq 选项编译才能支持此协议。

选项可以在 `ffmpeg`/`ffplay` 命令行上设置。支持以下选项：

- **`pkt_size`** 强制发送/接收数据的最大数据包大小。默认值为 131,072 字节。在服务器端，它设置通过 ZeroMQ 发送的数据包的最大大小。在客户端，它设置接收数据包的内部缓冲区大小。注意，客户端上的 pkt_size 应当等于或大于服务器上的 pkt_size，否则接收到的消息可能被截断从而导致解码错误。

# 另请参见

ffmpeg(1), ffplay(1), ffprobe(1), libavformat(3)
