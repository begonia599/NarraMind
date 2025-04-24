"""
事件-角色关联模型类，用于管理事件和角色之间的关系
"""
from src.db import db

class EventCharacter:
    """事件-角色关联模型类"""
    
    def __init__(self, relation_id=None, event_id=None, character_id=None, role_in_event=None):
        self.relation_id = relation_id
        self.event_id = event_id
        self.character_id = character_id
        self.role_in_event = role_in_event
    
    @classmethod
    def add_character_to_event(cls, event_id, character_id, role_in_event=None):
        """
        向事件添加角色
        
        Args:
            event_id (str): 事件ID
            character_id (str): 角色ID
            role_in_event (str, optional): 角色在事件中的角色
            
        Returns:
            int: 关联ID
        """
        query = """
        INSERT INTO event_characters (event_id, character_id, role_in_event) 
        VALUES (%s, %s, %s)
        """
        
        try:
            relation_id = db.execute_insert(query, (event_id, character_id, role_in_event))
            return relation_id
        except Exception as e:
            print(f"添加角色到事件失败: {e}")
            raise
    
    @classmethod
    def get_characters_in_event(cls, event_id):
        """
        获取事件中的所有角色
        
        Args:
            event_id (str): 事件ID
            
        Returns:
            list: 角色列表，包含角色信息和角色在事件中的角色
        """
        query = """
        SELECT ec.*, c.name, c.played_by 
        FROM event_characters ec 
        JOIN characters c ON ec.character_id = c.character_id 
        WHERE ec.event_id = %s
        """
        
        return db.execute_query(query, (event_id,))
    
    @classmethod
    def get_events_involving_character(cls, character_id):
        """
        获取包含特定角色的所有事件
        
        Args:
            character_id (str): 角色ID
            
        Returns:
            list: 事件列表
        """
        query = """
        SELECT e.*, ec.role_in_event 
        FROM events e 
        JOIN event_characters ec ON e.event_id = ec.event_id 
        WHERE ec.character_id = %s 
        ORDER BY e.timestamp DESC
        """
        
        return db.execute_query(query, (character_id,))
    
    @classmethod
    def update_character_role_in_event(cls, event_id, character_id, role_in_event):
        """
        更新角色在事件中的角色
        
        Args:
            event_id (str): 事件ID
            character_id (str): 角色ID
            role_in_event (str): 新的角色
            
        Returns:
            int: 受影响的行数
        """
        query = """
        UPDATE event_characters 
        SET role_in_event = %s 
        WHERE event_id = %s AND character_id = %s
        """
        
        return db.execute_update(query, (role_in_event, event_id, character_id))
    
    @classmethod
    def remove_character_from_event(cls, event_id, character_id):
        """
        从事件中移除角色
        
        Args:
            event_id (str): 事件ID
            character_id (str): 角色ID
            
        Returns:
            int: 受影响的行数
        """
        query = """
        DELETE FROM event_characters 
        WHERE event_id = %s AND character_id = %s
        """
        
        return db.execute_update(query, (event_id, character_id))
    
    @classmethod
    def delete_all_characters_from_event(cls, event_id):
        """
        删除事件的所有角色关联
        
        Args:
            event_id (str): 事件ID
            
        Returns:
            int: 受影响的行数
        """
        query = "DELETE FROM event_characters WHERE event_id = %s"
        return db.execute_update(query, (event_id,))