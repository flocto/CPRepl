import os
import termcolor
import argparse
from config import TEMPLATES, VERSION
from cprepl import CPRepl

def main():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="CPHelper", description="CLI tool for competitive programming")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + VERSION)
    parser.add_argument('--list', action='store_true',
                        help='List all available templates')
    
    parser.add_argument('path', nargs='?', default='.', help='Path to contest directory (will be created if it does not exist)')

    args = parser.parse_args()
    if args.list:
        print("Available templates:")
        for template in TEMPLATES:
            print(termcolor.colored(f"  - {template}", 'blue'))
    else:
        if not os.path.exists(args.path):
            os.makedirs(args.path)
            print(termcolor.colored(
                f"Created directory {args.path}", 'green'))
        else:
            print(termcolor.colored(
                f"Using existing directory {args.path}", 'green'))
        
        repl = CPRepl(args.path)
        repl.run()