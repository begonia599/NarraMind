"""
角色工具类，提供角色相关的MCP工具函数
"""
import uuid
from typing import Dict, Any, List, Optional

from src.models import Character

class CharacterTools:
    """角色工具类"""
    
    def create_character(self, 
                     name: str, 
                     played_by: str, 
                     age: Optional[int] = None,
                     gender: Optional[str] = None,
                     occupation: Optional[str] = None, 
                     appearance: Optional[str] = None, 
                     voice_tone: Optional[str] = None,
                     voice_style: Optional[str] = None,
                     mannerisms: Optional[str] = None,
                     current_goal: Optional[str] = None,
                     backstory: Optional[str] = None,
                     notes: Optional[str] = None,
                     character_id: Optional[str] = None) -> Dict[str, Any]:
        """
        创建新角色
        
        Args:
            name: 角色名称
            played_by: 由谁扮演 ('player' 或 'ai')
            age: 年龄 (可选)
            gender: 性别 (可选)
            occupation: 职业 (可选)
            appearance: 外貌描述 (可选)
            voice_tone: 声音音调 (可选)
            voice_style: 说话方式 (可选)
            mannerisms: 行为习惯 (可选)
            current_goal: 当前目标 (可选)
            backstory: 背景故事 (可选)
            notes: 备注 (可选)
            character_id: 角色ID (可选，如果不提供将自动生成)
            
        Returns:
            dict: 包含角色数据和ID的字典
        """
        # 如果没有提供ID，生成一个新的UUID
        if not character_id:
            character_id = str(uuid.uuid4())
        
        character_data = {
            'character_id': character_id,
            'name': name,
            'played_by': played_by,
            'age': age,
            'gender': gender,
            'occupation': occupation,
            'appearance': appearance,
            'voice_tone': voice_tone,
            'voice_style': voice_style,
            'mannerisms': mannerisms,
            'current_goal': current_goal,
            'backstory': backstory,
            'notes': notes
        }
        
        # 创建角色并获取ID
        created_id = Character.create(character_data)
        
        return {"character_id": created_id, "data": character_data}
    
    def get_character(self, character_id: str) -> Dict[str, Any]:
        """
        获取角色信息
        
        Args:
            character_id: 角色ID
            
        Returns:
            dict: 角色数据
        """
        character = Character.get_by_id(character_id)
        if not character:
            raise ValueError(f"未找到ID为 {character_id} 的角色")
        
        return character
    
    def get_all_characters(self) -> List[Dict[str, Any]]:
        """
        获取所有角色
        
        Returns:
            list: 角色列表
        """
        return Character.get_all()
    
    def update_character(self, character_id: str, attribute: str, value: Any) -> Dict[str, Any]:
        """
        更新角色属性
        
        Args:
            character_id: 角色ID
            attribute: 要更新的属性名
            value: 新的属性值
            
        Returns:
            dict: 更新后的角色数据
        """
        # 检查角色是否存在
        character = Character.get_by_id(character_id)
        if not character:
            raise ValueError(f"未找到ID为 {character_id} 的角色")
        
        # 更新角色属性
        rows_affected = Character.update(character_id, attribute, value)
        if rows_affected == 0:
            raise ValueError(f"更新角色属性失败")
        
        # 返回更新后的角色数据
        updated_character = Character.get_by_id(character_id)
        return updated_character
    
    def delete_character(self, character_id: str) -> Dict[str, Any]:
        """
        删除角色
        
        Args:
            character_id: 角色ID
            
        Returns:
            dict: 操作结果
        """
        # 检查角色是否存在
        character = Character.get_by_id(character_id)
        if not character:
            raise ValueError(f"未找到ID为 {character_id} 的角色")
        
        # 删除角色
        rows_affected = Character.delete(character_id)
        if rows_affected == 0:
            raise ValueError(f"删除角色失败")
        
        return {"success": True, "message": f"角色 {character_id} 已成功删除"}