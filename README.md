# PAMA Discord Bot

## What does this bot do?

This Discord bot uses Ollama to respond messages and saves them into a json file. This bot also uses Mediapipe to detect in the Ollama message for each sentence if it's positive or negative and it expresses that emotion with an Emoji.

Here is a postitive message from PAMA:

![Positive message example](./readme-images/message-1.jpg)

And here is a negative message:

![Negative message example](./readme-images/message-2.jpg)

## How to setup?
First make sure you have the following things installed:

- [Python 3.10 or 3.12 (other version untested)](https://www.python.org/)
- [Ollama](https://ollama.com/)

### Automatic installation

If you are on Mac or Linux run

```bash
./start.sh
```

Then you might get a 401 error. That's because you need to modify the `config.json` the discord token to your's and then run

```bash
./start.sh
```
again.

If you're on windows run

```pwsh
.\start.ps1
```
In powershell

Then you might get a 401 error. That's because you need to modify the `config.json` the discord token to your's and then run

```pwsh
.\start.ps1
```
again.

### Manual installation
1. Create a venv

```
python3 -m venv .venv
```

2. Activate the venv (On Linux and Mac run):
```bash
source .venv/bin/activate
```

(On Windows run):

```pwsh
.venv\Scripts\Activate.ps1
```

3. Install dependencies
```bash
pip3 install -r requirements.txt
```

4. Create config json

```bash
cp example.config.json config.json
```
And modify the Discord token

Then run

```bash
python3 main.py
```

## Commands
This bot at the moment has 1 command which is

`TRUNCATE PAMA;` Which will remove the whole conversation. You can disable this functionality by changing `allowFakeSQLInjection` to `false` in your `config.json`