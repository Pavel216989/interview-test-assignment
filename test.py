"""
Sends post-requests with a set of jsons that need to return a status code. Validates whether the status code is correct.
"""
import requests


def test_response_code(url: str, jsons: list, expected_status_code: int):
    """
    Check status codes for a list of jsons
    :param url: api endpoint
    :param jsons: list of jsons to validate
    :param expected_status_code: expected status code (e.g. 200 or 400)
    :return: Inform if tests were passed
    """
    for request in jsons:
        response = requests.post(url=url, json=request)
        assert response.status_code == expected_status_code, f"Wrong status code for {request}."
    return f"all tests passed: {url}"

# User Events tests
url = "http://0.0.0.0:5000/track"
correct_event_jsons = []
# one event with eventName, metadata and timestampUTC
correct_event_jsons.append(
    {"userId": "ab132", "events": [{"eventName": "login", "metadata": {}, "timestampUTC": 10}]})
# one event with eventName and metadata, without timestampUTC
correct_event_jsons.append(
    {"userId": "ab132", "events": [{"eventName": "logout", "metadata": {"os":"linux"}}]})
# two events with eventName only
correct_event_jsons.append(
    {"userId": "ab132", "events": [{"eventName": "login"}, {"eventName": "logout"}]})

wrong_events_jsons = []
# wrong events type
wrong_events_jsons.append(
    {"userId": "ab132", "events": {"eventName":"login"}})
# wrong userId type
wrong_events_jsons.append(
    {"userId": 123, "events": [{"eventName": "login", "metadata": {}, "timestampUTC": 10}]})
# misspelled field eventName -> events_name
wrong_events_jsons.append(
    {"userId": "ab132", "events": [{"events_name": "login", "metadata": {}, "timestampUTC": 10}]})

print(test_response_code(url, correct_event_jsons, 200))
print(test_response_code(url, wrong_events_jsons, 400))

# Alias tests
url = "http://0.0.0.0:5000/alias"
correct_alias_jsons = []
# all parameters correct
correct_alias_jsons.append(
    {"newUserId": "abb1211", "originalUserId": "ab132", "timestampUTC": 10})
# all parameters without timestampUTC
correct_alias_jsons.append(
    {"newUserId": "abb1211", "originalUserId": "ab132"})

wrong_alias_jsons = []
# wrong userId type
wrong_alias_jsons.append(
    {"newUserId": 123, "originalUserId": "ab132", "timestampUTC": 10})
# wrong timestampUTC type
wrong_alias_jsons.append(
    {"newUserId": "abb1311", "originalUserId": "ab132", "timestampUTC": "10"})

print(test_response_code(url, correct_alias_jsons, 200))
print(test_response_code(url, wrong_alias_jsons, 400))

# Profile tests
url = "http://0.0.0.0:5000/profile"

correct_profile_jsons = []
# all parameters correct
correct_profile_jsons.append(
    {"userId": "new_user_id", "attributes": {"name":"Pavel", "location":"Lisbon"}, "timestampUTC": 0})

wrong_profile_jsons = []
# wrong attributes type
wrong_profile_jsons.append(
    {"userId": "new_user_id", "attributes": [{"name":"Pavel", "location":"Lisbon"}], "timestampUTC": 0})
# misspeled attributes name
wrong_profile_jsons.append(
    {"userId": "new_user_id", "att": {"name":"Pavel", "location":"Lisbon"}})

print(test_response_code(url, correct_profile_jsons, 200))
print(test_response_code(url, wrong_profile_jsons, 400))
