
class FileUploadException(Exception):
    """Raise when a file upload fails."""
    pass


class MissingPipeException(Exception):
    """Raise when patter is called without receiving input with the pipe operator."""
    pass


class MissingChannel(Exception):
    """Raise when the requested Mattermost channel does not exist."""
    pass


class MissingUser(Exception):
    """Raise when the requested Mattermost user does not exist."""
    pass


class MissingEnvVars(Exception):
    """Raise when not all the necessary environment variables are set."""
    pass
