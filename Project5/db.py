#!/usr/bin/python3 

import mysql.connector
#from mysql.connector import Error
#from mysql.connector import errorcode

humidity = []
temp = []

def create_table():
	magicwand_table_exist = "SHOW TABLES LIKE 'MAGICWAND1'"
	cursor.execute(magicwand_table_exist)
	result_magicwand = cursor.fetchone()
	if result_magicwand:
		print ('there is a table named MAGICWAND1')
	else:
		print ('there are no tables named "MAGICWAND1"')
		cursor.execute("CREATE TABLE MAGICWAND1(id INT NOT NULL AUTO_INCREMENT, Label VARCHAR(20) NOT NULL, Image_correct VARCHAR(20) NOT NULL, Image_wrong VARCHAR(20) NOT NULL, Voice_correct VARCHAR(20) NOT NULL, Voice_wrong VARCHAR(20) NOT NULL, PRIMARY KEY (id));")
 
def put_data(a, c, d, e, f):
	#sql_insert_blob_query = """ INSERT INTO MAGICWAND
         #                 (Label, Image, Image_correct, Image_wrong, Voice_correct, Voice_wrong) VALUES (%s,%s,%s,%s,%s,%s)"""
	#empPicture = convertToBinaryData(b)
	#insert_blob_tuple = (a, empPicture, c, d, e, f)
	#result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
	cursor.execute("INSERT INTO MAGICWAND1 (Label, Image_correct, Image_wrong, Voice_correct, Voice_wrong) VALUES (%s, %s, %s,%s, %s)", (a, c, d, e, f))
	print("Record inserted successfully into MAGICWAND able")
	mariadb_connection.commit()
	
def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
		
def get_data(photo):
	sql_fetch_blob_query = """SELECT Image from MAGICWAND """
	
def get_data():
	
	#fetch_data = "SELECT * FROM MAGICWAND1 ORDER BY id DESC LIMIT 10"
	fetch_data = "SELECT * FROM MAGICWAND1"
	cursor.execute(fetch_data)
	count = int(cursor.rowcount)
	row = cursor.fetchall()
	print (row)



mariadb_connection = mysql.connector.connect(user='srisan', password='srisan1234', database='super_project')
cursor = mariadb_connection.cursor()
create_table()

put_data("car",10,20,30,40)
get_data()

mariadb_connection.close()
