"""
关系模型类，用于管理角色之间的关系
"""
from src.db import db

class Relationship:
    """关系模型类"""
    
    def __init__(self, relationship_id=None, character_id_1=None, character_id_2=None, 
                relationship_type=None, strength=None, description=None):
        self.relationship_id = relationship_id
        self.character_id_1 = character_id_1
        self.character_id_2 = character_id_2
        self.relationship_type = relationship_type
        self.strength = strength
        self.description = description
    
    @classmethod
    def create(cls, relationship_data):
        """
        创建新关系
        
        Args:
            relationship_data (dict): 关系数据
                {
                    'relationship_id': str,
                    'character_id_1': str,
                    'character_id_2': str,
                    'relationship_type': str,
                    'strength': int (1-100),
                    'description': str
                }
                
        Returns:
            str: 关系ID
        """
        query = """
        INSERT INTO relationships (
            relationship_id, character_id_1, character_id_2, 
            relationship_type, strength, description
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        params = (
            relationship_data.get('relationship_id'),
            relationship_data.get('character_id_1'),
            relationship_data.get('character_id_2'),
            relationship_data.get('relationship_type'),
            relationship_data.get('strength'),
            relationship_data.get('description')
        )
        
        try:
            db.execute_update(query, params)
            return relationship_data.get('relationship_id')
        except Exception as e:
            print(f"创建关系失败: {e}")
            raise
    
    @classmethod
    def get_by_id(cls, relationship_id):
        """
        根据ID获取关系
        
        Args:
            relationship_id (str): 关系ID
            
        Returns:
            dict: 关系数据
        """
        query = "SELECT * FROM relationships WHERE relationship_id = %s"
        result = db.execute_query(query, (relationship_id,))
        
        if result:
            return result[0]
        return None
    
    @classmethod
    def get_character_relationships(cls, character_id):
        """
        获取角色的所有关系
        
        Args:
            character_id (str): 角色ID
            
        Returns:
            list: 关系列表
        """
        query = """
        SELECT r.*, c1.name as character_1_name, c2.name as character_2_name
        FROM relationships r
        JOIN characters c1 ON r.character_id_1 = c1.character_id
        JOIN characters c2 ON r.character_id_2 = c2.character_id
        WHERE r.character_id_1 = %s OR r.character_id_2 = %s
        """
        return db.execute_query(query, (character_id, character_id))
    
    @classmethod
    def get_relationship_between_characters(cls, character_id_1, character_id_2):
        """
        获取两个角色之间的关系
        
        Args:
            character_id_1 (str): 角色1 ID
            character_id_2 (str): 角色2 ID
            
        Returns:
            dict: 关系数据
        """
        query = """
        SELECT * FROM relationships 
        WHERE (character_id_1 = %s AND character_id_2 = %s)
           OR (character_id_1 = %s AND character_id_2 = %s)
        """
        result = db.execute_query(query, (character_id_1, character_id_2, character_id_2, character_id_1))
        
        if result:
            return result[0]
        return None
    
    @classmethod
    def update_relationship(cls, relationship_id, attribute, value):
        """
        更新关系属性
        
        Args:
            relationship_id (str): 关系ID
            attribute (str): 属性名
            value: 属性值
            
        Returns:
            int: 受影响的行数
        """
        valid_attributes = ['relationship_type', 'strength', 'description']
        
        if attribute not in valid_attributes:
            raise ValueError(f"无效的关系属性: {attribute}")
        
        query = f"UPDATE relationships SET {attribute} = %s WHERE relationship_id = %s"
        return db.execute_update(query, (value, relationship_id))
    
    @classmethod
    def delete(cls, relationship_id):
        """
        删除关系
        
        Args:
            relationship_id (str): 关系ID
            
        Returns:
            int: 受影响的行数
        """
        query = "DELETE FROM relationships WHERE relationship_id = %s"
        return db.execute_update(query, (relationship_id,))