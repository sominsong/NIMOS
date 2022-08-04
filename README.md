# Syscall Attack Sequence

Analysis of Syscall Attack Sequence from Exploit Codes

## Getting started

```
sudo su
apt update
apt install -y make git-all

git clone https://gitlab.com/sominsong97/hyper-seccomp.git
cd hyper-seccomp
make build
```
if you meet `make:execvp *.sh: Permission denied` error, please enter below command first.
```
chmod 755 configure.sh setup.sh
```

## How to run

You should be a **sudo-privileged user** or run it with **sudo privileges**.
There is help option(-h) for providing short explanations for all options.
Except for the help option, the remaining options are executed in the following order.

You can run all options in sequence at once with following -a option (in progress) 

```
./run.sh -A
```

Each execution command and process are as follows:

1. Crawl exploit codes and information related to the exploit codes collected.

    ```
    ./run.sh -C
    ```

    After this process, The exploit code for each source is collected in each source folder under the `exploit` folder of the project folder. 
    Also, `exploit.json` with information about the exploit collected under the `/opt/output/perm/` folder is created.

2. Analyze the exploit code and generate mapping the library functions used in the exploit codes and the syscall sequences invoked by the library functions.

    ```
    ./run.sh -S
    ```

    After this process, GCC GIMPLE files (`*.original` files) for each exploit code are created under `/opt/output/temp/` folder.
    
    And unit test codes for the usecases of the library functions used in each exploit code are created under the `/opt/output/temp/testcase` folder.
    The name of the test code of the library function is in the following format:
    `{library function name}-{exploit-ID}-{function name in the code where the library function is used}-{(optional) delimiter number when used multiple times in the same function}`
    of
    `{library function name}-default-default`

    Also, the execution results of the unit test codes of each library functions are parsed and saved in the form of a system call sequence (sequence consisting of system call numbers) under the `/opt/output/temp/testcase/result/` folder.

3. Generate library function execution paths by analyzing the control flow graph (CFG) of the exploit codes, and Generate the syscall execution paths (sequences) of the exploit codes by combining it with the result of step 2 ('library function-syscall sequnece' mapping).

    ```
    ./run.sh -P
    ```

    After this process, control flow graphs (`*.cfg` files) for each exploit code are created under `/opt/output/temp/` folder.
    Also, the sets of all possible paths consisting of a sequence of system calls for each exploit code are created under the path `/opt/output/perm/path/`. It is saved in a json file format, and the file name means the ID of each exploit code as follow: `{exploit-ID}.json`. The file shows the sequence of system call numbers for each user-defined function.


4. Generate N-gram patterns from the 'exploit-syscall sequence' mapping obtained as a result of step 3.

    ```
    ./run.sh -N
    ```

    After this process, 3 files (`{date}_ngram_sysname_max200.csv`, `{date}_ngram_sysnum_max200.csv`, `ngram_result.pkl`) are created under the `/opt/output/perm/analysis/` folder.
    Each file is as follows:
    - `{date}_ngram_sysname_max200.csv`: It is a csv file consisting of the 'N-gram pattern length, the number of exploit codes from which the N-gram pattern is extracted, and the N-gram pattern consisting of syscall names' columns.
    - `{date}_ngram_sysnum_max200.csv`: It is a csv file consisting of the 'N-gram pattern length, the number of exploit codes from which the N-gram pattern is extracted, and the N-gram pattern consisting of syscall numbers' columns.
    - `ngram_result.pkl`: It is a file that saves a dictionary in the form of `{'N-gram pattern':'Number of exploits with N-gram pattern found'}` in binary format.

5. By testing 15 applications, Extract benign syscall sequence that is invoked when each application opereates normally. This option is only for settings for application testing. Application tests need to be manually executed through individual commands because of the ftrace setting.

    ```
    ./run.sh -B
    ```
