import os

VERSION = "0.1.0"

# order of language preference
LANGUAGE_PREF = ['py', 'cpp', 'java']

_template_suffixes = ['.py', '.cpp', '.java']
_template_path = os.path.join(os.path.dirname(__file__), 'templates')
TEMPLATES = {}
if os.path.exists(_template_path):
    for file in os.listdir(_template_path):
        for suffix in _template_suffixes:
            if file == 'template' + suffix:
                TEMPLATES[suffix[1:]] = open(
                    os.path.join(_template_path, file), 'r').read()
                break


# compile commands
COMPILE_CMDS = {
    'cpp': 'g++ -g -O2 -o {name} -std=gnu++23 -static -lrt -Wl,--whole-archive -lpthread -Wl,--no-whole-archive {name}.cpp',
    'java': 'javac -encoding UTF-8 {name}.java',
}

# adjust this as needed
TIMEOUT = 10  # seconds
JAVA_MEMLIM = 1024  # MB
