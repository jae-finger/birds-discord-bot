# RescueTheBirds! Discord Bot

## Description
RescueTheBirds! is a Discord bot designed for the save-the-birds project. It enhances user interaction by welcoming new members and responding to various commands.

## Table of Contents
- [RescueTheBirds! Discord Bot](#rescuethebirds-discord-bot)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Installation and Setup](#installation-and-setup)
  - [Usage](#usage)

## Installation and Setup
1. Clone the repository:
`git clone https://github.com/jae-finger/birds-discord-bot.git`
2. Install dependencies:
`pip install -r requirements.txt`
3. Set your Discord bot token in an environment variable:
`export BIRB_DISCORD_TOKEN='your-token-here'`

## Usage
After installation, run the bot with:
```bash
docker build -t discord-bot .
docker run -e BIRB_DISCORD_TOKEN='XXXXXXXXXXX' discord-bot
```
Commands:
- `?hello`: Responds with "Ahoy!"
- `source_code`: Links to source code