<h1> Highlights Web Application </h1>

This is a web application for watching highlights of different sports tournaments. Currently, the application supports the following two tournaments:

* Premier League 2022/2023
* World Cup 2022 Qatar

The highlights are fetched from their respective YouTube playlists using the YouTube Data API v3.

<h2> Getting Started </h2>

To use this application on your local machine, follow the steps below:

1. Clone this repository using the following command:
    ```
    git clone https://github.com/username/highlights.git
    ```

2. Install the required Python packages by running:
    ```
    pip install -r requirements.txt
    ```

3. Create a .env file in the root directory and add your YouTube API key as follows:

    ```
    API_KEY=your_api_key_here
    ```

4. Run the Django development server:
    ```
    python manage.py runserver
    ```
5. Open your web browser and navigate to http://localhost:8000 to view the application.
    
<h2> Usage </h2>

<h3> Homepage </h3>

The homepage displays a search bar where users can search for a specific tournament or sport.

<h3> Landing Page </h3>

Clicking on the thumbnail of a tournament/sport from the homepage will take the user to the landing page for that tournament/sport. The landing page displays the most recent video highlights along with a brief description.

<h3> Video Playback Page </h3>

Clicking on a video thumbnail on the landing page will take the user to the video playback page. This page allows the user to watch the video and read the detailed description of the video, including the date of the match and the highlights of the game.

<h3> Search </h3>

The search bar on the homepage allows the user to search for a specific tournament or sport. The search results will display the tournament/sport thumbnail along with the title and a link to the landing page.

<h3> Coming Soon </h3>

If the user clicks on a tournament/sport that does not have any highlights yet, the user will be redirected to the coming soon page.

<h2> Built With </h2>

  * **Python** - Programming language used
  * **Django** - Python web framework used
  * **YouTube Data API v3** - API used to fetch YouTube playlists and videos
  * **Bootstrap** - Front-end component library used
