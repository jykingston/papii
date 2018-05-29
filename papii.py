import requests
import json
import csv

header = {'grant_type': 'client_credentials'}
base_url = 'https://api.plagscan.com/v3/'
method = {'token': 'token', 'users': 'users?', 'userMod': 'users/'}
line_break = '---------------------'

# get the damn access token


def get_access_token(client_id, apikey):
    r = requests.post(url=base_url + (method['token']), data={
                      'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': apikey})
    access_token = r.json()
    print(line_break)
    access_token = (access_token['access_token'])
    print'access token for ' + \
        ('client id ' + (client_id)) + '\n' + ('access token ' + access_token)
    return access_token

# Print basic details about the users of an account


def get_user_details_func(access_token):
    get_users = requests.get(
        url=base_url + (method['users']) + 'access_token=' + (access_token['access_token']))
    get_user_details = get_users.json()
    print(line_break + '\n')
    print('Internal ID ' + get_user_details['data'][0]['internalID'])
    get_user_indiv = requests.patch(url=base_url + (method['userMod']) + (
        get_user_details['data'][0]['internalID']) + '?&access_token=' + (access_token['access_token']))
    get_user_indiv_details = get_user_indiv.json()
    print('Username ' + get_user_details['data'][0]['username'])
    print('\nBelow are the current settings')
    print(line_break)
    print('Institution Mode: ' +
          get_user_indiv_details['data']['institutionMode'])
    print('Check Plagiarism: ' + get_user_indiv_details['data']['checkPS'])
    print('Email Notifs: ' + get_user_indiv_details['data']['emailPolicy'])
    print('Check Org Repo: ' +
          get_user_indiv_details['data']['checkOrgaRepository'])
    print('Check Own repo: ' +
          get_user_indiv_details['data']['checkOwnRepository'])
    print('Bibliography check: ' +
          get_user_indiv_details['data']['biblioPolicy'])
    print('Check Documents: ' + get_user_indiv_details['data']['checkPolicy'])
    print('Check Internets: ' + get_user_indiv_details['data']['checkNetwork'])
    print('Automatic Checks: ' + get_user_indiv_details['data']['autoPolicy'])
    print('Check Citation: ' + get_user_indiv_details['data']['citePolicy'])
    internal_id = get_user_details['data'][0]['internalID']
    return internal_id

# Check if they have plagarism against the internet on


def check_ps(access_token, internal_id):
    print(line_break)
    print('Setting Check PS - updating')
    update_ps = requests.patch(url=base_url + (method['userMod']) + (internal_id) + '?&access_token=' + (access_token['access_token']), params='checkPS=1')
    updated_ps = update_ps.json()
    print('The Plagarsim Check is set to ' + updated_ps['data']['checkPS'])

# Check if they are sending auto emails


def check_email(access_token, internal_id):
    print(line_break)
    print('Setting Check Email - updating')
    update_email = requests.patch(url=base_url + (method['userMod']) + (internal_id) + '?&access_token=' + (access_token['access_token']), params='email=0')
    updated = update_email.json()
    print('Email is set to ' + updated['data']['emailPolicy'])

# Update the biblio


def check_biblio(access_token, internal_id):
    print(line_break)
    print('Setting biblioPolicy - updating')
    update_biblio = requests.patch(url=base_url + (method['userMod']) + (internal_id) + '?&access_token=' + (access_token['access_token']), params='biblio=1')
    updated = update_biblio.json()
    print('Biblio Policy is set to ' + updated['data']['biblioPolicy'])

# Update the Citation setting


def check_cite(access_token, internal_id):
    print(line_break)
    print('Setting citePolicy - updating')
    update_cite = requests.patch(url=base_url + (method['userMod']) + (internal_id) + '?&access_token=' + (access_token['access_token']), params='cite=2')
    updated = update_cite.json()
    print('Citation Policy is set to ' + updated['data']['citePolicy'])

# Check if they have Documnet Archiving Enabled, 3= Never archive


def check_cleanup(access_token, internal_id):
    print(line_break)
    print('Setting cleanupPolicy - updating')
    update_cite = requests.patch(url=base_url + (method['userMod']) + (internal_id) + '?&access_token=' + (access_token['access_token']), params='cleanup=3')
    updated = update_cite.json()
    print('Cleanup is set to ' + updated['data']['cleanupPolicy'])


with open('tokens.csv') as tokens:
    readCSV = csv.reader(tokens, delimiter=',')
    apikey = []
    client_id = []
    for row in readCSV:
        apikey = row[0]
        client_id = row[1]
        header['apikey'] = apikey
        header['client_id'] = client_id
        get_access_token(client_id, apikey)
        r = requests.post(url=base_url + (method['token']), data={
                          'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': apikey})
        access_token = r.json()
        get_users = requests.get(
            url=base_url + (method['users']) + 'access_token=' + (access_token['access_token']))
        internal_id = get_users.json()
        get_user_details_func(access_token)
        check_ps(access_token, internal_id['data'][0]['internalID'])
        check_email(access_token, internal_id['data'][0]['internalID'])
        check_biblio(access_token, internal_id['data'][0]['internalID'])
        check_cite(access_token, internal_id['data'][0]['internalID'])
        check_cleanup(access_token, internal_id['data'][0]['internalID'])

