import mysql.connector

db = mysql.connector.connect(host='localhost', database='Sales_Person', user='root', password='1234')
cursor = db.cursor()

# cursor.execute("SHOW TABLES")
# print(cursor)
# tables = cursor.fetchall()
# print(tables)
#
# for table in tables:
#     print(table[0])


def get_table_names(cursor):
    table_names = []
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for table in tables:
        table_names.append(table[0])

    return table_names,tables

def get_columns_names(cursor,table):
    cursor.execute("DESCRIBE " + table[0])
    columns = cursor.fetchall()
    columns_names = []
    for column in columns:
        columns_names.append(column[0])
    return columns_names


def get_database_info(cursor):
    table_names,tables = get_table_names(cursor)
    table_dict = []
    for table in tables:
        columns = get_columns_names(cursor,table)
        table_column_dict = {
            "table_name": table[0],
            "columns": columns
        }
        table_dict.append(table_column_dict)
    return table_dict

database_schema_dict = get_database_info(cursor)
database_schema_string = "\n".join(
    [
        f"Table: {table['table_name']}\nColumns: {', '.join(table['columns'])}" for table in database_schema_dict
    ]
)
print(database_schema_string)
# x = [
#     f"Table: {table['table_name']}\nColumns: {', '.join(table['columns'])}" for table in database_schema_dict
# ]
# print('\n'.join(x))
# print(' ,'.join(database_schema_dict[0]['columns']))


# for table in tables:
#     cursor.execute("DESCRIBE " + table[0])
#     columns = cursor.fetchall()
#
#     for column in columns:
#         print(column[0])

# def get_column_names(cursor,table_name):




#
# table_columns = []
# for table in tables:
#     cursor.execute("DESCRIBE " + table[0])
#     columns = cursor.fetchall()
#
#     table_column_dict = {
#         "table_name": table[0],
#         "columns": columns
#     }
#
#     table_columns.append(table_column_dict)
#
# print(table_columns)
#
# database_schema_string = "\n".join(
#     [
#         f"Table: {table['table_name']}\nColumns: {', '.join(table['columns'])}" for table in table_columns
#     ]
# )
# print(database_schema_string)
#
#
def ask_database(query):
    try:
        cursor.execute(query)
        results = str(cursor.fetchall())
        # print(results)
    except Exception as e:
        results = f"query failed with error: {e}"
    return results
