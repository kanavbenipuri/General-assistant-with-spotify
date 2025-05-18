import datetime
import webbrowser
import os
import spotipy
import ctypes
import psutil
import platform
from spotipy.oauth2 import SpotifyOAuth
from spotify_config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPES

class JarvisAssistant:
    def __init__(self):
        # Initialize basic settings
        self.name = 'Jarvis'
        self.active_device_id = None
        
        # Initialize Spotify client
        try:
            self.spotify = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=CLIENT_ID,
                    client_secret=CLIENT_SECRET,
                    redirect_uri=REDIRECT_URI,
                    scope=SCOPES
                )
            )
            self.spotify_connected = True
            self.update_active_device()
        except Exception as e:
            print(f'Failed to connect to Spotify: {e}')
            self.spotify_connected = False
    
    def display(self, text):
        """Display Jarvis's response"""
        print(f'{self.name}: {text}')
    
    def get_input(self):
        """Get text input from user"""
        try:
            command = input('You: ').lower().strip()
            return command
        except Exception as e:
            print(f'Error reading input: {e}')
            return ''
    
    def greet(self):
        """Greet the user based on time of day"""
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.display('Good morning!')
        elif 12 <= hour < 18:
            self.display('Good afternoon!')
        else:
            self.display('Good evening!')
        
        # Add weather information
        try:
            weather_data = self.get_weather()
            self.display(f"Current weather in {weather_data['city']}:")
            self.display(f"Temperature: {weather_data['temp']}°C")
            self.display(f"Conditions: {weather_data['description']}")
        except Exception as e:
            self.display("Weather information unavailable at the moment")
            
        self.display('I am Jarvis, your AI assistant. How can I help you today?')
    
    def update_active_device(self):
        """Update the active Spotify device ID without automatic activation"""
        try:
            devices = self.spotify.devices()
            active_devices = [d for d in devices['devices'] if d['is_active']]
            if active_devices:
                self.active_device_id = active_devices[0]['id']
            elif devices['devices']:
                # Store the first available device ID without activating it
                self.active_device_id = devices['devices'][0]['id']
            else:
                self.active_device_id = None
                self.display('No Spotify devices found. Please open Spotify on your device.')
        except Exception as e:
            self.display(f'Error updating device status: {e}')
            self.active_device_id = None

    def get_system_info(self):
        """Get system information including CPU and memory usage"""
        try:
            # CPU Information
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_avg = sum(cpu_percent) / len(cpu_percent)
            
            # Memory Information
            memory = psutil.virtual_memory()
            memory_total = memory.total / (1024 * 1024 * 1024)  # Convert to GB
            memory_used = memory.used / (1024 * 1024 * 1024)   # Convert to GB
            memory_percent = memory.percent
            
            # System Information
            system_info = platform.uname()
            
            return {
                'system': system_info.system,
                'node': system_info.node,
                'release': system_info.release,
                'cpu_cores': psutil.cpu_count(),
                'cpu_usage': cpu_avg,
                'memory_total': round(memory_total, 2),
                'memory_used': round(memory_used, 2),
                'memory_percent': memory_percent
            }
        except Exception as e:
            return str(e)
    
    def show_help(self):
        """Display all available commands and their usage"""
        commands = {
            'General Commands': {
                'help': 'Show this help message',
                'date': 'Show current date',
                'search [query]': 'Search Google for the specified query',
                'weather': 'Show current weather information',
                'lock': 'Lock the system',
                'exit/goodbye/bye': 'Exit Jarvis'
            },
            'System Commands': {
                'system': 'Show detailed system information including:',
                '  - OS Details': 'Operating system name and version',
                '  - Hostname': 'System hostname',
                '  - CPU Information': 'Number of CPU cores and current usage percentage',
                '  - Memory Stats': 'Total memory, used memory, and usage percentage'
            },
            'Spotify Commands': {
                'play [song/album/playlist] [name]': 'Play music on Spotify',
                'pause': 'Pause current playback',
                'next': 'Skip to next track',
                'previous': 'Go to previous track',
                'queue [song]': 'Add a song to the queue',
                'current song': 'Show currently playing track',
                'repeat [off/track/context]': 'Set repeat mode (off, current track, or current context)'
            }
        }
        
        help_text = 'Available Commands:\n'
        for cmd, desc in commands.items():
            if isinstance(desc, dict):
                help_text += f'\n{cmd}:\n'
                for subcmd, subdesc in desc.items():
                    help_text += f'  {subcmd}: {subdesc}\n'
            else:
                help_text += f'{cmd}: {desc}\n'
        self.display(help_text.rstrip())
    
    def process_command(self, command):
        """Process commands and execute corresponding actions"""
        if command == 'help':
            self.show_help()
            return True
        
        elif 'system' in command:
            sys_info = self.get_system_info()
            if isinstance(sys_info, dict):
                print(f'{self.name}: System Information:')
                print(f'    OS: {sys_info["system"]} {sys_info["release"]}')
                print(f'    Hostname: {sys_info["node"]}')
                print(f'    CPU Cores: {sys_info["cpu_cores"]}')
                print(f'    CPU Usage: {sys_info["cpu_usage"]}%')
                print(f'    Memory Total: {sys_info["memory_total"]}GB')
                print(f'    Memory Used: {sys_info["memory_used"]}GB')
                print(f'    Memory Usage: {sys_info["memory_percent"]}%')
            else:
                self.display(f'Error getting system information: {sys_info}')
            return True
        
        elif 'date' in command:
            current_date = datetime.datetime.now().strftime('%B %d, %Y')
            self.display(f'Today is {current_date}')
        
        elif 'search' in command:
            search_term = command.replace('search', '').strip()
            url = f'https://www.google.com/search?q={search_term}'
            webbrowser.open(url)
            self.display(f'Searching for {search_term}')
        
        elif 'queue' in command:
            if not self.spotify_connected:
                self.display('Spotify is not connected. Please check your credentials.')
                return True
            self.update_active_device()
            if not self.active_device_id:
                self.display('Please open Spotify on your device and try again.')
                return True
            query = command.replace('queue', '').strip()
            if query:
                try:
                    # Search for tracks only
                    results = self.spotify.search(q=query, type='track', limit=5)
                    tracks = results['tracks']['items']
                    if tracks:
                        self.display('Select a track to add to queue:')
                        for idx, track in enumerate(tracks, 1):
                            name = track['name']
                            artist = track['artists'][0]['name']
                            self.display(f'{idx}. {name} by {artist}')
                        while True:
                            self.display('Enter the number of the track you want to queue (or 0 to cancel):')
                            try:
                                selection = int(input('You: ').strip())
                                if selection == 0:
                                    self.display('Cancelled song selection.')
                                    break
                                elif 1 <= selection <= len(tracks):
                                    track = tracks[selection-1]
                                    self.spotify.add_to_queue(uri=track['uri'], device_id=self.active_device_id)
                                    self.display(f'Added to queue: {track["name"]} by {track["artists"][0]["name"]}')
                                    break
                                else:
                                    self.display('Invalid selection. Please try again.')
                            except ValueError:
                                self.display('Invalid input. Please enter a number.')
                    else:
                        self.display('No matching tracks found.')
                except Exception as e:
                    if 'No active device found' in str(e):
                        self.display('No active Spotify device found. Please open Spotify on your device.')
                    else:
                        self.display(f'Error adding to queue: {e}')
            else:
                self.display('Please specify what song you would like to queue.')

        elif 'play' in command:
            if not self.spotify_connected:
                self.display('Spotify is not connected. Please check your credentials.')
                return True
            self.update_active_device()
            if not self.active_device_id:
                self.display('Please open Spotify on your device and try again.')
                return True
            query = command.replace('play', '').strip()
            if query:
                try:
                    # Check if playlist or album is specifically requested
                    playlist_mode = 'playlist' in command.lower()
                    album_mode = 'album' in command.lower()
                    if playlist_mode:
                        query = command.replace('play', '').replace('playlist', '').strip()
                    elif album_mode:
                        query = command.replace('play', '').replace('album', '').strip()
                    
                    if album_mode:
                        # Search for albums only
                        album_results = self.spotify.search(q=query, type='album', limit=5)
                        albums = album_results['albums']['items']
                        
                        if albums:
                            self.display('Select an album to play:')
                            for idx, album in enumerate(albums, 1):
                                self.display(f'{idx}. {album["name"]} by {album["artists"][0]["name"]}')
                            
                            while True:
                                self.display('Enter the number of the album you want to play (or 0 to cancel):')
                                try:
                                    selection = int(input('You: ').strip())
                                    if selection == 0:
                                        self.display('Cancelled album selection.')
                                        break
                                    elif 1 <= selection <= len(albums):
                                        album = albums[selection-1]
                                        self.spotify.start_playback(
                                            device_id=self.active_device_id,
                                            context_uri=album['uri']
                                        )
                                        self.display(f'Playing album: {album["name"]} by {album["artists"][0]["name"]}')
                                        break
                                    else:
                                        self.display('Invalid selection. Please try again.')
                                except ValueError:
                                    self.display('Invalid input. Please enter a number.')
                        else:
                            self.display('No matching albums found.')
                    
                    elif playlist_mode:
                        # Search for playlists only
                        playlist_results = self.spotify.search(q=query, type='playlist', limit=5)
                        playlists = playlist_results['playlists']['items']
                        
                        if playlists:
                            self.display('Select a playlist to play:')
                            for idx, playlist in enumerate(playlists, 1):
                                self.display(f'{idx}. {playlist["name"]} by {playlist["owner"]["display_name"]}')
                            
                            while True:
                                self.display('Enter the number of the playlist you want to play (or 0 to cancel):')
                                try:
                                    selection = int(input('You: ').strip())
                                    if selection == 0:
                                        self.display('Cancelled playlist selection.')
                                        break
                                    elif 1 <= selection <= len(playlists):
                                        playlist = playlists[selection-1]
                                        self.spotify.start_playback(
                                            device_id=self.active_device_id,
                                            context_uri=playlist['uri']
                                        )
                                        self.display(f'Playing playlist: {playlist["name"]}')
                                        break
                                    else:
                                        self.display('Invalid selection. Please try again.')
                                except ValueError:
                                    self.display('Invalid input. Please enter a number.')
                        else:
                            self.display('No matching playlists found.')
                    else:
                        # Search for tracks only
                        results = self.spotify.search(q=query, type='track', limit=5)
                        tracks = results['tracks']['items']
                        if tracks:
                            self.display('Select a track to play:')
                            for idx, track in enumerate(tracks, 1):
                                name = track['name']
                                artist = track['artists'][0]['name']
                                self.display(f'{idx}. {name} by {artist}')
                            while True:
                                self.display('Enter the number of the track you want to play (or 0 to cancel):')
                                try:
                                    selection = int(input('You: ').strip())
                                    if selection == 0:
                                        self.display('Cancelled song selection.')
                                        break
                                    elif 1 <= selection <= len(tracks):
                                        track = tracks[selection-1]
                                        self.spotify.start_playback(
                                            device_id=self.active_device_id,
                                            uris=[track['uri']]
                                        )
                                        self.display(f'Playing {track["name"]} by {track["artists"][0]["name"]}')
                                        break
                                    else:
                                        self.display('Invalid selection. Please try again.')
                                except ValueError:
                                    self.display('Invalid input. Please enter a number.')
                        else:
                            self.display('No matching tracks found.')
                except Exception as e:
                    if 'No active device found' in str(e):
                        self.display('No active Spotify device found. Please open Spotify on your device.')
                    else:
                        self.display(f'Error playing music: {e}')
            else:
                self.display('Please specify what you would like to play (song, album, or playlist).')
        
        elif 'pause' in command:
            if self.spotify_connected:
                try:
                    self.spotify.pause_playback(device_id=self.active_device_id)
                    self.display('Paused playback')
                except Exception as e:
                    if 'No active device found' in str(e):
                        self.display('No active Spotify device found. Please open Spotify on your device.')
                    else:
                        self.display('No active playback to pause')
            else:
                self.display('Spotify is not connected')
        
        elif 'next' in command:
            if self.spotify_connected:
                self.update_active_device()
                if not self.active_device_id:
                    return True
                try:
                    self.spotify.next_track(device_id=self.active_device_id)
                    self.display('Playing next track')
                except Exception as e:
                    if 'No active device found' in str(e):
                        self.display('No active Spotify device found. Please open Spotify on your device.')
                    else:
                        self.display('Unable to skip to next track')
            else:
                self.display('Spotify is not connected')
        
        elif 'previous' in command:
            if self.spotify_connected:
                self.update_active_device()
                if not self.active_device_id:
                    return True
                try:
                    self.spotify.previous_track(device_id=self.active_device_id)
                    self.display('Playing previous track')
                except Exception as e:
                    if 'No active device found' in str(e):
                        self.display('No active Spotify device found. Please open Spotify on your device.')
                    else:
                        self.display('Unable to go to previous track')
            else:
                self.display('Spotify is not connected')
        
        elif 'current' in command and 'song' in command:
            if self.spotify_connected:
                try:
                    current = self.spotify.current_user_playing_track()
                    if current and current['item']:
                        track = current['item']
                        self.display(f'Currently playing: {track["name"]} by {track["artists"][0]["name"]}')
                    else:
                        self.display('No track currently playing')
                except:
                    self.display('Unable to get current track information')
            else:
                self.display('Spotify is not connected')

        elif 'repeat' in command:
            if not self.spotify_connected:
                self.display('Spotify is not connected. Please check your credentials.')
                return True
            self.update_active_device()
            if not self.active_device_id:
                self.display('Please open Spotify on your device and try again.')
                return True
            
            state = command.replace('repeat', '').strip().lower()
            valid_states = {'off': 'off', 'track': 'track', 'context': 'context'}
            
            if state in valid_states:
                try:
                    self.spotify.repeat(valid_states[state], device_id=self.active_device_id)
                    self.display(f'Repeat mode set to: {state}')
                except Exception as e:
                    if 'No active device found' in str(e):
                        self.display('No active Spotify device found. Please open Spotify on your device.')
                    else:
                        self.display(f'Error setting repeat mode: {e}')
            else:
                self.display('Please specify repeat mode: off, track, or context')
                self.display('- off: Turn repeat off')
                self.display('- track: Repeat current track')
                self.display('- context: Repeat current playlist/album')
        
        elif 'weather' in command:
            self.display('Checking weather...')
            try:
                weather_data = self.get_weather()
                self.display(f"Current weather in {weather_data['city']}:")
                self.display(f"Temperature: {weather_data['temp']}°C")
                self.display(f"Conditions: {weather_data['description']}")
                self.display(f"Humidity: {weather_data['humidity']}%")
            except Exception as e:
                self.display(f"Couldn't fetch weather data: {e}")
        
        elif 'lock' in command:
            self.display('Locking your system. Goodbye!')
            try:
                ctypes.windll.user32.LockWorkStation()
                return True
            except Exception as e:
                self.display(f'Failed to lock system: {e}')
                return True

        elif 'exit' in command or 'goodbye' in command or 'bye' in command:
            self.display('Goodbye! Have a great day!')
            return False
        
        return True

    def get_weather(self):
        """Fetch weather data from Weatherbit API"""
        import requests
        from weather_config import API_KEY, DEFAULT_CITY
        
        try:
            url = f"https://api.weatherbit.io/v2.0/current?city={DEFAULT_CITY}&key={API_KEY}&units=M"
            response = requests.get(url)
            data = response.json()
            
            return {
                'city': DEFAULT_CITY,
                'temp': data['data'][0]['temp'],
                'description': data['data'][0]['weather']['description'],
                'humidity': data['data'][0]['rh']
            }
        except Exception as e:
            raise Exception(f"Weather API error: {str(e)}")

def main():
    jarvis = JarvisAssistant()
    jarvis.greet()
    
    running = True
    while running:
        command = jarvis.get_input()
        if command:
            running = jarvis.process_command(command)

if __name__ == '__main__':
    main()