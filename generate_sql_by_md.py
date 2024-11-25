# Description: 根据markdown表格生成建表语句

table_name = "mytable"
remark = "我的表"
md = """| 表名    | 类型            | 备注  |
| ----- | ------------- | --- |
| id    | bigint        | 主键  |
| name  | varchar(255)  | 姓名  |
| sex   | tinyint       | 性别  |
| money | decimal(10,2) | 余额  |"""

def md_to_sql(md: str, table_name: str, remark: str) -> str:
    sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n"
    for line in md.split("\n")[2:]:
        if not line:
            continue
        name, type_, comment = line.split("|")[1:4]
        name, type_, comment = name.strip(), type_.strip(), comment.strip()
        sql += f"    `{name}` {type_} COMMENT '{comment}',\n"
    sql += f"    PRIMARY KEY (`id`)\n"
    sql += f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{remark}';"
    return sql

print(md_to_sql(md, table_name, remark))
