
# 🦜 RescueTheBirds! Discord Bot

## 📝 Description
RescueTheBirds! 🚀 is an innovative Discord bot designed for the save-the-birds project. It's crafted to boost user engagement 🌟 and create a lively server atmosphere by welcoming new members 👋, responding to commands 🛠️, and offering interactive bird-related trivia and fun facts 🐦. 

## 📚 Table of Contents
- [🦜 RescueTheBirds! Discord Bot](#-rescuethebirds-discord-bot)
  - [📝 Description](#-description)
  - [📚 Table of Contents](#-table-of-contents)
  - [🛠️ Installation and Setup](#️-installation-and-setup)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [🐳 Docker Support](#-docker-support)
    - [Building the Docker Image](#building-the-docker-image)
    - [Running the Docker Container](#running-the-docker-container)
  - [🤖 Commands and Features](#-commands-and-features)
  - [📖 Usage](#-usage)

## 🛠️ Installation and Setup
Get RescueTheBirds! chirping on your server with these easy steps:

### Prerequisites
- A Discord server 🌐
- Python 3.11+ 🐍

### Steps
1. Clone this repository 🔄:
   ```
   git clone [repository-link]
   ```
2. Install dependencies 📦:
   ```
   pip install -r requirements.txt
   ```
3. Configure your .env file 🔐:
   ```
   BIRB_DISCORD_TOKEN=your_discord_bot_token
   DEFAULT_DISCORD_ID=your_discord_user_id
   GENERAL_CHANNEL_ID=your_general_channel_id
   DISCORD_GUILD_ID=your_discord_guild_id
   ```

## 🐳 Docker Support
Easily deploy RescueTheBirds! using Docker 📦:

### Building the Docker Image
```
docker build -t bird-bot .
```

### Running the Docker Container
```
docker run --name bird-bot bird-bot
```

## 🤖 Commands and Features
RescueTheBirds! is equipped with a range of functionalities to enhance your Discord experience:

- **Custom Help Command**: Use `?help` to explore our intuitive and user-friendly help interface, designed to make your interactions smoother.
- **Interactive Commands**: Engage with various bird-themed commands, like trivia and fun facts, to keep your server lively and informative 🐦.
- **New Member Welcome**: Automated greetings to welcome new members, making them feel right at home in your server community 👋.

Experiment with the bot to discover more hidden features and commands!

(Note: As the bot continues to evolve, new features and commands will be added. Stay tuned for updates!)

## 📖 Usage
After installation, invite RescueTheBirds! to your server and interact with it using the commands. Customize the bot further in the settings file.
