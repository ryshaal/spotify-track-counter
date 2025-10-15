import csv
import re
from collections import Counter
from utils.spotify_client import get_spotify_client
from utils.helpers import safe_spotify_call, format_duration
from tqdm import tqdm
from colorama import init
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import os

# Clear terminal screen
os.system('cls' if os.name == 'nt' else 'clear')

# Initialize color and console
init(autoreset=True)
console = Console()


def main():
    # Initialize Spotify client
    try:
        sp = get_spotify_client()
    except Exception as e:
        console.print(f"[red]❌ Failed to initialize Spotify Client: {e}")
        return

    # Display app banner
    console.print(Panel.fit(
        "[bold white]Spotify Artist Discography Fetcher[/bold white]\n"
        "[green]Created by https://github.com/ryshaal — powered by Spotipy API[/green]",
        border_style="magenta",
        padding=(1, 2),
        title="Welcome"
    ))

    # Get artist name or URL
    artist_input = console.input("[yellow]Enter artist name or Spotify artist URL: [/yellow]")

    # Extract artist ID from URL if provided
    match = re.search(r"spotify\.com/artist/([a-zA-Z0-9]+)", artist_input)
    if match:
        artist_id = match.group(1)
        try:
            artist = safe_spotify_call(sp.artist, artist_id)
        except Exception as e:
            console.print(f"[red]❌ Error fetching artist from URL: {e}")
            return
    else:
        # Search artist by name
        try:
            results = safe_spotify_call(sp.search, q=f"artist:{artist_input}", type='artist', limit=5)
            artists = results['artists']['items']
            if not artists:
                console.print(f"[red]❌ Artist '{artist_input}' not found.")
                return

            if len(artists) > 1:
                console.print("\n[cyan]Multiple artists found with similar names:[/cyan]")
                for i, artist in enumerate(artists, 1):
                    console.print(f"{i}. {artist['name']} ({artist['followers']['total']:,} followers)")
                choice = int(console.input("\n[yellow]Select artist number (1-5): [/yellow]")) - 1
                artist = artists[choice]
            else:
                artist = artists[0]

            artist_id = artist['id']
        except Exception as e:
            console.print(f"[red]❌ Error searching artist: {e}")
            return

    # Display artist info
    artist_name = artist['name']
    followers = artist['followers']['total']
    genres = ", ".join(artist['genres'][:3]) if artist['genres'] else "No genres available"
    console.print(f"\n[green]✅ Artist selected: [bold]{artist_name}[/bold][/green]")
    console.print(f"[yellow]• Followers:[/yellow] {followers:,}")
    console.print(f"[magenta]• Genres:[/magenta] {genres}")
    console.print(f"[blue]• Link:[/blue] {artist['external_urls']['spotify']}")
    console.print("\n[cyan]Fetching artist's discography...[/cyan]\n")

    # Fetch all albums and singles
    albums = []
    results = safe_spotify_call(sp.artist_albums, artist_id, album_type='album,single,compilation,appears_on', limit=50)
    albums.extend(results['items'])
    while results['next']:
        results = safe_spotify_call(sp.next, results)
        albums.extend(results['items'])

    # Remove duplicate albums
    unique_albums = {}
    for album in albums:
        if album['name'] not in unique_albums:
            unique_albums[album['name']] = album
    console.print(f"[green]Retrieved {len(unique_albums)} releases in total.[/green]\n")

    # Fetch tracks from each album
    track_data = []
    album_count = len(unique_albums)
    console.print(f"[cyan]Processing {album_count} albums/singles...[/cyan]\n")

    for album in tqdm(unique_albums.values(), desc="Fetching tracks", unit="album", colour="cyan"):
        album_id = album['id']
        album_name = album['name']
        release_date = album['release_date']
        release_year = release_date.split("-")[0]
        album_type = album['album_type']

        tracks = safe_spotify_call(sp.album_tracks, album_id)
        for track in tracks['items']:
            track_data.append({
                'artist': artist_name,
                'track': track['name'],
                'album': album_name,
                'year': release_year,
                'type': album_type,
                'duration': format_duration(track['duration_ms']),
                'url': track['external_urls']['spotify']
            })

    console.print("\n[green]✅ Data successfully fetched![/green]\n")

    # Display discography statistics
    console.print("[bold cyan]📊 DISCOGRAPHY STATISTICS[/bold cyan]")
    total_songs = len(track_data)
    years = [int(t['year']) for t in track_data if t['year'].isdigit()]
    types = [t['type'] for t in track_data]
    total_minutes = sum([int(t['duration'].split(':')[0]) * 60 + int(t['duration'].split(':')[1]) for t in track_data]) // 60

    console.print(f"\n• Total Songs: [bold]{total_songs}[/bold]")
    console.print(f"• Year Range: [bold]{min(years)} - {max(years)}[/bold]")
    console.print(f"• Total Duration: [bold]{total_minutes} minutes[/bold]")

    year_counter = Counter(years)
    console.print(f"\n📈 Top 5 Most Productive Years:")
    for year, count in year_counter.most_common(5):
        console.print(f"   {year}: {count} songs")

    type_counter = Counter(types)
    console.print(f"\n💿 Release Type Distribution:")
    for album_type, count in type_counter.items():
        console.print(f"   {album_type.capitalize()}: {count} songs")

    # Display full tracklist table
    console.print("\n[bold cyan]🎵 FULL TRACKLIST[/bold cyan]\n")
    table = Table(show_lines=False, box=box.MINIMAL_HEAVY_HEAD)
    table.add_column("No", justify="right", style="cyan", no_wrap=True)
    table.add_column("Track Title", style="magenta", no_wrap=True)
    table.add_column("Album", style="green", no_wrap=True)
    table.add_column("Year", justify="center", style="yellow")
    table.add_column("Duration", justify="center", style="blue")
    table.add_column("Type", justify="center", style="red")

    for idx, data in enumerate(track_data, 1):
        table.add_row(
            str(idx),
            data['track'][:35],
            data['album'][:30],
            data['year'],
            data['duration'],
            data['type'].capitalize()
        )
    console.print(table)

    # Export data to CSV
    console.print("\n[bold cyan]💾 EXPORT DATA[/bold cyan]\n")
    export = console.input("[yellow]Export data to CSV? (y/n): [/yellow]").lower()
    if export == 'y':
        folder_path = os.path.join(os.getcwd(), "discography")
        os.makedirs(folder_path, exist_ok=True)
        base_filename = f"{artist_name.replace(' ', '_')}_discography.csv"
        file_path = os.path.join(folder_path, base_filename)

        counter = 1
        while os.path.exists(file_path):
            name, ext = os.path.splitext(base_filename)
            file_path = os.path.join(folder_path, f"{name}_copy_{counter}{ext}")
            counter += 1

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['artist', 'track', 'album', 'year', 'type', 'duration', 'url'])
                writer.writeheader()
                writer.writerows(track_data)
            console.print(f"[green]✅ Data saved successfully![/green]")
            console.print(f"[cyan]📁 File location: [underline]{file_path}[/underline][/cyan]\n")
        except Exception as e:
            console.print(f"[red]❌ Error saving file: {e}")

    # Search for a specific song
    console.print("\n[bold cyan]🔍 SONG SEARCH[/bold cyan]\n")
    search_song = console.input("[yellow]Search for a specific song? (y/n): [/yellow]").lower()
    if search_song == 'y':
        keyword = console.input("Enter keyword: ").lower()
        found = [t for t in track_data if keyword in t['track'].lower()]
        if found:
            console.print(f"\n[green]✅ Found {len(found)} songs:[/green]\n")
            for idx, song in enumerate(found, 1):
                console.print(f"{idx}. {song['track']} - {song['album']} ({song['year']})")
                console.print(f"   🔗 {song['url']}\n")
        else:
            console.print(f"[red]❌ No songs found matching '{keyword}'")

    # End program
    console.print("\n[green]🎉 Done! Thank you for using Spotify Discography Analyzer.")
    console.print("[cyan]📌 Remember to support your favorite artists on Spotify!\n")


if __name__ == "__main__":
    main()
