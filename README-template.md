# Welcome to Vast.ai’s documentation!

# vast-python

Super basic git repo so interested folks can pull request.
More to follow. There are a few additional files here that may
be of use to developers of the project.


* mypi.ini : config file for the mypy static type checker.

* make-archive.sh : Shell script to build the tarball that ships to customers. I’ve gotten rid of the venv directory for now.

* watcher.sh : A little shell script to help development of the PDF invoices.
    It basically just uses the watch command to watch the directory
    using ls. When anything changes it dies. Then the script regenerates
    the PDF. This is all done in a “while true” construct that loops forever.
    You’ll need to hit Ctrl-C *twice* to kill it. The first one only kills
    the watch command within the script.


The CLI API is all contained in a python script called `vast.py`.
This script can be called with various commands as arguments. Commands follow
a simple "verb-object" pattern. As an example, consider "show machines". To run this
command we type `./vast.py show machines`




usage: vast.py [-h] [--url URL] [--raw] [--api-key API_KEY]
               command ...

positional arguments:
  command               command to run. one of:
  *  help                print this help message
  *  search offers
  *  show instances
    ssh-url
    scp-url
    show machines
    show invoices
    show user
    generate pdf-invoices
    list machine
    unlist machine
    remove defjob
    start instance
    stop instance
    label instance
    destroy instance
    set defjob
    create instance
    change bid
    set min-bid
    set api-key
    create account
    login

optional arguments:
  -h, --help            show this help message and exit
  --url URL             server REST api url
  --raw                 output machine-readable json
  --api-key API_KEY     api key. defaults to using the one
                        stored in ~/.vast_api_key