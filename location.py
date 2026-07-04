import geocoder


def get_current_location():
    """
    Returns the user's current city using IP address.
    """

    try:
        g = geocoder.ip("me")

        if g.ok:
            return g.city

        return None

    except Exception:
        return None