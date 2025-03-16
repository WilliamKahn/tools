import os
import pymysql
import re
import yaml
from jinja2 import Template


field_mapping = {
        "int": "Integer",
        "varchar": "String",
        "text": "String",
        "datetime": "Date",
        "timestamp": "Date",
        "decimal": "BigDecimal",
        "tinyint": "Boolean",
        "bigint": "Long",
        "double": "Double",
        "float": "Float",
        "date": "Date",
        "char": "String",
        "mediumtext": "String",
        "longtext": "String",
        "smallint": "Integer",
        "mediumint": "Integer",
        "enum": "String",
        "json": "String",
        "blob": "byte[]",
        "longblob": "byte[]",
        "tinytext": "String",
        "binary": "byte[]",
        "varbinary": "byte[]",
        "bit": "Boolean",
        "time": "Time",
        "year": "Date",
        "set": "String",
        "geometry": "String",
        "point": "String",
        "linestring": "String",
        "polygon": "String",
        "multipoint": "String",
        "multilinestring": "String",
        "multipolygon": "String",
        "geometrycollection": "String",
    }

def connect_to_db(database):
    return pymysql.connect(**database)

def snake_to_camel(snake_str):
    components = snake_str.lower().split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def get_table_metadata(cursor, table_name, database):
    cursor.execute(f"SHOW FULL COLUMNS FROM {table_name}")
    columns = cursor.fetchall()
    cursor.execute(f"SELECT table_comment FROM information_schema.tables WHERE table_schema = '{database}' AND table_name = '{table_name}'")
    remark = cursor.fetchone()[0]
    return columns, remark

def generate_parameters(columns, field_mapping):
    parameters = []
    id_type = "Integer"
    for row in columns:
        # parameter = {"testTest", "TestTest", "String", "测试", "test_test"}
        parameter = {
            "field": snake_to_camel(row[0]),
            "Field": row[0].title().replace('_', ''),
            "type": field_mapping[re.sub(r'\(\d+(,\d+)?\)', '', row[1])],
            "remark": row[8],
            "raw": row[0]
        }
        if parameter['field'] == "id":
            id_type = parameter['type']
        parameters.append(parameter)
    return parameters, id_type

def render_template(template_path, context):
    with open(template_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(context)

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_file_name(filePath):
    parts = re.split(r'[/\\]', filePath)
    fileName = parts[-1]
    return fileName.split('.')[0]
# 获取格式
def get_file_type(filePath):
    parts = re.split(r'[/\\]', filePath)
    fileName = parts[-1]
    return fileName.split('.')[1]

def parse_value(filePath):
    package = filePath.replace('/', '.')
    # 去除开头和结尾的.(可能没有)
    if package.startswith('.'):
        package = package[1:]
    if package.endswith('.'):
        package = package[:-1]
    return package

def generate(database, db_name, table_name, project_path, extra, template_files):
    database["database"] = db_name
    packages = {}
    # 获取所有模板配置的包名
    for key, value in template_files.items():
        if get_file_type(key) == "java":
            packages[get_file_name(key)] = parse_value(value[2]+"/"+value[3])
            #packages = {parse_key(key): parse_value(value[2]+"/"+value[3]) for key, value in template_files.items()}

    with connect_to_db(database) as conn:
        cursor = conn.cursor()
        # 获取表中列信息和表备注
        columns, remark = get_table_metadata(cursor, table_name, db_name)
    # 获取生成列类型字段和主键类型
    parameters, id_type = generate_parameters(columns, field_mapping)

    table_name = table_name.strip()
    TableName = table_name.title().replace('_', '')
    for filePath, value in template_files.items():
        checked = value[0]
        if not checked:
            continue
        module = value[1]
        package = value[2]
        alias = value[3]
        context = {
            "table_name": table_name,
            "TableName": TableName,
            "tableName": snake_to_camel(table_name),
            "remark": remark,
            "columns": parameters,
            "packages": packages,
            "id_type": id_type,
            "primary_key": "id",
        }
        context.update(extra)
        entity_code = render_template(filePath, context)
        module_path = f'/{module.replace(".", "/")}' if module else ''

        fileName = get_file_name(filePath)
        fileType = get_file_type(filePath)
        src = "/"
        if fileType == "java":
            src = "/src/main/java/"
        elif fileType == "xml":
            src = "/src/main/resources"
        path = f'{project_path}{module_path}{src}{package.replace(".", "/")}/{alias}/{TableName}{fileName}.{fileType}'
        # 生成模板文件
        create_file(path, entity_code)
        print(f'{TableName}{fileName}.{fileType}生成成功')