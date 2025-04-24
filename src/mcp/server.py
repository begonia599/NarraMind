"""
MCP服务器模块，实现基于FastMCP的工具函数
"""
import logging
from typing import Dict, Any, List, Optional, Union
from fastmcp import FastMCP

from src.models import Character, Skill, CharacterSkill, Location, Relationship, Event
from src.mcp.tools import (
    CharacterTools, 
    SkillTools, 
    LocationTools, 
    RelationshipTools, 
    EventTools, 
    MemoryTools
)

# 配置日志
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastMCP实例
mcp_server = FastMCP("NarraMind")

# 初始化工具集
character_tools = CharacterTools()
skill_tools = SkillTools()
location_tools = LocationTools()
relationship_tools = RelationshipTools()
event_tools = EventTools()
memory_tools = MemoryTools()

# 角色工具
@mcp_server.tool()
def character_create(name: str, played_by: str, age: Optional[int] = None,
                 gender: Optional[str] = None, occupation: Optional[str] = None, 
                 appearance: Optional[str] = None, voice_tone: Optional[str] = None,
                 voice_style: Optional[str] = None, mannerisms: Optional[str] = None,
                 current_goal: Optional[str] = None, backstory: Optional[str] = None,
                 notes: Optional[str] = None, character_id: Optional[str] = None) -> Dict[str, Any]:
    """创建新角色"""
    return character_tools.create_character(
        name, played_by, age, gender, occupation, appearance, voice_tone,
        voice_style, mannerisms, current_goal, backstory, notes, character_id
    )

@mcp_server.tool()
def character_get(character_id: str) -> Dict[str, Any]:
    """获取角色信息"""
    return character_tools.get_character(character_id)

@mcp_server.tool()
def character_get_all() -> List[Dict[str, Any]]:
    """获取所有角色"""
    return character_tools.get_all_characters()

@mcp_server.tool()
def character_update(character_id: str, attribute: str, value: Any) -> Dict[str, Any]:
    """更新角色属性"""
    return character_tools.update_character(character_id, attribute, value)

@mcp_server.tool()
def character_delete(character_id: str) -> Dict[str, Any]:
    """删除角色"""
    return character_tools.delete_character(character_id)

# 技能工具
@mcp_server.tool()
def skill_create(name: str, description: str, skill_id: Optional[str] = None) -> Dict[str, Any]:
    """创建新技能"""
    return skill_tools.create_skill(name, description, skill_id)

@mcp_server.tool()
def skill_get(skill_id: str) -> Dict[str, Any]:
    """获取技能信息"""
    return skill_tools.get_skill(skill_id)

@mcp_server.tool()
def skill_get_all() -> List[Dict[str, Any]]:
    """获取所有技能"""
    return skill_tools.get_all_skills()

@mcp_server.tool()
def skill_update(skill_id: str, description: str) -> Dict[str, Any]:
    """更新技能描述"""
    return skill_tools.update_skill(skill_id, description)

@mcp_server.tool()
def skill_delete(skill_id: str) -> Dict[str, Any]:
    """删除技能"""
    return skill_tools.delete_skill(skill_id)

@mcp_server.tool()
def character_add_skill(character_id: str, skill_id: str, level: int = 1) -> Dict[str, Any]:
    """为角色添加技能"""
    return skill_tools.add_character_skill(character_id, skill_id, level)

@mcp_server.tool()
def character_get_skills(character_id: str) -> List[Dict[str, Any]]:
    """获取角色的所有技能"""
    return skill_tools.get_character_skills(character_id)

@mcp_server.tool()
def character_update_skill(character_id: str, skill_id: str, level: int) -> Dict[str, Any]:
    """更新角色的技能等级"""
    return skill_tools.update_character_skill(character_id, skill_id, level)

@mcp_server.tool()
def character_remove_skill(character_id: str, skill_id: str) -> Dict[str, Any]:
    """移除角色的技能"""
    return skill_tools.remove_character_skill(character_id, skill_id)

# 地点工具
@mcp_server.tool()
def location_create(name: str, description: str, location_type: str,
               parent_location_id: Optional[str] = None,
               location_id: Optional[str] = None) -> Dict[str, Any]:
    """创建新地点"""
    return location_tools.create_location(
        name, description, location_type, parent_location_id, location_id
    )

@mcp_server.tool()
def location_get(location_id: str) -> Dict[str, Any]:
    """获取地点信息"""
    return location_tools.get_location(location_id)

@mcp_server.tool()
def location_get_all() -> List[Dict[str, Any]]:
    """获取所有地点"""
    return location_tools.get_all_locations()

@mcp_server.tool()
def location_update(location_id: str, attribute: str, value: Any) -> Dict[str, Any]:
    """更新地点属性"""
    return location_tools.update_location(location_id, attribute, value)

