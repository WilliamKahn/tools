import os
import pymysql
import re
import yaml
from jinja2 import Template

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)

def connect_to_db(config):
    return pymysql.connect(**config['mysql-config'])

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

def main():
    config = load_config('./config.yml')
    template_files = config['template']
    packages = {key: value['package'] for key, value in template_files.items()}
    field_mapping = config['field-mapping']
    project_path = config['project-path']
    resultful = config['resultful']
    table_name = config['table-name']
    primary_key = config['primary-key']
    author_name = config['author-name']

    with connect_to_db(config) as conn:
        cursor = conn.cursor()
        columns, remark = get_table_metadata(cursor, table_name, config['mysql-config']['database'])

    TableName = table_name.title().replace('_', '')
    tableName = snake_to_camel(table_name)
    parameters, id_type = generate_parameters(columns, field_mapping)

    for key, value in template_files.items():
        module = value['module']
        package = value['package']
        context = {
            "table_name": table_name.strip(),
            "remark": remark,
            "TableName": TableName,
            "tableName": tableName,
            "columns": parameters,
            "packages": packages,
            "resultful": resultful,
            "id_type": id_type,
            "primary_key": primary_key,
            "author": author_name
        }
        entity_code = render_template(f'template/{key}.java.j2', context)
        if key == 'Model':
            key = ''
        module_path = f'/{module.replace(".", "/")}' if module else ''
        path = f'{project_path}{module_path}/src/main/java/{package.replace(".", "/")}/{TableName}{key}.java'
        create_file(path, entity_code)
        print(f'{TableName}{key}.java生成成功')
        if key == 'Mapper':
            xml = render_template(f'template/{key}.xml.j2', context)
            xml_path = value['path']
            path = f'{project_path}{module_path}/src/main/resources/mapper{xml_path}/{TableName}{key}.xml'
            create_file(path, xml)
            print(f'{TableName}{key}.xml生成成功')

if __name__ == "__main__":
    main()