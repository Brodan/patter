import os

from mattermostdriver import Driver


class Patter(object):

    def __init__(*args):
        print(args)

        mm_client = Driver({
            'url': os.getenv("MATTERMOST_URL"),
            'login_id': os.getenv("MATTERMOST_USERNAME"),
            'password': os.getenv("MATTERMOST_PASSWORD"),
            'scheme': 'https',
            'port': os.getenv("MATTERMOST_PORT", 443),
            'basepath': '/api/v4',
            'verify': True,
            'timeout': 30,
            'debug': False,
        })
        mm_client.login()
