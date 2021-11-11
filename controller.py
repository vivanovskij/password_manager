import model
import view


def start():
    '''Start application'''
    view.start_view()
    action = input()
    if action == 'y':
        return show_all_items()
    else:
        return view.end_view()

def show_all_items():
    '''Show all items of database'''
    content = model.get_content()
    return view.show_all_view(content)

if __name__ == "__main__":
    start()

