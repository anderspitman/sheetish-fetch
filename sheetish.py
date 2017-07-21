import pygsheets


class Database(object):
    
    def __init__(self, sheet_id):

        gc = pygsheets.authorize()

        self._spreadsheet  = gc.open_by_url(sheet_id)

    def list_tables(self):

        return [ x.title for x in self._spreadsheet.worksheets() ]

    def get_table(self, table_name):

        return Table(self, self._spreadsheet.worksheet_by_title(table_name))

    def create_table(self, table_name):

        return Table(self, self._spreadsheet.add_worksheet(table_name))


class Table(object):

    def __init__(self, db, sheet):
        self._db = db
        self._sheet = sheet

    def insert_one(self, item):
        current = self._sheet.get_all_values()
        current_columns = current[0]
        if current_columns[0] == '':
            current_columns = current_columns[1:]
        new_columns = []
        new_row = []


        for requested_column in item.keys():
            if requested_column not in current_columns:
                new_columns.append(requested_column)

        all_columns = current_columns + new_columns

        # write the new column headers
        self._sheet.delete_rows(index=1, number=1)
        self._sheet.insert_rows(row=0, number=1, values=all_columns)

        for col in all_columns:
            if col in item:
                new_row.append(item[col])

        self._sheet.insert_rows(row=len(current), number=1, values=new_row)

        return len(current)
        

    def find_one(self, query):

        match = {}
        def on_match(x):
            match['value'] = x
            should_continue = False
            return should_continue

        self._search(query, on_match)

        return match['value']

    def find(self, query):
        matches = []

        def on_match(x):
            matches.append(x)
            should_continue = True
            return should_continue

        self._search(query, on_match)

        return matches

    def _search(self, query, on_match):

        current = self._sheet.get_all_values()
        headers = current[0]
        data = current[1:]

        for i, row in enumerate(data):
            row_matches = True
            for j, header in enumerate(headers):
                if header in query:
                    if str(query[header]) != data[i][j]:
                        # this row doesn't match
                        row_matches = False
                        break
            if row_matches:
                if not on_match({ x: y for x,y in zip(headers, row) }):
                    return
