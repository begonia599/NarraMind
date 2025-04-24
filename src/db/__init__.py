"""
数据库模块初始化文件
"""

from .connection import DatabaseConnection

# 创建全局数据库连接实例
db = DatabaseConnection()