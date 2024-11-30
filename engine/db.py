import sqlite3

# Establish connection to the database (or create it if it doesn't exist)
con = sqlite3.connect('commands.db', check_same_thread=False)  # Added check_same_thread=False to prevent threading issues

# Create a cursor object to interact with the database
cursor = con.cursor()

# Create the sys_command table if it doesn't exist
query = "CREATE TABLE IF NOT EXISTS sys_command(id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# Create the web_command table if it doesn't exist
query = "CREATE TABLE IF NOT EXISTS web_command(id INTEGER PRIMARY KEY, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)

# Optionally insert data into sys_command (commented out as per your original code)
# query = "INSERT INTO sys_command VALUES (null, 'one note', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.exe')"
# cursor.execute(query)
# con.commit()

# Optionally insert data into web_command (commented out as per your original code)
# query = "INSERT INTO web_command VALUES (null, 'youtube', 'https://www.youtube.com/')"
# cursor.execute(query)
# con.commit()

# We don't close the connection here, so it stays open for the entire program's duration.
# Connection will be closed when the program terminates or explicitly done somewhere else in the code.
