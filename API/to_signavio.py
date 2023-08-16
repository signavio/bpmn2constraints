import requests
from conf import *

def authenticate():
    login_url = base_url + '/p/login'
    data = {'name': username,
             'password': password,
             'tokenonly': 'true'}
    if 'workspace_id' in locals():
       data['tenant'] = workspace_id
    # authenticate
    login_request = requests.post(login_url, data)

    # retrieve token and session ID
    auth_token = login_request.content.decode('utf-8')
    jsesssion_ID = login_request.cookies['JSESSIONID']

    # The cookie is named 'LBROUTEID' for base_url 'editor.signavio.com',
    # 'AWSELB' for base_url 'app-au.signavio.com' and 'app-us.signavio.com'
    lb_route_ID = login_request.cookies['LBROUTEID']
    print('auth_token')
    # return credentials
    return {
        'jsesssion_ID': jsesssion_ID,
        'lb_route_ID': lb_route_ID,
        'auth_token': auth_token
    }

authenticate()



