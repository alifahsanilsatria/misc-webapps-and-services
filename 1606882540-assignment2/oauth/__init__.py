import requests 

def ambil_token(user, pasw, client_id, client_secret):
  URL = "http://oauth.infralabs.cs.ui.ac.id/oauth/token"
  payload = {'username': user, 'password': pasw, 'grant_type': 'password', 'client_id': client_id, 'client_secret': client_secret}

  r = requests.post(url = URL, data=payload)
  return r

def ambil_resource(access_token):
  URL = "http://oauth.infralabs.cs.ui.ac.id/oauth/resource"
  data_headers = { 'Authorization': 'Bearer ' + access_token }
  r = requests.get(url = URL, headers = data_headers)
  return r