def getDate():
    dt = datetime.now(timezone.utc)
    return dt

def getUrlVars(url_var):
    code = request.args.get(url_var)

    return code

def defineNotionUrl(version):
    token_url = 'https://api.notion.com/{}/oauth/token'
    callback_uri = "https://oauth2-notion.herokuapp.com/redirect"
    search_url = 'https://api.notion.com/{}/search'

    return token_url, callback_uri, search_url

def declareEnvVars():
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['SECRET']
    DATABASE_URL = os.environ.get('DATABASE_URL')

    return client_id, client_secret, DATABASE_URL

def getStaticVars(url_var, version):
    code = getUrlVars(url_var)
    token_url, callback_uri, search_url = defineNotionUrl(version)
    client_id, client_secret, DATABASE_URL = declareEnvVars()
    dt = getDate()

    return code, token_url, callback_uri, search_url, client_id, client_secret, DATABASE_URL, dt

def getUserInfo(access_token_response):
    main_json = access_token_response.json()
    access_token = main_json['access_token']
    bot_id = main_json['bot_id']
    workspace_id = main_json['workspace_id']
    user = main_json['owner']['user']
    user_id = user['id']
    email = user['person']['email']
    name = user['name']
    user_workspace_id = user_id + workspace_id
    return access_token, bot_id, workspace_id, user_id, email, name, user_workspace_id

def generateCredentials(client_id, client_secret):
   print('Encoding and generating credentials...')
   
   userpass = client_id + ':' + client_secret
   encoded_u = base64.b64encode(userpass.encode()).decode()
   auth = {"Authorization" : "Basic {}".format(encoded_u)}
   data_body = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': callback_uri}
   
   return encoded_u, data_body

def getAccessToken(token_url, encoded_u, data_body):

   access_token_response = requests.post(token_url, headers= {"Authorization":"Basic {}".format(encoded_u)}, data=data_body)
   response = access_token_response.text
   
   return access_token_response, response

def defineHeaders(access_token):
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13"
        }
    return headers

def notionFilter():

    search_payload = {
       "filter": {
           "value": "database",
           "property": "object"
       },
       "page_size": 100
   }
   
    return search_payload

def notionParams(access_token):
   headers = defineHeaders(access_token)
   search_payload = notionFilter()

   return headers, search_payload

def getDatabaseId(search_url, search_payload, headers):
   db_json = requests.request("POST", search_url, json=search_payload, headers=headers)
   database_id = db_json.json()['results'][0]['id']
   
   return database_id
