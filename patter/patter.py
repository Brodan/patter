import os
# import logging

from mattermostdriver import Driver
from requests.exceptions import ConnectionError, HTTPError

from patter.exceptions import (
    FileUploadException,
    MissingChannel,
    MissingEnvVars,
    MissingUser,

)


config_vars = {
    "MATTERMOST_TEAM_NAME": os.getenv("MATTERMOST_TEAM_NAME", None),
    "MATTERMOST_URL": os.getenv("MATTERMOST_URL", None),
    "MATTERMOST_USERNAME": os.getenv("MATTERMOST_USERNAME", None),
    "MATTERMOST_PASSWORD": os.getenv("MATTERMOST_PASSWORD", None),
    "MATTERMOST_PORT": os.getenv("MATTERMOST_PORT", None),
}


class Patter(object):

    def __init__(self, message, filename, format_as_code, user, channel, verbose):
        self.message = self._format_message(message, format_as_code)
        self.filename = filename
        self.user = user
        self.channel = channel
        self.verbose = verbose

        self._check_env_vars()

        self.mm_client = Driver({
            "url": config_vars["MATTERMOST_URL"],
            "login_id": config_vars["MATTERMOST_USERNAME"],
            "password": config_vars["MATTERMOST_PASSWORD"],
            "scheme": "https",
            "port": int(config_vars["MATTERMOST_PORT"]),
            "basepath": "/api/v4",
            "verify": True,
            "timeout": 30,
            "debug": False,
        })
        self.team_name = config_vars["MATTERMOST_TEAM_NAME"]

        try:
            self.mm_client.login()
        except ConnectionError:
            print("Unable to connect to the configured Mattermost server.")
            raise

    def send_message(self):
        """Send the message."""
        channel_id = self._get_message_channel_id()

        attached_file_id = None
        if self.filename:
            attached_file_id = self._attach_file(self.filename, channel_id)

        options = {
            "channel_id": channel_id,
            "message": self.message,
        }
        if attached_file_id:
            options["file_ids"] = [attached_file_id]

        self.mm_client.posts.create_post(options)

    def _format_message(self, message, format_as_code):
        """Adds formatting to the given message.

        :param message: Message for format
        :param format_as_code: Boolen if message should be formatted as code.

        :returns: Formatted message.

        """
        formatted_message = message
        if format_as_code:
            formatted_message = "```\n{}```".format(message)
        formatted_message += "\n⁽ᵐᵉˢˢᵃᵍᵉ ᵇʳᵒᵘᵍʰᵗ ᵗᵒ ʸᵒᵘ ᵇʸ ᵖᵃᵗᵗᵉʳ⁾"
        return formatted_message

    def _get_message_channel_id(self):
        """Get the channel to send the message to.

        :returns: Channel id string.

        """

        if self.channel:
            try:
                return self._get_channel_id_by_name(self.channel)
            except HTTPError:
                raise MissingChannel(
                    "The channel \'{}\' does not exist.".format(
                        self.channel,
                    ))

        if self.user:
            return self._get_channel_id_for_user(self.user)

    def _get_channel_id_by_name(self, channel_name):
        """Use this function to get an ID from a channel name.

        :param channel_name: Name of channel
        :returns: Channel id string.

        """
        channel = self.mm_client.channels.get_channel_by_name_and_team_name(
            team_name=self.team_name,
            channel_name=channel_name,
        )
        return channel["id"]

    def _get_channel_id_for_user(self, user_name):
        """Get the channel id for a direct message with the target user.

        :returns: Channel id string.

        """
        try:
            recipient_user_id = self._get_user_id_by_name(user_name)
        except HTTPError:
            raise MissingUser("The user \'{}\' does not exist.".format(
                user_name,
            ))
        my_id = self.mm_client.users.get_user("me")["id"]

        # The Mattermost API treats direct messages the same as regular
        # channels so we need to first get a channel ID to send the direct
        # message.
        user_channel = self.mm_client.channels.create_direct_message_channel(
            [recipient_user_id, my_id]
        )
        return user_channel["id"]

    def _get_user_id_by_name(self, user_name):
        """The Mattermost API expects a user ID, not a username.

        Use this function to get an ID from a username.

        :param user_name: Name of user to get user id for.

        :returns: User id string.

        """
        user = self.mm_client.users.get_user_by_username(
            username=user_name,
        )
        return user["id"]

    def _check_env_vars(self):
        """Check that all of the required environment variables are set.

        If not, raise exception noting the ones that are missing.

        :raises: MissingEnvVars.
        """
        missing_vars = list(k for k, v in config_vars.items() if v is None)
        if len(missing_vars) > 0:
            error_string = "\n\t".join(missing_vars)
            raise MissingEnvVars(
                "The following environment variables are required but not set:\n\t{}".format(
                    error_string
                )
            )

    def _attach_file(self, filename, channel_id):
        """Attach the given filename into the given channel.

        :param filename: Name of file to attach.
        :param channel_id: Id string of channel to attach file to.

        :returns; Id string of file attachment.

        """
        response = self.mm_client.files.upload_file(
            channel_id=channel_id,
            files={"files": (filename, open(filename))}
        )
        try:
            file_id = response["file_infos"][0]["id"]
        except (KeyError, IndexError):
            raise FileUploadException("Unable to upload file '{}'".format(filename))
        return file_id
