from group import Group
from tests.base_test import BaseTestCase
from user_group import UserGroup
from users import User


class TestUserUpdateResource(BaseTestCase):
    def parse_result(self, response):
        result = self.result(response)

        return list(map(lambda item: UserGroup(item), result))

    def test_all_users_in_one_group(self):
        self.login()
        current_user = self.default_user()

        # ----------------

        group = Group({})
        group.name = "GROUP_A"
        self.add_and_safe(group)

        user_group = UserGroup({})
        user_group.user_id = current_user.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)
        expected_result = [user_group]

        # ----------------

        user = User({})
        user.first_name = "USER_A"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_B"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        response = self.test_client.get('/user/group/updates', headers=self.default_user_json(current_user))

        actual_result = self.parse_result(response)
        assert expected_result == actual_result

    def test_no_groups(self):
        self.login()
        current_user = self.default_user()

        # ----------------

        user = User({})
        user.first_name = "USER_A"
        self.add_and_safe(user)

        # ----------------

        user = User({})
        user.first_name = "USER_B"
        self.add_and_safe(user)

        # ----------------

        user = User({})
        user.first_name = "USER_C"
        self.add_and_safe(user)

        response = self.test_client.get('/user/group/updates', headers=self.default_user_json(current_user))

        result = self.result(response)
        assert len(result) == 0

    def test_user_group_empty(self):
        self.login()
        current_user = self.default_user()

        group = Group({})
        group.name = "GROUP_1"
        self.add_and_safe(group)

        # ----------------

        user = User({})
        user.first_name = "USER_1"
        self.add_and_safe(user)

        # ----------------

        user = User({})
        user.first_name = "USER_2"
        self.add_and_safe(user)

        # ----------------

        user = User({})
        user.first_name = "USER_3"
        self.add_and_safe(user)

        response = self.test_client.get('/user/group/updates', headers=self.default_user_json(current_user))

        result = self.result(response)
        assert len(result) == 0

    def test_user_group_only_creator(self):
        self.login()

        group = Group({})
        group.name = "GROUP_1"
        self.add_and_safe(group)

        # ----------------

        current_user = self.default_user()

        user_group = UserGroup({})
        user_group.user_id = current_user.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)
        expected_result = [user_group]

        # ----------------

        user = User({})
        user.first_name = "USER_1"
        self.add_and_safe(user)

        # ----------------

        user = User({})
        user.first_name = "USER_2"
        self.add_and_safe(user)

        # ----------------

        user = User({})
        user.first_name = "USER_3"
        self.add_and_safe(user)

        response = self.test_client.get('/user/group/updates',
                                        headers=self.default_user_json(current_user))

        actual_result = self.parse_result(response)
        assert expected_result == actual_result

    def test_user_group_not_all_users(self):
        self.login()
        expected_result = []

        group = Group({})
        group.name = "GROUP_1"
        self.add_and_safe(group)

        # ----------------

        current_user = self.default_user()

        user_group = UserGroup({})
        user_group.user_id = current_user.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_1"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_2"
        self.add_and_safe(user)

        # ----------------

        user = User({})
        user.first_name = "USER_3"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        # ----------------

        response = self.test_client.get('/user/group/updates', headers=self.default_user_json(current_user))

        actual_result = self.parse_result(response)
        assert expected_result == actual_result

    def test_single_user_in_multiple_groups(self):
        self.login()
        expected_result = []

        group_1 = Group({})
        group_1.name = "GROUP_1"
        self.add_and_safe(group_1)

        group_2 = Group({})
        group_2.name = "GROUP_2"
        self.add_and_safe(group_2)

        group_3 = Group({})
        group_3.name = "GROUP_3"
        self.add_and_safe(group_3)

        group_4 = Group({})
        group_4.name = "GROUP_3"
        self.add_and_safe(group_4)

        # ----------------

        current_user = self.default_user()

        user_group = UserGroup({})
        user_group.user_id = current_user.user_id
        user_group.group_id = group_1.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_1"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group_2.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        user_group = UserGroup({})
        user_group.user_id = current_user.user_id
        user_group.group_id = group_2.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_2"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group_3.group_id
        self.add_and_safe(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_3"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group_4.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        user_group = UserGroup({})
        user_group.user_id = current_user.user_id
        user_group.group_id = group_4.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        # ----------------

        response = self.test_client.get('/user/group/updates', headers=self.default_user_json(current_user))

        actual_result = self.parse_result(response)
        assert expected_result == actual_result

    def test_multiple_users_in_multiple_groups(self):
        self.login()
        expected_result = []

        group_1 = Group({})
        group_1.name = "GROUP_1"
        self.add_and_safe(group_1)

        group_2 = Group({})
        group_2.name = "GROUP_2"
        self.add_and_safe(group_2)

        group_3 = Group({})
        group_3.name = "GROUP_3"
        self.add_and_safe(group_3)

        group_4 = Group({})
        group_4.name = "GROUP_3"
        self.add_and_safe(group_4)

        # ----------------

        current_user = self.default_user()

        user_group = UserGroup({})
        user_group.user_id = current_user.user_id
        user_group.group_id = group_1.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_1"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group_2.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        user_group = UserGroup({})
        user_group.user_id = current_user.user_id
        user_group.group_id = group_2.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_2"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group_3.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        user_group = UserGroup({})
        user_group.user_id = current_user.user_id
        user_group.group_id = group_3.group_id
        self.add_and_safe(user_group)
        expected_result.append(user_group)

        # ----------------

        user = User({})
        user.first_name = "USER_3"
        self.add_and_safe(user)

        user_group = UserGroup({})
        user_group.user_id = user.user_id
        user_group.group_id = group_4.group_id
        self.add_and_safe(user_group)

        # ----------------

        response = self.test_client.get('/user/group/updates', headers=self.default_user_json(current_user))

        actual_result = self.parse_result(response)
        assert expected_result == actual_result
