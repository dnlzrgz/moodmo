# MoodMo - A Self-Hosted Mood Tracking App

MoodMo is an Open-Source, Self-Hosted mood tracking application made to be simple to use and deploy.

## Key Features
### Usage
- Record your mood easily with just a few clicks or taps.
- Correlate mood fluctuations with specific activities and routines.
- Quickly find past mood entries or activities using MoodMo's robust search.
- Navigate seamlessly across all devices thanks to MoodMo's fluid and intuitive design.
- Enjoy a clutter-free interface that prioritizes ease of use above all else.
### Development
- Developed with Django 4.2 and Python >= 3.11.
- Utilizes TailwindCSS for clean and responsive styles.
- No need for Node.js or npm work-arounds.
- Dynamic user interactions provided by Alpine.js + htmx.
- Easily configurable settings through environment variables.
- Docker support with `docker-compose` for development and production environments, including a *testing* version with `PyPy` as the Python interpreter.
- Support for `Mailpit` for local email testing and `AnyMail` for production email.
- Robust auth functionality provided by `django-allauth`, with a ready-to-go custom user model.
- Static files managed with `Whitenoise`.
- Includes a `Makefile` for simplified setup and common tasks along with pre-configured linting tools like `djhtml` and `ruff` ready to use with `pre-commit`.


## Roadmap - Future Features

- [ ] Advanced analytics and visualizations.
- [ ] Multi-language support.
- [ ] Dark mode.
- [ ] Custom user themes.
- [ ] Support for custom moods.
- [ ] Weather integration.
- [ ] Journaling.

## Help Not Wanted but Attention Is Appreciated

At the moment I'm not seeking external contributions through pull requests nor I would accept them, but your attention and feedback are highly appreciated. If you encounter any issues, have suggestions for improvements or just want to share your thoughts on MoodMo, feel free to open an issue!
