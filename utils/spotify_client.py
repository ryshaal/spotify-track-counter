# Authentication and connection to the Spotify API
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_client():
    """
    Creates a secure connection to the Spotify API using credentials from the .env file.
    Returns a ready-to-use Spotipy client instance.
    """
    # Load environment variables
    load_dotenv()

    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError(
            "❌ Spotify credentials not found. Make sure your .env file contains:\n"
            "SPOTIFY_CLIENT_ID=your_client_id\n"
            "SPOTIFY_CLIENT_SECRET=your_client_secret"
        )

    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret
            )
        )
        print("✅ Successfully connected to Spotify API!\n")
        return sp
    except Exception as e:
        raise ConnectionError(f"❌ Failed to connect to Spotify API: {e}")
