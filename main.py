#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校园社交内容智能分发优化 - 演示系统
模拟基于BERT和协同过滤的混合推荐策略
"""

import json
import random
import time
from datetime import datetime
from typing import List, Dict, Any

class ContentRecommendationSystem:
    """校园社交内容推荐系统"""
    
    def __init__(self):
        """初始化推荐系统"""
        # 模拟用户兴趣标签（实际项目中由BERT模型生成）
        self.user_profiles = {
            "user_001": ["学习", "科技", "编程"],
            "user_002": ["美食", "旅游", "摄影"],
            "user_003": ["体育", "游戏", "音乐"],
            "user_004": ["社团", "活动", "社交"]
        }
        
        # 模拟内容数据库
        self.content_db = self._init_content_database()
        
        # 模拟协同过滤数据（用户-内容交互历史）
        self.interaction_history = {
            "user_001": ["post_001", "post_003", "post_005"],
            "user_002": ["post_002", "post_004"],
            "user_003": ["post_001", "post_006"],
            "user_004": ["post_003", "post_007"]
        }
        
        # 推荐策略权重配置
        self.strategy_weights = {
            "bert_content": 0.6,    # BERT内容兴趣匹配权重
            "collaborative": 0.3,   # 协同过滤权重
            "hot_trend": 0.1        # 热门趋势权重
        }
    
    def _init_content_database(self) -> List[Dict[str, Any]]:
        """初始化模拟内容数据库"""
        contents = []
        content_templates = [
            {"id": "post_001", "title": "Python机器学习入门指南", "tags": ["学习", "编程", "科技"], "likes": 150},
            {"id": "post_002", "title": "校园周边美食探店分享", "tags": ["美食", "生活"], "likes": 89},
            {"id": "post_003", "title": "最新AI技术研讨会通知", "tags": ["科技", "活动", "学习"], "likes": 120},
            {"id": "post_004", "title": "秋季校园摄影大赛作品", "tags": ["摄影", "艺术", "活动"], "likes": 210},
            {"id": "post_005", "title": "数据结构与算法复习资料", "tags": ["学习", "编程"], "likes": 95},
            {"id": "post_006", "title": "校园篮球联赛决赛预告", "tags": ["体育", "活动"], "likes": 180},
            {"id": "post_007", "title": "新生社团招新活动汇总", "tags": ["社团", "社交", "活动"], "likes": 76},
            {"id": "post_008", "title": "深度学习在推荐系统中的应用", "tags": ["科技", "学习", "编程"], "likes": 134},
            {"id": "post_009", "title": "校园音乐会演出安排", "tags": ["音乐", "活动"], "likes": 155},
            {"id": "post_010", "title": "毕业季求职经验分享会", "tags": ["学习", "社交", "活动"], "likes": 98}
        ]
        return content_templates
    
    def _bert_content_match(self, user_id: str, content: Dict[str, Any]) -> float:
        """
        模拟BERT内容兴趣匹配得分
        实际项目中：使用微调的BERT模型计算用户兴趣与内容语义匹配度
        """
        if user_id not in self.user_profiles:
            return 0.0
        
        user_tags = set(self.user_profiles[user_id])
        content_tags = set(content["tags"])
        
        # 计算Jaccard相似度（简化版，实际使用BERT语义匹配）
        intersection = len(user_tags & content_tags)
        union = len(user_tags | content_tags)
        
        return intersection / union if union > 0 else 0.0
    
    def _collaborative_filtering(self, user_id: str, content_id: str) -> float:
        """
        模拟协同过滤推荐得分
        实际项目中：基于用户-物品交互矩阵计算相似度
        """
        if user_id not in self.interaction_history:
            return 0.0
        
        # 查找与当前用户有相似交互行为的其他用户
        similar_users = []
        current_user_items = set(self.interaction_history[user_id])
        
        for other_user, items in self.interaction_history.items():
            if other_user != user_id:
                other_items = set(items)
                similarity = len(current_user_items & other_items) / len(current_user_items | other_items)
                if similarity > 0:
                    similar_users.append((other_user, similarity))
        
        # 计算基于相似用户的推荐得分
        if not similar_users:
            return 0.0
        
        # 检查相似用户是否对当前内容有过交互
        total_score = 0.0
        for other_user, similarity in similar_users:
            if content_id in self.interaction_history[other_user]:
                total_score += similarity
        
        return min(total_score / len(similar_users), 1.0) if similar_users else 0.0
    
    def _hot_trend_score(self, content: Dict[str, Any]) -> float:
        """计算热门趋势得分（基于点赞数）"""
        max_likes = max(item["likes"] for item in self.content_db)
        return content["likes"] / max_likes if max_likes > 0 else 0.0
    
    def get_personalized_recommendations(self, user_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        获取个性化内容推荐列表
        使用混合推荐策略：BERT内容匹配 + 协同过滤 + 热门趋势
        """
        if user_id not in self.user_profiles:
            return []
        
        scored_contents = []
        
        for content in self.content_db:
            # 计算各项得分
            bert_score = self._bert_content_match(user_id, content)
            cf_score = self._collaborative_filtering(user_id, content["id"])
            hot_score = self._hot_trend_score(content)
            
            # 加权综合得分
            total_score = (
                bert_score * self.strategy_weights["bert_content"] +
                cf_score * self.strategy_weights["collaborative"] +
                hot_score * self.strategy_weights["hot_trend"]
            )
            
            # 避免重复推荐用户已交互的内容
            if content["id"] not in self.interaction_history.get(user_id, []):
                scored_contents.append({
                    "content": content,
                    "score": total_score,
                    "score_breakdown": {
                        "bert_score": round(bert_score, 3),
                        "cf_score": round(cf_score, 3),
                        "hot_score": round(hot_score, 3)
                    }
                })
        
        # 按得分排序并返回top_k
        scored_contents.sort(key=lambda x: x["score"], reverse=True)
        
        return scored_contents[:top_k]
    
    def simulate_user_interaction(self, user_id: str, content_id: str):
        """模拟用户交互行为（用于更新协同过滤数据）"""
        if user_id in self.interaction_history:
            if content_id not in self.interaction_history[user_id]:
                self.interaction_history[user_id].append(content_id)
        else:
            self.interaction_history[user_id] = [content_id]

