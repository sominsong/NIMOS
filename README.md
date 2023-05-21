# What is "NIMOS"?

- One line description of this project

    > "Analysis of syscall sequence pattern from exploit codes for advanced system call sequence filtering for enhanced container security"

- Detailed description of the project

    This project attempts to speculate and verify that focusing on the sequence of syscall invocations can lead to more effective defenses against container attacks, as opposed to traditional filtering mechanisms (such as Seccomp) handling the syscalls individually.

    In this project, the primary objective is instead to investigate the existence of system call sequence patterns that are shared across different attacks.
    Additionally, the goal is to investigate what syscall sequence patterns shared by different attacks do not interfere with the behavior of a normally functioning application.

    So, this project consists of two main phases of action: **1) Malicious N-gram pattern analysis for exploit codes**, **2) benign system call sequence analysis for 15 normal application**.
    The goal of the first step is extracting system call sequence patterns across exploit codes and the goal of the second step is extracing system call sequence from benign applciations

## Index
[1.Architecture](#architecture)

[2.Getting Started](#getting-started)

[3.How to Run](#how-to-run)

  [3.1 Cralwing exploit codes](#step-1-cralwing-exploit-codes)

  [3.2 Generating ligc-to-syscall seqeunce mapping](#step-2-generating-ligc-to-syscall-seqeunce-mapping)

  [3.3 Generating syscall sequence per exploit code](#step-3-generating-syscall-sequence-per-exploit-code)

  [3.4 Generating N-gram syscall patterns per exploit code](#step-4-generating-n-gram-syscall-patterns-per-exploit-code)

  [3.5 Tracing syscall sequence per application](#step-5-tracing-syscall-sequence-per-application)

  [3.6 Parsing syscall sequence per application](#step-6-parsing-syscall-sequence-per-application)

## Architecture

**1. Malicious N-gram Pattern Analysis for Exploit Codes**

- Resaerch Architecture

    <img src="https://github.com/sominsong/NIMOS/blob/main/fig/research_archi.png">
    
    The figure above shows the overall design ofour methodology for extracting system call sequence patterns across exploit codes. It consists of three stages:

    1. Input data collection: collects exploit codes, their vulnerability metadata, and C-library unit tests from publicly available sources.

    2. System call sequence analysis: employs a hybrid approach, utilizing (i) static analysis atop exploit codes, to extract library function sequences on all possible control flows where the exploits can be successfully triggered, and (ii) dynamic analysis atop C-library unit tests, to build a mapping between library functions and system call sequences. Then, it **combines both analyses** *<u>(libc sequence per exploit code from static analysis + libc-to-syscall sequence from dynamic analysis)</u>* to generate a system call sequence corresponding to each exploit code.

    3. Pattern extraction: discovers common system call sequence patterns of various lengths using the Generalized Sequential Pattern (GSP) mining algorithm.

- Implementation

    <img src="https://github.com/sominsong/NIMOS/blob/main/fig/git_readme.png">

    The figure above shows the implementation of the Research design.

    It shows the directory name in charge of the module in the research architecture figure, the file name in charge of the operation process of the module, and where the input/output files of each module are created.

    The `exploit/` directory is a module that crawls exploit codes and metadata about exploit code.

    The `syscall-generation/` folder corresponds to the dynamic analysis module in research architecture. The files in the folder are responsible for creating the *libc-to-syscall sequence mapping* by analyzing the exploit codes.

    The `path-generation/` folder corresponds to the static analysis module in research architecture. The files in the folder analyze the exploit code to extract the library function sequence, and combine it with the dynamic analysis result to generate the final *syscall sequence per exploit codes*.

    The `analysis/` folder corresponds to the sequential pattern mining module in research architecture. By analyzing the syscall sequence per exploit codes, it finds *patterns of length N (N-gram pattern)* shared by the exploit codes.

**2. Benign System Call Sequence Analysis for 15 Normal Applications**

- Research Architecture

    <img src="https://github.com/sominsong/NIMOS/blob/main/fig/benign_archi.png" width="500">

    The goal of this process is to investigate the relationship between the length of the sequence of system calls extracted from the exploit code and the likelihood of interfering with the legitimate activity of a harmless application.

    The figure above shows the process of extracting the syscall sequence invoked by the benign operations of the applications.

    To this end, this project tests the application behavior from 15 popular images.
    
    By performing diverse application-specific operations such as {GET, PUT, POST} for web servers, and {INSERT, DELETE, SELECT} for NoSQL databases, amongst others.

    The result of this process is to generate *per-thread system call traces*.

- Implementation

    <img src="https://github.com/sominsong/NIMOS/blob/main/fig/git_benign.png" width="600">

    The figure above shows the implementation of the Research design.

    It shows the directory name in charge of the module in the research architecture figure, the file name in charge of the operation process of the module, and where the input/output files of each module are created.

    The `app/` folder includes all of the 'container execution, container tracking, and tracking result parsing' processes shown in research architecture.
    As a result, it creates a *syscall sequence per application*.


## Getting started

```
sudo su
apt update && apt install -y make git-all

git clone git@github.com:sominsong/NIMOS.git
cd NIMOS && make build
```

## How to run

You should be a **sudo-privileged user** or run it with **sudo privileges**.

There is help option(-h) for providing short explanations for all options.
Except for the help option, the remaining options are executed in the following order.

You can run almost all options (includes -C,-S, -P and -N options) in sequence at once with following -a option.

But, you need to run -B option and -R option manually.

```
./run.sh -A
```

Each execution command and process are as follows:

### Step 1. Cralwing exploit codes

Crawl exploit codes and information related to the exploit codes collected.

```
./run.sh -C
```

After this process, The exploit code for each source is collected in each source folder under the `exploit` folder of the project folder. 

Also, `exploit.json` with information about the exploit collected under the `/opt/output/perm/` folder is created.

### Step 2. Generating ligc-to-syscall seqeunce mapping

Analyze the exploit code and generate mapping the library functions used in the exploit codes and the syscall sequences invoked by the library functions.

> **Do not panic if the `[ERROR]` output statement is printed during this process! This project handles errors by itself..**

```
./run.sh -S
```

After this process, GCC GIMPLE files (`*.original` files) for each exploit code are created under `/opt/output/temp/` folder.

And unit test codes for the usecases of the library functions used in each exploit code are created under the `/opt/output/temp/testcase` folder.

The name of the test code of the library function is in the following format:

`{library function name}-{exploit-ID}-{function name in the code where the library function is used}-{(optional) delimiter number}`

Delimiter number is created when library function is used multiple times in the same function.

or

`{library function name}-default-default`

Also, the execution results of the unit test codes of each library functions are parsed and saved in the form of a system call sequence (sequence consisting of system call numbers) under the `/opt/output/temp/testcase/result/` folder.

### Step 3. Generating syscall sequence per exploit code

Generate library function execution paths by analyzing the control flow graph (CFG) of the exploit codes, and Generate the syscall execution paths (sequences) of the exploit codes by combining it with the result of step 2 ('library function-syscall sequnece' mapping).

```
./run.sh -P
```

After this process, control flow graphs (`*.cfg` files) for each exploit code are created under `/opt/output/temp/` folder.

Also, the sets of all possible paths consisting of a sequence of system calls for each exploit code are created under the path `/opt/output/perm/path/`. It is saved in a json file format, and the file name means the ID of each exploit code as follow: `{exploit-ID}.json`

The file shows the sequence of system call numbers for each user-defined function.

### Step 4. Generating N-gram syscall patterns per exploit code

Generate N-gram patterns from the 'exploit-syscall sequence' mapping obtained as a result of step 3.

```
./run.sh -N
```

After this process, 3 files (`{date}_ngram_sysname_max200.csv`, `{date}_ngram_sysnum_max200.csv`, `ngram_result.pkl`) are created under the `/opt/output/perm/analysis/` folder.

Each file is as follows:

- `{date}_ngram_sysname_max200.csv`: It is a csv file consisting of the 'N-gram pattern length, the number of exploit codes from which the N-gram pattern is extracted, and the N-gram pattern consisting of syscall names' columns.

- `{date}_ngram_sysnum_max200.csv`: It is a csv file consisting of the 'N-gram pattern length, the number of exploit codes from which the N-gram pattern is extracted, and the N-gram pattern consisting of syscall numbers' columns.

- `ngram_result.pkl`: It is a file that saves a dictionary in the form of `{'N-gram pattern':'Number of exploits with N-gram pattern found'}` in binary format.

### Step 5. Tracing syscall sequence per application

By testing 15 applications, Extract benign syscall sequence that is invoked when each application opereates normally. This option is only for settings for application testing. Application tests need to be manually executed through individual commands because of the ftrace setting.

```
./run.sh -B
```

After this process, folders for docker bind mount are created under the `/data/` folder. Also, several docker networks and docker volumes are created.
You can check `docker network ls` and `docker volume ls` command.

You can see help description of option -B with `./run.sh -B -h` command.

- You can test the application with the following command (The options that can be tested vary from application to application):

```
./run.sh -B -e [mongodb|mysql|httpd|nginx|redis|mariadb|node|tomcat]
    e.g. ./run.sh -B -e mongodb
or
./run.sh -B -d [gcc|openjdk|gzip|bzip2|qalc|ghostscript|lowriter]
    e.g. ./run.sh -B -d gcc
```

After this process, syscall sequence trace results for each test operation in each application are created under the `/opt/output/tracing/` folder.

A description of the file name format follows:
`{application name}_{test case type}.txt`

### Step 6. Parsing syscall sequence per application

Parse the syscall sequence for each application from the trace results (stop 5) of all 15 applications.

```
./run.sh -R
```

After this process, The results of the system call sequence parsed for each thread of the application are created under the `/opt/output/tracing/split/` folder.

A description of the file name format follows:
`{application name}-{test case type}-{process id(thread id)}`

In addition, as the tracing result is parsed, a file with a sequence of system call names is created under the `/opt/output/parsing` directory.

The format of the file name is same with above: `{application name}-{test case type}-{process id(thread id)}`
