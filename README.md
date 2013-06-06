# [![Spaceclone](images/spaceclone.png)](http://openclipart.org/detail/94573/fireball-by-mazeo)  Spaceclone

Spaceclone is a management tool for RHN Satellite channels.  It's feature incomplete and a work in progress.  Use at your own risk!

Why
---

Channel cloning has been long used by many RHN Satellite and Spacewalk users to control the patch levels of their systems.  Managing the clones and the systems has been a bit difficult in the past, and spaceclone attemps to make it a bit easier.

There's two primary workflows spaceclone can be used for:

 - Create clones on a time basis, perhaps quarterly

 - Create a chain of clones to support a testing -> current -> stable, or development -> staging -> production methodology

# Usage

Run without options to see the usage:

    [stbenjam@atlantis lib]\$ spaceclone
    Usage: spaceclone <command> <options>

    Commands:
    create      Creates a new cloneset
    list        List all clonesets
    move        Move a system to a cloneset
    promote     Promotes one snapshot to another
    show        Show a specific Cloneset

To get help for a command:

    [stbenjam@atlantis lib]\$ spaceclone create --help
    Usage: clone [options]

    Options:
       -h, --help            show this help message and exit

    Satellite Options:
        -s SAT_SERVER, --server=SAT_SERVER
                            Server Name
        -u SAT_USERNAME, --username=SAT_USERNAME
                            Username
        -p SAT_PASSWORD, --password=SAT_PASSWORD
                            Password

      Create Options:
        -o ORIGIN, --origin=ORIGIN
                            Origin Base Channel
        -t TARGET, --target=TARGET
                           Target Cloneset Name
        -f PREFIX, --prefix=PREFIX
                            Prefix for Channel Name


## Create a New Cloneset

### Time-based Snapshot Example


        [stbenjam@atlantis lib]\$ spaceclone create -s abydos.bitbin.de -u satadmin -p password -o rhel-x86_64-server-6 -t "June 2013" -f "ACME Inc"

        Creating clone channels:
            sc-june-2013-rhel-x86_64-server-6...  [ OK ]
            sc-june-2013-rhel-x86_64-server-optional-6...  [ OK ]
            sc-june-2013-rhel-x86_64-server-supplementary-6...  [ OK ]
            sc-june-2013-rhn-tools-rhel-x86_64-server-6...  [ OK ]
            sc-june-2013-epel-6-x86_64...  [ OK ]

### Workflow Example

One might also want to have a workflow like development -> staging -> production:

    spaceclone create -s abydos.bitbin.de -u satadmin -p password -o rhel-x85_64-server-6 -t development -f "ACME Inc"

    spaceclone create -s abydos.bitbin.de -u satadmin -p password -o sc-development-rhel-x86_64-server-6... -t staging -f "ACME Inc"

    spaceclone create -s abydos.bitbin.de -u satadmin -p password -o sc-staging-rhel-x86_64-server-6... -t production -f "ACME Inc"

## List all Clonesets

    [stbenjam@atlantis lib]\$ spaceclone list -s abydos.bitbin.de -u satadmin -p password
    +-------------+--------------+-------------------------------------+----------------------+--------------------+
    | Cloneset    | Created      | Source                              | Base                 | Registered Systems |
    +-------------+--------------+-------------------------------------+----------------------+--------------------+
    | development | 06 June 2013 | rhel-x86_64-server-6                | rhel-x86_64-server-6 | 1                  |
    | production  | 06 June 2013 | sc-staging-rhel-x86_64-server-6     | rhel-x86_64-server-6 | 0                  |
    | staging     | 06 June 2013 | sc-development-rhel-x86_64-server-6 | rhel-x86_64-server-6 | 0                  |
    | june-2013   | 06 June 2013 | rhel-x86_64-server-6                | rhel-x86_64-server-6 | 0                  |
    +-------------+--------------+-------------------------------------+----------------------+--------------------+

## Showing Cloneset Details

    [stbenjam@atlantis lib]\$ spaceclone show -s abydos.bitbin.de -u satadmin -p password -c staging
    +-----------------------------------------------+--------+---------------------------------------------------+------------------------------------+
    | Channel                                       | Type   | Source                                            | Base                               |
    +-----------------------------------------------+--------+---------------------------------------------------+------------------------------------+
    | sc-staging-rhel-x86_64-server-6               | parent | sc-development-rhel-x86_64-server-6               | rhel-x86_64-server-6               |
    | sc-staging-rhel-x86_64-server-optional-6      | child  | sc-development-rhel-x86_64-server-optional-6      | rhel-x86_64-server-optional-6      |
    | sc-staging-rhel-x86_64-server-supplementary-6 | child  | sc-development-rhel-x86_64-server-supplementary-6 | rhel-x86_64-server-supplementary-6 |
    | sc-staging-rhn-tools-rhel-x86_64-server-6     | child  | sc-development-rhn-tools-rhel-x86_64-server-6     | rhn-tools-rhel-x86_64-server-6     |
    | sc-staging-epel-6-x86_64                      | child  | sc-development-epel-6-x86_64                      | epel-6-x86_64                      |
    +-----------------------------------------------+--------+---------------------------------------------------+------------------------------------+

## Moving Systems Between Clones


    [stbenjam@atlantis lib]\$ spaceclone move -s abydos.bitbin.de -u satadmin -p password -i 1000010000 -c staging
    Moving system...
    +---------------------------------------------------+-----------------------------------------------+
    | Before                                            | After                                         |
    +---------------------------------------------------+-----------------------------------------------+
    | sc-development-rhel-x86_64-server-6               | sc-staging-rhel-x86_64-server-6               |
    | sc-development-rhel-x86_64-server-optional-6      | sc-staging-rhel-x86_64-server-optional-6      |
    | sc-development-epel-6-x86_64                      | sc-staging-epel-6-x86_64                      |
    | sc-development-rhel-x86_64-server-supplementary-6 | sc-staging-rhel-x86_64-server-supplementary-6 |
    | sc-development-rhn-tools-rhel-x86_64-server-6     | sc-staging-rhn-tools-rhel-x86_64-server-6     |
    +---------------------------------------------------+-----------------------------------------------+

    Confirm changes? [Y/n] Y

## Delete Clonesets

Unimplemented

## Update Clone Channels (Promotion)

Unimplemented



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

