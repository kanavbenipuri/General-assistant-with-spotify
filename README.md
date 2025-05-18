# JARVIS AI Assistant

JARVIS is a powerful AI assistant that helps you control your computer, manage your music, and stay informed about weather and system status. With intelligent features like time-aware greetings, system monitoring, and Spotify integration, JARVIS makes your daily computing experience more efficient and enjoyable.

## Features

- Intelligent time-based greetings
- Real-time weather information
- Comprehensive system monitoring and control
- Full Spotify music playback control with queue management
- Smart web search capabilities
- System resource monitoring (CPU, Memory, OS details)

## Installation

1. Clone or download this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Spotify integration:
   - Create a Spotify Developer account at https://developer.spotify.com
   - Create a new application to get Client ID and Secret
   - Create `spotify_config.py` with your credentials:
     ```python
     CLIENT_ID = 'your_client_id'
     CLIENT_SECRET = 'your_client_secret'
     REDIRECT_URI = 'your_redirect_uri'
     SCOPES = ['user-modify-playback-state', 'user-read-playback-state']
     ```
4. Set up weather configuration (optional):
   - Create `weather_config.py` with your API credentials

## Available Commands

### General Commands

- `help`: Display all available commands and their usage
- `date`: Show the current date in a readable format
- `search [query]`: Search Google for any topic or question
- `weather`: Get current weather conditions and temperature
- `lock`: Secure your system by locking the screen
- `exit/goodbye/bye`: Gracefully exit JARVIS

### System Commands

- `system`: Display comprehensive system information including:
  - Operating System name and version
  - System hostname
  - CPU cores count and real-time usage percentage
  - Memory statistics (total, used, usage percentage)
  - Detailed resource monitoring

### Spotify Commands

- `play [song/album/playlist] [name]`: Control Spotify playback
  - Play specific songs: `play song Shape of You`
  - Play entire albums: `play album 1989`
  - Start playlists: `play playlist Summer Hits`
- `pause`: Temporarily stop playback
- `next`: Skip to the next track in queue
- `previous`: Return to the previous track
- `queue [song]`: Add songs to your playback queue
- `current song`: Display the currently playing track
- `repeat [off/track/context]`: Control playback repeat mode
  - `off`: Disable repeat
  - `track`: Repeat current song
  - `context`: Repeat current album/playlist

### Weather Information

JARVIS provides detailed weather updates including:
- Current temperature in Celsius
- Weather conditions and description
- Location-based weather data
- Real-time updates

## Requirements

- Python 3.6 or higher
- Spotify Premium account (for music features)
- Active internet connection
- Required Python packages (see requirements.txt)

## Dependencies

- spotipy: Spotify API integration
- psutil: System resource monitoring
- requests: API communications
- platform: System information gathering
- Additional dependencies in requirements.txt

## Contributing

Contributions are welcome! Please feel free to:
- Submit bug reports
- Propose new features
- Create pull requests
- Improve documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.