# CPRepl

CPRepl (Competitive Programming REPL) is a small command line tool that helps automate competitive programming tasks. It is written in Python and uses little external libraries. It is designed to be used in a terminal or command prompt.

**NOTE: This project is in early stages of development and only supports Python, C++, and Java.**
Please open an issue or contribute a PR if you would like to see support for other languages.

## Installation
You can clone this repository using:
```bash
git clone https://github.com/flocto/CPRepl.git
```

Then, simply run the main file:
```bash
python3 main.py </path/to/contest/directory>
```

### Linux
You can also add an alias to your `.bashrc` file to run CPRepl from anywhere:
```bash
alias cprepl="python3 /path/to/CPRepl/main.py ."
```

## Running
The only requirement for CPRepl is `termcolor`. You can install it using pip:
```bash
pip install termcolor
```

Then you can run CPRepl using:
```bash
python3 main.py </path/to/contest/directory>
```

## Features
CPRepl will create problem files based on your provided templates and specified language preferences. 

Adjust the templates in `templates/` to suit your needs, as well as any options in `config.py`.

To create a file for a problem, simply type the name of the problem and press enter. For example, to create a file for problem A, type `A` and press enter. To create a file for problem B, type `B` and press enter.
You can also specify the language you want to use by typing `A.py` or `A.cpp` or `A.java`. If you don't specify a language, CPRepl will use the first language specified in `config.py`.

```text
> a
File a not found, creating file
Created file a.py
> a
Running a.py
1
---OUTPUT---

>
```

There are also several built-in commands that you can use:
```text
> help
- "clear" or "cls": clear the screen
- "ls": list all files
- "rm": remove a file (must be full file name)
- "q" or "quit": quit the program
- "help": show these instructions

> ls
---FILES---
a: py
b: py

> rm b
File b not found

> rm b.py
Removed file b.py

> ls
---FILES---
a: py

> q
```

## To-Do
- [ ] Add timer / clock 
- [ ] Add ability to change config in REPL
- [ ] Add tab completion to built-in commands