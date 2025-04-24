"""
NarraMind：智能角色扮演与记忆管理系统主入口文件
"""
import argparse
import sys
import logging
import os
import mysql.connector
from mysql.connector import Error

from src.mcp.server import mcp_server
from src.utils.init_database import create_database, create_tables
from config.database import MYSQL_CONFIG, DB_CONFIG

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_database_exists():
    """检查数据库是否存在"""
    try:
        # 尝试连接到指定数据库
        connection = mysql.connector.connect(**DB_CONFIG)
        connection.close()
        return True
    except Error:
        return False

def initialize_database():
    """初始化数据库和表结构"""
    logger.info("正在检查数据库...")
    
    # 检查数据库是否已存在
    if not check_database_exists():
        logger.info("数据库不存在，开始初始化...")
        if create_database():
            logger.info("数据库创建成功，正在初始化表结构...")
            if create_tables():
                logger.info("数据库表结构初始化完成")
            else:
                logger.error("创建表结构失败")
                return False
        else:
            logger.error("创建数据库失败")
            return False
    else:
        logger.info("数据库已存在")
    
    return True

def main():
    """主函数，解析命令行参数并启动MCP服务器"""
    parser = argparse.ArgumentParser(description='启动NarraMind智能角色扮演与记忆管理系统')
    parser.add_argument('--host', type=str, default='localhost', help='服务器主机地址')
    parser.add_argument('--port', type=int, default=8080, help='服务器端口')
    parser.add_argument('--skip-db-init', action='store_true', help='跳过数据库初始化')
    
    args = parser.parse_args()
    
    # 初始化数据库（除非指定跳过）
    if not args.skip_db_init:
        if not initialize_database():
            logger.error("数据库初始化失败，程序退出")
            sys.exit(1)
    
    # 设置服务器配置
    mcp_server.host = args.host
    mcp_server.port = args.port
    
    logger.info(f"启动NarraMind服务器：{args.host}:{args.port}")
    
    # 启动服务器
    mcp_server.run()

if __name__ == "__main__":
    main()
