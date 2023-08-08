# YouTube Database Builder
### Project Overview
This project is designed to pull the 50 most popular YouTube videos from the Google YouTube API(https://developers.google.com/youtube/v3) daily from specific regions (US, IN, JP, BR, RU, DE) and store the data in a PostgreSQL database. The data is then digested in a Tableau dashboard, allowing for insightful analysis and visualization of YouTube's most popular content.

### Technologies Used
- Python: The main programming language used for scripting.
- Google API Client Library: For interacting with YouTube's API.
- Pandas: For data manipulation and analysis.
- Airflow: For orchestrating the workflow of the tasks.
- PostgreSQL: For storing the pulled data.
- Tableau: For visualizing the data.
- SQLAlchemy: For SQL toolkit and Object-Relational Mapping (ORM) library for Python.

### Instructions on Implementing
###### Prerequisites
- Python 3.x
- Apache Airflow
- PostgreSQL
- Tableau

### Installation
###### Clone the Repository:
- bash
- Copy code
- git clone <repository_url>

###### Install Dependencies:
- Copy code
- pip install google-api-python-client pandas apache-airflow sqlalchemy psycopg2

###### Configure Airflow:
- Set up the Airflow configuration to include your YouTube API key.
- Configure the PostgreSQL connection in Airflow with the ID postgres_yt.

###### Set Up the Database:
- Ensure that a PostgreSQL database is set up with the appropriate schema for the YouTube data.

###### Schedule the DAG:
- Place the DAG file in your Airflow DAGs folder.
- Start the Airflow web server and scheduler.
- Enable the DAG in the Airflow web UI.

###### Running the Project:
The DAG will run daily if the machine it's on is available, pulling the data and storing it in the PostgreSQL database.

### Tableau Visualization
I chose to explore the data with a Tableau dashboard. The full interactive version of the Tableau dashboard is published on their public site and can be accessed here: https://public.tableau.com/app/profile/lacey.morgan/viz/YouTubeTop50VideostheWeekof84/Dashboard1?publish=yes

<img width="1059" alt="Screen Shot 2023-08-07 at 5 42 45 PM" src="https://github.com/earlyann/youtube_api_airflow/assets/119711479/d48a1f11-753e-4fd2-8bff-c5f8ab1b676f">

### Next Steps
- Expand Region Coverage: Include more regions to get a broader view of popular videos.
- Enhance Data Analysis: Implement more sophisticated data analysis, incorporating other endpoints to derive insights.
- Automate Tableau Public: Set up the automation of the extraction of the SQL data and push it to Tableau Public.

Feel free to fork the project, submit PRs, and contribute to enhancing this YouTube Database Builder.

##### License
This project is licensed under the MIT License - see the LICENSE.md file for details.

Author: Lacey Morgan
