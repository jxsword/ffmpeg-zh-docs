# Synopsis

ffprobe \[\<options\>\] `input_url`

# Description

ffprobe gathers information from multimedia streams and prints it in human- and machine-readable fashion.

For example it can be used to check the format of the container used by a multimedia stream and the format and type of each media stream contained in it.

If a url is specified in input, ffprobe will try to open and probe the url content. If the url cannot be opened or recognized as a multimedia file, a positive exit code is returned.

If no output is specified as output with `o` ffprobe will write to stdout.

ffprobe may be employed both as a standalone application or in combination with a textual filter, which may perform more sophisticated processing, e.g. statistical processing or plotting.

Options are used to list some of the formats supported by ffprobe or for specifying which information to display, and for setting how ffprobe will show it.

ffprobe output is designed to be easily parsable by a textual filter, and consists of one or more sections of a form defined by the selected writer, which is specified by the `output_format` option.

Sections may contain other nested sections, and are identified by a name (which may be shared by other sections), and an unique name. See the output of `sections`.

Metadata tags stored in the container or in the streams are recognized and printed in the corresponding "FORMAT", "STREAM", "STREAM_GROUP_STREAM" or "PROGRAM_STREAM" section.

# Options

## Main options

- **`-f format`** Force format to use.

- **`-unit`** Show the unit of the displayed values.

- **`-prefix`** Use SI prefixes for the displayed values. Unless the "-byte_binary_prefix" option is used all the prefixes are decimal.

- **`-byte_binary_prefix`** Force the use of binary prefixes for byte values.

- **`-sexagesimal`** Use sexagesimal format HH:MM:SS.MICROSECONDS for time values.

- **`-pretty`** Prettify the format of the displayed values, it corresponds to the options "-unit -prefix -byte_binary_prefix -sexagesimal".

- **`-output_format, -of, -print_format writer_name[=writer_options]`** Set the output printing format.

  \<writer_name\> specifies the name of the writer, and \<writer_options\> specifies the options to be passed to the writer.

  For example for printing the output in JSON format, specify:

  ``` text
  -output_format json
  ```

  For more details on the available output printing formats, see the Writers section below.

- **`-sections`** Print sections structure and section information, and exit. The output is not meant to be parsed by a machine.

- **`-select_streams stream_specifier`** Select only the streams specified by \<stream_specifier\>. This option affects only the options related to streams (e.g. `show_streams`, `show_packets`, etc.).

  For example to show only audio streams, you can use the command:

  ``` text
  ffprobe -show_streams -select_streams a INPUT
  ```

  To show only video packets belonging to the video stream with index 1:

  ``` text
  ffprobe -show_packets -select_streams v:1 INPUT
  ```

- **`-show_data`** Show payload data, as a hexadecimal and ASCII dump (other formats can be selected using `-data_dump_format`). Coupled with `-show_packets`, it will dump the packets' data. Coupled with `-show_streams`, it will dump the codec extradata.

  The dump is printed as the "data" field. It may contain newlines.

- **`-show_data_hash algorithm`** Show a hash of payload data, for packets with `-show_packets` and for codec extradata with `-show_streams`.

- **`-data_dump_format format`** Select a format used for the data dumps enabled with the `-show_data` option. The default is `xxd` which is a hexdump format compatible with the well-known `xxd` program. `base64` is also supported.

- **`-show_error`** Show information about the error found when trying to probe the input.

  The error information is printed within a section with name "ERROR".

- **`-show_format`** Show information about the container format of the input multimedia stream.

  All the container format information is printed within a section with name "FORMAT".

