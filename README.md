# ARAMStats

Project to track stats from the video game League of Legends. The project pulls match data from the official League of Legends API and uses an object relational mapper to store the data in a PostgreSQL database.
Runs in a docker compose container; one container for the frontend to display the stats and another for the backend that makes API calls and performs data manipulation. 
