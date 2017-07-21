from flask_restful import inputs
from flask_restful import Resource
from flask_restful import reqparse

from category import Category
from constants import Constants
from response_formatter import ResponseFormatter
from user_group import UserGroup
from shared_objects import swagger_app
from credentials_validator import CredentialsValidator


def get_parameters(parser):
    parser.add_argument(Constants.k_time_stamp, type=inputs.iso8601interval, help='Time stamp date (ISO 8601)',
                        location='headers')
    parser.add_argument(Constants.k_user_id, type=int, help='User ID', location='headers', required=True)
    parser.add_argument(Constants.k_token, help='User token', location='headers', required=True)
    parser.add_argument(Constants.k_pagination_start, help='Start page', type=int)
    parser.add_argument(Constants.k_pagination_page_size, help='Pagination size page', type=int)


get_parser = reqparse.RequestParser()
swagger_get_parser = swagger_app.parser()

get_parameters(get_parser)
get_parameters(swagger_get_parser)


class CategoryUpdateResource(Resource):
    @swagger_app.doc(parser=swagger_get_parser)
    def get(self):
        args = get_parser.parse_args()

        user_id = args[Constants.k_user_id]
        token = args[Constants.k_token]
        status, message = CredentialsValidator.is_user_credentials_valid(user_id, token)

        if status is False:
            return message, 401

        query = Category.query.filter(user_id == UserGroup.user_id,
                                      UserGroup.group_id == Category.group_id)

        time_stamp = args.get(Constants.k_time_stamp)
        if type(time_stamp) is tuple:
            time_stamp = time_stamp[0].replace(tzinfo=None)
            query = query.from_self().filter(Category.time_stamp >= time_stamp)
        query = query.order_by(Category.time_stamp.asc())

        start_page = args[Constants.k_pagination_start]
        page_size = args[Constants.k_pagination_page_size]

        return ResponseFormatter.format_response(query=query, start_page=start_page, page_size=page_size)