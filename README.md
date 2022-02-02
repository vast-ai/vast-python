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

## Commands

The CLI API is all contained in a python script called `vast.py`.
This script can be called with various commands as arguments. Commands follow
a simple "verb-object" pattern. As an example, consider "show machines". To run this
command we type `./vast.py show machines`

### Comprehensive list of commands

```
usage: vast.py [-h] [--url URL] [--raw] [--api-key API_KEY] command ...

positional arguments:
  command               command to run. one of:
    help                print this help message
    search offers
    show instances
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
  --api-key API_KEY     api key. defaults to using the one stored in
                        ~/.vast_api_key

```

## Individual commands and options


```
usage: vast search offers [--help] [--api-key API_KEY] [--raw] <query>

positional arguments:
  query                 Query to search for. default: 'external=false
                        rentable=true verified=true', pass -n to ignore
                        default

optional arguments:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  Show 'bid'(interruptible) or 'on-demand' offers.
                        default: on-demand
  -i, --interruptible   Alias for --type=bid
  -b, --bid             Alias for --type=bid
  -d, --on-demand       Alias for --type=on-demand
  -n, --no-default      Disable default query
  --disable-bundling    Show identical offers. This request is more heavily
                        rate limited.
  --storage STORAGE     Amount of storage to use for pricing, in GiB.
                        default=5.0GiB
  -o ORDER, --order ORDER
                        Comma-separated list of fields to sort on. postfix
                        field with - to sort desc. ex: -o
                        'num_gpus,total_flops-'. default='score-'
  --url URL             server REST api url
  --raw                 output machine-readable json
  --api-key API_KEY     api key. defaults to using the one stored in
                        ~/.vast_api_key

Query syntax:

    query = comparison comparison...
    comparison = field op value
    field = <name of a field>
    op = one of: <, <=, ==, !=, >=, >, in, notin
    value = <bool, int, float, etc> | 'any'

note: to pass '>' and '<' on the command line, make sure to use quotes

Examples:

    ./vast search offers 'compute_cap > 610 total_flops < 5'
    ./vast search offers 'reliability > 0.99  num_gpus>=4' -o 'num_gpus-'
    ./vast search offers 'rentable = any'

Available fields:

      Name                  Type       Description

    compute_cap:            int       cuda compute capability*100  (ie:  650 for 6.5, 700 for 7.0)
    cpu_cores:              int       # virtual cpus
    cpu_cores_effective:    float     # virtual cpus you get
    cpu_ram:                float     system RAM in gigabytes
    cuda_vers:              float     cuda version
    disk_bw:                float     disk read bandwidth, in MB/s
    disk_space:             float     disk storage space, in GB
    dlperf:                 float     DL-perf score  (see FAQ for explanation)
    dlperf_usd:             float     DL-perf/$
    dph:                    float     $/hour rental cost
    driver_version          string    driver version in use on a host.
    duration:               float     max rental duration in days
    external:               bool      show external offers
    flops_usd:              float     TFLOPs/$
    gpu_mem_bw:             float     GPU memory bandwidth in GB/s
    gpu_ram:                float     GPU RAM in GB
    gpu_frac:               float     Ratio of GPUs in the offer to gpus in the system
    has_avx:                bool      CPU supports AVX instruction set.
    id:                     int       instance unique ID
    inet_down:              float     internet download speed in Mb/s
    inet_down_cost:         float     internet download bandwidth cost in $/GB
    inet_up:                float     internet upload speed in Mb/s
    inet_up_cost:           float     internet upload bandwidth cost in $/GB
    min_bid:                float     current minimum bid price in $/hr for interruptible
    num_gpus:               int       # of GPUs
    pci_gen:                float     PCIE generation
    pcie_bw:                float     PCIE bandwidth (CPU to GPU)
    reliability:            float     machine reliability score (see FAQ for explanation)
    rentable:               bool      is the instance currently rentable
    rented:                 bool      is the instance currently rented
    storage_cost:           float     storage cost in $/GB/month
    total_flops:            float     total TFLOPs from all GPUs
    verified:               bool      is the machine verified

```
---
```
usage: vast show instances [--api-key API_KEY] [--raw]

optional arguments:
  -h, --help         show this help message and exit
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: vast ssh-url

optional arguments:
  -h, --help         show this help message and exit
  --id ID            id of instance
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: vast scp-url

optional arguments:
  -h, --help         show this help message and exit
  --id ID            id of instance
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: vast show machines [OPTIONS]

optional arguments:
  -h, --help         show this help message and exit
  -q, --quiet        only display numeric ids
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: vast show invoices [OPTIONS]

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           only display numeric ids
  -s START_DATE, --start_date START_DATE
                        start date and time for report. Many formats accepted
                        (optional)
  -e END_DATE, --end_date END_DATE
                        end date and time for report. Many formats accepted
                        (optional)
  -c, --only_charges    Show only charge items.
  -p, --only_credits    Show only credit items.
  --url URL             server REST api url
  --raw                 output machine-readable json
  --api-key API_KEY     api key. defaults to using the one stored in
                        ~/.vast_api_key

```
---
```
usage: vast show user[OPTIONS]

optional arguments:
  -h, --help         show this help message and exit
  -q, --quiet        display information about user
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: vast generate pdf_invoices [OPTIONS]

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           only display numeric ids
  -s START_DATE, --start_date START_DATE
                        start date and time for report. Many formats accepted
                        (optional)
  -e END_DATE, --end_date END_DATE
                        end date and time for report. Many formats accepted
                        (optional)
  -c, --only_charges    Show only charge items.
  -p, --only_credits    Show only credit items.
  --url URL             server REST api url
  --raw                 output machine-readable json
  --api-key API_KEY     api key. defaults to using the one stored in
                        ~/.vast_api_key

```
---
```
usage: vast list machine id [--price_gpu PRICE_GPU] [--price_inetu PRICE_INETU] [--price_inetd PRICE_INETD] [--api-key API_KEY]

positional arguments:
  id                    id of machine to list

optional arguments:
  -h, --help            show this help message and exit
  -g PRICE_GPU, --price_gpu PRICE_GPU
                        per gpu rental price in $/hour (price for active
                        instances)
  -s PRICE_DISK, --price_disk PRICE_DISK
                        storage price in $/GB/month (price for inactive
                        instances), default: $0.15/GB/month
  -u PRICE_INETU, --price_inetu PRICE_INETU
                        price for internet upload bandwidth in $/GB
  -d PRICE_INETD, --price_inetd PRICE_INETD
                        price for internet download bandwidth in $/GB
  -m MIN_CHUNK, --min_chunk MIN_CHUNK
                        minimum amount of gpus
  -e END_DATE, --end_date END_DATE
                        unix timestamp of the available until date (optional)
  --url URL             server REST api url
  --raw                 output machine-readable json
  --api-key API_KEY     api key. defaults to using the one stored in
                        ~/.vast_api_key

```
---
```
usage: vast unlist machine <id>

positional arguments:
  id                 id of machine to unlist

optional arguments:
  -h, --help         show this help message and exit
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: vast.py remove defjob [-h] [--url URL] [--raw] [--api-key API_KEY] id

positional arguments:
  id                 id of machine to remove default instance from

optional arguments:
  -h, --help         show this help message and exit
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: vast start instance <id> [--raw]

positional arguments:
  id                 id of instance to start/restart

optional arguments:
  -h, --help         show this help message and exit
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: vast stop instance [--raw] <id>

positional arguments:
  id                 id of instance to stop

optional arguments:
  -h, --help         show this help message and exit
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: vast label instance <id> <label>

positional arguments:
  id                 id of instance to label
  label              label to set

optional arguments:
  -h, --help         show this help message and exit
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: vast destroy instance id [-h] [--api-key API_KEY] [--raw]

positional arguments:
  id                 id of instance to delete

optional arguments:
  -h, --help         show this help message and exit
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: vast set defjob id [--api-key API_KEY] [--price_gpu PRICE_GPU] [--price_inetu PRICE_INETU] [--price_inetd PRICE_INETD] [--image IMAGE] [--args ...]

positional arguments:
  id                    id of machine to launch default instance on

optional arguments:
  -h, --help            show this help message and exit
  --price_gpu PRICE_GPU
                        per gpu rental price in $/hour
  --price_inetu PRICE_INETU
                        price for internet upload bandwidth in $/GB
  --price_inetd PRICE_INETD
                        price for internet download bandwidth in $/GB
  --image IMAGE         docker container image to launch
  --args ...            list of arguments passed to container launch
  --url URL             server REST api url
  --raw                 output machine-readable json
  --api-key API_KEY     api key. defaults to using the one stored in
                        ~/.vast_api_key

```
---
```
usage: vast create instance id [OPTIONS] [--args ...]

positional arguments:
  id                    id of instance type to launch

optional arguments:
  -h, --help            show this help message and exit
  --price PRICE         per machine bid price in $/hour
  --disk DISK           size of local disk partition in GB
  --image IMAGE         docker container image to launch
  --label LABEL         label to set on the instance
  --onstart ONSTART     filename to use as onstart script
  --onstart-cmd ONSTART_CMD
                        contents of onstart script as single argument
  --jupyter             Launch as a jupyter instance instead of an ssh
                        instance.
  --jupyter-dir JUPYTER_DIR
                        For runtype 'jupyter', directory in instance to use to
                        launch jupyter. Defaults to image's working directory.
  --jupyter-lab         For runtype 'jupyter', Launch instance with jupyter
                        lab.
  --lang-utf8           Workaround for images with locale problems: install
                        and generate locales before instance launch, and set
                        locale to C.UTF-8.
  --python-utf8         Workaround for images with locale problems: set
                        python's locale to C.UTF-8.
  --args ...            DEPRECATED: list of arguments passed to container
                        launch. Onstart is recommended for this purpose.
  --create-from CREATE_FROM
                        Existing instance id to use as basis for new instance.
                        Instance configuration should usually be identical, as
                        only the difference from the base image is copied.
  --force               Skip sanity checks when creating from an existing
                        instance
  --url URL             server REST api url
  --raw                 output machine-readable json
  --api-key API_KEY     api key. defaults to using the one stored in
                        ~/.vast_api_key

```
---
```
usage: vast change bid id [--price PRICE]

positional arguments:
  id                 id of instance type to change bid

optional arguments:
  -h, --help         show this help message and exit
  --price PRICE      per machine bid price in $/hour
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

Change the current bid price of instance id to PRICE.
If PRICE is not specified, then a winning bid price is used as the default.

```
---
```
usage: vast set min_bid id [--price PRICE]

positional arguments:
  id                 id of machine to set min bid price for

optional arguments:
  -h, --help         show this help message and exit
  --price PRICE      per gpu min bid price in $/hour
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

Change the current min bid price of machine id to PRICE.

```
---
```
usage: vast set api-key APIKEY

positional arguments:
  new_api_key        Api key to set as currently logged in user

optional arguments:
  -h, --help         show this help message and exit
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: 
login via the command line is no longer supported.
go to https://vast.ai/console/cli in a web browser to get your api key, then run:

    vast set api-key YOUR_API_KEY_HERE

positional arguments:
  ignored

optional arguments:
  -h, --help         show this help message and exit
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
```
usage: 
login via the command line is no longer supported.
go to https://vast.ai/console/cli in a web browser to get your api key, then run:

    vast set api-key YOUR_API_KEY_HERE

positional arguments:
  ignored

optional arguments:
  -h, --help         show this help message and exit
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
