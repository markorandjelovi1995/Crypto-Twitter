# important-tweets
Get important statuses (tweets / replies / retweets / quotes) from set of Twitter accounts.

## Usage
1. Create a txt file containing a single Twitter screen name in each line.
```code
Twitter
jack
POTUS
```
2. Create a JSON file containing your Twitter API credential.
```json
{
    "consumer_key": "[fill here]",
    "consumer_secret": "[fill here]",
    "access_token": "[fill here]",
    "access_token_secret": "[fill here]"
}
```
3. Create a python environment and install requirements.
```console
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt
```
4. Set values in environment file (.env).
```code
SCREEN_NAMES_TXT_PATH=[path to txt file created in step 1]
TWITTER_CREDENTIAL_PATH=[path to json file created in step 2]
DB_PATH=[path to json file that will be created by tinydb]
```
5. Use CLI to run your command.

General usage.
```console
python main.py --help
```
```console
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  daily
  fetch
  historical
  monthly
  weekly
```

Usage of `daily` command.
```console
python main.py daily --help
```
```console
Usage: main.py daily [OPTIONS]

Options:
  -d, --db PATH             path to database json file (for tinydb json
                            storage)  [env var: DB_PATH;required]
  -c, --count INTEGER       returns (at most) top `count` statuses  [default:
                            5]
  --date [%Y-%m-%d]         filter statuses on `date` (in ISO format)
                            [default: (today)]
  --tweet / --no-tweet      include only tweets / exclude tweets
  --reply / --no-reply  include only replies / exclude replies
  --retweet / --no-retweet  include only retweets / exclude retweets
  --quote / --no-quote      include only quotes / exclude quotes
  --help                    Show this message and exit.
```

Usage of `weekly` command.
```console
python main.py weekly --help
```
```console
Usage: main.py weekly [OPTIONS]

Options:
  -d, --db PATH             path to database json file (for tinydb json
                            storage)  [env var: DB_PATH;required]
  -c, --count INTEGER       returns (at most) top `count` statuses  [default:
                            5]
  --date [%Y-%m-%d]         filter statuses in week containing `date` (in ISO
                            format)  [default: (today)]
  --tweet / --no-tweet      include only tweets / exclude tweets
  --reply / --no-reply  include only replies / exclude replies
  --retweet / --no-retweet  include only retweets / exclude retweets
  --quote / --no-quote      include only quotes / exclude quotes
  --help                    Show this message and exit.
```

Usage of `monthly` command.
```console
python main.py monthly --help
```
```console
Usage: main.py monthly [OPTIONS]

Options:
  -d, --db PATH             path to database json file (for tinydb json
                            storage)  [env var: DB_PATH;required]
  -c, --count INTEGER       returns (at most) top `count` statuses  [default:
                            5]
  --date [%Y-%m-%d]         filter statuses in month containing `date` (in ISO
                            format)  [default: (today)]
  --tweet / --no-tweet      include only tweets / exclude tweets
  --reply / --no-reply  include only replies / exclude replies
  --retweet / --no-retweet  include only retweets / exclude retweets
  --quote / --no-quote      include only quotes / exclude quotes
  --help                    Show this message and exit.
```


Usage of `historical` command.
```console
python main.py historical --help
```
```console
Usage: main.py historical [OPTIONS]

Options:
  -d, --db PATH               path to database json file (for tinydb json
                              storage)  [env var: DB_PATH;required]
  -c, --count INTEGER         returns (at most) top `count` statuses
                              [default: 5]
  --since Optional[%Y-%m-%d]  filter statuses since datetime (in ISO format)
  --until Optional[%Y-%m-%d]  filter statuses until datetime (in ISO format)
  --tweet / --no-tweet        include only tweets / exclude tweets
  --reply / --no-reply    include only replies / exclude replies
  --retweet / --no-retweet    include only retweets / exclude retweets
  --quote / --no-quote        include only quotes / exclude quotes
  --help                      Show this message and exit.
```

