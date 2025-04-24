"""
数据库初始化脚本，用于创建所需的表结构
"""
import os
import sys
import logging
import mysql.connector
from mysql.connector import pooling

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.database import MYSQL_CONFIG, DB_CONFIG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_database():
    """创建数据库"""
    try:
        # 连接到MySQL，不指定数据库
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()
        
        # 创建数据库
        db_name = DB_CONFIG["database"]
        logger.info(f"创建数据库 {db_name}...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        logger.info(f"数据库 {db_name} 创建成功")
        
        # 关闭连接
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as err:
        logger.error(f"创建数据库失败: {err}")
        return False

def create_tables():
    """创建所有数据库表"""
    try:
        # 连接到指定数据库
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # 创建角色表
        create_characters_table = """
        CREATE TABLE IF NOT EXISTS characters (
            character_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            played_by ENUM('player', 'ai') NOT NULL,
            age INT,
            gender VARCHAR(50),
            occupation VARCHAR(100),
            appearance TEXT,
            voice_tone VARCHAR(100),
            voice_style VARCHAR(100),
            mannerisms TEXT,
            current_goal TEXT,
            backstory TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # 创建地点表
        create_locations_table = """
        CREATE TABLE IF NOT EXISTS locations (
            location_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            location_type VARCHAR(50),
            parent_location_id VARCHAR(36),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_location_id) REFERENCES locations(location_id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # 创建关系表
        create_relationships_table = """
        CREATE TABLE IF NOT EXISTS relationships (
            relationship_id VARCHAR(36) PRIMARY KEY,
            character_id_1 VARCHAR(36) NOT NULL,
            character_id_2 VARCHAR(36) NOT NULL,
            relationship_type VARCHAR(50) NOT NULL,
            strength INT CHECK (strength BETWEEN 1 AND 100),
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (character_id_1) REFERENCES characters(character_id) ON DELETE CASCADE,
            FOREIGN KEY (character_id_2) REFERENCES characters(character_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # 创建事件表
        create_events_table = """
        CREATE TABLE IF NOT EXISTS events (
            event_id VARCHAR(36) PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            location_id VARCHAR(36),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event_type VARCHAR(50),
            importance INT CHECK (importance BETWEEN 1 AND 100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # 创建技能表
        create_skills_table = """
        CREATE TABLE IF NOT EXISTS skills (
            skill_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # 创建角色-技能关联表
        create_character_skills_table = """
        CREATE TABLE IF NOT EXISTS character_skills (
            relation_id INT AUTO_INCREMENT PRIMARY KEY,
            character_id VARCHAR(36) NOT NULL,
            skill_id VARCHAR(36) NOT NULL,
            level INT DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE CASCADE,
            UNIQUE KEY (character_id, skill_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # 创建事件-角色关联表
        create_event_characters_table = """
        CREATE TABLE IF NOT EXISTS event_characters (
            relation_id INT AUTO_INCREMENT PRIMARY KEY,
            event_id VARCHAR(36) NOT NULL,
            character_id VARCHAR(36) NOT NULL,
            role_in_event VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
            FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # 创建角色-地点状态表
        create_character_location_state_table = """
        CREATE TABLE IF NOT EXISTS character_location_state (
            relation_id INT AUTO_INCREMENT PRIMARY KEY,
            character_id VARCHAR(36) NOT NULL,
            location_id VARCHAR(36) NOT NULL,
            state ENUM('未知', '已知', '去过', '当前') DEFAULT '未知',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (character_id) REFERENCES characters(character_id) ON DELETE CASCADE,
            FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE,
            UNIQUE KEY (character_id, location_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # 创建物品表
        create_items_table = """
        CREATE TABLE IF NOT EXISTS items (
            item_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            item_type VARCHAR(50),
            properties JSON,
            rarity VARCHAR(50),
            value INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # 执行SQL语句创建表格
        tables = [
            ("characters", create_characters_table),
            ("locations", create_locations_table),
            ("relationships", create_relationships_table),
            ("events", create_events_table),
            ("skills", create_skills_table),
            ("character_skills", create_character_skills_table),
            ("event_characters", create_event_characters_table),
            ("character_location_state", create_character_location_state_table),
            ("items", create_items_table)
        ]
        
        for table_name, create_table_sql in tables:
            try:
                logger.info(f"创建表 {table_name}...")
                cursor.execute(create_table_sql)
                logger.info(f"表 {table_name} 创建成功")
            except Exception as e:
                logger.error(f"创建表 {table_name} 失败: {e}")
                
        # 关闭连接
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as err:
        logger.error(f"创建表失败: {err}")
        return False

def main():
    """主函数，初始化数据库"""
    logger.info("开始初始化数据库...")
    
    # 先创建数据库
    if create_database():
        # 然后创建表
        if create_tables():
            logger.info("数据库初始化完成")
        else:
            logger.error("表结构创建失败")
    else:
        logger.error("数据库创建失败")

if __name__ == "__main__":
    main()