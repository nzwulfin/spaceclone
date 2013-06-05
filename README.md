spaceclone
=========

Spaceclone is a software channel cloning tool for RHN Satellite and Spacewalk.

Spaceclones are copies of a base software channel and it's child channels.  

For example, one might create clones on a rolling time basis, which allows you to keep a group of systems easily at the same patch level.  When it's time to apply the next period's patches, spaceclone can move a system into another snapshot's software channels.

Configuration
-------------
The default configuration file is /etc/spaceclone.conf

### General
Specify the Spacewalk server's hostname, username, and password here.

## Usage

### Create a New Snapshot


    # spaceclone create -n "2013 July"

    Creating new 2013 May Snapshot...
    Creating base channel snapshot-2013-may-rhel-x86_64-server-6... [OK]
    Creating child channel snapshot-2013-may-rhel-x86_64-server-optional-6... [OK]
    Snapshot sucessfully created


You can also use custom names.  The label is all lowercase, joined by "-".

    # spaceclone create --name "2013 June Test"
    Creating new 2013 June Test Snapshot...
    Creating base channel snapshot-2013-june-test-rhel-x86_64-server-6... [OK]
    Creating child channel snapshot-2013-june-test-rhel-x86_64-server-optional-6... [OK]
    Snapshot sucessfully created

### Manage Snapshots

spaceclone also supports the idea of setting up a channel workflow, such as development -> preprpoduction -> production or testing -> current -> stable.  You can use promote to promote from one channel to another.

First you need to create the snapshots with a custom naming scheme:

    # spaceclone create --name development
    # spaceclone create --name preproduction
    # spaceclone create --name production

You can then "promote":

    # spaceclone promote --source development --target stable

    Promoting "development" channels to "stable".... [OK]

### List All Snapshots

    # spaceclone list

    |Snapshot Label          |Date Created| Systems            |
    |------------------------|------------|--------------------|
    | snapshot-2013-april    | 2013-04-04 | 1,392              |
    | snapshot-2013-may      | 2013-05-04 | 385                |

### Moving Systems Between Snapshot

    # spaceclone move --server webserver01.example.com --target-snapshot=snapshot-2013-may

    Moving server "webserver01.example.com" to target snapshot-2013-may.... [OK]

### Delete Snapshots

    # spaceclone delete --target-snapshot=snapshot-2013-april

    Deleting snapshot-2013-april... [OK]

    # spaceclone delete --older-than 365

    No snapshots older than 365 days found.

### Showing Snapshot Details

    # spaceclone show

    snapshot-2013-may-rhel-x86_64-server-6
     |.. snapshot-2013-may-rhel-x86_64-server-optional-6
     |.. snapshot-2013-may-rhel-x86_64-server-supplmentary-6
     |.. snapshot-2013-may-custom-channel-6

## License

Copyright (c) 2013 Stephen Benjamin

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software 
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.

