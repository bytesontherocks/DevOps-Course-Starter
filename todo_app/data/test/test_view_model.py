
from  todo_app.data.Item import Item
from  todo_app.data.ViewModel import ViewModel

def test_view_model_done_property():
    it = Item(1, "testing1", "Done")
    vm = ViewModel(it)
    done_its = vm.done_items

    assert(len(done_its) == 1)
    assert(done_its[0] == it)
    

