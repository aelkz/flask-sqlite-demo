from app import (
    app,
)
from app.query_helper import (
    init_db
)
import os

if __name__ == "__main__":
    if not os.path.isfile('app.db'):
        init_db()
    app.run(debug=True, host='0.0.0.0', port=8080)
