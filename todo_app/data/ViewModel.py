class ViewModel:
    def __init__(self, items):
        self._items = items
 
    @property
    def items(self):
        return self._items
    
    @property
    def done_items(self):
        done_items = []
        for it in self._items:
            if it.status == "Done":
                done_items.append(it)
        return done_items
    
    @property
    def to_do_items(self):
        to_do_items = []
        for it in self._items:
            if it.status == "To Do":
                to_do_items.append(it)
        return to_do_items
    
    @property
    def doing_items(self):
        doing_items = []
        for it in self._items:
            if it.status == "Doing":
                doing_items.append(it)
        return doing_items