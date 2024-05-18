import sqlite3
import os
import json
import  pypdf
from pypdf import PdfReader
import spacy
import numpy as np
import re

# Create vector database

def create_database():
    try:
        if not os.path.exists('embedding_database.db'):
            conn = sqlite3.connect('embedding_database.db')
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS embeddings
                              (id INTEGER PRIMARY KEY, content TEXT , vector TEXT)''')
            conn.commit()
            conn.close()
            return "Database created successfully."
        else:
            return "Database already exists."
    except Exception as e:
        return "Error creating database: " + str(e)

# Insert data into vector database 

def insert_embedding(chunk,embedding_vector):
    try:
        conn = sqlite3.connect('embedding_database.db')
        cursor = conn.cursor()
        embedding_json = json.dumps(embedding_vector)
        cursor.execute("INSERT INTO embeddings (content,vector) VALUES (?,?)", (chunk,embedding_json))
        conn.commit()
        conn.close()
        return "Embedding vector inserted successfully."
    except Exception as e:
        print('Error inserting embedding vector:'+ str(e))
        return "Error inserting embedding vector: " + str(e)
       
# Retrieve Data from vector Database

def retrieve_embeddings():
    try:
        conn = sqlite3.connect('embedding_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM embeddings")
        rows = cursor.fetchall()
        content_list=[]
        embeddings_list = []

        for row in rows:
            retrived_content_list = row[1]
            content_list.append(retrived_content_list)
            retrieved_embedding_vector = json.loads(row[2])
            embeddings_list.append(retrieved_embedding_vector)

        conn.close()
        return content_list,embeddings_list
    except Exception as e:
        print("Error retrieving embeddings: " + str(e))
        return [],[]
    
# Convert pdf data in to multiple Junks

def content_curation(path):
    file = open(path, 'rb')
    pdf_reader =  pypdf.PdfReader(file)
    chunks = []
 
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        for i in range(0, len(text), 1000):
            chunks.append(text[i:i+1000])

    file.close()
    return(chunks)

# Convert text chunk into vector array

def convert_nltovector(chunks):
    nlp = spacy.load('en_core_web_sm')
    embedding_vectors = []

    for chunk in chunks:
        doc = nlp(chunk)
        embedding_vector = doc.vector
        array_vec = np.array(embedding_vector)
        insert_embedding(chunk,array_vec.tolist())
        embedding_vectors.append(array_vec)

    return embedding_vectors

# Snapshot of vector Database into managable array - as Sqllite database will not support vector dotproduct operation

def combine(content,arrayvector):
    if len(content) > 0:
        combined_database = [[None,None,None] for i in range(len(content))]
        i=0
        for text , vector in zip(content , arrayvector):
            combined_database[i][0] = 0
            combined_database[i][1] = text
            combined_database[i][2] = vector
            i+=1  
        return combined_database 
    else:
        return []

# Accept user input --> Convert into Vector --> Match with vector Database snapshot --> Find Similarity Score --> Create Context for LLM

def accept_user_input(user_input,database_vector_data):

    nlp = spacy.load('en_core_web_sm')
    user_doc = nlp(user_input)
    user_vector = user_doc.vector

    for i in range(len(database_vector_data)):
        similarity = np.dot(user_vector, database_vector_data[i][2]) / (np.linalg.norm(user_vector) * np.linalg.norm(database_vector_data[i][2]))
        database_vector_data[i][0] = similarity
        #print(similarity)

    database_vector_data.sort(key=lambda x: x[0], reverse=True)

    context = f' Summarize below to a kid like a story \n"'
    for i in range(5):
        context += re.sub(r'[^a-zA-Z0-9\s]', ' ', database_vector_data[i][1])
        context += '\n'
        print(f'Similarity Score: {database_vector_data[i][0]}')
    context += '"'


    return(context)

    
if __name__ == "__main__":

    # Create a Vector Database and load it into database
    create_database()
    final_data = content_curation(r'my_novel.pdf')
    convert_nltovector(final_data)

    # Retrieve all embeddings from the database and create a snapshot
    content , arrayvector = retrieve_embeddings()
    database_vector_data = combine(content,arrayvector)

    # Compare retrieved embeddings with new user input
    user_input = "Did sally found any treasure"
    context = accept_user_input(user_input,database_vector_data)
    print(context)