import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host = 'gateway01.ap-southeast-1.prod.aws.tidbcloud.com',
        user = '4CuwMfft8gE2Hqc.root',
        password = 'UndON7nXlwnah6Bo',
        database = 'student_task_manager',
        port = 4000
    )
    return connection

