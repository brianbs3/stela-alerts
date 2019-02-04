import boto3, pymysql.cursors, json, time, decimal, os, datetime

db_host = os.environ["DB_HOST"]
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
db_port = os.environ["DB_PORT"]
db_config = {'host': db_host, 'user': db_user, 'passwd': db_pass, 'db': db_name, 'connect_timeout': 5, 'port': int(db_port), 'charset': 'utf8', 'use_unicode':True}

def db_conn():
    num_db_attempts = 0
    while num_db_attempts < 10:
        try:
            print("Trying to establish a connection to MySQL.\n")
            conn = pymysql.connect(**db_config)

            print("Connection established..\n")
            return conn
        except pymysql.Error, e:
            try:
                print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]) + '\n')
            except IndexError:
                print("MySQL Error: %s" % str(e) + '\n')
        num_db_attempts += 1
        time.sleep(10)
    raise Exception("Error: could not connect to DB!\n")

def getUpcomingAppointments():
    conn = db_conn()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM stela.appointmentsview WHERE ts BETWEEN DATE_ADD(CURDATE(), INTERVAL 1 day) AND DATE_ADD(CURDATE(), INTERVAL 2 day)  AND appointmentAlert = 1"
    cursor.execute(query)
    appointments = []
    for row in cursor:
        appointments.append(row)
        # print row
    # print cursor.fetchAll()
    return appointments

def processAppointments(appt):
    client = boto3.client("sns")
    message = ""
    toPhone = ""
    formattedDate = ""
    for a in appt:
        fd = datetime.datetime.strptime(str(a['ts']), '%Y-%m-%d %H:%M:%S')
        formattedDate = fd.strftime('%m/%d/%Y')
        formattedTime = fd.strftime('%I:%M %p')
        message = "This is a friendly reminder from Inspirations Salon that you have an appointment on " + formattedDate + " at " + formattedTime + " with " + a['stylistFirstName'] + " " + a['stylistLastName'] + "."
        toPhone = "+1" + str(a['areaCode']) + str(a['phonePrefix'] + str(a['phoneLineNumber']))
        print message + " - " + toPhone
        client.publish(
            PhoneNumber = toPhone,
            Message = message
        )

if __name__ == '__main__':
    # try:
        appointments = getUpcomingAppointments()
        processAppointments(appointments)



        # # Send your sms message.

    # except Exception, e:
    #     print(e)
    # except:
    #     import traceback
    #     print("Unhandled exception caught!\n")
    #     print(traceback.print_exc())
    # finally:
    #     exit(0)


