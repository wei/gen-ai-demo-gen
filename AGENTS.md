# Follow Best Practices
- Don't use python virtual environments, use python directly
- All the commands should run on macOS.
- I already created a .env with a Google Gemini API Key (labeled as `GEMINI_API_KEY`) for you to use.
- Do not run any commands in the background using '&'. Do not chain any commands.
- Use AJAX to make API requests from the frontend to the backend
- index.html should be placed under templates directory.
- Make sure all endpoints input and output are in JSON format and properly serialized.
- Chat responses should be in markdown without any HTML tags or tables for better readability.

# Project Dependencies
- Install the following packages using `pip3` and use in the project: `flask`, `google-generativeai`, `markdown`, and `python-dotenv`.
- ngrok has been installed and available in $PATH

# Styling
- Use Tailwind for styling to make our project look professional.
- Use the Tailwind CDN. Do not compile it locally.

# Accessibility
- Always run `python3 app.py` to start the python server once the application is ready for testing.
- Use ngrok to make our localhost webapp accessible from other computers.
- When running ngrok, always use my custom ngrok domain: rested-asp-welcomed.ngrok-free.app
