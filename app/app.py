from config import app

from controllers.bus_controller import api

# register the api
app.register_blueprint(api)

if __name__ == '__main__':
    ''' run application '''
    app.run(host='0.0.0.0', port=5000)
