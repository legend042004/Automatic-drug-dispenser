import mysql.connector

connection = mysql.connector.connect(host ="localhost", user = "root" , password = "", database = "maindb")

if connection.is_connected():
    print('connection done')
else:
    print('connection fail')

mycursor = connection.cursor()
sql = "UPDATE medicine SET medicineQuantity = medicineQuantity-1 WHERE medicineId = 4"

mycursor.execute(sql)

connection.commit()