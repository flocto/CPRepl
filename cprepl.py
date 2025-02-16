import os
import shlex
import subprocess
import argparse
import termcolor
from config import TEMPLATES, LANGUAGE_PREF, VERSION, COMPILE_CMDS, TIMEOUT, JAVA_MEMLIM
import string
import readline
readline.set_auto_history(False)

FILENAME_CHARS = string.ascii_lowercase + \
    string.ascii_uppercase + string.digits + '_.'


def _run_py(file):
    # suggest using pypy for performance
    return subprocess.Popen(['python3', file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _run_cpp(file):
    file = os.path.basename(file)
    name = file.split('.', 1)[0]
    print(termcolor.colored(f"Compiling {name}.cpp", 'blue'))
    compile_cmd = COMPILE_CMDS['cpp'].format(name=name)
    compile_out = subprocess.run(shlex.split(
        compile_cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if compile_out.returncode != 0:
        print(compile_out.stderr.decode('utf-8'))
        print(termcolor.colored(
            f"Compilation failed with exit code {compile_out.returncode}", 'red'))
        return None
    print(termcolor.colored(f"Finished compiling {name}.cpp, running", 'green'))
    return subprocess.Popen(['./' + name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _run_java(file):
    file = os.path.basename(file)
    name = file.split('.', 1)[0]
    print(termcolor.colored(f"Compiling {name}.java", 'blue'))
    compile_cmd = COMPILE_CMDS['java'].format(name=name)
    compile_out = subprocess.run(shlex.split(
        compile_cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if compile_out.returncode != 0:
        print(compile_out.stderr.decode('utf-8'))
        print(termcolor.colored(
            f"Compilation failed with exit code {compile_out.returncode}", 'red'))
        return None

    print(termcolor.colored(f"Finished compiling {name}.java, running", 'green'))
    run_cmd = f'java -Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms{JAVA_MEMLIM}m -Xmx{JAVA_MEMLIM}m {name}'
    return subprocess.Popen(shlex.split(run_cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class CPRepl:
    def __init__(self, path):
        self.path = path
        self.files = {}
        self._read_files()

    def _read_files(self):
        for file in os.listdir(self.path):
            if file.endswith('.cpp') or file.endswith('.py') or file.endswith('.java'):
                name, lang = file.rsplit('.', 1)
                if name not in self.files:
                    self.files[name] = set()
                self.files[name].add(lang)

    def _print_help(self):
        msg = """- "clear" or "cls": clear the screen
- "ls": list all files
- "rm": remove a file (must be full file name)
- "q" or "quit": quit the program
- "help": show these instructions
- "!": run shell command"""
        print(termcolor.colored(msg, 'cyan'))

    def _print_header(self):
        msg = f"""

 $$$$$$\  $$$$$$$\  $$\   $$\           $$\                               
$$  __$$\ $$  __$$\ $$ |  $$ |          $$ |                              
$$ /  \__|$$ |  $$ |$$ |  $$ | $$$$$$\  $$ | $$$$$$\   $$$$$$\   $$$$$$\  
$$ |      $$$$$$$  |$$$$$$$$ |$$  __$$\ $$ |$$  __$$\ $$  __$$\ $$  __$$\ 
$$ |      $$  ____/ $$  __$$ |$$$$$$$$ |$$ |$$ /  $$ |$$$$$$$$ |$$ |  \__|
$$ |  $$\ $$ |      $$ |  $$ |$$   ____|$$ |$$ |  $$ |$$   ____|$$ |      
\$$$$$$  |$$ |      $$ |  $$ |\$$$$$$$\ $$ |$$$$$$$  |\$$$$$$$\ $$ |      
 \______/ \__|      \__|  \__| \_______|\__|$$  ____/  \_______|\__|      
                                            $$ |                          
                                            $$ |                          
                                            \__|      v{VERSION}                    """
        print(termcolor.colored(msg, 'dark_grey'))
        msg = """
Welcome to CPHelper! This is a helper tool meant to assist you during competitive programming contests.

Entering the letter of a problem will run the associated file for that problem, 
choosing the first language in the LANGUAGE_PREF list that has been defined in the config.
> a

You can also directly call a specific file by entering the name of the file itself.
When passing in input, terminate the file with EOF signal (Ctrl-D).
> a.py
1
(EOF)

To run with file input, enter the letter or filename followed by the name of the input file.
> a.py inp.txt

If a file is not found, it will be created for you with a default template,
following the LANGUAGE_PREF list or with the specified language if it is provided.

There are also a few built-in commands:"""
        print(termcolor.colored(msg, 'cyan'))
        self._print_help()

    def list_files(self):
        print(termcolor.colored('---FILES---', 'light_grey'))
        for name, langs in self.files.items():
            print(termcolor.colored(f"{name}: {', '.join(langs)}", 'green'))

    def create_file(self, name, lang=None):
        if lang not in TEMPLATES:
            print(termcolor.colored(
                f"Template for {lang} not found, creating empty file", 'yellow'))
            template = ""
        else:
            template = TEMPLATES[lang]

        with open(os.path.join(self.path, name + '.' + lang), 'w') as f:
            f.write(template)
            self.files[name].add(lang)
            print(termcolor.colored(f"Created file {name}.{lang}", 'green'))\


    def read_input(self):
        inp = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            inp.append(line)
        return '\n'.join(inp)

    def run_file(self, file, lang, inp) -> str | None:
        file = os.path.join(self.path, file)
        if lang == 'py':
            proc = _run_py(file)
        elif lang == 'cpp':
            proc = _run_cpp(file)
        elif lang == 'java':
            proc = _run_java(file)
        else:
            print(termcolor.colored(f"Language {lang} not supported", 'red'))
            return

        if proc is None:
            return None

        try:
            output, err = proc.communicate(
                input=inp.encode('utf-8'), timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            proc.kill()
            print(termcolor.colored(
                f"Process timed out after {TIMEOUT} seconds", 'red'))
            return None

        if proc.returncode != 0:
            print(err.decode('utf-8'))
            print(termcolor.colored(
                f"Process exited with code {proc.returncode}", 'red'))
            return output.decode('utf-8').strip()

        return output.decode('utf-8').strip()

    def run(self):
        self._print_header()

        while True:
            cmd = input(termcolor.colored("> ", 'green'))
            readline.add_history(cmd)
            if cmd in ['q', 'quit']:
                break
            elif cmd in ['clear', 'cls']:
                print(termcolor.colored("\033[H\033[J", 'white'))
                continue
            elif cmd == 'ls':
                self.list_files()
                continue
            elif cmd == 'help':
                self._print_help()
                continue
            elif cmd.startswith('!'):
                subprocess.run(cmd[1:], cwd=self.path, shell=True)
                continue

            if cmd == '':
                continue

            parser = argparse.ArgumentParser()
            parser.add_argument('file', nargs='?', help='File to run')
            parser.add_argument('input', nargs='?', help='Input file')
            args = parser.parse_args(cmd.split())

            file = args.file
            inp = args.input
            lang = None

            if file is None:  # this should never happen but just in case
                print(termcolor.colored("No file specified", 'red'))
                continue

            # handle rm here
            if file == 'rm':
                if args.input is None:
                    print(termcolor.colored(
                        "No input file specified", 'red'))
                    continue

                filename = args.input
                if filename not in os.listdir(self.path):
                    print(termcolor.colored(
                        f"File {filename} not found", 'red'))
                    continue

                file, lang = filename.rsplit('.', 1)
                if lang not in self.files[file]:
                    print(termcolor.colored(
                        f"File {file}.{lang} not found", 'yellow'))
                    continue
                os.remove(os.path.join(self.path, file + '.' + lang))
                self.files[file].remove(lang)
                if len(self.files[file]) == 0:
                    del self.files[file]
                print(termcolor.colored(
                    f"Removed file {file}.{lang}", 'green'))
                continue

            if any(c not in FILENAME_CHARS for c in file):
                print(termcolor.colored(
                    f"Invalid filename {file}", 'red'))
                continue

            if '.' in file:
                file, lang = file.rsplit('.', 1)

            if file not in self.files:
                self.files[file] = set()

            if lang is None:
                # pick from existing first
                for l in LANGUAGE_PREF:
                    if l in self.files[file]:
                        lang = l
                        break
                # otherwise, first preferred
                if lang is None:
                    lang = LANGUAGE_PREF[0]

            if lang not in self.files[file]: 
                print(termcolor.colored(
                    f"File {file} not found, creating file", 'yellow'))
                self.create_file(file, lang)
                continue

            print(termcolor.colored(f"Running {file}.{lang}", 'blue'))

            if inp is not None:
                inp = os.path.join(self.path, inp)
                if not os.path.exists(inp):
                    print(termcolor.colored(
                        f"Input file {inp} not found, using stdin", 'yellow'))
                    inp = None
                else:
                    inp = open(inp, 'r').read()
                    print(termcolor.colored(
                        f"Using input file {inp}", 'green'))

            if inp is None:
                inp = self.read_input()

            output = self.run_file(file + '.' + lang, lang, inp)
            if output is not None:
                print(termcolor.colored('---OUTPUT---', 'light_grey'))
                print(output)