@mcp_server.tool()
def location_delete(location_id: str) -> Dict[str, Any]:
    """删除地点"""
    return location_tools.delete_location(location_id)

@mcp_server.tool()
def location_get_children(parent_location_id: str) -> List[Dict[str, Any]]:
    """获取子地点"""
    return location_tools.get_child_locations(parent_location_id)

# 关系工具
@mcp_server.tool()
def relationship_create(character_id_1: str, character_id_2: str, relationship_type: str,
                   strength: int, description: str,
                   relationship_id: Optional[str] = None) -> Dict[str, Any]:
    """创建新的角色关系"""
    return relationship_tools.create_relationship(
        character_id_1, character_id_2, relationship_type,
        strength, description, relationship_id
    )

@mcp_server.tool()
def relationship_get(relationship_id: str) -> Dict[str, Any]:
    """获取关系信息"""
    return relationship_tools.get_relationship(relationship_id)

@mcp_server.tool()
def relationship_get_character_relationships(character_id: str) -> List[Dict[str, Any]]:
    """获取角色的所有关系"""
    return relationship_tools.get_character_relationships(character_id)

@mcp_server.tool()
def relationship_get_between_characters(character_id_1: str, character_id_2: str) -> Dict[str, Any]:
    """获取两个角色之间的关系"""
    return relationship_tools.get_relationship_between_characters(character_id_1, character_id_2)

@mcp_server.tool()
def relationship_update(relationship_id: str, attribute: str, value: Any) -> Dict[str, Any]:
    """更新关系属性"""
    return relationship_tools.update_relationship(relationship_id, attribute, value)

@mcp_server.tool()
def relationship_delete(relationship_id: str) -> Dict[str, Any]:
    """删除关系"""
    return relationship_tools.delete_relationship(relationship_id)

# 事件工具
@mcp_server.tool()
def event_create(title: str, description: str, location_id: str,
            event_type: str, importance: int,
            timestamp: Optional[str] = None,
            event_id: Optional[str] = None) -> Dict[str, Any]:
    """创建新事件"""
    return event_tools.create_event(
        title, description, location_id, event_type,
        importance, timestamp, event_id
    )

@mcp_server.tool()
def event_get(event_id: str) -> Dict[str, Any]:
    """获取事件信息"""
    return event_tools.get_event(event_id)

@mcp_server.tool()
def event_get_all(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """获取所有事件"""
    return event_tools.get_all_events(limit, offset)

@mcp_server.tool()
def event_get_by_location(location_id: str) -> List[Dict[str, Any]]:
    """获取指定地点的所有事件"""
    return event_tools.get_events_by_location(location_id)

@mcp_server.tool()
def event_search(search_term: str) -> List[Dict[str, Any]]:
    """搜索事件"""
    return event_tools.search_events(search_term)

@mcp_server.tool()
def event_update(event_id: str, attribute: str, value: Any) -> Dict[str, Any]:
    """更新事件属性"""
    return event_tools.update_event(event_id, attribute, value)

@mcp_server.tool()
def event_delete(event_id: str) -> Dict[str, Any]:
    """删除事件"""
    return event_tools.delete_event(event_id)

# 记忆查询工具
@mcp_server.tool()
def memory_get_character_context(character_id: str, 
                            include_relationships: bool = True, 
                            include_events: bool = True,
                            include_skills: bool = True,
                            event_limit: int = 10) -> Dict[str, Any]:
    """获取角色的完整上下文信息"""
    return memory_tools.get_character_context(
        character_id, include_relationships, include_events,
        include_skills, event_limit
    )

@mcp_server.tool()
def memory_get_location_context(location_id: str, 
                           include_events: bool = True, 
                           event_limit: int = 10) -> Dict[str, Any]:
    """获取地点的完整上下文信息"""
    return memory_tools.get_location_context(
        location_id, include_events, event_limit
    )

@mcp_server.tool()
def memory_get_relationship_context(character_id_1: str, character_id_2: str) -> Dict[str, Any]:
    """获取两个角色之间的关系上下文"""
    return memory_tools.get_relationship_context(character_id_1, character_id_2)

@mcp_server.tool()
def memory_search(query: str, 
             search_characters: bool = True, 
             search_locations: bool = True, 
             search_events: bool = True,
             limit: int = 5) -> Dict[str, List[Dict[str, Any]]]:
    """搜索记忆知识库"""
    return memory_tools.search_memory(
        query, search_characters, search_locations, search_events, limit
    )

# 记录服务器已准备就绪
logger.info("MCP服务器初始化完成")

# 如果直接运行这个模块，启动服务器
if __name__ == "__main__":
    mcp_server.run()