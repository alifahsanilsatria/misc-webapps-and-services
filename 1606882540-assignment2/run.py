from service1 import app as app1
from service2 import app as app2
from service3 import app as app3

import sys

if __name__ == '__main__':
    service_option = sys.argv[1]

    if service_option == 'service1':
        from service1 import routes
        app1.run(debug=True)
    elif service_option == 'service2':
        from service2 import routes
        app2.run(debug=True)
    elif service_option == 'service3':
        from service3 import routes
        app3.run(debug=True)