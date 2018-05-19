from collections import MutableMapping


class CaseInsensitiveDict(MutableMapping):

    def __init__(self, data=None, **kwargs):
        self._store = {}
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __delitem__(self, key):
        del self._store[key.replace("_", "").lower()]

    def __getitem__(self, key):
        return self._store[key.replace("_", "").lower()][1]

    def __setitem__(self, key, value):
        self._store[key.replace("_", "").lower()] = (key, value)

    def __iter__(self):
        return (cased_key for cased_key, mapped_value in self._store.values())

    def __len__(self):
        return len(self._store)

    def __eq__(self, other):
        if isinstance(other, collections.Mapping):
            other = CaseInsensitiveDict(other)
        else:
            return NotImplemented
        return dict(self.lower_items()) == dict(other.lower_items())

    def __repr__(self):
        return str(dict(self.items()))

    def lower_items(self):
        return (
            (lowerkey, keyval[1])
            for (lowerkey, keyval)
            in self._store.items()
        )

    def copy(self):
        return CaseInsensitiveDict(self._store.values())

    @classmethod
    def from_json(cls, json):
        data = {}
        if isinstance(json, list):
            return [cls.from_json(element) for element in json]
        elif isinstance(json, dict):
            for key, value in json.items():
                if isinstance(value, (list, dict)):
                    data[key] = cls.from_json(value)
                else:
                    data[key] = value
        else:
            return json
        return cls(data)
