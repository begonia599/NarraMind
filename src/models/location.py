"""
地点模型类，用于管理地点的CRUD操作
"""
from src.db import db

class Location:
    """地点模型类"""
    
    def __init__(self, location_id=None, name=None, description=None, 
                location_type=None, parent_location_id=None):
        self.location_id = location_id
        self.name = name
        self.description = description
        self.location_type = location_type
        self.parent_location_id = parent_location_id
    
    @classmethod
    def create(cls, location_data):
        """
        创建新地点
        
        Args:
            location_data (dict): 地点数据
                {
                    'location_id': str,
                    'name': str,
                    'description': str,
                    'location_type': str,
                    'parent_location_id': str (可选)
                }
                
        Returns:
            str: 地点ID
        """
        query = """
        INSERT INTO locations (location_id, name, description, location_type, parent_location_id) 
        VALUES (%s, %s, %s, %s, %s)
        """
        
        params = (
            location_data.get('location_id'),
            location_data.get('name'),
            location_data.get('description'),
            location_data.get('location_type'),
            location_data.get('parent_location_id')
        )
        
        try:
            db.execute_update(query, params)
            return location_data.get('location_id')
        except Exception as e:
            print(f"创建地点失败: {e}")
            raise
    
    @classmethod
    def get_by_id(cls, location_id):
        """
        根据ID获取地点
        
        Args:
            location_id (str): 地点ID
            
        Returns:
            dict: 地点数据
        """
        query = "SELECT * FROM locations WHERE location_id = %s"
        result = db.execute_query(query, (location_id,))
        
        if result:
            return result[0]
        return None
    
    @classmethod
    def get_all(cls):
        """
        获取所有地点
        
        Returns:
            list: 地点列表
        """
        query = "SELECT * FROM locations"
        return db.execute_query(query)
    
    @classmethod
    def get_child_locations(cls, parent_location_id):
        """
        获取子地点
        
        Args:
            parent_location_id (str): 父地点ID
            
        Returns:
            list: 子地点列表
        """
        query = "SELECT * FROM locations WHERE parent_location_id = %s"
        return db.execute_query(query, (parent_location_id,))
    
    @classmethod
    def update(cls, location_id, attribute, value):
        """
        更新地点属性
        
        Args:
            location_id (str): 地点ID
            attribute (str): 属性名
            value: 属性值
            
        Returns:
            int: 受影响的行数
        """
        valid_attributes = ['name', 'description', 'location_type', 'parent_location_id']
        
        if attribute not in valid_attributes:
            raise ValueError(f"无效的地点属性: {attribute}")
        
        query = f"UPDATE locations SET {attribute} = %s WHERE location_id = %s"
        return db.execute_update(query, (value, location_id))
    
    @classmethod
    def delete(cls, location_id):
        """
        删除地点
        
        Args:
            location_id (str): 地点ID
            
        Returns:
            int: 受影响的行数
        """
        query = "DELETE FROM locations WHERE location_id = %s"
        return db.execute_update(query, (location_id,))