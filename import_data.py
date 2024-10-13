import csv
import mariadb

# Connect to MariaDB database
def connect_db():
    try:
        return mariadb.connect(
            user="vijay",  # Replace with your MariaDB username
            password="vijay123",  # Replace with your MariaDB password
            host="localhost",  # Replace with your MariaDB host
            port=3306,  # Replace with your MariaDB port, if different
            database="tickets_db"  # Replace with your database name
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None

# Insert categories into the 'Categories' table
def insert_categories(cursor, category_name):
    cursor.execute("SELECT id FROM Categories WHERE category_name = %s", (category_name,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO Categories (category_name) VALUES (%s)", (category_name,))
        return cursor.lastrowid
    return result[0]

# Insert agents into the 'Agents' table
def insert_agents(cursor, agent_name, language):
    cursor.execute("SELECT id FROM Agents WHERE agent_name = %s", (agent_name,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO Agents (agent_name, language) VALUES (%s, %s)", (agent_name, language))
        return cursor.lastrowid
    return result[0]

# Insert tickets into the 'Tickets' table
def insert_ticket(cursor, ticket_id, problem_description, category_id, severity, agent_id, solution_comments):
    cursor.execute("""
        INSERT INTO Tickets_history (ticket_id, problem_description, category_id, severity, agent_id, solution_comments)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (ticket_id, problem_description, category_id, severity, agent_id, solution_comments))

# Read data from the CSV file and insert into MariaDB tables
def process_csv(file_path):
    connection = connect_db()
    if connection is None:
        return
    cursor = connection.cursor()

    # Sample agent languages
    languages = ['English', 'French', 'German', 'Spanish']

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ticket_id = int(row['Ticket_ID'])
            problem_description = row['Problem Description']
            category_name = row['Category']
            severity = row['Severity']
            agent_name = row['Agent Name']
            solution_comments = row['Solution Comments']
            language = languages[ticket_id % len(languages)]  # Assign a random language

            # Insert unique category and agent, retrieve their IDs
            category_id = insert_categories(cursor, category_name)
            agent_id = insert_agents(cursor, agent_name, language)

            # Insert ticket
            insert_ticket(cursor, ticket_id, problem_description, category_id, severity, agent_id, solution_comments)

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    # Replace 'tickets.csv' with your actual file path
    process_csv('data/payment_tickets_500.csv')
