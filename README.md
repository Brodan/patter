# patter

> Pipe stdout directly to [Mattermost](https://mattermost.com/).

![patter demo](https://github.com/Brodan/patter/blob/master/demo.gif)

## Install

```
$ pip install patter
```

Then set the following environment variables based on your Mattermost server's config:
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
- [ ] remove prints and add logging with verbose flag
- [ ] add unit tests via pytest
- [ ] allow text that is not UTF-8 to be sent
- [ ] add option of reading from a .patter file instead of using env vars.
- [ ] allow file attachments via -f flag

## Contribute

PRs accepted.

## License

MIT © Christopher Hranj

Notice: This project was developed in part during my 10% time at [Truveris, Inc](https://www.truveris.com/).
