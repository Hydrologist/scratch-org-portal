import json
import os
import subprocess
from subprocess import PIPE
import sys
import tempfile

default_config = {
    "orgName": "Scratch Org",
    "edition": "Developer",
    "features": ["API", "AuthorApex", "Communities", "DebugApex",
                 "PlatformEncryption", "ProcessBuilder", "Sites",
                 "StateAndCountryPicklist"],
    "settings": {
        "orgPreferenceSettings": {
            "chatterEnabled": True,
            "networksEnabled": True,
            "s1DesktopEnabled": True,
            "s1EncryptedStoragePref2": False
        }
    }
}

def sfdx_run(command: str) -> dict:
    output = subprocess.run('sfdx ' + command, encoding='utf-8',
                            stdout=PIPE, stderr=PIPE, shell=True)

    result = {
        'stdout': output.stdout,
        'stderr': output.stderr,
    }
    return result

def sfdx_test():
    return sfdx_run('version')['stdout']
