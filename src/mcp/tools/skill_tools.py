"""
技能工具类，提供技能相关的MCP工具函数
"""
import uuid
from typing import Dict, Any, List, Optional

from src.models import Skill, CharacterSkill

class SkillTools:
    """技能工具类"""
    
    def create_skill(self, 
                 name: str, 
                 description: str, 
                 skill_id: Optional[str] = None) -> Dict[str, Any]:
        """
        创建新技能
        
        Args:
            name: 技能名称
            description: 技能描述
            skill_id: 技能ID (可选，如果不提供将自动生成)
            
        Returns:
            dict: 包含技能数据和ID的字典
        """
        # 如果没有提供ID，生成一个新的UUID
        if not skill_id:
            skill_id = str(uuid.uuid4())
        
        skill_data = {
            'skill_id': skill_id,
            'name': name,
            'description': description
        }
        
        # 创建技能并获取ID
        created_id = Skill.create(skill_data)
        
        return {"skill_id": created_id, "data": skill_data}
    
    def get_skill(self, skill_id: str) -> Dict[str, Any]:
        """
        获取技能信息
        
        Args:
            skill_id: 技能ID
            
        Returns:
            dict: 技能数据
        """
        skill = Skill.get_by_id(skill_id)
        if not skill:
            raise ValueError(f"未找到ID为 {skill_id} 的技能")
        
        return skill
    
    def get_all_skills(self) -> List[Dict[str, Any]]:
        """
        获取所有技能
        
        Returns:
            list: 技能列表
        """
        return Skill.get_all()
    
    def update_skill(self, skill_id: str, description: str) -> Dict[str, Any]:
        """
        更新技能描述
        
        Args:
            skill_id: 技能ID
            description: 新的技能描述
            
        Returns:
            dict: 更新后的技能数据
        """
        # 检查技能是否存在
        skill = Skill.get_by_id(skill_id)
        if not skill:
            raise ValueError(f"未找到ID为 {skill_id} 的技能")
        
        # 更新技能描述
        rows_affected = Skill.update_description(skill_id, description)
        if rows_affected == 0:
            raise ValueError(f"更新技能描述失败")
        
        # 返回更新后的技能数据
        updated_skill = Skill.get_by_id(skill_id)
        return updated_skill
    
    def delete_skill(self, skill_id: str) -> Dict[str, Any]:
        """
        删除技能
        
        Args:
            skill_id: 技能ID
            
        Returns:
            dict: 操作结果
        """
        # 检查技能是否存在
        skill = Skill.get_by_id(skill_id)
        if not skill:
            raise ValueError(f"未找到ID为 {skill_id} 的技能")
        
        # 删除技能
        rows_affected = Skill.delete(skill_id)
        if rows_affected == 0:
            raise ValueError(f"删除技能失败")
        
        return {"success": True, "message": f"技能 {skill_id} 已成功删除"}
    
    def add_character_skill(self, 
                       character_id: str, 
                       skill_id: str, 
                       level: int = 1) -> Dict[str, Any]:
        """
        为角色添加技能
        
        Args:
            character_id: 角色ID
            skill_id: 技能ID
            level: 技能等级，默认为1
            
        Returns:
            dict: 包含关联ID和关联数据的字典
        """
        # 添加角色技能关联
        relation_id = CharacterSkill.add_character_skill(character_id, skill_id, level)
        
        return {
            "relation_id": relation_id,
            "character_id": character_id,
            "skill_id": skill_id,
            "level": level
        }
    
    def get_character_skills(self, character_id: str) -> List[Dict[str, Any]]:
        """
        获取角色的所有技能
        
        Args:
            character_id: 角色ID
            
        Returns:
            list: 角色技能列表
        """
        return CharacterSkill.get_character_skills(character_id)
    
    def update_character_skill(self, 
                        character_id: str, 
                        skill_id: str, 
                        level: int) -> Dict[str, Any]:
        """
        更新角色的技能等级
        
        Args:
            character_id: 角色ID
            skill_id: 技能ID
            level: 新的技能等级
            
        Returns:
            dict: 操作结果
        """
        # 更新角色技能等级
        rows_affected = CharacterSkill.update_character_skill_level(character_id, skill_id, level)
        if rows_affected == 0:
            raise ValueError(f"更新角色技能等级失败")
        
        return {
            "success": True,
            "character_id": character_id,
            "skill_id": skill_id,
            "level": level
        }
    
    def remove_character_skill(self, character_id: str, skill_id: str) -> Dict[str, Any]:
        """
        移除角色的技能
        
        Args:
            character_id: 角色ID
            skill_id: 技能ID
            
        Returns:
            dict: 操作结果
        """
        # 移除角色技能关联
        rows_affected = CharacterSkill.remove_character_skill(character_id, skill_id)
        if rows_affected == 0:
            raise ValueError(f"移除角色技能失败，可能关联不存在")
        
        return {
            "success": True,
            "message": f"已成功移除角色 {character_id} 的技能 {skill_id}"
        }