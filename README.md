**Automatically BackupTool for postgresql 9.4 | 9.6 on Servers**

This tool uses gmail account and sends dumped sqls to email as an attachment. You can use this tool in servers and cron it to send database dumps automatically. There is a file called .env which are configured to handle backups. There is another important file called **"projects.json"** to handle multiple backups. All backup files are stored in backups folder and all them are deleted after the email sent. 
>projects.json
>-domain: '[domain of your project]'
>-db_name: '[database name of the project]'
>-db_username: '[database username]'
>-db_password: ['database password']

>.env
-SENDER_EMAIL=[this is email that sends backups]
-SENDER_PASSWORD=[Password that sender owns on gmail]
-RECEIVER_EMAIL=[Provide gmail account to send backups]
-BACKUP_DIRECTORY=[Provide working directory]

**TO INSTALL**
Please, install pip install python-dotenv (Python version 2.7)
install pip install python3-dotenv (Python version 3.*)

**TO RUN**
python run_backup.py
