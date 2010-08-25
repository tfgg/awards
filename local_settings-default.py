# Debug settings
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'fffffffffffffffffff' # make unique

# If you have a local SMTP server with no authentication for local connections
EMAIL_HOST = "localhost"

# If you want to use GMail's SMTP server
#EMAIL_HOST = "smtp.gmail.com"
#EMAIL_HOST_USER = "you@gmail.com"
#EMAIL_HOST_PASSWORD = "your_password"
#EMAIL_USE_TLS = True
#EMAIL_PORT = 587

# Setting this to blank disables GA tracking
GOOGLE_ANALYTICS_ID = ""
