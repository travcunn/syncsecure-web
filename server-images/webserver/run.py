#!venv/bin/python
from flask_debugtoolbar import DebugToolbarExtension
from app import app


# :::WARNING:::
# This should only be used to launch the development version

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#toolbar = DebugToolbarExtension(app)

app.run(host='0.0.0.0', port=8000)
