import requests
import json
import sys
import os
import time
import re
import webbrowser
from urllib.parse import urlparse, parse_qs

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'  
    BRIGHT_RED = '\033[91m'

    
         

def display_large_title():
    title = f'{Colors.BRIGHT_CYAN}{Colors.BOLD}{Colors.UNDERLINE}Twitch Tool{Colors.ENDC}'
    subtitle = f'{Colors.BRIGHT_GREEN}{Colors.BOLD}Your Gateway to Twitch API!!{Colors.ENDC}'
    os.system('cls' if os.name == 'nt' else 'clear')

    console_width = os.get_terminal_size().columns
    title_width = len(title)
    subtitle_width = len(subtitle)
    title_padding = (console_width - title_width) // 2
    subtitle_padding = (console_width - subtitle_width) // 2

    print(f'{Colors.BRIGHT_CYAN}{" " * title_padding}{title}{Colors.ENDC}')
    print(f'{Colors.BRIGHT_GREEN}{" " * subtitle_padding}{subtitle}{Colors.ENDC}')
    print('\n' + '-' * console_width)

def display_title_animation():
    title = f'{Colors.BRIGHT_CYAN}{Colors.BOLD}Twitch Tool{Colors.ENDC}'
    animation = ['|', '/', '-', '\\']
    os.system('cls' if os.name == 'nt' else 'clear')

    for _ in range(10):
        for frame in animation:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'{Colors.BRIGHT_GREEN}{Colors.BOLD}{Colors.UNDERLINE}{title} {frame}{Colors.ENDC}')
            time.sleep(0.05)  

def exchange_code_for_token(authorization_code, redirect_uri, client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        tokens = response.json()

        with open('tokens.json', 'w') as f:
            json.dump(tokens, f, indent=2)

        print(f'{Colors.BRIGHT_GREEN}Tokens saved to tokens.json{Colors.ENDC}')
        print(f'{Colors.BRIGHT_CYAN}1. Return to main menu{Colors.ENDC}')
        print(f'{Colors.BRIGHT_CYAN}2. Exit{Colors.ENDC}')
        choice = input(f'{Colors.BLUE}Enter your choice: {Colors.ENDC}')
        if choice == '1':
            main_menu()
        else:
            sys.exit(0)
    except requests.exceptions.RequestException as error:
        error_message = f'Error exchanging code for token: {error}'
        print(f'{Colors.FAIL}{error_message}{Colors.ENDC}')
        with open('error.json', 'w') as f:
            json.dump({'error': error_message}, f, indent=2)
        time.sleep(5)
        sys.exit(1)

def token_exchange():
    settings = {}  # Initialize the settings dictionary
    
    # Load previous settings if they exist
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            settings = json.load(f)
    
    def get_input(prompt, validation=None):
        while True:
            value = input(prompt)
            if not value:
                print(f'{Colors.FAIL}Error: {prompt.strip(": ")} cannot be empty!{Colors.ENDC}')
            elif validation and not validation(value):
                print(f'{Colors.FAIL}Error: Invalid {prompt.strip(": ")}!{Colors.ENDC}')
            else:
                return value

    # Use settings if available
    client_id = settings.get('client_id', '')
    redirect_uri = settings.get('redirect_uri', '')
    client_secret = settings.get('client_secret', '')

    if client_id and redirect_uri and client_secret:
        print(f'{Colors.BRIGHT_GREEN}Using existing settings from settings.json{Colors.ENDC}')
        print(f'Client ID: {Colors.BOLD}{client_id}{Colors.ENDC}')
        print(f'Redirect URI: {Colors.BOLD}{redirect_uri}{Colors.ENDC}')
        print(f'Client Secret: {Colors.BOLD}{client_secret}{Colors.ENDC}')
        authorization_code = get_input(f'{Colors.BLUE}Enter Authorization Code: {Colors.ENDC}')
    else:
        authorization_code = get_input(f'{Colors.BLUE}Enter Authorization Code: {Colors.ENDC}')
        redirect_uri = get_input(f'{Colors.BLUE}Enter Redirect URI: {Colors.ENDC}', lambda url: re.match(r'^https?://', url))
        client_id = get_input(f'{Colors.BLUE}Enter Client ID: {Colors.ENDC}')
        client_secret = get_input(f'{Colors.BLUE}Enter Client Secret: {Colors.ENDC}')

        # Save settings to settings.json
        settings['client_id'] = client_id
        settings['redirect_uri'] = redirect_uri
        settings['client_secret'] = client_secret
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=2)

    print(f'{Colors.BRIGHT_GREEN}All details provided:{Colors.ENDC}')
    print(f'Authorization Code: {Colors.BOLD}{authorization_code}{Colors.ENDC}')
    print(f'Redirect URI: {Colors.BOLD}{redirect_uri}{Colors.ENDC}')
    print(f'Client ID: {Colors.BOLD}{client_id}{Colors.ENDC}')
    print(f'Client Secret: {Colors.BOLD}{client_secret}{Colors.ENDC}')

    print(f'{Colors.BRIGHT_CYAN}5. Execute{Colors.ENDC}')
    choice = input(f'{Colors.BLUE}Enter your choice: {Colors.ENDC}')
    if choice == '5':
        exchange_code_for_token(authorization_code, redirect_uri, client_id, client_secret)

