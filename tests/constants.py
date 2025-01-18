# Keeping a constant.py file is preferable to only using 
# contest.py fixtures because you cannot parametrize over
# a fixture with pytest.mark.parametrize()

TIMEZONE_NAMES = [
        "Europe/London",
        "Europe/Paris",
        "America/New_York",
        "America/Los_Angeles",
        "Asia/Tokyo",
        "Australia/Sydney",
    ]