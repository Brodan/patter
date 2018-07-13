# patter

> Pipe stdout directly to [Mattermost](https://mattermost.com/).

## Install

```
$ pip install patter
```

Then set the following environtment variables based on your Mattermost server's config:
```
MATTERMOST_TEAM_NAME
MATTERMOST_URL
MATTERMOST_USERNAME
MATTERMOST_PASSWORD
MATTERMOST_PORT
```

## Usage

> Send a message to a user.
```
$ echo "testing" | patter -u some_user
```

> Send a message to a channel.
```
$ echo "testing" | patter -c town-square
```

## Todo
- [] remove prints and add logging
- [] add unit tests via pytest
- [] handle verbose flag for logging
- [] allow text that is not UTF-8 to be sent
- [] add option of reading from a .patter file instead of using env vars.

## Contribute

PRs accepted.

## License

MIT © Christopher Hranj