- **`-show_entries section_entries`** Set list of entries to show.

  Entries are specified according to the following syntax. \<section_entries\> contains a list of section entries separated by `:`. Each section entry is composed by a section name (or unique name), optionally followed by a list of entries local to that section, separated by `,`.

  If section name is specified but is followed by no `=`, all entries are printed to output, together with all the contained sections. Otherwise only the entries specified in the local section entries list are printed. In particular, if `=` is specified but the list of local entries is empty, then no entries will be shown for that section.

  Note that the order of specification of the local section entries is not honored in the output, and the usual display order will be retained.

  The formal syntax is given by:

  ``` text
  LOCAL_SECTION_ENTRIES ::= SECTION_ENTRY_NAME[,LOCAL_SECTION_ENTRIES]
  SECTION_ENTRY         ::= SECTION_NAME[=[LOCAL_SECTION_ENTRIES]]
  SECTION_ENTRIES       ::= SECTION_ENTRY[:SECTION_ENTRIES]
  ```

  For example, to show only the index and type of each stream, and the PTS time, duration time, and stream index of the packets, you can specify the argument:

  ``` text
  packet=pts_time,duration_time,stream_index : stream=index,codec_type
  ```

  To show all the entries in the section "format", but only the codec type in the section "stream", specify the argument:

  ``` text
  format : stream=codec_type
  ```

  To show all the tags in the stream and format sections:

  ``` text
  stream_tags : format_tags
  ```

  To show only the `title` tag (if available) in the stream sections:

  ``` text
  stream_tags=title
  ```

- **`-show_packets`** Show information about each packet contained in the input multimedia stream.

  The information for each single packet is printed within a dedicated section with name "PACKET".

- **`-show_frames`** Show information about each frame and subtitle contained in the input multimedia stream.

  The information for each single frame is printed within a dedicated section with name "FRAME" or "SUBTITLE".

- **`-show_log loglevel`** Show logging information from the decoder about each frame according to the value set in \<loglevel\>, (see `-loglevel`). This option requires `-show_frames`.

  The information for each log message is printed within a dedicated section with name "LOG".

- **`-show_streams`** Show information about each media stream contained in the input multimedia stream.

  Each media stream information is printed within a dedicated section with name "STREAM".

- **`-show_programs`** Show information about programs and their streams contained in the input multimedia stream.

  Each media stream information is printed within a dedicated section with name "PROGRAM_STREAM".

- **`-show_stream_groups`** Show information about stream groups and their streams contained in the input multimedia stream.

  Each media stream information is printed within a dedicated section with name "STREAM_GROUP_STREAM".

- **`-show_chapters`** Show information about chapters stored in the format.

  Each chapter is printed within a dedicated section with name "CHAPTER".

- **`-count_frames`** Count the number of frames per stream and report it in the corresponding stream section.

- **`-count_packets`** Count the number of packets per stream and report it in the corresponding stream section.

- **`-read_intervals read_intervals`** Read only the specified intervals. \<read_intervals\> must be a sequence of interval specifications separated by ",". `ffprobe` will seek to the interval starting point, and will continue reading from that.

  Each interval is specified by two optional parts, separated by "%".

  The first part specifies the interval start position. It is interpreted as an absolute position, or as a relative offset from the current position if it is preceded by the "+" character. If this first part is not specified, no seeking will be performed when reading this interval.

  The second part specifies the interval end position. It is interpreted as an absolute position, or as a relative offset from the current position if it is preceded by the "+" character. If the offset specification starts with "#", it is interpreted as the number of packets to read (not including the flushing packets) from the interval start. If no second part is specified, the program will read until the end of the input.

  Note that seeking is not accurate, thus the actual interval start point may be different from the specified position. Also, when an interval duration is specified, the absolute end time will be computed by adding the duration to the interval start point found by seeking the file, rather than to the specified start value.

  The formal syntax is given by:

  ``` text
  INTERVAL  ::= [START|+START_OFFSET][%[END|+END_OFFSET]]
  INTERVALS ::= INTERVAL[,INTERVALS]
  ```

  A few examples follow.

  - Seek to time 10, read packets until 20 seconds after the found seek point, then seek to position `01:30` (1 minute and thirty seconds) and read packets until position `01:45`.

    ``` text
    10%+20,01:30%01:45
    ```

  - Read only 42 packets after seeking to position `01:23`:

    ``` text
    01:23%+#42
    ```

  - Read only the first 20 seconds from the start:

    ``` text
    %+20
    ```

  - Read from the start until position `02:30`:

    ``` text
    %02:30
    ```

- **`-show_private_data, -private`** Show private data, that is data depending on the format of the particular shown element. This option is enabled by default, but you may need to disable it for specific uses, for example when creating XSD-compliant XML output.

