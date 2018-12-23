



from dragonfly import ActionBase, Text





class Texter(ActionBase):

    def __init__(self, func, extra=()):
        self.func = func
        self.extra = extra
        self._str = func.__name__ 

    def _execute(self, data):
        arguments = {k:v for k,v in data.items() if k in self.extra}
        result = self.func(**arguments)
        Text(str(result)).execute()
