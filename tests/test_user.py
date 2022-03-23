import pytest
from specklepy.api.client import SpeckleClient
from specklepy.api.models import Activity, ActivityCollection, User
from specklepy.logging.exceptions import SpeckleException


@pytest.mark.run(order=1)
class TestUser:
    def test_user_get_self(self, client, user_dict):
        fetched_user = client.user.get()

        assert isinstance(fetched_user, User)
        assert fetched_user.name == user_dict["name"]
        assert fetched_user.email == user_dict["email"]

        user_dict["id"] = fetched_user.id

    def test_user_search(self, client, second_user_dict):
        search_results = client.user.search(search_query=second_user_dict["name"][:5])

        assert isinstance(search_results, list)
        assert isinstance(search_results[0], User)
        assert search_results[0].name == second_user_dict["name"]

        second_user_dict["id"] = search_results[0].id

    def test_user_get(self, client, second_user_dict):
        fetched_user = client.user.get(id=second_user_dict["id"])

        assert isinstance(fetched_user, User)
        assert fetched_user.name == second_user_dict["name"]
        assert fetched_user.email == second_user_dict["email"]

        second_user_dict["id"] = fetched_user.id

    def test_user_update(self, client):
        bio = "i am a ghost in the machine"

        failed_update = client.user.update()
        updated = client.user.update(bio=bio)

        me = client.user.get()

        assert isinstance(failed_update, SpeckleException)
        assert updated is True
        assert me.bio == bio

    def test_user_activity(self, client: SpeckleClient, second_user_dict):
        my_activity = client.user.activity(limit=10)
        their_activity = client.user.activity(second_user_dict["id"])

        assert isinstance(my_activity, ActivityCollection)
        assert isinstance(my_activity.items[0], Activity)
        assert my_activity.totalCount > 0
        assert isinstance(their_activity, ActivityCollection)

        older_activity = client.user.activity(before=my_activity.items[0].time)

        assert isinstance(older_activity, ActivityCollection)
        assert older_activity.totalCount < my_activity.totalCount
