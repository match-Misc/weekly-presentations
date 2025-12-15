# AGENTS.md for Meeting Scheduler Project

## Dev environment tips
- Use `python manage.py runserver` to start the development server.
- Activate the virtual environment with `. venv/bin/activate` before running commands.
- Run `python manage.py makemigrations` and `python manage.py migrate` after model changes.
- Use `python manage.py shell` for interactive Django shell.
- Check INSTALLED_APPS in settings.py to ensure the 'schedule' app is included.

## Testing instructions
- Run `python manage.py test` to execute all tests.
- Use `python manage.py test <app_name>` to test a specific app.
- Ensure migrations are applied before testing with `python manage.py migrate`.
- Check for linting with tools like flake8 or black if configured.
- Add or update tests for any code changes, ensuring the test suite passes.

## PR instructions
- Title format: [feature/fix] <Title>
- Always run `python manage.py test` and check for any linting issues before committing.
- Ensure the application runs without errors with `python manage.py runserver`.
- Update documentation or SPEC.md if necessary for changes.