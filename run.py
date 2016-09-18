import os
import sys
from app import app

reload(sys)
sys.setdefaultencoding('utf-8')
port = int(os.environ.get('PORT', 8080))

if len(sys.argv) > 1 and sys.argv[1] == 'public':
    host = '0.0.0.0'
else:
    host = 'localhost'

app.run(debug=True, host=host, port=port)
