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
    app.run(debug=True, port=1337)
