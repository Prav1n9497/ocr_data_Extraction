import streamlit as st
import easyocr
import mysql.connector
import re

mysql_connection = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="admin",
    database="ocr"
)
mysql_cursor = mysql_connection.cursor()

st.title("OCR Data Extraction from Business Cards")
st.header("Upload a Business Card Image for OCR Data Extraction")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    image = uploaded_file.read()
    

    # Commit the transaction and close the connection
    # connection.commit()
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    data = {}
    ind = 0
    print(result)
    for d in result:
        if "www" in d[1].lower():
            data["website"] = d[1]
        elif "@" in d[1]:
            data["email"] = d[1]
        
        elif "-" in d[1]:
            data["phone"] = d[1]
        
        elif ind ==0:
            data["name"] = d[1]
        
        elif ind ==1:
            data["designation"] = d[1]
        elif ind == len(result)-1:
            data["company"] = data.get("company",[])
            data["company"].append(d[1])

        # regex to check number and alphabet
        elif re.findall("^[0-9]+ [a-zA-Z]+", d[1]) or re.findall("^[a-zA-Z]+ [0-9]+",d[1]):
            print("Address:\n\n\n")
            data["address"] = data.get("address",[])
            data["address"].append(d[1])
            print(data["address"])
        ind+=1


    insert_query = "INSERT INTO business_card (name	,designation,address,phone,email,website,company,image) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    mysql_cursor.execute(insert_query, (data["name"],data["designation"],str(data["address"]),data["phone"],data["email"],data["website"],str(data["company"]),image))
    st.write(data)
    mysql_connection.commit()