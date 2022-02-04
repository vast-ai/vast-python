# Welcome to Vast.ai’s documentation!

## Overview
This repository contains the open source python command line interface for vast.ai.
This CLI has all of the main functionality of the vast.ai website GUI and uses the
same underlying REST API. Most of the functionality is self-contained in the single
script file `vast.py`, although the invoice generating commands
require installing an additional second script called `vast_pdf.py`.

## Quickstart

You should probably create a subdirectory in which to put this script and related files if you
haven't already. You can call it whatever you like but I'll refer to it as "vid" for "Vast Install Directory".
So just enter `mkdir vid` to create the directory. Once you've created the directory just change your working directory to it with `cd vid`. After you've
done that the quickest way to get started is to download the `vast.py` script using the `wget` command.

```wget https://raw.githubusercontent.com/vast-ai/vast-python/master/vast.py; chmod +x vast.py;```

You can verify that the script is working by doing `./vast.py --help`. You should see a list of the available
commands. In order to proceed further you will need to login to the vast.ai website and get your api-key.
Go to [https://vast.ai/console/cli/](https://vast.ai/console/cli/). Copy the command under 
the heading "Login / Set API Key" and run it. The command will be something like

```./vast.py set api-key xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx```

where the `xxxx...` is your api-key (a long hexadecimal number). Note that if the script is
named "vast" in this command on the website and your installed script is named "vast.py"
you will need to change the name of the script in the command you run. The `set api-key`
command saves your api-key in a hidden file in your home directory. Do not share your
api-key with anyone as it authenticates your other vast commands to your account.

## Usage

To see how the API works you can use it to find machines for rent. `vast.py search offers`. In this
form the command will show all available offers. To get more specific results try narrowing the search.
There is a large online help page on how to do this. Bring up the help by doing `vast.py search offers --help`.
There are many parameters that can be used to filter the results. The search command supports
all of the filters and sort options that the website GUI uses. To find Turing GPU instances
(compute capability 7.0 or higher):

```./vast.py search offers 'compute_cap > 700 '```

To find instances with a reliability score >= 0.99 and at least 4 gpus, ordering by num of gpus
descending:

```./vast.py search offers 'reliability > 0.99  num_gpus>=4' -o 'num_gpus-'```

The output of this command at the time of this writing is
```
ID       CUDA  Num  Model        PCIE_BW  vCPUs     RAM  Storage  $/hr     DLPerf  DLP/$  Nvidia Driver Version  Net_up  Net_down  R      Max_Days  machine_id
1596177  11.4  10x  GTX_1080     5.5      48.0    257.9  4628     2.0000   73.0    36.5   470.63.01              653.3   854.5     99.5   -         638
2459430  11.5   8x  RTX_A5000    9.1      128.0   515.8  3094     4.0000   209.4   52.3   495.46                 1844.2  2669.6    99.7   12.0      4384
2459380  11.4   8x  RTX_3070     6.3      12.0     64.0  710      1.4200   67.2    47.3   470.86                 0.0     0.0       99.8   -         4102
2456624  11.4   8x  RTX_2080_Ti  10.7     32.0    257.9  1653     2.8000   126.4   45.2   470.82.00              14.6    214.2     99.8   28.7      3047
2456622  11.4   8x  RTX_2080_Ti  10.8     32.0    128.9  1651     2.8000   127.1   45.4   470.82.00              14.9    214.7     99.1   28.7      1569
2456600  11.5   8x  RTX_2080_Ti  10.9     48.0    256.6  1704     2.4000   125.5   52.3   495.29.05              169.0   169.8     99.7   25.7      4058
2455617  11.2   8x  RTX_3090     21.7     64.0    515.8  6165     6.4000   261.1   40.8   460.67                 477.6   707.2     99.8   28.7      2980
2454397  11.2   8x  A100_SXM4    22.4     128.0  2064.1  21568    13.2000  300.1   22.7   460.106.00             708.7   1119.8    99.2   -         4762
2405590  11.4   8x  RTX_2080_Ti  11.2     48.0    257.9  1629     3.8000   125.5   33.0   470.82.00              389.4   608.8     100.0  1.8       2776
2364579  11.4   8x  A100_PCIE    18.5     128.0   515.8  4813     14.8000  278.8   18.8   470.74                 472.4   699.0     99.9   28.7      3459
2281839  11.2   8x  Tesla_V100   11.8     72.0    483.1  1171     5.6000   193.6   34.6   460.67                 493.0   697.8     100.0  28.7      2744
2281832  11.2   8x  A100_PCIE    17.7     64.0    515.9  5821     14.8000  276.7   18.7   460.91.03              478.2   655.5     99.9   28.7      2901
2452630  11.4   7x  RTX_3090     6.3      28.0     64.0  61       3.5000   165.5   47.3   470.86                 84.6    84.4      99.3   3.8       4420
2342561  11.4   7x  RTX_3090     6.1      96.0    257.6  1664     4.5500   149.2   32.8   470.82.00              476.9   671.7     99.4   1.7       4202
2237983  11.4   7x  RTX_3090     12.5     32.0    257.6  3228     3.1500   204.5   64.9   470.86                 194.4   183.8     99.1   -         4207
2459511  11.4   6x  RTX_3090     6.2      -       128.8  812      2.8200   150.2   53.2   470.94                 374.4   271.4     99.0   6.7       3129
2448342  11.5   6x  RTX_A6000    12.4     64.0    515.7  6695     3.6000   169.8   47.2   495.29.05              668.6   1082.6    99.6   -         3624
2437565  11.4   6x  RTX_3090     23.0     16.0    128.8  1676     5.4000   196.8   36.5   470.94                 34.1    131.5     99.4   -         4238
2332973  11.2   6x  RTX_3090     11.9     48.0    193.3  1671     3.3000   180.3   54.6   460.84                 582.1   737.6     99.9   25.6      3552
2459459  11.5   4x  RTX_3090     23.1     32.0    257.8  1363     2.0000   131.2   65.6   495.46                 1954.7  2725.8    99.6   12.0      3059
2459428  11.5   4x  RTX_A5000    24.6     64.0    515.8  1547     2.0000   104.9   52.4   495.46                 1844.2  2669.6    99.7   12.0      4384
2459368  11.4   4x  RTX_3090     25.3     48.0     64.2  133      1.3967   130.5   93.4   470.86                 0.0     0.0       99.4   -         4637
2458968  11.6   4x  RTX_3090     11.7     16.0    128.5  752      1.4000   79.8    57.0   510.39.01              797.8   842.7     99.9   4.0       2555
2458878  11.6   4x  RTX_3090     11.6     36.0    128.5  1531     1.4000   81.9    58.5   510.39.01              757.1   807.6     99.9   4.0       3646
2458845  11.6   4x  RTX_3090     3.1      12.0    128.5  369      1.4000   92.4    66.0   510.39.01              725.7   852.2     99.8   4.0       700
2458838  11.6   4x  RTX_3090     5.7      48.0    128.9  624      1.4000   85.3    60.9   510.39.01              574.9   731.7     99.8   4.0       2217
2454395  11.2   4x  A100_SXM4    22.9     64.0   2064.1  10784    6.6000   150.0   22.7   460.106.00             708.7   1119.8    99.2   -         4762
2452632  11.4   4x  RTX_3090     6.3      16.0     64.0  35       2.0000   123.5   61.8   470.86                 84.6    84.4      99.3   3.8       4420
2450275  11.4   4x  RTX_3080_Ti  12.5     32.0    128.7  817      1.8000   128.8   71.6   470.82.00              278.3   350.4     99.7   -         4260
2449210  11.5   4x  RTX_3090     11.2     48.0    128.9  324      2.0000   89.7    44.9   495.29.05              688.3   775.4     99.8   -         2764
2445175  11.4   4x  RTX_3090     11.9     32.0    257.6  1530     2.0000   135.4   67.7   470.86                 868.6   887.1     99.7   25.9      3055
2444916  11.4   4x  RTX_3090     11.9     16.0    128.7  1576     1.4000   131.8   94.2   470.82.00              39.4    402.3     99.9   -         3759
2437188  11.4   4x  Tesla_P100   11.7     24.0     95.2  2945     0.7200   44.8    62.2   470.82.00              10.9    76.2      99.5   0.1       3969
2437179  11.4   4x  Tesla_P100   11.7     32.0    192.1  3070     0.7200   44.8    62.3   470.82.00              11.1    66.0      99.2   0.0       4159
2431606  11.4   4x  RTX_3090     17.9     32.0    110.7  330      1.8400   134.3   73.0   470.82.01              584.6   813.4     99.7   4.4       4079
2419191  11.4   4x  RTX_2080_Ti  6.3      32.0     64.4  837      2.0000   64.7    32.4   470.63.01              40.5    205.9     99.7   -         162
2405589  11.4   4x  RTX_2080_Ti  10.8     24.0    257.9  815      1.9000   62.8    33.0   470.82.00              389.4   608.8     100.0  1.8       2776
2392087  11.4   4x  RTX_A6000    10.8     32.0    515.9  1247     1.8000   64.5    35.8   470.94                 669.9   705.4     99.1   10.9      4782
2377227  11.2   4x  RTX_3090     6.3      24.0     64.3  1638     2.0000   128.3   64.1   460.32.03              37.8    145.0     99.7   3.0       2672
2349173  11.4   4x  RTX_3090     23.2     48.0    128.7  1475     2.0000   107.4   53.7   470.86                 33.2    84.2      99.8   47.3      3949
2338635  11.4   4x  RTX_3090     23.0     32.0    128.5  3151     1.6000   108.8   68.0   470.86                 33.8    86.4      99.6   47.4      3948
2303959  11.2   4x  RTX_3090     11.7     28.0    128.8  791      2.1200   131.3   61.9   460.32.03              519.7   570.7     99.5   -         3042
2281830  11.2   4x  A100_PCIE    18.1     32.0    515.9  2910     7.4000   143.6   19.4   460.91.03              478.2   655.5     99.9   28.7      2901
2193726  11.4   4x  RTX_3090     12.4     32.0    128.8  1646     3.6000   153.9   42.8   470.82.01              33.3    137.5     99.5   -         3434
1737692  11.2   4x  RTX_3070     6.3      28.0    128.5  656      2.8000   37.5    13.4   460.91.03              452.6   703.2     99.6   -         3510
```

#### Launching Instances
To create an instance of type 2459368 (using an ID from the search) with the vastai/tensorflow image
and 32 GB of disk storage

```./vast.py create instance 2459368 --image vastai/tensorflow --disk 32```

## Install

If you followed the instructions in [Quickstart](#Quickstart) you have already installed the script that contains
most of the CLI functionality. If you wish to print PDF format invoices you will need a few other
things. First, you'll need the vast_pdf.py script. This can be found in this repository in the main
directory at [vast_pdf.py](vast_pdf.py). This script should be present in the same directory as the
`vast.py` script. It makes use of a third party library called Borb to create the PDF invoices. To install
this run the command `pip3 install borb`

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

### Commands in Detail

---

#### Change existing bid by id

```
usage: vast.py change bid id [--price PRICE]

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
#### Create account (command line account creation no longer supported)

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
#### Create instance

```
usage: vast.py create instance id [OPTIONS] [--args ...]

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
#### Destroy instance

```
usage: vast.py destroy instance id [-h] [--api-key API_KEY] [--raw]

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
#### Generate pdf-invoices

```
usage: vast.py generate pdf_invoices [OPTIONS]

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
#### Label instance

```
usage: vast.py label instance <id> <label>

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
#### List machine for rent

```
usage: vast.py list machine id [--price_gpu PRICE_GPU] [--price_inetu PRICE_INETU] [--price_inetd PRICE_INETD] [--api-key API_KEY]

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
#### Login (command line login no longer supported)

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
#### Remove default job

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
#### scp-url

```
usage: vast.py scp-url

optional arguments:
  -h, --help         show this help message and exit
  --id ID            id of instance
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
#### Search offers

```
usage: vast.py search offers [--help] [--api-key API_KEY] [--raw] <query>

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
#### Set api-key

```
usage: vast.py set api-key APIKEY

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
#### Set default job

```
usage: vast.py set defjob id [--api-key API_KEY] [--price_gpu PRICE_GPU] [--price_inetu PRICE_INETU] [--price_inetd PRICE_INETD] [--image IMAGE] [--args ...]

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
#### Set minimum bid

```
usage: vast.py set min_bid id [--price PRICE]

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
#### Show instances we are renting

```
usage: vast.py show instances [--api-key API_KEY] [--raw]

optional arguments:
  -h, --help         show this help message and exit
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
#### Show invoices

```
usage: vast.py show invoices [OPTIONS]

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
#### Show machines we are offering for rent

```
usage: vast.py show machines [OPTIONS]

optional arguments:
  -h, --help         show this help message and exit
  -q, --quiet        only display numeric ids
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
#### Show user account information

```
usage: vast.py show user[OPTIONS]

optional arguments:
  -h, --help         show this help message and exit
  -q, --quiet        display information about user
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
#### ssh-url

```
usage: vast.py ssh-url

optional arguments:
  -h, --help         show this help message and exit
  --id ID            id of instance
  --url URL          server REST api url
  --raw              output machine-readable json
  --api-key API_KEY  api key. defaults to using the one stored in
                     ~/.vast_api_key

```
---
#### Start instance

```
usage: vast.py start instance <id> [--raw]

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
#### Stop instance

```
usage: vast.py stop instance [--raw] <id>

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
#### Unlist machine

```
usage: vast.py unlist machine <id>

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
