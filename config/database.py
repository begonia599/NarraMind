"""
数据库连接配置文件
"""

# 不指定数据库名称的配置，用于初始连接和创建数据库
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # 请确保这是正确的密码
    'port': 3306,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True,
}

# 完整配置，包含数据库名称，用于后续操作
DB_CONFIG = {
    **MYSQL_CONFIG,
    'database': 'mcp_memory',
}