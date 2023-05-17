import re

MYSQL_TO_JAVA_TYPES = {
    'bigint': 'Long',
    'int': 'Integer',
    'tinyint': 'Boolean',
    'varchar(32)': 'String',
    'varchar(255)': 'String',
    'datetime': 'Date',
}


if __name__ == '__main__':
    a = re.sub(r'\([0-9]*\)', '', 'varchar(20)')

    print(a)


