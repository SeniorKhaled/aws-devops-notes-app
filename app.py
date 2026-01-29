from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

# DB configuration
db_config = {
    'user': 'admin',        # Using the admin user we created
    'password': '123456',   # The password for admin
    'host': 'localhost',
    'database': 'notes_db',
    'charset': 'utf8mb4'    # Supports all characters including emojis and Arabic
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Note Management System</title>
    <style>
        :root {
            --primary-color: #2c3e50;
            --accent-color: #3498db;
            --bg-color: #ecf0f1;
            --card-bg: #ffffff;
            --text-color: #2c3e50;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
        }

        h1 {
            color: var(--primary-color);
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #7f8c8d;
            font-size: 1.1rem;
        }

        .input-card {
            background: var(--card-bg);
            padding: 30px;
            border-radius: 15px;
            box-shadow: var(--shadow);
            margin-bottom: 30px;
            border-top: 5px solid var(--accent-color);
        }

        textarea {
            width: 100%;
            height: 100px;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
            font-family: inherit;
            resize: vertical;
            box-sizing: border-box;
            transition: border-color 0.3s;
        }

        textarea:focus {
            outline: none;
            border-color: var(--accent-color);
        }

        button {
            background-color: var(--accent-color);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            margin-top: 15px;
            transition: background-color 0.3s, transform 0.2s;
            width: 100%;
        }

        button:hover {
            background-color: #2980b9;
            transform: translateY(-2px);
        }

        .notes-list {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .note-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 10px;
            box-shadow: var(--shadow);
            border-left: 5px solid var(--accent-color); /* Left border for LTR design */
            transition: transform 0.2s;
        }

        .note-card:hover {
            transform: translateX(5px);
        }

        .note-meta {
            font-size: 0.85rem;
            color: #7f8c8d;
            margin-bottom: 8px;
            border-bottom: 1px solid #eee;
            padding-bottom: 8px;
            display: flex;
            justify-content: space-between;
        }

        .note-content {
            font-size: 1.1rem;
            white-space: pre-wrap;
        }

        /* Mobile Responsiveness */
        @media (max-width: 600px) {
            h1 { font-size: 2rem; }
            .input-card { padding: 20px; }
        }
    </style>
</head>
<body>

    <div class="container">
        <header>
            <h1>Secure Note App</h1>
            <p class="subtitle">DevOps Project on AWS EC2</p>
        </header>

        <div class="input-card">
            <form action="/" method="POST">
                <textarea name="note" placeholder="Write your new note here..." required></textarea>
                <button type="submit">Save Note</button>
            </form>
        </div>

        <div class="notes-list">
            {% for note in notes %}
                <div class="note-card">
                    <div class="note-meta">
                        <span>Created: {{ note[2] }}</span>
                        <span>ID: #{{ note[0] }}</span>
                    </div>
                    <div class="note-content">{{ note[1] }}</div>
                </div>
            {% endfor %}
        </div>
    </div>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Handle form submission
    if request.method == 'POST':
        note_content = request.form['note']
        cursor.execute("INSERT INTO notes (content) VALUES (%s)", (note_content,))
        conn.commit()

    # Retrieve all notes ordered by newest first
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    notes = cursor.fetchall()
    
    # Close connection
    cursor.close()
    conn.close()
    
    return render_template_string(HTML_TEMPLATE, notes=notes)

if __name__ == '__main__':
    # Run the application on port 80 accessible from anywhere
    app.run(host='0.0.0.0', port=80)