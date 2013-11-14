from flask import request, Flask, render_template
from functools import wraps

app = Flask(__name__)
app.config.from_object('config')

# This happens after EVERY request, currently disabling all cache, mostly for IE
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 0
    return response

def modern_browser_required(fn):
    """
    If you decorate a view with this, it will ensure the user is using a modern
    browser. If not sends them an html page to tell them to upgrade.

    :param fn: The view function to decorate.
    """
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        browser = request.user_agent.browser
        major_version = request.user_agent.version and int(request.user_agent.version.split('.')[0])

        # Limit access from known unsupoorted browsers
        if (browser == 'msie' and major_version < 9):
            return render_template("bad_browser.html", current_browser="Internet Explorer %d" % major_version )

        # All good, so carry on with original view
        return fn(*args, **kwargs)
    return decorated_view

app.template_folder = app.config['TEMPLATE_FOLDER']

# Setup a cache system
if True or app.config['DEBUG']:
    from werkzeug.contrib.cache import SimpleCache
    cache = SimpleCache()
else:
    from werkzeug.contrib.cache import MemcachedCache
    cache = MemcachedCache(['127.0.0.1:11211'])

# This route sets up a catchall. This is needed for HTML5 Url History
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@modern_browser_required
def index(path):
    response = render_template("index.html")

    browser = request.user_agent.browser
    major_version = request.user_agent.version and int(request.user_agent.version.split('.')[0])

    # # Inject the livereload for use with grunt's livereload, IE < 10 no web sockets
    if app.config['DEBUG'] and not (browser == 'msie' and major_version < 10):
                response = response.replace(
                    "</body>",
                    """
            <!-- livereload snippet -->
            <script>document.write('<script src="http://'
            + (location.host || 'localhost').split(':')[0]
            + ':35729/livereload.js?snipver=1"><\/script>')
            </script>
        </body>""")

    return response


# Serve static files that are usually served with production web server
#if app.config['DEBUG']:
#    from werkzeug import SharedDataMiddleware
#    import os
#    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
#        '/img/': os.path.join(app.config.get("MANHATTAN_ROOT"), 'app/images'),
#        '/styles/': os.path.join(app.config.get("MANHATTAN_ROOT"), '.tmp/styles'),
#        '/': os.path.join(app.config.get("MANHATTAN_ROOT"), 'app')
#    })

