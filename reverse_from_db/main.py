import os
import pymysql
import re
import yaml
from jinja2 import Template


# 读取配置
with open('./config.yml', 'r', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)
# 需要模板生成的引擎
template_files = config['template']
packages = {}
for key, value in template_files.items():
    packages[key] = value['package']
# 字段映射
field_mapping = config['field-mapping']
# 项目路径
project_path = config['project-path']
resultful = config['resultful']
table_name = config['table-name']
# 主键名称 后续从表中获取
primary_key = config['primary-key']
# 连接数据库
conn = pymysql.connect(
    **config['mysql-config']
)


# 蛇型转驼峰,第一个字母小写
def snake_to_camel(snake_str):
    components = snake_str.lower().split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


# 获取表的元数据
cursor = conn.cursor()
cursor.execute(f"SHOW FULL COLUMNS FROM {table_name}")
columns = cursor.fetchall()
cursor.execute(f"SELECT table_comment FROM information_schema.tables WHERE table_schema = '{config['mysql-config']['database']}' AND table_name = '{table_name}'")
# 获取备注
remark = cursor.fetchone()[0]
# 关闭数据库连接
conn.close()
TableName = table_name.title().replace('_', '')
tableName = snake_to_camel(table_name)
id_type = "Integer"
parameters = []
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


for key, value in template_files.items():
    # 模块
    module = value['module']
    # 包名
    package = value['package']
    # 读取模板文件
    with open(f'template/{key}.j2', 'r', encoding='utf-8') as f:
        template = Template(f.read())

    # 渲染模板文件并生成Java类文件
    entity_code = template.render(
        # 替换内容
        table_name=table_name,
        remark=remark,
        TableName=TableName,
        tableName=tableName,
        columns=parameters,
        packages=packages,
        resultful=resultful,
        id_type=id_type,
        primary_key=primary_key
    )
    if key == 'Model':
        key = ''
    module_path = f'/{module.replace(".", "/")}' if module else ''
    path = f'{project_path}{module_path}/src/main/java/{package.replace(".", "/")}'
    # 路径不存在先生成
    if not os.path.exists(path):
        os.makedirs(path)
    # 创建文件
    with open(f'{path}/{TableName}{key}.java', 'w', encoding='utf-8') as f:
        f.write(entity_code)
    print(f'{TableName}{key}.java生成成功')