def extract_authorization_code(url):
    """Extract the authorization code from the given URL."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get('code', [None])[0]

def get_authorization_code():
    settings = {}  # Initialize the settings dictionary
    
    # Load previous settings if they exist
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            settings = json.load(f)

    client_id = settings.get('client_id', '')
    redirect_uri = settings.get('redirect_uri', '')

    def get_input(prompt, validation=None):
        while True:
            value = input(prompt)
            if not value:
                print(f'{Colors.FAIL}Error: {prompt.strip(": ")} cannot be empty!{Colors.ENDC}')
            elif validation and not validation(value):
                print(f'{Colors.FAIL}Error: Invalid {prompt.strip(": ")}!{Colors.ENDC}')
            else:
                return value

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'{Colors.BOLD}{Colors.UNDERLINE}Get Authorization Code{Colors.ENDC}')
        
        # Display status of settings
        if client_id:
            print(f'{Colors.BRIGHT_CYAN}1. Set Client ID (Current: {client_id}){Colors.ENDC}')
            print(f'{Colors.BRIGHT_CYAN}2. Set Redirect URI (Current: {redirect_uri}){Colors.ENDC}')
        else:
            print(f'{Colors.BRIGHT_CYAN}1. Set Client ID{Colors.ENDC}')
            print(f'{Colors.BRIGHT_CYAN}2. Set Redirect URI{Colors.ENDC}')

        print(f'{Colors.BRIGHT_CYAN}3. Exchange Authorization Code{Colors.ENDC}')
        print(f'{Colors.BRIGHT_CYAN}4. Back to Main Menu{Colors.ENDC}')

        choice = input(f'{Colors.BLUE}Enter your choice: {Colors.ENDC}')
        
        if choice == '1':
            if client_id:
                print(f'{Colors.BRIGHT_YELLOW}Client ID is already set as {client_id}.{Colors.ENDC}')
                print(f'{Colors.BRIGHT_CYAN}1. Modify Client ID{Colors.ENDC}')
                print(f'{Colors.BRIGHT_CYAN}2. Return to Menu{Colors.ENDC}')
                modify_choice = input(f'{Colors.BLUE}Enter your choice: {Colors.ENDC}')
                if modify_choice == '1':
                    client_id = get_input(f'{Colors.BLUE}Enter new Client ID: {Colors.ENDC}')
                    settings['client_id'] = client_id
                    with open('settings.json', 'w') as f:
                        json.dump(settings, f, indent=2)
                elif modify_choice == '2':
                    continue
            else:
                client_id = get_input(f'{Colors.BLUE}Enter Client ID: {Colors.ENDC}')
                settings['client_id'] = client_id
                with open('settings.json', 'w') as f:
                    json.dump(settings, f, indent=2)
        
        elif choice == '2':
            if redirect_uri:
                print(f'{Colors.BRIGHT_YELLOW}Redirect URI is already set as {redirect_uri}.{Colors.ENDC}')
                print(f'{Colors.BRIGHT_CYAN}1. Modify Redirect URI{Colors.ENDC}')
                print(f'{Colors.BRIGHT_CYAN}2. Return to Menu{Colors.ENDC}')
                modify_choice = input(f'{Colors.BLUE}Enter your choice: {Colors.ENDC}')
                if modify_choice == '1':
                    redirect_uri = get_input(f'{Colors.BLUE}Enter new Redirect URI: {Colors.ENDC}', lambda url: re.match(r'^https?://', url))
                    settings['redirect_uri'] = redirect_uri
                    with open('settings.json', 'w') as f:
                        json.dump(settings, f, indent=2)
                elif modify_choice == '2':
                    continue
            else:
                redirect_uri = get_input(f'{Colors.BLUE}Enter Redirect URI: {Colors.ENDC}', lambda url: re.match(r'^https?://', url))
                settings['redirect_uri'] = redirect_uri
                with open('settings.json', 'w') as f:
                    json.dump(settings, f, indent=2)
        
        elif choice == '3':
            if not client_id or not redirect_uri:
                print(f'{Colors.FAIL}Error: Client ID and Redirect URI must be set first!{Colors.ENDC}')
                input(f'{Colors.BRIGHT_CYAN}Press Enter to continue...{Colors.ENDC}')
                continue

            authorization_url = (f'https://id.twitch.tv/oauth2/authorize?client_id={client_id}'
                                 f'&redirect_uri={redirect_uri}&response_type=code&scope=user:read:email')

            print(f'{Colors.BRIGHT_GREEN}Authorization URL generated:{Colors.ENDC}')
            print(f'{Colors.BRIGHT_CYAN}{authorization_url}{Colors.ENDC}')
            
            # Open the URL in the web browser
            webbrowser.open(authorization_url)
            
            print(f'{Colors.BRIGHT_YELLOW}Please follow the link and authorize the application. After authorization, paste the URL you were redirected to here:{Colors.ENDC}')
            redirected_url = input(f'{Colors.BLUE}Paste the URL: {Colors.ENDC}')
            authorization_code = extract_authorization_code(redirected_url)
            
            if not authorization_code:
                print(f'{Colors.FAIL}Error: Authorization code not found in the URL!{Colors.ENDC}')
                input(f'{Colors.BRIGHT_CYAN}Press Enter to continue...{Colors.ENDC}')
                continue
            
            with open('Authorization_Code.json', 'w') as f:
                json.dump({'authorization_code': authorization_code}, f, indent=2)
            
            print(f'{Colors.BRIGHT_GREEN}Authorization Code saved to Authorization_Code.json{Colors.ENDC}')
            input(f'{Colors.BRIGHT_CYAN}Press Enter to continue...{Colors.ENDC}')
        
        elif choice == '4':
            main_menu()
        
        else:
            print(f'{Colors.FAIL}Invalid choice, please try again.{Colors.ENDC}')
            input(f'{Colors.BRIGHT_CYAN}Press Enter to continue...{Colors.ENDC}')

def clear_settings():
    if os.path.exists('settings.json'):
        os.remove('settings.json')
        print(f'{Colors.BRIGHT_GREEN}Settings cleared successfully!{Colors.ENDC}')
    else:
        print(f'{Colors.FAIL}No settings file found to clear.{Colors.ENDC}')
    input(f'{Colors.BRIGHT_CYAN}Press Enter to return to the main menu...{Colors.ENDC}')
    main_menu()

def about():
    print(f'{Colors.HEADER}Programmed by M7md Aka: Sir.Witty{Colors.ENDC}')
    input(f'{Colors.BRIGHT_CYAN}Press Enter to return to the main menu...{Colors.ENDC}')
    main_menu()

def get_channel_info():
    settings = {}  # Initialize the settings dictionary

    # Load previous settings if they exist
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as f:
            settings = json.load(f)

    def get_input(prompt, default=None, validation=None):
        while True:
            value = input(prompt)
            if not value and default is not None:
                value = default
            if not value:
                print(f'{Colors.FAIL}Error: {prompt.strip(": ")} cannot be empty!{Colors.END}')
            elif validation and not validation(value):
                print(f'{Colors.FAIL}Error: Invalid {prompt.strip(": ")}!{Colors.END}')
            else:
                return value

    client_id = settings.get('client_id', '')
    
    # Load the latest token from tokens.json
    if os.path.exists('tokens.json'):
        with open('tokens.json', 'r') as f:
            tokens = json.load(f)
            authorization_code = tokens.get('access_token', '')
    else:
        authorization_code = settings.get('authorization_code', '')

    if not client_id:
        client_id = get_input(f'{Colors.BLUE}Enter Client ID: {Colors.END}')
        settings['client_id'] = client_id
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=2)

    if not authorization_code:
        authorization_code = get_input(f'{Colors.BLUE}Enter Authorization Code: {Colors.END}')
        settings['authorization_code'] = authorization_code
        with open('settings.json', 'w') as f:
            json.dump(settings, f, indent=2)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'{Colors.BOLD}{Colors.UNDERLINE}Get Channel Info{Colors.END}')

        login_name = settings.get('login_name', '')

        # Query Parameters
        login_name = get_input(f'{Colors.BLUE}Enter Login Name (Channel Name) (Current: {login_name}): {Colors.END}', default=login_name)

        # Display current settings
        print(f'{Colors.BRIGHT_CYAN}Current Query Params:{Colors.END}')
        print(f'Login Name: {Colors.BOLD}{login_name}{Colors.END}')
        
        # Display current headers
        print(f'{Colors.BRIGHT_CYAN}Current Headers:{Colors.END}')
        print(f'Client-ID: {Colors.BOLD}{client_id}{Colors.END}')
        print(f'Authorization: {Colors.BOLD}Bearer {authorization_code}{Colors.END}')

        print(f'{Colors.BRIGHT_CYAN}1. Save Channel Info to JSON{Colors.END}')
        print(f'{Colors.BRIGHT_CYAN}2. Modify Headers{Colors.END}')   # New option
        print(f'{Colors.BRIGHT_CYAN}3. Back to Main Menu{Colors.END}')

        choice = input(f'{Colors.BLUE}Enter your choice: {Colors.END}')
        
        if choice == '1':
            if not login_name:
                print(f'{Colors.FAIL}Error: Login Name must be set first!{Colors.END}')
                input(f'{Colors.BRIGHT_CYAN}Press Enter to continue...{Colors.END}')
                continue
            
            url = f'https://api.twitch.tv/helix/users?login={login_name}'
            headers = {
                'Client-ID': client_id,
                'Authorization': f'Bearer {authorization_code}'  # Ensure the token is correctly set
            }

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                # Extract the channel information from the response
                if 'data' in data and len(data['data']) > 0:
                    new_channel_info = data['data'][0]
                else:
                    new_channel_info = None

                if new_channel_info:
                    # Load existing data
                    if os.path.exists('channel_info.json'):
                        with open('channel_info.json', 'r') as f:
                            existing_info = json.load(f)
                    else:
                        existing_info = {"data": []}

                    # Check if this channel info already exists
                    if any(info['id'] == new_channel_info['id'] for info in existing_info['data']):
                        print(f'{Colors.BRIGHT_YELLOW}Channel info for this login already exists. Updating info...{Colors.END}')
                        for info in existing_info['data']:
                            if info['id'] == new_channel_info['id']:
                                info.update(new_channel_info)
                                break
                    else:
                        existing_info['data'].append(new_channel_info)

                    with open('channel_info.json', 'w') as f:
                        json.dump(existing_info, f, indent=2)

                    print(f'{Colors.BRIGHT_GREEN}Channel Info saved to channel_info.json{Colors.END}')
                else:
                    print(f'{Colors.FAIL}No data found for the specified login name!{Colors.END}')
            
            except requests.exceptions.RequestException as error:
                error_message = f'Error fetching channel info: {error}\nResponse Content: {response.text}'
                print(f'{Colors.FAIL}{error_message}{Colors.END}')
                with open('error.json', 'w') as f:
                    json.dump({'error': error_message}, f, indent=2)
                time.sleep(5)
            
            input(f'{Colors.BRIGHT_CYAN}Press Enter to continue...{Colors.END}')
        
        elif choice == '2':
            # Modify Headers
            client_id = get_input(f'{Colors.BLUE}Enter new Client ID (Current: {client_id}): {Colors.END}', default=client_id)
            authorization_code = get_input(f'{Colors.BLUE}Enter new Authorization Code (Current: {authorization_code}): {Colors.END}', default=authorization_code)

            settings['client_id'] = client_id
            settings['authorization_code'] = authorization_code
            with open('settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
            
            print(f'{Colors.BRIGHT_GREEN}Headers updated successfully!{Colors.END}')
            input(f'{Colors.BRIGHT_CYAN}Press Enter to continue...{Colors.END}')
        
        elif choice == '3':
            main_menu()
        
        else:
            print(f'{Colors.FAIL}Invalid choice, please try again.{Colors.END}')
            input(f'{Colors.BRIGHT_CYAN}Press Enter to continue...{Colors.END}')



def reload_application():
    """Clears the console and reloads the main menu."""
    os.system('cls' if os.name == 'nt' else 'clear')
    main_menu()

def main_menu():
    display_title_animation()
    display_large_title()

    print(f'{Colors.BOLD}{Colors.UNDERLINE}Main Menu{Colors.ENDC}')
    menu_items = [
        f'{Colors.BRIGHT_CYAN}1. Start Token Exchange{Colors.ENDC}',
        f'{Colors.BRIGHT_CYAN}2. Get Authorization Code{Colors.ENDC}',
        f'{Colors.BRIGHT_CYAN}3. Get Channel Info{Colors.ENDC}',  # New option
        f'{Colors.BRIGHT_CYAN}4. Clear Settings{Colors.ENDC}',      # Updated numbering
        f'{Colors.BRIGHT_CYAN}5. Reload{Colors.ENDC}',             # Reload option
        f'{Colors.BRIGHT_CYAN}6. Exit{Colors.ENDC}'                # Updated numbering
    ]
    
    max_length = max(len(item) for item in menu_items)
    
    print('   '.join(f'{item:<{max_length}}' for item in menu_items))

    choice = input(f'{Colors.BLUE}Enter your choice: {Colors.ENDC}')
    if choice == '1':
        token_exchange()
    elif choice == '2':
        get_authorization_code()
    elif choice == '3':
        get_channel_info()   # Updated to match new option
    elif choice == '4':
        if os.path.exists('settings.json'):
            clear_settings()  # Updated to match new position
        else:
            display_title_animation()
            main_menu()      # Refresh menu if no settings file
    elif choice == '5':
        reload_application()  # Call reload function
    elif choice == '6':
        sys.exit(0)       # Updated to match new position
    else:
        print(f'{Colors.FAIL}Invalid choice, please try again.{Colors.ENDC}')
        main_menu()

if __name__ == '__main__':
    main_menu()
