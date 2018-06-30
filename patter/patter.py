import os
import sys

from mattermostdriver import Driver

driver = Driver({
    """
    Required options

    Instead of the login/password, you can also use a personal access token.
    If you have a token, you don't need to pass login/pass.
    """
    'url': 'mattermost.server.com',
    'login_id': 'user.name',
    'password': 'verySecret',


    'scheme': 'https',
    'port': 8065,
    'basepath': '/api/v4',
    'verify': True,
    'mfa_token': 'YourMFAToken',

    """
    If for some reasons you get regular timeouts after a while, try to decrease
    this value. The websocket will ping the server in this interval to keep the connection
    alive.
    If you have access to your server configuration, you can of course increase the timeout
    there.
    """
    'timeout': 30,

    'debug': False
})

driver.login()
