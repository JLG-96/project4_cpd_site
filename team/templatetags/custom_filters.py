from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Retrieve an item from a dictionary by key."""
    return dictionary.get(key, [])


@register.filter(name="yes_count")
def yes_count(player_list):
    """Count players who set their status as 'yes'."""
    return sum(1 for player in player_list if player.status == "yes")


@register.filter(name="no_count")
def no_count(player_list):
    """Count players who set their status as 'no'."""
    return sum(1 for player in player_list if player.status == "no")
