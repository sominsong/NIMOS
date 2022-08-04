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
sudo bash run.sh -A
```

Each execution command and process are as follows.

1. Crawl exploit codes and information related to the exploit codes collected.

```
sudo bash run.sh -C
```

After this process, The exploit code for each source is collected in each source folder under the 'exploit' folder of the project folder. 
Also, 'exploit.json' with information about the exploit collected under the '/opt/output/perm/' folder is created.

2. Analyze the exploit code and generate mapping the library functions used in the exploit codes and the syscall sequences invoked by the library functions.

```
sudo bash run.sh -S
```

3. Generate library function execution paths by analyzing the control flow graph(CFG) of the exploit codes, and Generate the syscall execution paths (sequences) of the exploit codes by combining it with the result of step 2 ("library function-syscall sequnece" mapping).

```
sudo bash run.sh -P
```


4. Generate N-gram sequences from the "exploit-syscall sequence" mapping obtained as a result of step 3.

```
sudo bash run.sh -N
```