## Overview

On start, mana9er creates an instance of class `Core` and starts the Minecraft server according to configuration as  a subprocess. After that, the plugins are loaded in the order they appear in the plugin list in the configuration.

To know what's happening in the Minecraft server, an event-driven interface is provided to the plugins in the signal-slot mechanism of PyQt. Plugins can connect the signals provided by the core or `mcBasicLib` to their slot functions. For example, the core provides a signal `sig_server_output` to carry the output of the Minecraft server, and `mcBasicLib` provides a signal `sig_login` representing the event that a player enters the game. There is also a signal `sig_command` in the core representing user input on the server command line.

To send commands to the Minecraft server, use `write_server` method of the core to write text to the standard input of the Minecraft server, or use methods like `stop_server` and `start_server`.

## Plugin and Logger

A plugin is a folder named by the plugin name. When used, it should be put under the location where mana9er-core is and added to the plugin list in the configuration file. Under the plugin folder, there should be a `__init__.py`, in which there is a `load` function. It is called by the core when it loads the plugins in the form `load(log, core)`, where `log` is  a logger introduced later, and `core` is the instance of class `Core` that the plugin interacts with. You need to do the initialization work when `load` is called, like loading configuration, creating instance for  you class, and connecting signals to your slots.

The return value of the `load` call is stored by the core, and can be retrieved by `get_plugin`. If your plugin is not the dependency of some other plugin, you can just return `None`.

The class `Logger` provides a unified way to print logs. It has several methods like `info` and `warning` and decides whether to output logs for each log level according its log level setting. In the initialization, the core creates a logger for each plugin and passes it to the plugin when loading it. These loggers will add sender information (the name of corresponding plugin) and time stamp when printing logs.