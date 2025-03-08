import sqlite3
import matplotlib.pyplot as plt

# Database Setup
conn = sqlite3.connect("onboarding.db")
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

# Create Tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        experience_level TEXT CHECK(experience_level IN ('Junior', 'Mid', 'Senior')) NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS onboarding_process (
        process_id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        steps TEXT NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        feedback_id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
        comments TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
    )
''')

conn.commit()

# CRUD Operations
def add_employee():
    name = input("Enter Employee Name: ").strip()
    department = input("Enter Department: ").strip()
    experience_level = input("Enter Experience Level (Junior/Mid/Senior): ").strip().capitalize()

    if experience_level not in ["Junior", "Mid", "Senior"]:
        print("Invalid experience level! Please enter 'Junior', 'Mid', or 'Senior'.")
        return

    cursor.execute(
        "INSERT INTO employees (name, department, experience_level) VALUES (?, ?, ?)",
        (name, department, experience_level)
    )
    conn.commit()
    print(f"Employee {name} added successfully!")

def get_all_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    if not employees:
        print("No employees found.")
        return

    fig, ax = plt.subplots()
    ax.set_axis_off()

    # Table headers and data
    headers = ["ID", "Name", "Department", "Experience"]
    table_data = [list(emp) for emp in employees]

    table = ax.table(cellText=table_data, colLabels=headers, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width([0, 1, 2, 3])

    plt.title("Employee List")
    plt.show()

def update_employee():
    employee_id = input("Enter Employee ID to update: ").strip()

    cursor.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,))
    if not cursor.fetchone():
        print("Employee not found.")
        return

    name = input("Enter New Name: ").strip()
    department = input("Enter New Department: ").strip()
    experience_level = input("Enter New Experience Level (Junior/Mid/Senior): ").strip().capitalize()

    if experience_level not in ["Junior", "Mid", "Senior"]:
        print("Invalid experience level! Please enter 'Junior', 'Mid', or 'Senior'.")
        return

    cursor.execute(
        "UPDATE employees SET name=?, department=?, experience_level=? WHERE employee_id=?",
        (name, department, experience_level, employee_id)
    )
    conn.commit()
    print("Employee details updated successfully!")

def delete_employee():
    employee_id = input("Enter Employee ID to delete: ").strip()

    cursor.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,))
    if not cursor.fetchone():
        print("Employee not found.")
        return

    cursor.execute("DELETE FROM employees WHERE employee_id=?", (employee_id,))
    conn.commit()
    print("Employee deleted successfully!")

# Onboarding Plan Personalization
def personalize_onboarding():
    employee_id = input("Enter Employee ID to personalize onboarding: ").strip()

    cursor.execute("SELECT experience_level FROM employees WHERE employee_id=?", (employee_id,))
    result = cursor.fetchone()

    if result:
        experience_level = result[0]
        steps = {
            "Junior": "Introduction, Company Tour, Basic Training",
            "Mid": "Team Integration, Project Assignment",
            "Senior": "Leadership Training, Strategy Meetings"
        }.get(experience_level, "General Onboarding")

        cursor.execute(
            "INSERT INTO onboarding_process (employee_id, steps) VALUES (?, ?)",
            (employee_id, steps)
        )
        conn.commit()
        print(f"Personalized onboarding for Employee {employee_id}: {steps}")
    else:
        print("Employee not found.")

# Feedback Collection
def gather_feedback():
    employee_id = input("Enter Employee ID for feedback: ").strip()

    cursor.execute("SELECT * FROM employees WHERE employee_id=?", (employee_id,))
    if not cursor.fetchone():
        print("Employee not found.")
        return

    try:
        rating = int(input("Enter Rating (1-5): ").strip())
        if rating not in range(1, 6):
            raise ValueError
    except ValueError:
        print("Invalid rating! Please enter a number between 1 and 5.")
        return

    comments = input("Enter Comments: ").strip()

    cursor.execute(
        "INSERT INTO feedback (employee_id, rating, comments) VALUES (?, ?, ?)",
        (employee_id, rating, comments)
    )
    conn.commit()
    print("Feedback recorded successfully!")

# Visualization
def visualize_feedback():
    cursor.execute("SELECT rating, COUNT(*) FROM feedback GROUP BY rating")
    feedback_data = cursor.fetchall()

    if not feedback_data:
        print("No feedback available.")
        return

    ratings, counts = zip(*feedback_data)

    plt.bar(ratings, counts, color=['red', 'orange', 'yellow', 'green', 'blue'])
    plt.xlabel("Rating (1-5)")
    plt.ylabel("Number of Feedbacks")
    plt.title("Onboarding Feedback Distribution")
    plt.xticks(range(1, 6))
    plt.show()

# Menu-driven interface
def main():
    while True:
        print("\n--- Employee Onboarding Optimizer ---")
        print("1. Add New Employee")
        print("2. View All Employees (Table View)")
        print("3. Update Employee Details")
        print("4. Delete Employee")
        print("5. Personalize Onboarding Plan")
        print("6. Gather Onboarding Feedback")
        print("7. Visualize Feedback (Bar Chart)")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            add_employee()
        elif choice == '2':
            get_all_employees()
        elif choice == '3':
            update_employee()
        elif choice == '4':
            delete_employee()
        elif choice == '5':
            personalize_onboarding()
        elif choice == '6':
            gather_feedback()
        elif choice == '7':
            visualize_feedback()
        elif choice == '8':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
    conn.close()
