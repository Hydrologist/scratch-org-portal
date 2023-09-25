import json
import os
import subprocess
import sys
import tempfile

from . import auth_url, utils

from .models import Organization, SalesforceUser

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
        "Sites",
        "StateAndCountryPicklist",
        "Workflow"
    ],
    "namespace": "KGRenewal",
    "objectSettings": {
        "opportunity": {
            "sharingModel": "private"
        }
    },
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
    }
}


def sf_run(command, key_list:list=[], use_json=True) -> dict:
    if use_json or len(key_list) != 0:
        command = command + ' --json'
    result = utils.run('sf ' + command)
    
    # Parse JSON response
    if len(result['stderr']) > 1: # sf returns a status of 1 for warnings, including new version warnings
        return {'status': 1, 'result': result['stderr']}
    if use_json:
        data = json.loads(result['stdout'])
    else:
        data = result['stdout']

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
    return sf_run('org list')

def get_org_info(username: str) -> dict:
    return sf_run('org display -o "{}"'.format(username))

def get_user_info(username:str) -> dict:
    return sf_run('org display user -o "{}"'.format(username))

def generate_user_password(username:str) -> dict:
    return sf_run('org generate password -o "{}"'.format(username))

def get_login_url(username:str) -> dict:
    return sf_run('org open -o "{}" -r'.format(username))

def delete_org(alias:str) -> dict:
    return sf_run('org delete scratch -o "{}" -p'.format(alias))

def create_scratch_org(alias:str) -> dict:
    config_json = json.dumps(default_config)
    with tempfile.NamedTemporaryFile(mode='w+') as config_file:
        config_file.write(config_json)
        config_file.flush()

        create_command = '''org create scratch -f "{}" -v "{}" -a "{}" --name="{}"'''\
                            .format(config_file.name, auth_url.
                                    get_username(), alias, alias)
        
        result = sf_run(create_command)
        if result['status'] != 0:
            return {'status': result['status'], 'data': result['name'] + ': ' + result['message'] + '\n\nActions: ' + result['actions']}

        return result

def sfdx_test():
    return str(authenticate(auth_url.get_username(), auth_url.get_key_file_path(), auth_url.get_consumer_key()))
