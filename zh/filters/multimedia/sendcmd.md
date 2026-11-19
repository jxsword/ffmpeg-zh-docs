# sendcmd, asendcmd

Send commands to filters in the filtergraph.

These filters read commands to be sent to other filters in the filtergraph.

`sendcmd` must be inserted between two video filters, `asendcmd` must be inserted between two audio filters, but apart from that they act the same way.

The specification of commands can be provided in the filter arguments with the \<commands\> option, or in a file specified by the \<filename\> option.

These filters accept the following options:

| Term | Description |
|----|----|
| `commands, c` | Set the commands to be read and sent to the other filters. |
| `filename, f` | Set the filename of the commands to be read and sent to the other filters. |

## Commands syntax

A commands description consists of a sequence of interval specifications, comprising a list of commands to be executed when a particular event related to that interval occurs. The occurring event is typically the current frame time entering or leaving a given time interval.

An interval is specified by the following syntax:

``` text
START[-END] COMMANDS;
```

The time interval is specified by the \<START\> and \<END\> times. \<END\> is optional and defaults to the maximum time.

The current frame time is considered within the specified interval if it is included in the interval \[\<START\>, \<END\>), that is when the time is greater or equal to \<START\> and is lesser than \<END\>.

\<COMMANDS\> consists of a sequence of one or more command specifications, separated by ",", relating to that interval. The syntax of a command specification is given by:

``` text
[FLAGS] TARGET COMMAND ARG
```

\<FLAGS\> is optional and specifies the type of events relating to the time interval which enable sending the specified command, and must be a non-null sequence of identifier flags separated by "+" or "\|" and enclosed between "\[" and "\]".

The following flags are recognized:

- **`enter`** The command is sent when the current frame timestamp enters the specified interval. In other words, the command is sent when the previous frame timestamp was not in the given interval, and the current is.

- **`leave`** The command is sent when the current frame timestamp leaves the specified interval. In other words, the command is sent when the previous frame timestamp was in the given interval, and the current is not.

- **`expr`** The command \<ARG\> is interpreted as expression and result of expression is passed as \<ARG\>.

  The expression is evaluated through the eval API and can contain the following constants:

  - **`POS`** Original position in the file of the frame, or undefined if undefined for the current frame. Deprecated, do not use.

  - **`PTS`** The presentation timestamp in input.

  - **`N`** The count of the input frame for video or audio, starting from 0.

  - **`T`** The time in seconds of the current frame.

  - **`TS`** The start time in seconds of the current command interval.

  - **`TE`** The end time in seconds of the current command interval.

  - **`TI`** The interpolated time of the current command interval, TI = (T - TS) / (TE - TS).

  - **`W`** The video frame width.

  - **`H`** The video frame height.

If \<FLAGS\> is not specified, a default value of `[enter]` is assumed.

\<TARGET\> specifies the target of the command, usually the name of the filter class or a specific filter instance name.

\<COMMAND\> specifies the name of the command for the target filter.

\<ARG\> is optional and specifies the optional list of argument for the given \<COMMAND\>.

Between one interval specification and another, whitespaces, or sequences of characters starting with `#` until the end of line, are ignored and can be used to annotate comments.

A simplified BNF description of the commands specification syntax follows:

``` c
COMMAND_FLAG  ::= "enter" | "leave"
COMMAND_FLAGS ::= COMMAND_FLAG [(+|"|")COMMAND_FLAG]
COMMAND       ::= ["[" COMMAND_FLAGS "]"] TARGET COMMAND [ARG]
COMMANDS      ::= COMMAND [,COMMANDS]
INTERVAL      ::= START[-END] COMMANDS
INTERVALS     ::= INTERVAL[;INTERVALS]
```

## Examples

- Specify audio tempo change at second 4:

  ``` text
  asendcmd=c='4.0 atempo tempo 1.5',atempo
  ```

- Target a specific filter instance:

  ``` text
  asendcmd=c='4.0 atempo@my tempo 1.5',atempo@my
  ```

- Specify a list of drawtext and hue commands in a file.

  ``` c
  # show text in the interval 5-10
  5.0-10.0 [enter] drawtext reinit 'fontfile=FreeSerif.ttf:text=hello world',
           [leave] drawtext reinit 'fontfile=FreeSerif.ttf:text=';

  # desaturate the image in the interval 15-20
  15.0-20.0 [enter] hue s 0,
            [enter] drawtext reinit 'fontfile=FreeSerif.ttf:text=nocolor',
            [leave] hue s 1,
            [leave] drawtext reinit 'fontfile=FreeSerif.ttf:text=color';

  # apply an exponential saturation fade-out effect, starting from time 25
  25 [enter] hue s exp(25-t)
  ```

  A filtergraph allowing to read and process the above command list stored in a file `test.cmd`, can be specified with:

  ``` text
  sendcmd=f=test.cmd,drawtext=fontfile=FreeSerif.ttf:text='',hue
  ```
