

import threading


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        if not hasattr(self, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(self, "_instance"):
                    self._instance = super(SingletonType, self).__call__(*args, **kwargs)
        return self._instance