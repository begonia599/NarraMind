"""
数据库连接管理模块
"""
import mysql.connector
from mysql.connector import pooling
import sys
import os

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.database import DB_CONFIG

class DatabaseConnection:
    """数据库连接管理类"""
    
    _instance = None
    _connection_pool = None
    
    def __new__(cls):
        """单例模式，确保只创建一个数据库连接池"""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            try:
                cls._connection_pool = pooling.MySQLConnectionPool(
                    pool_name="mcp_pool",
                    pool_size=5,
                    **DB_CONFIG
                )
                print("数据库连接池创建成功")
            except mysql.connector.Error as err:
                print(f"数据库连接池创建失败: {err}")
                raise
        return cls._instance
    
    def get_connection(self):
        """获取数据库连接"""
        try:
            return self._connection_pool.get_connection()
        except mysql.connector.Error as err:
            print(f"无法获取数据库连接: {err}")
            raise
    
    def execute_query(self, query, params=None):
        """
        执行查询操作
        
        Args:
            query (str): SQL查询语句
            params (tuple, optional): 参数化查询的参数
            
        Returns:
            list: 查询结果
        """
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"查询执行失败: {err}")
            raise
        finally:
            if cursor:
                cursor.close()
            connection.close()
    
    def execute_update(self, query, params=None):
        """
        执行更新操作（INSERT, UPDATE, DELETE）
        
        Args:
            query (str): SQL更新语句
            params (tuple, optional): 参数化查询的参数
            
        Returns:
            int: 影响的行数
        """
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            connection.commit()
            return cursor.rowcount
        except mysql.connector.Error as err:
            print(f"更新操作失败: {err}")
            connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            connection.close()
    
    def execute_insert(self, query, params=None):
        """
        执行插入操作并返回自动生成的ID
        
        Args:
            query (str): SQL插入语句
            params (tuple, optional): 参数化查询的参数
            
        Returns:
            int: 最后插入的ID
        """
        connection = self.get_connection()
        cursor = None
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"插入操作失败: {err}")
            connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            connection.close()