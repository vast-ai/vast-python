# vast-python

Super basic git repo so interested folks can pull request.
More to follow. There are a few additional files here that may
be of use to developers of the project.

* `mypi.ini` : config file for the mypy static type checker.
* `make-archive.sh` :
   Shell script to build the tarball that ships to
   customers. The `venv` subdirectory should contain all the python
   modules needed by the vast.py and vast_pdf.py scripts. This makes
   the resulting tarball self-sufficient and the scripts should
   run no matter what the customer has installed on his machine.
   Note that I have not yet added the contents of this directory
   because I'm still debating whether to check in a tarball of it
   or just check all the files into git.
