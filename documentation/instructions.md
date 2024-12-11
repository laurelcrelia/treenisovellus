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
