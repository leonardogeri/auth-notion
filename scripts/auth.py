import os
from wsgiref import headers
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import psycopg2
from functions import notionTools, utils, envVars, auth, notionTools, UrlVars


app = Flask(__name__)

@app.route('/redirect', methods=['GET', 'POST'])
def authorizeUser():
   
   code, token_url, callback_uri, search_url, client_id, client_secret, DATABASE_URL, dt = envVars.getStaticVars('code', 'v1')
   encoded_u, data_body = auth.generateCredentials(client_id, client_secret)
   access_token_response, response = notionTools.getAccessToken(token_url, encoded_u, data_body)    
   access_token, bot_id, workspace_id, user_id, email, name, user_workspace_id = auth.getUserInfo(access_token_response)

   headers, search_payload = notionTools.notionParams(access_token)

   database_id = getDatabaseId(search_url, search_payload, headers)

   # define sql commands
   cmd_create_action_table = """INSERT INTO workspaces (
                                 id,
                                 access_token,
                                 url_code,
                                 user_id,
                                 email, 
                                 bot_id, 
                                 workspace_id, 
                                 dt_partition, 
                                 name,
                                 database_id
                                )
                                VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                                ON CONFLICT (id) 
                                DO UPDATE SET 
                                 url_code = EXCLUDED.url_code,
                                 database_id = EXCLUDED.database_id;
                             """.format(user_workspace_id, access_token, code, user_id, email, bot_id, workspace_id, dt, name, database_id)

   # execute
   con = None
   try:
       # create a new database connection by calling the connect() function
       con = psycopg2.connect(DATABASE_URL)

       # switch on autocommit
       con.autocommit = 1

       #  create a new cursor
       cur = con.cursor()

       # execute an SQL statement to get the HerokuPostgres database version
       cur.execute(cmd_create_action_table)

       # close the communication with the HerokuPostgres
       cur.close()
   except Exception as error:
       print('Could not connect to the Database.')
       print('Cause: {}'.format(error))

   finally:
       # close the communication with the database server by calling the close()
       if con is not None:
           con.close()
           print('Database connection closed.')   
   return render_template('welcome.html', code=code)
