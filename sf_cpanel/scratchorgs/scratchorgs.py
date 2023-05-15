import json
import os
import subprocess
import sys
import tempfile

from . import auth_url, utils

default_config = {
    "orgName": "Scratch Org",
    "edition": "Developer",
    "features": [
        "API",
        "AuthorApex",
        "Communities",
        "DebugApex",
        "Interaction",
        "LightningSalesConsole",
        "LightningServiceConsole",
        "Multicurrency",
        "PlatformEncryption",
        "ProcessBuilder",
        "RecordTypes",
        "SalesUser",
        "ServiceCloud",
        "SiteDotCom",
        "Sites",
        "StateAndCountryPicklist",
        "Workflow"
    ],
    "settings": {
        "chatterSettings": {
            "enableChatter": True,
        },
        "communitiesSettings": {
            "enableNetworksEnabled": True
        },
        "lightningExperienceSettings": {
            "enableS1DesktopEnabled": True
        },
        "mobileSettings": {
            "enableS1EncryptedStoragePref2": True
        }
    },
    "objectSettings": {
        "opportunity": {
            "sharingModel": "private"
        }
    }
}


def sf_run(command, key_list:list=[], use_json=True) -> dict:
    if use_json or len(key_list) != 0:
        command = command + ' --json'
    result = utils.run('sf ' + command)

    if use_json and len(key_list) == 0:
        return result
    
    # Parse JSON response
    if len(result['stderr']) > 0:
        return {'status': 1, 'result': result['stderr']}
    data = json.loads(result['stdout'])
    
    # Return data if we are not looking for a particular key or we
    # received an error.
    if len(key_list) == 0 or data['status'] != 0:
        return data
    
    # Loop over the keys in the list and navigate down
    # into the response
    current_node = data['result']
    for key in key_list:
        current_node = current_node[key]
    return {'status': 0, 'result': current_node}

def authenticate(username:str, key_file:str, client_id:str):
    # Create a temporary file to pass the authentication URL 
    # to the SFDX CLI.
    auth_command = '''login org jwt --username "{}" --keyfile "{}" 
                      --clientid "{}"'''.format(username, 
                                              key_file, 
                                              client_id)
    data = sf_run(auth_command)
    return data['result']
    with tempfile.NamedTemporaryFile(mode='w+') as auth_file:
        try:
            # Write the url to the file and flush the buffer.
            auth_file.write(auth_url.get_auth_url())
            auth_file.flush()

            # Format the command with the filename.
            auth_command = 'force:auth:sfdxurl:store -f "{}"'.format(
                auth_file.name)

            # Run the command and extract its output.
            data = sfdx_run(auth_command)
            # Return the username.
            return data['result']['username']
        except Exception as e:
            return e

def get_org_list() -> dict:
    data = sf_run('org list')
    return data['result']

def get_org_url(target:str) -> dict:
    data = sf_run('org open -r -u ' + target, [])
    return data

def get_org_info(username: str) -> dict:
    data = sf_run('org display -o {}'.format(username))
    return data

def get_user_info(username:str) -> dict:
    data = sf_run('org display user -o {}'.format(username))
    return data

def create_scratch_org(alias:str) -> dict:
    config_json = json.dumps(default_config)
    with tempfile.NamedTemporaryFile(mode='w+') as config_file:
        config_file.write(config_json)
        config_file.flush()

        create_command = '''org create scratch -f "{}" -v "{}" -a "{}" --name="{}"'''\
                            .format(config_file.name, auth_url.
                                    get_username(), alias, alias)
        
        result = sf_run(create_command)
        print(json.dumps(result))

        org_info = json.loads(result['stdout'])

        return org_info['username']

def sfdx_test():
    return str(authenticate(auth_url.get_username(), auth_url.get_key_file_path(), auth_url.get_consumer_key()))
