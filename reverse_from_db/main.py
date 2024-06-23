import os
import pymysql
import re
import yaml
from jinja2 import Template


# 读取配置
with open('./config.yml', 'r', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)
# 需要模板生成的引擎
template = config['template']
# 字段映射
field_mapping = config['field-mapping']
# 项目路径
project_path = config['project-path']
table_name = config['table-name']
table_remark = config['table-remark']
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
TableName = table_name.title().replace('_', '')
tableName = snake_to_camel(table_name)

parameters = []
for row in columns:
    parameter = [
        snake_to_camel(row[0]),
        row[0].title().replace('_', ''),
        field_mapping[re.sub(r'\([0-9]*\)', '', row[1])],
        row[8],
        row[0]
    ]
    parameters.append(parameter)

# 关闭数据库连接
conn.close()

for key, value in template.items():
    # 模块
    module = value['module']
    # 包名
    package = value['package']
    # 读取模板文件
    with open(f'template/{key}.template', 'r', encoding='utf-8') as f:
        template = Template(f.read())

    # 渲染模板文件并生成Java类文件
    entity_code = template.render(
        # 替换内容
        table_name=table_name,
        table_remark=table_remark,
        TableName=TableName,
        tableName=tableName,
        columns=parameters,
        packages=template
    )
    if key == 'Model':
        key = ''
    path = f'{project_path}/{module.replace(".", "/")}/src/main/java/{package.replace(".", "/")}'
    # 路径不存在先生成
    if not os.path.exists(path):
        os.makedirs(path)
    # 创建文件
    with open(f'{path}/{TableName}{key}.java', 'w', encoding='utf-8') as f:
        f.write(entity_code)
    print(f'{TableName}{key}.java生成成功')
