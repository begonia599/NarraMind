"""
事件模型类，用于管理游戏世界中发生的事件
"""
from datetime import datetime
from src.db import db

class Event:
    """事件模型类"""
    
    def __init__(self, event_id=None, title=None, description=None, location_id=None,
                timestamp=None, event_type=None, importance=None):
        self.event_id = event_id
        self.title = title
        self.description = description
        self.location_id = location_id
        self.timestamp = timestamp or datetime.now()
        self.event_type = event_type
        self.importance = importance
    
    @classmethod
    def create(cls, event_data):
        """
        创建新事件
        
        Args:
            event_data (dict): 事件数据
                {
                    'event_id': str,
                    'title': str,
                    'description': str,
                    'location_id': str,
                    'timestamp': datetime (可选),
                    'event_type': str,
                    'importance': int (1-100)
                }
                
        Returns:
            str: 事件ID
        """
        query = """
        INSERT INTO events (
            event_id, title, description, location_id, 
            timestamp, event_type, importance
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        # 如果没有提供时间戳，使用当前时间
        if 'timestamp' not in event_data or not event_data['timestamp']:
            event_data['timestamp'] = datetime.now()
            
        params = (
            event_data.get('event_id'),
            event_data.get('title'),
            event_data.get('description'),
            event_data.get('location_id'),
            event_data.get('timestamp'),
            event_data.get('event_type'),
            event_data.get('importance')
        )
        
        try:
            db.execute_update(query, params)
            return event_data.get('event_id')
        except Exception as e:
            print(f"创建事件失败: {e}")
            raise
    
    @classmethod
    def get_by_id(cls, event_id):
        """
        根据ID获取事件
        
        Args:
            event_id (str): 事件ID
            
        Returns:
            dict: 事件数据
        """
        query = "SELECT * FROM events WHERE event_id = %s"
        result = db.execute_query(query, (event_id,))
        
        if result:
            return result[0]
        return None
    
    @classmethod
    def get_all(cls, limit=100, offset=0):
        """
        获取所有事件，默认按时间戳降序排列
        
        Args:
            limit (int): 返回的最大事件数量
            offset (int): 分页偏移量
            
        Returns:
            list: 事件列表
        """
        query = "SELECT * FROM events ORDER BY timestamp DESC LIMIT %s OFFSET %s"
        return db.execute_query(query, (limit, offset))
    
    @classmethod
    def get_events_by_location(cls, location_id):
        """
        获取指定地点的所有事件
        
        Args:
            location_id (str): 地点ID
            
        Returns:
            list: 事件列表
        """
        query = "SELECT * FROM events WHERE location_id = %s ORDER BY timestamp DESC"
        return db.execute_query(query, (location_id,))
    
    @classmethod
    def search_events(cls, search_term):
        """
        搜索事件（标题和描述）
        
        Args:
            search_term (str): 搜索关键词
            
        Returns:
            list: 匹配的事件列表
        """
        search_pattern = f"%{search_term}%"
        query = """
        SELECT * FROM events 
        WHERE title LIKE %s OR description LIKE %s 
        ORDER BY timestamp DESC
        """
        return db.execute_query(query, (search_pattern, search_pattern))
    
    @classmethod
    def update(cls, event_id, attribute, value):
        """
        更新事件属性
        
        Args:
            event_id (str): 事件ID
            attribute (str): 属性名
            value: 属性值
            
        Returns:
            int: 受影响的行数
        """
        valid_attributes = [
            'title', 'description', 'location_id', 
            'timestamp', 'event_type', 'importance'
        ]
        
        if attribute not in valid_attributes:
            raise ValueError(f"无效的事件属性: {attribute}")
        
        query = f"UPDATE events SET {attribute} = %s WHERE event_id = %s"
        return db.execute_update(query, (value, event_id))
    
    @classmethod
    def delete(cls, event_id):
        """
        删除事件
        
        Args:
            event_id (str): 事件ID
            
        Returns:
            int: 受影响的行数
        """
        query = "DELETE FROM events WHERE event_id = %s"
        return db.execute_update(query, (event_id,))