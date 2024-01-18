# fyle-web-development

Fyle Web Development is a GitHub repository viewer designed to interact with GitHub APIs. This web application allows users to view specific user repositories and details on GitHub. Users can clone repositories, create and activate virtual environments, install dependencies, and run the server to explore GitHub repositories conveniently. The project emphasizes ease of use and customization, enabling users to tailor their GitHub repository viewing experience.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/VykSI/fyle-web-development.git
cd fyle-web-development/fyle
```

### Create and Activate Virtual Environment

```bash
windows:
python -m venv env
env\Scripts\activate

linux:
pip install virtualenv
virtualenv env
source env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Add your GitHub API to run the code in views.py (GITHUB_ACCESS_TOKEN).

### Run the Server

```bash
python manage.py runserver
```

## Additional Notes

1. Make sure to activate the virtual environment before running the server.
2. Customize the GitHub API integration in views.py as needed for your project.
3. Ensure that you have the necessary dependencies installed from requirements.txt.

