def get_content():
    '''Get content from database'''
    with open('db.csv', 'r') as file:
        return file.read()
