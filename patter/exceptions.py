
class MissingPipeException(Exception):
    """Raise when patter is called without receiving input with the pipe operator."""
    pass


class MissingChannel(Exception):
    """Raise when the requested Mattermost channel does not exist."""
    pass


class MissingUser(Exception):
    """Raise when the requested Mattermost user does not exist."""
    pass


class MissingTeamName(Exception):
    """Raise when the user has not configured a Mattermost team name."""
    pass
