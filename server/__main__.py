import app
import sys

if "debug" in sys.argv:
    app.app.run(debug=True)
else:
    app.app.run(host="0.0.0.0")
