"""
角色-技能关联模型类，用于管理角色和技能之间的关系
"""
from src.db import db

class CharacterSkill:
    """角色-技能关联模型类"""
    
    def __init__(self, relation_id=None, character_id=None, skill_id=None, level=None):
        self.relation_id = relation_id
        self.character_id = character_id
        self.skill_id = skill_id
        self.level = level
    
    @classmethod
    def add_character_skill(cls, character_id, skill_id, level=1):
        """
        为角色添加技能
        
        Args:
            character_id (str): 角色ID
            skill_id (str): 技能ID
            level (int, optional): 技能等级，默认为1
            
        Returns:
            int: 关联ID
        """
        query = """
        INSERT INTO character_skills (character_id, skill_id, level) 
        VALUES (%s, %s, %s)
        """
        
        try:
            relation_id = db.execute_insert(query, (character_id, skill_id, level))
            return relation_id
        except Exception as e:
            print(f"为角色添加技能失败: {e}")
            raise
    
    @classmethod
    def get_character_skills(cls, character_id):
        """
        获取角色的所有技能
        
        Args:
            character_id (str): 角色ID
            
        Returns:
            list: 技能列表，包含技能信息和等级
        """
        query = """
        SELECT cs.*, s.name, s.description 
        FROM character_skills cs 
        JOIN skills s ON cs.skill_id = s.skill_id 
        WHERE cs.character_id = %s
        """
        
        return db.execute_query(query, (character_id,))
    
    @classmethod
    def update_character_skill_level(cls, character_id, skill_id, level):
        """
        更新角色的技能等级
        
        Args:
            character_id (str): 角色ID
            skill_id (str): 技能ID
            level (int): 新的技能等级
            
        Returns:
            int: 受影响的行数
        """
        query = """
        UPDATE character_skills 
        SET level = %s 
        WHERE character_id = %s AND skill_id = %s
        """
        
        return db.execute_update(query, (level, character_id, skill_id))
    
    @classmethod
    def remove_character_skill(cls, character_id, skill_id):
        """
        移除角色的技能
        
        Args:
            character_id (str): 角色ID
            skill_id (str): 技能ID
            
        Returns:
            int: 受影响的行数
        """
        query = """
        DELETE FROM character_skills 
        WHERE character_id = %s AND skill_id = %s
        """
        
        return db.execute_update(query, (character_id, skill_id))
    
    @classmethod
    def get_characters_with_skill(cls, skill_id):
        """
        获取拥有特定技能的所有角色
        
        Args:
            skill_id (str): 技能ID
            
        Returns:
            list: 角色列表，包含角色信息和技能等级
        """
        query = """
        SELECT cs.*, c.name, c.played_by
        FROM character_skills cs
        JOIN characters c ON cs.character_id = c.character_id
        WHERE cs.skill_id = %s
        """
        
        return db.execute_query(query, (skill_id,))