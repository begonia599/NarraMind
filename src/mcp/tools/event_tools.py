"""
事件工具类，提供事件相关的MCP工具函数
"""
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from src.models import Event

class EventTools:
    """事件工具类"""
    
    def create_event(self, 
                 title: str, 
                 description: str, 
                 location_id: str,
                 event_type: str,
                 importance: int,
                 timestamp: Optional[datetime] = None,
                 event_id: Optional[str] = None) -> Dict[str, Any]:
        """
        创建新事件
        
        Args:
            title: 事件标题
            description: 事件描述
            location_id: 事件发生地点ID
            event_type: 事件类型
            importance: 事件重要性 (1-100)
            timestamp: 事件发生时间 (可选，默认为当前时间)
            event_id: 事件ID (可选，如果不提供将自动生成)
            
        Returns:
            dict: 包含事件数据和ID的字典
        """
        # 检查事件重要性范围
        if not 1 <= importance <= 100:
            raise ValueError("事件重要性必须在1到100之间")
            
        # 如果没有提供ID，生成一个新的UUID
        if not event_id:
            event_id = str(uuid.uuid4())
        
        event_data = {
            'event_id': event_id,
            'title': title,
            'description': description,
            'location_id': location_id,
            'timestamp': timestamp,
            'event_type': event_type,
            'importance': importance
        }
        
        # 创建事件并获取ID
        created_id = Event.create(event_data)
        
        return {"event_id": created_id, "data": event_data}
    
    def get_event(self, event_id: str) -> Dict[str, Any]:
        """
        获取事件信息
        
        Args:
            event_id: 事件ID
            
        Returns:
            dict: 事件数据
        """
        event = Event.get_by_id(event_id)
        if not event:
            raise ValueError(f"未找到ID为 {event_id} 的事件")
        
        return event
    
    def get_all_events(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        获取所有事件，按时间戳降序排序
        
        Args:
            limit: 返回记录的最大数量
            offset: 分页偏移量
            
        Returns:
            list: 事件列表
        """
        return Event.get_all(limit, offset)
    
    def get_events_by_location(self, location_id: str) -> List[Dict[str, Any]]:
        """
        获取指定地点的所有事件
        
        Args:
            location_id: 地点ID
            
        Returns:
            list: 事件列表
        """
        return Event.get_events_by_location(location_id)
    
    def search_events(self, search_term: str) -> List[Dict[str, Any]]:
        """
        搜索事件
        
        Args:
            search_term: 搜索关键词
            
        Returns:
            list: 匹配的事件列表
        """
        return Event.search_events(search_term)
    
    def update_event(self, event_id: str, attribute: str, value: Any) -> Dict[str, Any]:
        """
        更新事件属性
        
        Args:
            event_id: 事件ID
            attribute: 属性名
            value: 新的属性值
            
        Returns:
            dict: 更新后的事件数据
        """
        # 检查事件是否存在
        event = Event.get_by_id(event_id)
        if not event:
            raise ValueError(f"未找到ID为 {event_id} 的事件")
        
        # 如果是更新重要性，检查范围
        if attribute == 'importance' and (not isinstance(value, int) or not 1 <= value <= 100):
            raise ValueError("事件重要性必须是1到100之间的整数")
            
        # 更新事件属性
        rows_affected = Event.update(event_id, attribute, value)
        if rows_affected == 0:
            raise ValueError(f"更新事件属性失败")
        
        # 返回更新后的事件数据
        updated_event = Event.get_by_id(event_id)
        return updated_event
    
    def delete_event(self, event_id: str) -> Dict[str, Any]:
        """
        删除事件
        
        Args:
            event_id: 事件ID
            
        Returns:
            dict: 操作结果
        """
        # 检查事件是否存在
        event = Event.get_by_id(event_id)
        if not event:
            raise ValueError(f"未找到ID为 {event_id} 的事件")
        
        # 删除事件
        rows_affected = Event.delete(event_id)
        if rows_affected == 0:
            raise ValueError(f"删除事件失败")
        
        return {"success": True, "message": f"事件 {event_id} 已成功删除"}