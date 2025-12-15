# Meeting Scheduler Webapp

A Django-based web application for scheduling meetings and presentations.

## Prerequisites

- Docker
- Docker Compose

## Environment Variables

The application requires the following environment variables to be set for security:

- `SECRET_KEY`: A secret key used by Django for cryptographic signing. Generate a random string for production.
- `ADMIN_PASSWORD`: The password for the admin user created by the `seed_admin` management command.

For both Docker deployment and local development, create a `.env` file in the project root with these variables (note: `.env` is ignored by git).

Example `.env` file:

```
SECRET_KEY=your-random-secret-key-here
ADMIN_PASSWORD=your-secure-admin-password
```

## Setup and Running

1. Clone the repository:
   ```
   git clone <repository-url>
   cd match-runde-terminator
   ```

2. Build and run the application:
   ```
   docker-compose up --build
   ```

3. Access the application at http://localhost:8000

## Database Setup

The application uses SQLite, and the database file is persisted via a Docker volume.

On first run, the database will be created and migrations applied automatically.

## Seeding Data

To populate the database with initial data:

1. Create an admin user:
   ```
   docker-compose exec web python manage.py seed_admin
   ```

2. Seed sample data:
   ```
   docker-compose exec web python manage.py seed_data
   ```

## Development

For local development without Docker:

1. Install Python 3.11 and pip
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py migrate
   ```
5. Start the server:
   ```
   python manage.py runserver
   ```

## Testing

Run tests with:
```
python manage.py test
```

## Project Structure

- `meeting_scheduler/`: Django project settings
- `schedule/`: Main app with models, views, templates
- `requirements.txt`: Python dependencies
- `Dockerfile`: Docker image definition
- `docker-compose.yml`: Docker Compose configuration