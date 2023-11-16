
# 🦜 RescueTheBirds! Discord Bot

## 📝 Description
RescueTheBirds! 🚀 is a Discord bot designed for the save-the-birds project. It enhances user interaction 🤖 by welcoming new members 👋 and responding to various commands 🛠️.

## 📚 Table of Contents
- [🦜 RescueTheBirds! Discord Bot](#-rescuethebirds-discord-bot)
  - [📝 Description](#-description)
  - [📚 Table of Contents](#-table-of-contents)
  - [🛠️ Installation and Setup](#%EF%B8%8F-installation-and-setup)
  - [💻 Using the Bot](#-using-the-bot)
  - [🐳 Docker Support](#-docker-support)
  - [🤖 Commands List](#-commands-list)
  - [🙋‍♂️ Contributing](#%EF%B8%8F-contributing)
  - [📄 License](#-license)

## 🛠️ Installation and Setup
Here's how you get RescueTheBirds! up and running on your server.

### Prerequisites
- A Discord server to deploy the bot 🌐
- Python 3.11 or higher 🐍

### Steps
1. Clone this repository 🔄:
   ```
   git clone [repository-link]
   ```
2. Install the required packages 📦:
   ```
   pip install -r requirements.txt
   ```
3. Set up the .env file 🔐:
   ```
   BIRB_DISCORD_TOKEN= # Discord Bot Token
   DEFAULT_DISCORD_ID= # Botmaster's Discord User ID
   GENERAL_CHANNEL_ID= # General Output Channel ID
   ```

## 🐳 Docker Support
Deploy RescueTheBirds! with Docker 📦:

### Building the Docker Image
```
docker build -t bird-bot .
```

### Running the Docker Container
```
docker run --env-file .env --name bird-bot bird-bot
```

## 🤖 Commands List
Here are the commands that RescueTheBirds! can respond to:

```
Commands:
- ?hello: Responds with "Ahoy!"
- ?source_code: Links to source code
```


