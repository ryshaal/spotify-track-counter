# 🎧 Spotify Artist Discography Fetcher

A command-line Python application that fetches and analyzes an artist’s full discography using the **Spotify Web API** via **Spotipy**.  
Displays formatted statistics, release summaries, and tracklists in a colorful console interface — and optionally exports the results to a CSV file.

---

## 🚀 Features

- Fetch artist information directly by **name** or **Spotify URL**
- Retrieve complete **discography** (albums, singles, compilations, and appearances)
- Display:
  - Total song count
  - Active year range
  - Release type distribution
  - Top productive years
- Interactive **tracklist table**
- Export data to **CSV**
- Built-in **song search**
- Clean terminal output using **Rich** and **Colorama**
- Progress bar with **tqdm**

---

## 📂 Project Structure

```
spotify-discography-fetcher/
│
├── main.py
├── utils/
│   ├── spotify_client.py
│   └── helpers.py
│
├── requirements.txt
└── README.md
```

---

## 🧩 Dependencies

This project uses the following Python packages:

```txt
spotipy
tqdm
colorama
rich
```

You can install them all with:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install spotipy tqdm colorama rich
```

---

## ⚙️ Setting Up Spotify API

This application uses **Spotify Web API** through the **Spotipy** library.

### 1. Create a Spotify Developer Account

Go to [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)  
and **log in** with your Spotify account.

### 2. Create a New App

Click **"Create App"** and fill in:

- **App name:** `Spotify Discography Fetcher`
- **Redirect URI:** `http://localhost:8888/callback`

After creation, you will get:

- **Client ID**
- **Client Secret**

---

### 3. Set Up Environment Variables

You must store your **Spotify API credentials** as environment variables so the app can authenticate.

Create a file named `.env` in your project root and add the following:

```env
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

Then make sure your `utils/spotify_client.py` includes something like this:

```python
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-library-read"
    ))
```

> ⚠️ If you don’t have `python-dotenv` installed, run:
> ```bash
> pip install python-dotenv
> ```

---

## ▶️ How to Run

1. Open your terminal in the project directory  
2. Run the main script:

```bash
python main.py
```

3. When prompted, enter:
   - The **artist name** (e.g. `The Weeknd`)  
   - Or paste the **Spotify artist URL**, e.g.  
     ```
     https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05PJ
     ```

4. Follow the interactive prompts to:
   - Choose the correct artist (if multiple found)
   - Export discography to CSV (optional)
   - Search songs by keyword (optional)

---

## 🧠 Example Output

```
Welcome — Spotify Artist Discography Fetcher
Created by https://github.com/ryshaal — powered by Spotipy API

Enter artist name or Spotify artist URL: The Weeknd

✅ Artist selected: The Weeknd
• Followers: 97,812,410
• Genres: canadian contemporary r&b, pop, dance pop

Fetching artist's discography...

Retrieved 154 releases in total.
Processing 154 albums/singles...
Fetching tracks: 100%|█████████████████████████████████████|

✅ Data successfully fetched!

📊 DISCOGRAPHY STATISTICS
• Total Songs: 792
• Year Range: 2011 - 2025
• Total Duration: 2526 minutes

📈 Top 5 Most Productive Years:
   2020: 102 songs
   2022: 84 songs
   2018: 66 songs
   2015: 60 songs
   2023: 54 songs

💿 Release Type Distribution:
   Album: 401 songs
   Single: 254 songs
   Compilation: 87 songs

🎵 FULL TRACKLIST
... (Table displayed in console)

💾 EXPORT DATA
Export data to CSV? (y/n): y
✅ Data saved successfully!
📁 File location: discography/The_Weeknd_discography.csv
```

---

## 📁 CSV Output Example

| artist     | track                 | album              | year | type   | duration | url |
|-------------|----------------------|--------------------|------|--------|-----------|-----|
| The Weeknd  | Blinding Lights      | After Hours        | 2020 | album  | 3:20      | https://open.spotify.com/track/... |
| The Weeknd  | Save Your Tears      | After Hours        | 2020 | album  | 3:36      | https://open.spotify.com/track/... |

---

## 🧩 Utility Modules

### `utils/helpers.py`

Contains helper functions used by the main program, such as:

```python
def safe_spotify_call(func, *args, **kwargs):
    """Safely calls a Spotify API function with error handling."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Spotify API error: {e}")
        return {}

def format_duration(duration_ms):
    """Convert milliseconds to mm:ss format."""
    minutes = duration_ms // 60000
    seconds = (duration_ms % 60000) // 1000
    return f"{minutes}:{seconds:02}"
```

---

## 🧑‍💻 Author

**Created by:** [@ryshaal](https://github.com/ryshaal)  
**Language:** Python 3.10+  
**API:** [Spotify Web API](https://developer.spotify.com/documentation/web-api/)  
**License:** MIT

---

## 🪶 License

This project is licensed under the [MIT License](LICENSE).  
Feel free to use, modify, and distribute with attribution.

---

## ⭐ Support

If you find this project useful, please give it a ⭐ on GitHub to support the development.
