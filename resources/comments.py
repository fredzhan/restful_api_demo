from flask_restful import Resource, reqparse
from models.comments import CommentsModel
from utils.env_vars import LOGGER
from flask import jsonify

class Comments(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('kw',
                        type=str,
                        required=True,
                        help="[Required] Keyword in comments to search"
                        )

    def get(self):
        param = self.parser.parse_args()
        kw = param['kw']
        LOGGER.info('Received search keyword: {kw}'.format(kw=kw))
        cm = CommentsModel()
        result = cm.searchComments(kw)
        return jsonify(result)

    def post(self, id):
        pass

    def delete(self, name):
        pass