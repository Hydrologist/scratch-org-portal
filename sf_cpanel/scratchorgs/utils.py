import subprocess
from shlex import quote
from os import environ

def run(args) -> dict:
    if 'SHELL' in environ:
        args = quote(args) # Escape the input for use in the shell. 
                           # Only works in POSIX-compliant shells.
    output = subprocess.run(args, encoding='utf-8', 
                            capture_output=True, shell=True)

    result = {
        'stdout': output.stdout,
        'stderr': output.stderr,
    }
    return result