- **`-show_program_version`** Show information related to program version.

  Version information is printed within a section with name "PROGRAM_VERSION".

- **`-show_library_versions`** Show information related to library versions.

  Version information for each library is printed within a section with name "LIBRARY_VERSION".

- **`-show_versions`** Show information related to program and library versions. This is the equivalent of setting both `-show_program_version` and `-show_library_versions` options.

- **`-show_pixel_formats`** Show information about all pixel formats supported by FFmpeg.

  Pixel format information for each format is printed within a section with name "PIXEL_FORMAT".

- **`-show_optional_fields value`** Some writers viz. JSON and XML, omit the printing of fields with invalid or non-applicable values, while other writers always print them. This option enables one to control this behaviour. Valid values are `always`/`1`, `never`/`0` and `auto`/`-1`. Default is \<auto\>.

- **`-analyze_frames`** Analyze frames and/or their side data up to the provided read interval, providing additional information that may be useful at a stream level. Must be paired with the `-show_streams` option or it will have no effect.

  Currently, the additional fields provided by this option when enabled are the `closed_captions` and `film_grain` fields.

  For example, to analyze the first 20 seconds and populate these fields:

  ``` text
  ffprobe -show_streams -analyze_frames -read_intervals "%+20" INPUT
  ```

- **`-bitexact`** Force bitexact output, useful to produce output which is not dependent on the specific build.

- **`-i input_url`** Read \<input_url\>.

- **`-o output_url`** Write output to \<output_url\>. If not specified, the output is sent to stdout.

- **`-c:media_specifier codec_name`** Force a specific decoder implementation for the stream identified by \<media_specifier\>, which can assume the values `a` (audio), `v` (video), `s` (subtitle), and `d` (data).

# Writers

A writer defines the output format adopted by `ffprobe`, and will be used for printing all the parts of the output.

A writer may accept one or more arguments, which specify the options to adopt. The options are specified as a list of \<key\>=\<value\> pairs, separated by ":".

All writers support the following options:

- **`string_validation, sv`** Set string validation mode.

  The following values are accepted.

  - **`fail`** The writer will fail immediately in case an invalid string (UTF-8) sequence or code point is found in the input. This is especially useful to validate input metadata.

  - **`ignore`** Any validation error will be ignored. This will result in possibly broken output, especially with the json or xml writer.

  - **`replace`** The writer will substitute invalid UTF-8 sequences or code points with the string specified with the `string_validation_replacement`.

  Default value is `replace`.

- **`string_validation_replacement, svr`** Set replacement string to use in case `string_validation` is set to `replace`.

  In case the option is not specified, the writer will assume the empty string, that is it will remove the invalid sequences from the input strings.

A description of the currently available writers follows.

## default

Default format.

Print each section in the form:

``` text
[SECTION]
key1=val1
...
keyN=valN
[/SECTION]
```

Metadata tags are printed as a line in the corresponding FORMAT, STREAM, STREAM_GROUP_STREAM or PROGRAM_STREAM section, and are prefixed by the string "TAG:".

A description of the accepted options follows.

- **`nokey, nk`** If set to 1 specify not to print the key of each field. Default value is 0.

- **`noprint_wrappers, nw`** If set to 1 specify not to print the section header and footer. Default value is 0.

## compact, csv

Compact and CSV format.

The `csv` writer is equivalent to `compact`, but supports different defaults.

Each section is printed on a single line. If no option is specified, the output has the form:

``` text
section|key1=val1| ... |keyN=valN
```

Metadata tags are printed in the corresponding "format" or "stream" section. A metadata tag key, if printed, is prefixed by the string "tag:".

The description of the accepted options follows.

- **`item_sep, s`** Specify the character to use for separating fields in the output line. It must be a single printable character, it is "\|" by default ("," for the `csv` writer).

- **`nokey, nk`** If set to 1 specify not to print the key of each field. Its default value is 0 (1 for the `csv` writer).

