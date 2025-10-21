\# Client Query Management System 📋

A comprehensive web-based application built with Streamlit for managing
client support queries with role-based access control.

\## Features ✨

\### Client Features - \*\*Submit Queries\*\*: Submit support queries
with priority levels - \*\*Contact Information\*\*: Provide name, email,
and mobile number - \*\*Query Tracking\*\*: View all submitted queries -
\*\*Priority Setting\*\*: Set query priority (Low, Medium, High)

\### Support Team Features - \*\*Query Management\*\*: View all client
queries in a centralized dashboard - \*\*Status Updates\*\*: Update
query status (Open, In Progress, Resolved) - \*\*Assignment\*\*: Assign
queries to support team members - \*\*Automatic Timestamps\*\*: Track
submission and resolution times

\## Technology Stack 🛠️

\- \*\*Frontend\*\*: Streamlit - \*\*Backend\*\*: Python 3.x -
\*\*Database\*\*: MySQL - \*\*Libraries\*\*:  - pandas  - numpy  -
mysql-connector-python  - hashlib (password security)

\## Prerequisites 📋

Before running this application, ensure you have:

1\. Python 3.7 or higher installed 2. MySQL Server installed and running
3. Required Python packages (see Installation)

\## Installation 🚀

\### 1. Clone the Repository \`\`\`bash git clone \<repository-url\> cd
client-query-management \`\`\`

\### 2. Install Required Packages \`\`\`bash pip install streamlit
pandas numpy mysql-connector-python \`\`\`

\### 3. Setup MySQL Database

Create a MySQL database: \`\`\`sql CREATE DATABASE client_queries_mgmt;
\`\`\`

\### 4. Configure Database Connection

Update the \`DB_CONFIG\` in the code if your MySQL settings differ:
\`\`\`python DB_CONFIG = { \'host\': \'localhost\', \'user\': \'root\',
\'password\': \'root\', \# Change to your MySQL password \'database\':
\'client_queries_mgmt\' } \`\`\`

\## Running the Application ▶️

\`\`\`bash streamlit run app.py \`\`\`

The application will open in your default browser at
\`http://localhost:8501\`

\## Default User Accounts 👤

The system comes with two default accounts:

\### Support Account - \*\*Username\*\*: \`support_admin\` -
\*\*Password\*\*: \`support123\` - \*\*Role\*\*: Support

\### Client Account - \*\*Username\*\*: \`client_user\` -
\*\*Password\*\*: \`client123\` - \*\*Role\*\*: Client

\> \*\*Note\*\*: Change these default passwords in production!

\## Usage Guide 📖

\### For Clients

1\. \*\*Registration\*\*  - Click on \"Register\" option  - Enter
username and password (min 6 characters)  - Confirm password and
register

2\. \*\*Login\*\*  - Enter username and password  - Select \"client\"
role  - Click \"Log In\"

3\. \*\*Submit Query\*\*  - Fill in your name (required)  - Add email
and mobile number (optional)  - Enter query heading and details
(required)  - Select priority level  - Click \"Submit Query\"

4\. \*\*View Queries\*\*  - Scroll down to see all your submitted
queries  - View status, priority, and timestamps

\### For Support Team

1\. \*\*Login\*\*  - Enter username and password  - Select \"support\"
role  - Click \"Log In\"

2\. \*\*View All Queries\*\*  - See complete list of all client queries
 - View client details, status, priority, and timestamps

3\. \*\*Update Query Status\*\*  - Enter Query ID  - Select new status
(Open/In Progress/Resolved)  - Optionally assign to a team member  -
Click \"Update Query\"

\## Database Schema 📊

\### \`queries\` Table \| Column \| Type \| Description \|
\|\-\-\-\-\-\-\--\|\-\-\-\-\--\|\-\-\-\-\-\-\-\-\-\-\-\--\| \| query_id
\| INT \| Primary key (auto-increment) \| \| client_name \| TEXT \|
Client name \| \| email_id \| VARCHAR(255) \| Client email \| \|
mobile_number \| VARCHAR(20) \| Client phone \| \| query_heading \| TEXT
\| Query subject \| \| query_text \| TEXT \| Query description \| \|
status \| VARCHAR(50) \| Open/In Progress/Resolved \| \| priority \|
VARCHAR(50) \| Low/Medium/High \| \| submitted_on \| DATE \| Submission
date \| \| submitted_time \| TIME \| Submission time \| \| resolved_on
\| DATE \| Resolution date \| \| resolved_time \| TIME \| Resolution
time \| \| assigned_to \| TEXT \| Assigned support member \|

\### \`users\` Table \| Column \| Type \| Description \|
\|\-\-\-\-\-\-\--\|\-\-\-\-\--\|\-\-\-\-\-\-\-\-\-\-\-\--\| \| user_id
\| INT \| Primary key (auto-increment) \| \| username \| VARCHAR(50) \|
Unique username \| \| password \| VARCHAR(255) \| Hashed password
(SHA-256) \| \| role \| VARCHAR(20) \| client/support \|

\## Security Features 🔒

\- \*\*Password Hashing\*\*: All passwords are hashed using SHA-256 -
\*\*Role-Based Access\*\*: Separate dashboards for clients and support -
\*\*Session Management\*\*: Secure session state handling - \*\*SQL
Injection Protection\*\*: Parameterized queries

\## CSV Data Import 📥

The application automatically imports initial data from a CSV file on
first setup. The CSV should contain: - client_name - email_id -
mobile_number - query_heading - query_text - status - priority -
submitted_on - submitted_time - resolved_on - resolved_time -
assigned_to

\## Troubleshooting 🔧

\### Database Connection Error - Verify MySQL is running - Check
database credentials in \`DB_CONFIG\` - Ensure database
\`client_queries_mgmt\` exists

\### Import Error - Install missing packages: \`pip install
\<package-name\>\` - Verify Python version compatibility

\### CSV Import Issues - Check internet connection (CSV loads from
Google Drive) - Verify CSV format matches expected schema

\## Future Enhancements 🚀

\- \[ \] Email notifications for query updates - \[ \] Advanced search
and filtering - \[ \] Query analytics dashboard - \[ \] File attachment
support - \[ \] Comment/response system - \[ \] Export queries to
PDF/Excel

\## Contributing 🤝

Contributions are welcome! Please: 1. Fork the repository 2. Create a
feature branch 3. Commit your changes 4. Push to the branch 5. Open a
Pull Request

\## License 📄

This project is open-source and available under the MIT License.

\## Support 💬

For issues or questions: - Open an issue in the repository - Contact:
\[your-email@example.com\]

\## Acknowledgments 🙏

\- Built with \[Streamlit\](https://streamlit.io/) - Database:
\[MySQL\](https://www.mysql.com/)

\-\--

\*\*Version\*\*: 1.0.0 \*\*Last Updated\*\*: October 2025
