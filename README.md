# Workout diary

This app was developed as a project for the [Databases and Web Programming](https://hy-tsoha.github.io/materiaali/) course, which focuses on building a web application that utilizes a database, using Python (Flask) and PostgreSQL.

This app is a workout diary where users can log their training sessions, track progress and interact with other users. It also includes basic authentication and social features, like adding friends, viewing their workouts, and leaving comments.

## What I learned
- web development in general and principles behind dynamic websites
- building a secure web application
- database integration
- designing of a database and its queries
- deployment practices

#### Technologies
- Python
- Flask
- PostgreSQL
- Git version control
- HTML
- CSS

## Features
A user can..
- ..create an account, log in, and log out.
- ..add a new workout.
- ..delete their own workout.
- ..view their own workouts and details on their homepage.
- ..view a summary section showing the total duration and total number of workouts.
- ..send a friend request to another user by searching for their username in the system.
- ..confirm friendship when other user sends a friend request.
- ..remove friendship (which then deletes the friendship from both users)
- ..view friend's homepage and workouts.
- ..write a comment for either their own or friend's workout.
- ..delete a comment that they have written.

## Instructions for launching the app locally

1) Clone this repository to your local machine.

2) If you haven’t installed PostgreSQL and are using Linux, follow [these instructions](https://github.com/hy-tsoha/local-pg).   
  For installation instructions on other systems, visit [PostgreSQL's official website](https://postgresql.org/download/).

3) Open a new terminal window, navigate to the directory where PostgreSQL was installed, and start the database with the command:
    ```$ start-pg.sh```

4) Open another terminal window and launch the PostgreSQL interpreter with:   
    ```$ psql```    
  Create a new database for the application using the command:    
    ```user=# CREATE DATABASE <database_name>;```

5) Navigate to the root directory of the application and create a .env file.
If you installed PostgreSQL following the first link, set the file’s content as:      
  ```
  DATABASE_URL=postgresql+psycopg2:///<database_name>    
  SECRET_KEY=<secret_key>
  ```
  Otherwise:   
  ```
  DATABASE_URL=postgresql:///<database_name>   
  SECRET_KEY=<secret_key>
  ```

6) Activate a virtual environment and install the application dependencies with the following commands:    
  ```$ python3 -m venv venv```    
  ```$ source venv/bin/activate```    
  ```$ pip install -r ./requirements.txt```


7) Define the database schema by running the following command in the application’s root directory:   
```$ psql -d <database_name> < schema.sql```  

8) Start the previously created database in the PostgreSQL interpreter with:    
```user=# \connect <database_name>;```  

9) Finally, run the application from its root directory with:   
```$ flask run```




