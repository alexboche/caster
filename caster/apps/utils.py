from dragonfly import ActionBase
from dragonfly import Context
from dragonfly import Text


class Texter(ActionBase):

    def __init__(self, func, extra=()):
        self.func = func
        self.extra = extra
        self._str = func.__name__ 

    def _execute(self, data):
        arguments = {k:v for k,v in data.items() if k in self.extra}
        result = self.func(**arguments)
        Text(str(result)).execute()



class MultiAppContext(Context):

    # ----------------------------------------------------------------------
    # Initialization methods.

    def __init__(self, relevant_apps=None, title=None, exclude=False):
        super(MultiAppContext, self)

        if relevant_apps is None:
            self._relevant_apps = None
        else:
            self._relevant_apps = set(relevant_apps)

        self._title = title
        self._exclude = bool(exclude)

        self._str = "%s, %s, %s" % (self._relevant_apps, self._title,
                                    self._exclude)

    # ----------------------------------------------------------------------
    # Matching methods.

    def matches(self, executable, title, handle):
        
        executable = executable.lower()

        if not self._relevant_apps:
            # If no apps are relevant, then all apps will match.

            if self._log_match:
                self._log_match.debug("%s: Match." % self)
            return True

        for app in self._relevant_apps:
            if app.lower() in executable:
                if self._log_match:
                    self._log_match.debug("%s: Match." % self)
                return True

        return False

