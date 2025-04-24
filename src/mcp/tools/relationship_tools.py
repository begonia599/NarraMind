"""
关系工具类，提供角色关系相关的MCP工具函数
"""
import uuid
from typing import Dict, Any, List, Optional

from src.models import Relationship

class RelationshipTools:
    """关系工具类"""
    
    def create_relationship(self, 
                       character_id_1: str, 
                       character_id_2: str, 
                       relationship_type: str,
                       strength: int,
                       description: str,
                       relationship_id: Optional[str] = None) -> Dict[str, Any]:
        """
        创建新的角色关系
        
        Args:
            character_id_1: 角色1 ID
            character_id_2: 角色2 ID
            relationship_type: 关系类型 (如 'friend', 'enemy', 'family', 等)
            strength: 关系强度 (1-100)
            description: 关系描述
            relationship_id: 关系ID (可选，如果不提供将自动生成)
            
        Returns:
            dict: 包含关系数据和ID的字典
        """
        # 检查关系强度范围
        if not 1 <= strength <= 100:
            raise ValueError("关系强度必须在1到100之间")
            
        # 如果没有提供ID，生成一个新的UUID
        if not relationship_id:
            relationship_id = str(uuid.uuid4())
        
        relationship_data = {
            'relationship_id': relationship_id,
            'character_id_1': character_id_1,
            'character_id_2': character_id_2,
            'relationship_type': relationship_type,
            'strength': strength,
            'description': description
        }
        
        # 创建关系并获取ID
        created_id = Relationship.create(relationship_data)
        
        return {"relationship_id": created_id, "data": relationship_data}
    
    def get_relationship(self, relationship_id: str) -> Dict[str, Any]:
        """
        获取关系信息
        
        Args:
            relationship_id: 关系ID
            
        Returns:
            dict: 关系数据
        """
        relationship = Relationship.get_by_id(relationship_id)
        if not relationship:
            raise ValueError(f"未找到ID为 {relationship_id} 的关系")
        
        return relationship
    
    def get_character_relationships(self, character_id: str) -> List[Dict[str, Any]]:
        """
        获取角色的所有关系
        
        Args:
            character_id: 角色ID
            
        Returns:
            list: 关系列表
        """
        return Relationship.get_character_relationships(character_id)
    
    def get_relationship_between_characters(self, character_id_1: str, character_id_2: str) -> Dict[str, Any]:
        """
        获取两个角色之间的关系
        
        Args:
            character_id_1: 角色1 ID
            character_id_2: 角色2 ID
            
        Returns:
            dict: 关系数据，如果不存在则返回None
        """
        relationship = Relationship.get_relationship_between_characters(character_id_1, character_id_2)
        return relationship
    
    def update_relationship(self, relationship_id: str, attribute: str, value: Any) -> Dict[str, Any]:
        """
        更新关系属性
        
        Args:
            relationship_id: 关系ID
            attribute: 属性名 ('relationship_type', 'strength', 或 'description')
            value: 新的属性值
            
        Returns:
            dict: 更新后的关系数据
        """
        # 检查关系是否存在
        relationship = Relationship.get_by_id(relationship_id)
        if not relationship:
            raise ValueError(f"未找到ID为 {relationship_id} 的关系")
        
        # 如果是更新强度，检查范围
        if attribute == 'strength' and (not isinstance(value, int) or not 1 <= value <= 100):
            raise ValueError("关系强度必须是1到100之间的整数")
            
        # 更新关系属性
        rows_affected = Relationship.update_relationship(relationship_id, attribute, value)
        if rows_affected == 0:
            raise ValueError(f"更新关系属性失败")
        
        # 返回更新后的关系数据
        updated_relationship = Relationship.get_by_id(relationship_id)
        return updated_relationship
    
    def delete_relationship(self, relationship_id: str) -> Dict[str, Any]:
        """
        删除关系
        
        Args:
            relationship_id: 关系ID
            
        Returns:
            dict: 操作结果
        """
        # 检查关系是否存在
        relationship = Relationship.get_by_id(relationship_id)
        if not relationship:
            raise ValueError(f"未找到ID为 {relationship_id} 的关系")
        
        # 删除关系
        rows_affected = Relationship.delete(relationship_id)
        if rows_affected == 0:
            raise ValueError(f"删除关系失败")
        
        return {"success": True, "message": f"关系 {relationship_id} 已成功删除"}