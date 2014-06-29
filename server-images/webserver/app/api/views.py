from flask import Blueprint
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Api, Resource


mod = Blueprint('api', __name__, url_prefix='/api')
api = Api(mod)
auth = HTTPBasicAuth()

users = {
    "travis": "llamas123"
}


@auth.get_password
def get_pw(username):
    if username is not None:
        return users.get(username)
    return None


TEST_LIST = {}
TEST_LIST['test.png'] = { "size": "1 KB",
                          "bytes": 1024,
                          "thumb_exists": True,
                          "rev": "714f029684fe",
                          "modified": 1403618279,
                          "path": "/test.png",
                          "is_dir": False,
                          "icon": "photo",
                          "mime_type": "image/jpeg"}
TEST_LIST['Pictures'] = {"size": "0 bytes",
                         "rev": "38af1b183490",
                         "hash": "37eb1ba1849d4b0fb0b28caf7ef3af52",
                         "bytes": 0,
                         "modified": 1403618278,
                         "thumb_exists": False,
                         "path": "/test.png",
                         "is_dir": True,
                         "icon": "folder",
                         "contents": []}

class ProtectedResource(Resource):
    method_decorators = [auth.login_required]


class MetaData(ProtectedResource):
    def get(self, path=None):
        if path is None or path=="/":
            return [path for path in TEST_LIST.itervalues()]
        return TEST_LIST.get(path)


api.add_resource(MetaData, '/metadata', '/metadata/',
                 '/metadata/<string:path>')