def main():
    """主函数 - 演示推荐系统工作流程"""
    print("=" * 60)
    print("校园社交内容智能分发优化系统")
    print("=" * 60)
    
    # 初始化推荐系统
    print("\n[1] 初始化推荐系统...")
    recommender = ContentRecommendationSystem()
    print(f"    ✓ 已加载 {len(recommender.content_db)} 条内容")
    print(f"    ✓ 已注册 {len(recommender.user_profiles)} 名用户")
    
    # 为不同用户生成推荐
    print("\n[2] 生成个性化推荐...")
    test_users = ["user_001", "user_002", "user_003"]
    
    for user_id in test_users:
        print(f"\n--- 用户 {user_id} 的推荐结果 ---")
        print(f"用户兴趣标签: {recommender.user_profiles[user_id]}")
        
        recommendations = recommender.get_personalized_recommendations(user_id, top_k=3)
        
        if not recommendations:
            print("暂无推荐内容")
            continue
        
        for i, rec in enumerate(recommendations, 1):
            content = rec["content"]
            print(f"{i}. {content['title']}")
            print(f"   标签: {content['tags']} | 点赞: {content['likes']}")
            print(f"   推荐得分: {rec['score']:.3f} (BERT:{rec['score_breakdown']['bert_score']}, "
                  f"协同过滤:{rec['score_breakdown']['cf_score']}, "
                  f"热门:{rec['score_breakdown']['hot_score']})")
    
    # 模拟A/B测试效果
    print("\n[3] 模拟A/B测试效果评估...")
    print("   实验组（使用推荐系统） vs 对照组（随机推荐）")
    
    # 模拟实验数据
    experimental_group = {
        "avg_browse_time": 25.3,  # 分钟
        "interaction_rate": 0.32   # 互动率
    }
    
    control_group = {
        "avg_browse_time": 22.0,  # 分钟
        "interaction_rate": 0.27   # 互动率
    }
    
    # 计算提升效果
    time_improvement = ((experimental_group["avg_browse_time"] - control_group["avg_browse_time"]) 
                       / control_group["avg_browse_time"] * 100)
    interaction_improvement = ((experimental_group["interaction_rate"] - control_group["interaction_rate"]) 
                              / control_group["interaction_rate"] * 100)
    
    print(f"   ✓ 日均浏览时长提升: {time_improvement:.1f}%")
    print(f"   ✓ 帖子互动率增加: {interaction_improvement:.1f}%")
    
    print("\n" + "=" * 60)
    print("演示完成 - 该项目展示了从需求分析、模型应用到效果评估的完整AI产品迭代流程")
    print("=" * 60)

if __name__ == "__main__":
    main()