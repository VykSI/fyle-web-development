import json
import requests
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
import math
GITHUB_ACCESS_TOKEN = 'YOUR_GITHUB_API'
headers = {'Authorization': f'token {GITHUB_ACCESS_TOKEN}'}

def search(request):
  
    data = json.loads(request.body.decode('utf-8'))

    
    username = data.get('username', '')
    reposearchinp = data.get('repoSearchValue', '')
    cache_key = f'github_repos_{username}'
    cached_data = cache.get(cache_key)
    per_page=int(data.get('nop',''))
    if cached_data is not None:
        repos = [repo for repo in cached_data['repositories'] if reposearchinp.lower() in repo.get('name', '').lower()]
        nop = int(math.ceil(len(repos) / per_page))
        return JsonResponse({
            'logo': cached_data.get('logo', ''),
            'location': cached_data.get('location', ''),
            'url': cached_data.get('url', ''),
            'repositories': repos,
            'languages': cached_data.get('languages', {}),
            'number_of_pages': nop
        }, status=200)
    else:
        return JsonResponse({'error': 'No cached data found for the user.'}, status=400)





def get_user_repositories_and_languages(username):
    # Fetch repositories from GitHub API
    
    
    try:
        repositories=[]
        for i in range(1,8):
            api_url = f'https://api.github.com/users/{username}/repos?page={i}&per_page=100'
            response = requests.get(api_url,headers=headers)
            if response.status_code == 200:
                repositori = response.json()
                if len(repositori)<=0:
                    break
                else:
                    repositories.extend(repositori)
                   
                
                # Fetch languages, stars, and forks for each repository in a batch
        languages = {}
        

        for repo in repositories:
            repo_name = repo['name']
            languages_url = repo['languages_url']

            # Check if languages are already cached for the repository
            cached_languages = cache.get(f'languages_{repo_name}')
            if cached_languages is not None:
                languages[repo_name] = cached_languages
            else:
                # Fetch languages for the repository
                repo_languages_response = requests.get(languages_url,headers=headers)
                if repo_languages_response.status_code == 200:
                    repo_languages = repo_languages_response.json()
                    languages[repo_name] = repo_languages
                    # Cache languages for the repository for 1 hour
                    cache.set(f'languages_{repo_name}', repo_languages, 3600)
                else:
                    return JsonResponse({'error': f'Failed to fetch languages for repository {repo_name}. Status code: {repo_languages_response.status_code}'}, status=500)

        return repositories, languages

            

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


def get_or_cache_repositories(cache_key, username):
    # Check if repositories are already cached
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        # Use cached data if the username is the same
        if cached_data.get('username') == username:
            return  cached_data['repositories'], cached_data['languages'], cached_data['logo'],cached_data['location'],cached_data['url']

    # Fetch user information from GitHub API
    user_info_url = f'https://api.github.com/users/{username}'
    try:
        user_info_response = requests.get(user_info_url,headers=headers)
        if user_info_response.status_code == 200:
            user_info = user_info_response.json()
            avatar_url = user_info.get('avatar_url', '')
            location = user_info.get('location', '')
            github_url = user_info.get('html_url', '')
            # Fetch repositories, languages, stars, and forks for the user
            repositories, languages= get_user_repositories_and_languages(username)

            # Cache user information, repositories, languages, stars, and forks for 5 minutes
            cache.set(cache_key, {'username': username, 'logo': avatar_url,'location':location,'url':github_url, 'repositories': repositories,
                                  'languages': languages}, 300)

            return  repositories, languages,avatar_url,location,github_url

        else:
            return JsonResponse({'error': f'Failed to fetch user information. Status code: {user_info_response.status_code}'}, status=404)

    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


def get_github_repos(request):
    if request.method == 'GET':
        return render(request, 'github_repositories.html')

    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        # Extract the username from the data
        username = data.get('username', '')
        page_start = data.get('start', '')
        page_end = data.get('end', '')
        cache_key = f'github_repos_{username}'

        # Fetch user information, repositories, languages, stars, and forks from cache or GitHub API
        repositories, languages,avatar,location,url = get_or_cache_repositories(cache_key, username)

        # Paginate the repositories based on the provided start and end indices
        try:
            page_start = int(page_start)
            page_end = int(page_end)
            if((page_end-page_start)>len(repositories)):
                return JsonResponse({'logo': avatar,'location':location,'url':url, 'repositories': repositories, 'languages': languages,
                                  'number_of_pages': 1}, status=200)
            else:
                paginated_repos = repositories[page_start:page_end]
                nop = int(math.ceil(len(repositories) / (page_end-page_start)))
                return JsonResponse({'logo': avatar,'location':location,'url':url, 'repositories': paginated_repos, 'languages': languages,
                                    'number_of_pages': nop}, status=200)
        except ValueError:
            return JsonResponse({'error': 'Invalid page_start or page_end values. Must be integers.'}, status=400)
