```markdown
# Twitch Tool

## Overview

The **Twitch Tool** is a command-line utility for interacting with the Twitch API. It provides features for obtaining access tokens, extracting authorization codes, fetching channel information, and managing settings. This tool is useful for developers and enthusiasts who want to automate the interaction with Twitch API.

## Features

- **Token Exchange**: Exchange an authorization code for an access token and save it to a file.
- **Authorization Code Extraction**: Generate an authorization URL, retrieve the authorization code, and save it.
- **Channel Information Retrieval**: Fetch and save channel information from Twitch based on login names.
- **Settings Management**: Save and modify settings like `Client-ID`, `Client Secret`, and `Redirect URI`.
- **Error Handling**: Log errors to `error.json` if any issues arise during API requests.
- **Reload and Clear Settings**: Reload the application or clear settings if needed.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/M7mdJs/twitch-tool.git
   cd twitch-tool
   ```

2. **Install Dependencies**

   Ensure you have Python 3.x installed. Install the required Python packages using `pip`:

   ```bash
   pip install requests
   ```

## Usage

1. **Run the Tool**

   Execute the tool from the command line:

   ```bash
   python twitch_tool.py
   ```

2. **Main Menu Options**

   - **1. Start Token Exchange**: Exchange an authorization code for an access token.
   - **2. Get Authorization Code**: Generate an authorization URL, authorize the app, and get the authorization code.
   - **3. Get Channel Info**: Retrieve and save information about a Twitch channel.
   - **4. Clear Settings**: Clear the settings file (`settings.json`).
   - **5. Reload**: Clear the console and reload the main menu.
   - **6. Exit**: Exit the application.

3. **Token Exchange**

   - Input your `Authorization Code`, `Redirect URI`, `Client ID`, and `Client Secret`.
   - Tokens will be saved to `tokens.json`.

4. **Authorization Code**

   - Set or modify `Client ID` and `Redirect URI`.
   - Generate an authorization URL, open it in a browser, and enter the redirected URL to extract the authorization code.

5. **Channel Info**

   - Input the channel `Login Name`.
   - The channel information will be saved to `channel_info.json`.

## Error Handling

Errors encountered during API requests are logged to `error.json`. Check this file for details if the tool fails to fetch or save data.

## Developer

**[M7md_Js](https://github.com/M7mdJs)**

- **GitHub**: [github.com/M7mdJs](https://github.com/M7mdJs)
- **Discord**: [M7md](discord.com/users/1091118468155314306)


Feel free to reach out if you have any questions or issues. Contributions and feedback are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```


