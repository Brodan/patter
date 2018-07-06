import os

from mattermostdriver import Driver
from requests.exceptions import ConnectionError, HTTPError

from patter.exceptions import MissingTeamName, MissingUser, MissingChannel


class Patter(object):

    def __init__(self, message, format_as_code, user, channel):
        self.message = message
        self.format_as_code = format_as_code
        self.user = user
        self.channel = channel

        self.team_name = os.getenv("MATTERMOST_TEAM_NAME", None)
        if not self.team_name:
            raise MissingTeamName(
                "The MATTERMOST_TEAM_NAME environment variable must be set.")

        self.mm_client = Driver({
            "url": os.getenv("MATTERMOST_URL"),
            "login_id": os.getenv("MATTERMOST_USERNAME"),
            "password": os.getenv("MATTERMOST_PASSWORD"),
            "scheme": "https",
            "port": int(os.getenv("MATTERMOST_PORT", 8065)),
            "basepath": "/api/v4",
            "verify": True,
            "timeout": 30,
            "debug": False,
        })

        try:
            self.mm_client.login()
        except ConnectionError:
            print("Unable to connect to the configured Mattermost server.")
            raise

    def send_message(self):
        if self.format_as_code:
            self.message = "```\n{}```".format(self.message)

        if self.channel:
            try:
                channel_id = self._get_channel_id_by_name(self.channel)
            except HTTPError:
                raise MissingChannel("The channel \'{}\' does not exist.".format(
                    self.channel,
                ))
            self.mm_client.posts.create_post(options={
                "channel_id": channel_id,
                "message": self.message,
            })

        if self.user:
            try:
                recipient_user_id = self._get_user_id_by_name(self.user)
            except HTTPError:
                raise MissingUser("The user \'{}\' does not exist.".format(
                    self.user,
                ))
            my_id = self.mm_client.users.get_user('me')['id']

            user_channel_id = self.mm_client.channels.create_direct_message_channel(
                [recipient_user_id, my_id]
            )['id']

            self.mm_client.posts.create_post(options={
                "channel_id": user_channel_id,
                "message": self.message,
            })

        print("Mattermost message sent!")
        return

    def _get_channel_id_by_name(self, channel_name):
        channel = self.mm_client.channels.get_channel_by_name_and_team_name(
            team_name=self.team_name,
            channel_name=channel_name,
        )
        return channel["id"]

    def _get_user_id_by_name(self, user_name):
        user = self.mm_client.users.get_user_by_username(
            username=user_name,
        )
        return user["id"]
