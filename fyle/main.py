import requests
GITHUB_ACCESS_TOKEN = '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'
headers = {'Authorization': f'token {GITHUB_ACCESS_TOKEN}'}
api_url = f'https://api.github.com/users/johnpapa/repos?page=4&per_page=200'
try:
    response = requests.get(api_url,headers=headers)
    
    repo_data=response.json()
    print(len(response.json()),response.status_code)

except requests.exceptions.RequestException as e:
    print(f"Error fetching repository information: {e}")
    print('lol')
