# Syscall Attack Sequence

Analysis of Syscall Attack Sequence from Exploit Codes

## Notion

This project is managed on the [Notion](https://flame-appeal-2c5.notion.site/064b5204333944b7bcbcf6da2aa50c92?v=562fac4f80634990a9aed0fde193c9fe).

Also, the progress of the project can be checked on the [Milestones](https://gitlab.com/sominsong97/syscall-attack-sequence/-/issues).


## Getting started

```
sudo su
apt update
apt install -y git-all

git clone https://gitlab.com/sominsong97/syscall-attack-sequence.git
cd syscall-attack-sequence
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

1. Crawling exploit codes and information related to the exploit codes collected.

```
sudo bash run.sh -C
```

After this process, The exploit code for each source is collected in each source folder under the 'exploit' folder of the project folder. 
Also, 'exploit.json' with information about the exploit collected under the '/opt/output/perm/' folder is created.

2. Generate library function path from each exploit codes collected (in progress)

```
sudo bash run.sh -P
```

3. Generate system call sequences for library functions included in the exploit code's path (in progress)

```
sudo bash run.sh -S
```

4. System call path creation for each exploit code by integrating library function path information for each exploit code and system call sequence information for each library function (in progress)

```
sudo bash run.sh -M
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/-/experiment/new_project_readme_content:9d8f5800ac35c2b50894260a4b1ebd9e?https://gitlab.com/sominsong97/syscall-attack-sequence/-/settings/integrations)