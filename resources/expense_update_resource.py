from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from flask_restplus import Resource, reqparse

from application import api
from model.expense import Expense
from model.user_group import UserGroup
from utility.constants import Constants
from utility.resource_parser import ResourceParser
from utility.response_formatter import ResponseFormatter


def get_parameters(parser):
    ResourceParser.add_default_update_parameters(parser)


get_parser = reqparse.RequestParser()
swagger_get_parser = api.parser()

get_parameters(get_parser)
get_parameters(swagger_get_parser)


class ExpenseUpdateResource(Resource):
    @jwt_required()
    @api.doc(parser=swagger_get_parser)
    def get(self):
        args = get_parser.parse_args()
        user_id = get_jwt_identity()

        query = Expense.query.filter(user_id == UserGroup.user_id, UserGroup.group_id == Expense.group_id)

        time_stamp = args.get(Constants.JSON.time_stamp)
        if type(time_stamp) is tuple:
            time_stamp = time_stamp[0].replace(tzinfo=None)
            query = query.from_self().filter(Expense.time_stamp > time_stamp)
        query = query.order_by(Expense.time_stamp.asc())

        start_page = args[Constants.JSON.pagination_start]
        page_size = args[Constants.JSON.pagination_page_size]

        return ResponseFormatter.format_response(query=query, start_page=start_page, page_size=page_size)
