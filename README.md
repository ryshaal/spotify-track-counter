# Spotify Artist Discography Fetcher

A command-line Python application that fetches and analyzes an artist’s full discography using the **Spotify Web API** via **Spotipy**.
Displays formatted statistics, release summaries, and tracklists in a colorful console interface — and optionally exports the results to a CSV file.

 **Features:**

* Fetch artist information directly by **name** or **Spotify URL**
* Retrieve complete **discography** (albums, singles, compilations, and appearances)
* Display:

  * Total song count
  * Active year range
  * Release type distribution
  * Top productive years
* Interactive **tracklist table**
* Export data to **CSV**
* Built-in **song search**
* Clean terminal output using **Rich** and **Colorama**
* Progress bar with **tqdm**

<a href='https://ko-fi.com/riyhsal/5' target='_blank'><img height='40' style='border:0px;height:40px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
---
### Clone Repository
```bash
git clone https://github.com/ryshaal/spotify-track-counter.git
cd spotify-track-counter
```
### Install Dependencies

This project uses the following Python packages:

```txt
certifi==2023.11.17
charset-normalizer==3.3.2
colorama==0.4.6
idna==3.6
markdown-it-py==4.0.0
mdurl==0.1.2
Pygments==2.19.2
python-dotenv==1.0.1
redis==6.4.0
requests==2.31.0
rich==13.7.1
six==1.17.0
spotipy==2.23.0
tqdm==4.66.4
urllib3==2.0.7
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```


### Setting Up Spotify API

This application uses **Spotify Web API** through the **Spotipy** library.

#### 1. Create a Spotify Developer Account

Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and **log in** with your Spotify account.

#### 2. Create a New App

Click **"Create App"** and fill in:

* **App name:** `Spotify Discography Fetcher`
* **Redirect URI:** `https://localhost:8888/callback`

After creation, you will get:

* **Client ID**
* **Client Secret**

#### 3. Set Up Environment Variables

You must store your **Spotify API credentials** as environment variables so the app can authenticate.

Create a file named `.env` in your project root and add the following:

```env
# Spotify API Credentials

SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```
### Structure

```
spotify-track-counter/
│
├── .env
├── .gitignore
├── LICENSE
├── main.py
├── utils/
│   ├── spotify_client.py
│   └── helpers.py
│
├── requirements.txt
└── README.md
```

### How to Run

1. Open your terminal in the project directory
2. Run the main script:

```bash
python main.py
```

3. When prompted, enter:

* The **artist name** (e.g. `The Weeknd`)
* Or paste the **Spotify artist URL**, e.g.:

```text
https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05PJ
```

4. Follow the interactive prompts to:

* Choose the correct artist (if multiple found)
* Export discography to CSV (optional)
* Search songs by keyword (optional)



### Example Output

```text
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

### CSV Output Example

| artist     | track           | album       | year | type  | duration | url                                                                   |
| ---------- | --------------- | ----------- | ---- | ----- | -------- | --------------------------------------------------------------------- |
| The Weeknd | Blinding Lights | After Hours | 2020 | album | 3:20     | [https://open.spotify.com/track/](https://open.spotify.com/track/)... |
| The Weeknd | Save Your Tears | After Hours | 2020 | album | 3:36     | [https://open.spotify.com/track/](https://open.spotify.com/track/)... |



## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute with attribution.



## Support

If you find this project useful, please give it a ⭐ on GitHub to support the development.
