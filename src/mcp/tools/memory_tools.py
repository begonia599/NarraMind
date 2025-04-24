"""
记忆工具类，提供高级记忆检索和上下文生成功能
"""
from typing import Dict, Any, List, Optional
import json

from src.models import Character, Location, Relationship, Event, EventCharacter

class MemoryTools:
    """记忆工具类，负责提供角色记忆与上下文检索服务"""
    
    def get_character_context(self, character_id: str, 
                          include_relationships: bool = True, 
                          include_events: bool = True,
                          include_skills: bool = True,
                          event_limit: int = 10) -> Dict[str, Any]:
        """
        获取角色的完整上下文信息
        
        Args:
            character_id: 角色ID
            include_relationships: 是否包含角色的关系
            include_events: 是否包含角色参与的事件
            include_skills: 是否包含角色的技能
            event_limit: 最多包含多少个事件
            
        Returns:
            dict: 角色的上下文信息
        """
        # 获取角色基本信息
        character = Character.get_by_id(character_id)
        if not character:
            raise ValueError(f"未找到ID为 {character_id} 的角色")
        
        result = {
            "character": character
        }
        
        # 如果需要，添加角色关系信息
        if include_relationships:
            relationships = Relationship.get_character_relationships(character_id)
            result["relationships"] = relationships
        
        # 如果需要，添加角色技能信息
        if include_skills:
            from src.models import CharacterSkill
            skills = CharacterSkill.get_character_skills(character_id)
            result["skills"] = skills
        
        # 如果需要，添加角色参与的事件
        if include_events:
            events = EventCharacter.get_events_involving_character(character_id)
            # 限制事件数量
            result["events"] = events[:event_limit]
        
        return result
    
    def get_location_context(self, location_id: str, 
                         include_events: bool = True, 
                         event_limit: int = 10) -> Dict[str, Any]:
        """
        获取地点的完整上下文信息
        
        Args:
            location_id: 地点ID
            include_events: 是否包含发生在该地点的事件
            event_limit: 最多包含多少个事件
            
        Returns:
            dict: 地点的上下文信息
        """
        # 获取地点基本信息
        location = Location.get_by_id(location_id)
        if not location:
            raise ValueError(f"未找到ID为 {location_id} 的地点")
        
        result = {
            "location": location
        }
        
        # 获取子地点
        child_locations = Location.get_child_locations(location_id)
        if child_locations:
            result["child_locations"] = child_locations
        
        # 如果需要，添加地点相关事件
        if include_events:
            events = Event.get_events_by_location(location_id)
            # 限制事件数量
            result["events"] = events[:event_limit]
        
        return result
    
    def get_relationship_context(self, character_id_1: str, character_id_2: str) -> Dict[str, Any]:
        """
        获取两个角色之间的关系上下文
        
        Args:
            character_id_1: 角色1 ID
            character_id_2: 角色2 ID
            
        Returns:
            dict: 关系上下文信息
        """
        # 获取角色1信息
        character1 = Character.get_by_id(character_id_1)
        if not character1:
            raise ValueError(f"未找到ID为 {character_id_1} 的角色")
        
        # 获取角色2信息
        character2 = Character.get_by_id(character_id_2)
        if not character2:
            raise ValueError(f"未找到ID为 {character_id_2} 的角色")
        
        # 获取两个角色之间的关系
        relationship = Relationship.get_relationship_between_characters(character_id_1, character_id_2)
        
        # 查找两个角色共同参与的事件
        # 这需要通过子查询实现，此处简化处理
        query = """
        SELECT e.* FROM events e
        JOIN event_characters ec1 ON e.event_id = ec1.event_id
        JOIN event_characters ec2 ON e.event_id = ec2.event_id
        WHERE ec1.character_id = %s AND ec2.character_id = %s
        ORDER BY e.timestamp DESC
        LIMIT 5
        """
        from src.db import db
        shared_events = db.execute_query(query, (character_id_1, character_id_2))
        
        return {
            "character1": character1,
            "character2": character2,
            "relationship": relationship,
            "shared_events": shared_events
        }
    
    def search_memory(self, 
                  query: str, 
                  search_characters: bool = True, 
                  search_locations: bool = True, 
                  search_events: bool = True,
                  limit: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        搜索记忆知识库
        
        Args:
            query: 搜索关键词
            search_characters: 是否搜索角色
            search_locations: 是否搜索地点
            search_events: 是否搜索事件
            limit: 每类结果的最大数量
            
        Returns:
            dict: 搜索结果
        """
        result = {}
        search_pattern = f"%{query}%"
        
        # 搜索角色
        if search_characters:
            character_query = """
            SELECT * FROM characters
            WHERE name LIKE %s OR occupation LIKE %s OR backstory LIKE %s
            LIMIT %s
            """
            from src.db import db
            characters = db.execute_query(
                character_query, 
                (search_pattern, search_pattern, search_pattern, limit)
            )
            result["characters"] = characters
        
        # 搜索地点
        if search_locations:
            location_query = """
            SELECT * FROM locations
            WHERE name LIKE %s OR description LIKE %s
            LIMIT %s
            """
            from src.db import db
            locations = db.execute_query(
                location_query, 
                (search_pattern, search_pattern, limit)
            )
            result["locations"] = locations
        
        # 搜索事件
        if search_events:
            event_query = """
            SELECT * FROM events
            WHERE title LIKE %s OR description LIKE %s
            ORDER BY timestamp DESC
            LIMIT %s
            """
            from src.db import db
            events = db.execute_query(
                event_query, 
                (search_pattern, search_pattern, limit)
            )
            result["events"] = events
        
        return result