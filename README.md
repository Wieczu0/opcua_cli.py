# opcua_cli.py
This is a program to read, write or subscribe to data on opc server
Run opcclient.exe in the build/exe.win-amd64-3.10 folder using CLI


First positional argument is opc server UATCP address and it is required. App won't work without server connection.


Next arguments are different use applications

-h, --help:                      Shows help message
-n, --nodeid NODEID [NODEID ...]:Read values from specified nodes and prints it to CLI. 
                                In windows case you have to use '' but CMD doesn't need them. Examples: for PS: 'ns=3;i=1002'; for cmd: ns=3;i=1002.
                                 You can also input more than one NodeID. Example for PS: 
-l, --loop                      :Makes your program read and print Nodes values in loop.
-f, --file FILE                 :Load NodeIDs form txt file. Example txt file named txt.txt in the main folder
-s, --send SEND VALUE           :Sends value to an object. First NodeID then value. Example: 'ns=3;i=1002' 69
-S, --sub SUB                   :Subscribes to a node. Server sends value to the cli every time the value on the node changes.
                                 Using subscription you don't have to ask server in loop for a value of the node, decreasing traffic.


