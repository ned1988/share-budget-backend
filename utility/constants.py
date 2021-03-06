from datetime import datetime


class Constants:
    class JSON:
        def __init__(self):
            pass

        date = 'date'
        name = 'name'
        limit = 'limit'
        email = 'email'
        price = 'price'
        token = 'token'
        total = 'total'
        result = 'result'
        status = 'status'
        user_id = 'userID'
        message = 'message'
        group_id = 'groupID'
        password = 'password'
        last_name = 'lastName'
        date_format = '%Y-%m-%d'
        first_name = 'firstName'
        expense_id = 'expenseID'
        is_removed = 'isRemoved'
        time_stamp = 'timeStamp'
        pagination = 'pagination'
        period_date = 'periodDate'
        internal_id = 'internalID'
        category_id = 'categoryID'
        pagination_start = 'start'
        pagination_total = 'total'
        user_group_id = 'userGroupID'
        creation_date = 'creationDate'
        user_not_exist = 'userNotExist'
        pagination_page_size = 'pageSize'
        budget_limit_id = 'budgetLimitID'
        creator_user_id = 'creatorUserID'
        modified_user_id = 'modifiedUserID'
        invitation_token = 'invitationToken'
        category_limit_id = 'categoryLimitID'

        category_not_exist = 'category_not_exist'
        group_is_not_exist = 'group_is_not_exist'
        user_is_already_exist = 'user_is_already_exist'
        permission_not_allowed = 'Permission not allowed'
        user_is_not_creator_of_entity = 'user_is_not_creator_of_entity'

    registration_resource_path = '/registration'
    project_email = 'sharebudgetproject@gmail.com'

    default_page_size = 50
    default_categories = ['Home', 'Food', 'Transport', 'Sport']

    def __init__(self):
        pass

    @staticmethod
    def default_response(response, time_stamp=datetime.utcnow(), pagination=None):
        result = {Constants.JSON.result: response,
                  Constants.JSON.time_stamp: time_stamp.isoformat()}

        if pagination is not None:
            pagination_dict = {Constants.JSON.pagination_total: pagination.total,
                               Constants.JSON.pagination_start: pagination.page,
                               Constants.JSON.pagination_page_size: pagination.per_page}
            result[Constants.JSON.pagination] = pagination_dict

        return result

    @staticmethod
    def error_reponse(message):
        result = {Constants.JSON.message: message}
        return result
