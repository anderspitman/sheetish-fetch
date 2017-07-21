from sheetish import Database 
from pprint import pprint


if __name__ == '__main__':

    db = Database('https://docs.google.com/spreadsheets/d/1v75bv5LaKn1jNCvPm42u1oJAjEQ1gbgSTTeWATrUpf8/edit?usp=sharing')

    table = db.get_table('DuhTable')

    id_ = table.insert_one({
        'name': 'yolo',
        'age': 10
    })

    print(id_)

    table.insert_one({
        'name': 'frank',
        'age': 12,
        'hobby': 'coding'
    })

    table.insert_one({
        'name': 'bob',
        'age': 10,
        'hobby': 'skating'
    })

    table.insert_one({
        'name': 'nancy',
    })

    print(table.find({'age': '10'}))
    #print(table.find_one({'age': '12'}))
    
