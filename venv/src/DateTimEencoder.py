import datetime
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.isoformat()
        return super().default(obj)


def as_datetime(dict):
    for key, val in dict.items():
        if isinstance(val,str):
            try:
                dict[key] = datetime.datetime.fromisoformat(val)
            except (TypeError, ValueError):
                pass
    return(dict)