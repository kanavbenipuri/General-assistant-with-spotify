# Spotify API Configuration

# Get these values from your Spotify Developer Dashboard
# https://developer.spotify.com/dashboard
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://127.0.0.1:8888/callback'

# Spotify API permission scopes
SCOPES = [
    'user-read-playback-state',
    'user-modify-playback-state',
    'user-read-currently-playing',
    'streaming',
    'app-remote-control'
]