- **`escape, e`** Set the escape mode to use, default to "c" ("csv" for the `csv` writer).

  It can assume one of the following values:

  - **`c`** Perform C-like escaping. Strings containing a newline (`\n`), carriage return (`\r`), a tab (`\t`), a form feed (`\f`), the escaping character (`\`) or the item separator character \<SEP\> are escaped using C-like fashioned escaping, so that a newline is converted to the sequence `\n`, a carriage return to `\r`, `\` to `\\` and the separator \<SEP\> is converted to `\SEP`.

  - **`csv`** Perform CSV-like escaping, as described in RFC4180. Strings containing a newline (`\n`), a carriage return (`\r`), a double quote (`"`), or \<SEP\> are enclosed in double-quotes.

  - **`none`** Perform no escaping.

- **`print_section, p`** Print the section name at the beginning of each line if the value is `1`, disable it with value set to `0`. Default value is `1`.

## flat

Flat format.

A free-form output where each line contains an explicit key=value, such as "streams.stream.3.tags.foo=bar". The output is shell escaped, so it can be directly embedded in sh scripts as long as the separator character is an alphanumeric character or an underscore (see \<sep_char\> option).

The description of the accepted options follows.

- **`sep_char, s`** Separator character used to separate the chapter, the section name, IDs and potential tags in the printed field key.

  Default value is `.`.

- **`hierarchical, h`** Specify if the section name specification should be hierarchical. If set to 1, and if there is more than one section in the current chapter, the section name will be prefixed by the name of the chapter. A value of 0 will disable this behavior.

  Default value is 1.

## ini

INI format output.

Print output in an INI based format.

The following conventions are adopted:

- all key and values are UTF-8

- `.` is the subgroup separator

- newline, `\t`, `\f`, `\b` and the following characters are escaped

- `\` is the escape character

- `#` is the comment indicator

- `=` is the key/value separator

- `:` is not used but usually parsed as key/value separator

This writer accepts options as a list of \<key\>=\<value\> pairs, separated by `:`.

The description of the accepted options follows.

- **`hierarchical, h`** Specify if the section name specification should be hierarchical. If set to 1, and if there is more than one section in the current chapter, the section name will be prefixed by the name of the chapter. A value of 0 will disable this behavior.

  Default value is 1.

## json

JSON based format.

Each section is printed using JSON notation.

The description of the accepted options follows.

- **`compact, c`** If set to 1 enable compact output, that is each section will be printed on a single line. Default value is 0.

For more information about JSON, see <http://www.json.org/>.

## xml

XML based format.

The XML output is described in the XML schema description file `ffprobe.xsd` installed in the FFmpeg datadir.

An updated version of the schema can be retrieved at the url <http://www.ffmpeg.org/schema/ffprobe.xsd>, which redirects to the latest schema committed into the FFmpeg development source code tree.

Note that the output issued will be compliant to the `ffprobe.xsd` schema only when no special global output options (`unit`, `prefix`, `byte_binary_prefix`, `sexagesimal` etc.) are specified.

The description of the accepted options follows.

- **`fully_qualified, q`** If set to 1 specify if the output should be fully qualified. Default value is 0. This is required for generating an XML file which can be validated through an XSD file.

- **`xsd_strict, x`** If set to 1 perform more checks for ensuring that the output is XSD compliant. Default value is 0. This option automatically sets `fully_qualified` to 1.

For more information about the XML format, see <https://www.w3.org/XML/>.

# Timecode

`ffprobe` supports Timecode extraction:

- MPEG1/2 timecode is extracted from the GOP, and is available in the video stream details (`-show_streams`, see \<timecode\>).

- MOV timecode is extracted from tmcd track, so is available in the tmcd stream metadata (`-show_streams`, see \<TAG:timecode\>).

- DV, GXF and AVI timecodes are available in format metadata (`-show_format`, see \<TAG:timecode\>).

# See Also

ffmpeg(1), ffplay(1), ffmpeg-utils(1), ffmpeg-scaler(1), ffmpeg-resampler(1), ffmpeg-codecs(1), ffmpeg-bitstream-filters(1), ffmpeg-formats(1), ffmpeg-devices(1), ffmpeg-protocols(1), ffmpeg-filters(1)
