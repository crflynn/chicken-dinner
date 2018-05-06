"""Utility functions."""
import re


stats_map = {
    "DBNOs": "dbnos",
    "dBNOs": "dbnos",
    "top10s": "top_10s",
}

def camel_to_snake(name):
    try:
        return stats_map[name]
    except KeyError as exc:
        pass
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
