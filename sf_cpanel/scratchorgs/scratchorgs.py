import json
import os
import subprocess
import sys
import tempfile

from . import auth_url, utils

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

def sfdx_run(command, json=True) -> dict:
    if json:
        command = command + ' --json'
    return utils.run('sfdx ' + command)

def authenticate():
    # Create a temporary file to pass the authentication URL 
    # to the SFDX CLI.
    with tempfile.NamedTemporaryFile(mode='w+') as auth_file:
        try:
            # Write the url to the file and flush the buffer.
            auth_file.write(auth_url.get_auth_url())
            auth_file.flush()

            # Format the command with the filename.
            auth_command = 'force:auth:sfdxurl:store -f "{}"'.format(
                auth_file.name)

            # Run the command and extract its output.
            result = sfdx_run(auth_command)
            data = json.loads(result['stdout'])
            # Return the username.
            return data['result']['username']
        except Exception as e:
            return e

def get_org_url(target:str):
    result = sfdx_run('force:org:open -r -u ' + target)
    data = json.loads(result['stdout'])
    return data['result']['url']

def get_auth_list():
    result = sfdx_run('auth:list')
    return result['stdout']

def sfdx_test():
    return authenticate()
