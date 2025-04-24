"""
地点工具类，提供地点相关的MCP工具函数
"""
import uuid
from typing import Dict, Any, List, Optional

from src.models import Location

class LocationTools:
    """地点工具类"""
    
    def create_location(self, 
                    name: str, 
                    description: str, 
                    location_type: str,
                    parent_location_id: Optional[str] = None,
                    location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        创建新地点
        
        Args:
            name: 地点名称
            description: 地点描述
            location_type: 地点类型 (如 'city', 'building', 'room', 等)
            parent_location_id: 父地点ID (可选)
            location_id: 地点ID (可选，如果不提供将自动生成)
            
        Returns:
            dict: 包含地点数据和ID的字典
        """
        # 如果没有提供ID，生成一个新的UUID
        if not location_id:
            location_id = str(uuid.uuid4())
        
        location_data = {
            'location_id': location_id,
            'name': name,
            'description': description,
            'location_type': location_type,
            'parent_location_id': parent_location_id
        }
        
        # 创建地点并获取ID
        created_id = Location.create(location_data)
        
        return {"location_id": created_id, "data": location_data}
    
    def get_location(self, location_id: str) -> Dict[str, Any]:
        """
        获取地点信息
        
        Args:
            location_id: 地点ID
            
        Returns:
            dict: 地点数据
        """
        location = Location.get_by_id(location_id)
        if not location:
            raise ValueError(f"未找到ID为 {location_id} 的地点")
        
        return location
    
    def get_all_locations(self) -> List[Dict[str, Any]]:
        """
        获取所有地点
        
        Returns:
            list: 地点列表
        """
        return Location.get_all()
    
    def get_child_locations(self, parent_location_id: str) -> List[Dict[str, Any]]:
        """
        获取子地点
        
        Args:
            parent_location_id: 父地点ID
            
        Returns:
            list: 子地点列表
        """
        return Location.get_child_locations(parent_location_id)
    
    def update_location(self, location_id: str, attribute: str, value: Any) -> Dict[str, Any]:
        """
        更新地点属性
        
        Args:
            location_id: 地点ID
            attribute: 属性名
            value: 新的属性值
            
        Returns:
            dict: 更新后的地点数据
        """
        # 检查地点是否存在
        location = Location.get_by_id(location_id)
        if not location:
            raise ValueError(f"未找到ID为 {location_id} 的地点")
        
        # 更新地点属性
        rows_affected = Location.update(location_id, attribute, value)
        if rows_affected == 0:
            raise ValueError(f"更新地点属性失败")
        
        # 返回更新后的地点数据
        updated_location = Location.get_by_id(location_id)
        return updated_location
    
    def delete_location(self, location_id: str) -> Dict[str, Any]:
        """
        删除地点
        
        Args:
            location_id: 地点ID
            
        Returns:
            dict: 操作结果
        """
        # 检查地点是否存在
        location = Location.get_by_id(location_id)
        if not location:
            raise ValueError(f"未找到ID为 {location_id} 的地点")
        
        # 删除地点
        rows_affected = Location.delete(location_id)
        if rows_affected == 0:
            raise ValueError(f"删除地点失败")
        
        return {"success": True, "message": f"地点 {location_id} 已成功删除"}