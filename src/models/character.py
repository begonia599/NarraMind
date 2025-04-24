"""
角色模型类，用于管理角色的CRUD操作
"""
from src.db import db

class Character:
    """角色模型类"""
    
    def __init__(self, character_id=None, name=None, played_by=None, age=None, gender=None,
                 occupation=None, appearance=None, voice_tone=None, voice_style=None,
                 mannerisms=None, current_goal=None, backstory=None, notes=None):
        self.character_id = character_id
        self.name = name
        self.played_by = played_by
        self.age = age
        self.gender = gender
        self.occupation = occupation
        self.appearance = appearance
        self.voice_tone = voice_tone
        self.voice_style = voice_style
        self.mannerisms = mannerisms
        self.current_goal = current_goal
        self.backstory = backstory
        self.notes = notes
    
    @classmethod
    def create(cls, character_data):
        """
        创建新角色
        
        Args:
            character_data (dict): 角色数据
                {
                    'character_id': str,
                    'name': str,
                    'played_by': str ('player' or 'ai'),
                    'age': int,
                    'gender': str,
                    'occupation': str,
                    'appearance': str,
                    'voice_tone': str,
                    'voice_style': str,
                    'mannerisms': str,
                    'current_goal': str,
                    'backstory': str,
                    'notes': str
                }
                
        Returns:
            str: 角色ID
        """
        query = """
        INSERT INTO characters (
            character_id, name, played_by, age, gender, occupation, 
            appearance, voice_tone, voice_style, mannerisms, 
            current_goal, backstory, notes
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        params = (
            character_data.get('character_id'),
            character_data.get('name'),
            character_data.get('played_by'),
            character_data.get('age'),
            character_data.get('gender'),
            character_data.get('occupation'),
            character_data.get('appearance'),
            character_data.get('voice_tone'),
            character_data.get('voice_style'),
            character_data.get('mannerisms'),
            character_data.get('current_goal'),
            character_data.get('backstory'),
            character_data.get('notes')
        )
        
        try:
            db.execute_update(query, params)
            return character_data.get('character_id')
        except Exception as e:
            print(f"创建角色失败: {e}")
            raise
    
    @classmethod
    def get_by_id(cls, character_id):
        """
        根据ID获取角色
        
        Args:
            character_id (str): 角色ID
            
        Returns:
            dict: 角色数据
        """
        query = "SELECT * FROM characters WHERE character_id = %s"
        result = db.execute_query(query, (character_id,))
        
        if result:
            return result[0]
        return None
    
    @classmethod
    def get_all(cls):
        """
        获取所有角色
        
        Returns:
            list: 角色列表
        """
        query = "SELECT * FROM characters"
        return db.execute_query(query)
    
    @classmethod
    def update(cls, character_id, attribute, value):
        """
        更新角色属性
        
        Args:
            character_id (str): 角色ID
            attribute (str): 属性名
            value: 属性值
            
        Returns:
            int: 受影响的行数
        """
        valid_attributes = [
            'name', 'played_by', 'age', 'gender', 'occupation', 
            'appearance', 'voice_tone', 'voice_style', 'mannerisms', 
            'current_goal', 'backstory', 'notes'
        ]
        
        if attribute not in valid_attributes:
            raise ValueError(f"无效的角色属性: {attribute}")
        
        query = f"UPDATE characters SET {attribute} = %s WHERE character_id = %s"
        return db.execute_update(query, (value, character_id))
    
    @classmethod
    def delete(cls, character_id):
        """
        删除角色
        
        Args:
            character_id (str): 角色ID
            
        Returns:
            int: 受影响的行数
        """
        query = "DELETE FROM characters WHERE character_id = %s"
        return db.execute_update(query, (character_id,))