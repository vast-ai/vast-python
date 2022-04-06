# Data Transfer System

## High Level Design

### Basic logic and control flow

We start with a new command in the CLI called 'copy'. The syntax is simple - `copy src dst` where
'src' and 'dest' are special types of URLs of the form "instance_no:path | path"
If only path is present the instance number is assumed to be that of the present instance.

This is implemented as an endpoint or endpoints in the CLI. Once a copy
directive is accepted, a set of commands is added to the command queue table
in the database to be sent out to the intended receiver and sender of the data.
Along with the commands would be any IP addresses and port addresses needed for
the transfer.



