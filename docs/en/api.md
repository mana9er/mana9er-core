## Class `Core`

+ Signal `sig_server_start`: The event that the subprocess of Minecraft server is started.
+ Signal `sig_server_stop`: The event that the subprocess of Minecraft server stops.
+ Signal `sig_server_output(lines)`: The event that the Minecraft server outputs some lines. `lines` is a list of strings, and each element is a line.
+ Signal `sig_command(cmd)`: The event that a command line command `cmd` is received.
+ Method `write_server(content)`: Write a string to the standard input of the server, with a `'\n'` appended.
+ Method `quit()`: If the server is running, stop it. And then quit mana9er.
+ Method `command(cmd)`: send a command to mana9er as if it is typed into the console.

## Class `Logger`

+ Method `error/warning/info/debug(message, time_stamp=True)`: Output a string `message` in corresponding log level. `time_stamp` indicates whether to add time stamp to the output.
+ Method `direct_output(message, ending='\n')`: Output a string `message + ending` as it is, without adding color, sender name, and time stamp.