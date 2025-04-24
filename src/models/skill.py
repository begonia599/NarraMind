"""
技能模型类，用于管理技能的CRUD操作
"""
from src.db import db

class Skill:
    """技能模型类"""
    
    def __init__(self, skill_id=None, name=None, description=None):
        self.skill_id = skill_id
        self.name = name
        self.description = description
    
    @classmethod
    def create(cls, skill_data):
        """
        创建新技能
        
        Args:
            skill_data (dict): 技能数据
                {
                    'skill_id': str,
                    'name': str,
                    'description': str
                }
                
        Returns:
            str: 技能ID
        """
        query = """
        INSERT INTO skills (skill_id, name, description) 
        VALUES (%s, %s, %s)
        """
        
        params = (
            skill_data.get('skill_id'),
            skill_data.get('name'),
            skill_data.get('description')
        )
        
        try:
            db.execute_update(query, params)
            return skill_data.get('skill_id')
        except Exception as e:
            print(f"创建技能失败: {e}")
            raise
    
    @classmethod
    def get_by_id(cls, skill_id):
        """
        根据ID获取技能
        
        Args:
            skill_id (str): 技能ID
            
        Returns:
            dict: 技能数据
        """
        query = "SELECT * FROM skills WHERE skill_id = %s"
        result = db.execute_query(query, (skill_id,))
        
        if result:
            return result[0]
        return None
    
    @classmethod
    def get_all(cls):
        """
        获取所有技能
        
        Returns:
            list: 技能列表
        """
        query = "SELECT * FROM skills"
        return db.execute_query(query)
    
    @classmethod
    def update_description(cls, skill_id, description):
        """
        更新技能描述
        
        Args:
            skill_id (str): 技能ID
            description (str): 新的描述
            
        Returns:
            int: 受影响的行数
        """
        query = "UPDATE skills SET description = %s WHERE skill_id = %s"
        return db.execute_update(query, (description, skill_id))
    
    @classmethod
    def delete(cls, skill_id):
        """
        删除技能
        
        Args:
            skill_id (str): 技能ID
            
        Returns:
            int: 受影响的行数
        """
        query = "DELETE FROM skills WHERE skill_id = %s"
        return db.execute_update(query, (skill_id,))