# Handling errors, progress bars, retries, and data formatting
import time
import spotipy.exceptions


def safe_spotify_call(func, *args, **kwargs):
    """
    Handles Spotify API rate limits (HTTP 429) and unexpected errors automatically.
    Will retry after the 'Retry-After' period if rate limit is reached.
    """
    while True:
        try:
            return func(*args, **kwargs)
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get("Retry-After", 5))
                print(f"\n⚠️ Rate limit reached. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                raise e
        except Exception as e:
            print(f"❌ Unexpected error occurred: {e}")
            time.sleep(3)


def format_duration(ms):
    """
    Converts track duration from milliseconds into MM:SS format.
    """
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    return f"{minutes}:{seconds:02d}"


def progress_bar(current, total, length=25):
    """
    Creates a simple text-based progress bar in the terminal.
    """
    progress = int((current / total) * length)
    bar = "█" * progress + "░" * (length - progress)
    print(f"\r[{bar}] {current}/{total}", end="", flush=True)
