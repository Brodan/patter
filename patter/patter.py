
import os
# import logging

from mattermostdriver import Driver
from requests.exceptions import ConnectionError, HTTPError

from patter.exceptions import MissingUser, MissingChannel


class Patter(object):

    def __init__(self, message, format_as_code, user, channel, verbose):
        self.message = message
        self.format_as_code = format_as_code
        self.user = user
        self.channel = channel
        self.verbose = verbose

        self._check_env_vars()

        self.team_name = os.getenv("MATTERMOST_TEAM_NAME")
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
        self.message += "\n⁽ᵐᵉˢˢᵃᵍᵉ ᵇʳᵒᵘᵍʰᵗ ᵗᵒ ʸᵒᵘ ᵇʸ ᵖᵃᵗᵗᵉʳ⁾"

        if self.channel:
            self._send_message_to_channel()

        if self.user:
            self._send_message_to_user()

        return

    def _send_message_to_channel(self):
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

    def _send_message_to_user(self):
        try:
            recipient_user_id = self._get_user_id_by_name(self.user)
        except HTTPError:
            raise MissingUser("The user \'{}\' does not exist.".format(
                self.user,
            ))
        my_id = self.mm_client.users.get_user('me')['id']

        # The Mattermost API treats direct messages the same as regular channels,
        # so we need to first get a channel ID to send the direct message.
        user_channel_id = self.mm_client.channels.create_direct_message_channel(
            [recipient_user_id, my_id]
        )['id']

        self.mm_client.posts.create_post(options={
            "channel_id": user_channel_id,
            "message": self.message,
        })

    def _get_channel_id_by_name(self, channel_name):
        """
        The Mattermost API expects a channel ID, not a channel name.
        Use this function to get an ID from a channel name.
        """
        channel = self.mm_client.channels.get_channel_by_name_and_team_name(
            team_name=self.team_name,
            channel_name=channel_name,
        )
        return channel["id"]

    def _get_user_id_by_name(self, user_name):
        """
        The Mattermost API expects a user ID, not a username.
        Use this function to get an ID from a username.
        """
        user = self.mm_client.users.get_user_by_username(
            username=user_name,
        )
        return user["id"]

    def _check_env_vars(self):
        """Check that all of the required environment variables are set. If not,
        print the ones that are missing.
        TODO: Finish implementation
        """
        pass
