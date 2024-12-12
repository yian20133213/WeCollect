from datetime import datetime
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin
import re
from loguru import logger

from .base_parser import BaseParser
from config.settings import CRAWLER

class ArticleParser(BaseParser):
    """文章解析器"""
    
    def parse(self, html: str) -> Dict[str, Any]:
        """解析文章内容"""
        self.init_soup(html)
        
        return {
            "meta": self._parse_meta(),
            "content": self._parse_content(),
            "media": self._parse_media()
        }
        
    def _parse_meta(self) -> Dict[str, Any]:
        """解析文章元数据"""
        try:
            # 提取文章标题
            title = self.soup.select_one('#activity-name')
            title = self.clean_text(title.text) if title else ""
            
            # 提取作者
            author = self.soup.select_one('#js_name')
            author = self.clean_text(author.text) if author else ""
            
            # 提取发布时间
            publish_time = self.soup.select_one('#publish_time')
            if publish_time:
                publish_time = datetime.strptime(
                    self.clean_text(publish_time.text),
                    '%Y-%m-%d %H:%M'
                )
            
            # 提取原文链接
            original_url = self.soup.select_one('meta[property="og:url"]')
            original_url = original_url.get('content', '') if original_url else ""
            
            return {
                "title": title,
                "author": author,
                "publish_time": publish_time,
                "original_url": original_url
            }
        except Exception as e:
            logger.error(f"解析文章元数据失败: {str(e)}")
            raise
            
    def _parse_content(self) -> Dict[str, str]:
        """解析文章内容"""
        try:
            content_element = self.soup.select_one('#js_content')
            if not content_element:
                raise ValueError("未找到文章内容区域")
                
            # 获取原始HTML
            original_html = str(content_element)
            
            # 清理HTML
            self._clean_content(content_element)
            
            # 获取纯文本
            text_content = self.clean_text(content_element.get_text())
            
            # 获取清理后的HTML
            clean_html = str(content_element)
            
            return {
                "text": text_content,
                "html": clean_html,
                "original_html": original_html
            }
        except Exception as e:
            logger.error(f"解析文章内容失败: {str(e)}")
            raise
            
    def _clean_content(self, element) -> None:
        """清理内容元素"""
        # 移除样式属性
        for tag in element.find_all(True):
            # 保留的属性列表
            keep_attrs = ['src', 'data-src', 'href', 'title', 'alt']
            attrs = dict(tag.attrs)
            for attr in attrs:
                if attr not in keep_attrs:
                    del tag[attr]
            
            # 移除空标签
            if not tag.contents and tag.name not in ['img', 'br']:
                tag.decompose()
            
            # 处理图片标签
            if tag.name == 'img':
                # 将data-src属性值复制到src
                if tag.get('data-src'):
                    tag['src'] = tag['data-src']
                    del tag['data-src']
                    
    def _parse_media(self) -> Dict[str, List[Dict]]:
        """解析媒体资源"""
        try:
            content_element = self.soup.select_one('#js_content')
            if not content_element:
                return {"images": [], "videos": []}
                
            images = self._extract_images(content_element)
            videos = self._extract_videos(content_element)
            
            return {
                "images": images,
                "videos": videos
            }
        except Exception as e:
            logger.error(f"解析媒体资源失败: {str(e)}")
            raise
            
    def _extract_images(self, element) -> List[Dict[str, str]]:
        """提取图片资源"""
        images = []
        for img in element.find_all('img'):
            try:
                # 获取图片URL
                url = img.get('data-src') or img.get('src')
                if not url:
                    continue
                    
                # 清理URL
                url = url.split('?')[0]  # 移除查询参数
                
                # 获取图片说明
                alt = self.clean_text(img.get('alt', ''))
                
                images.append({
                    "url": url,
                    "type": "image",
                    "description": alt,
                    "format": url.split('.')[-1].lower()
                })
            except Exception as e:
                logger.warning(f"提取图片信息失败: {str(e)}")
                continue
                
        return images
        
    def _extract_videos(self, element) -> List[Dict[str, str]]:
        """提取视频资源"""
        videos = []
        # 处理视频标签
        for video in element.find_all('video'):
            try:
                # 获取视频URL
                url = video.get('data-src') or video.get('src')
                if not url:
                    continue
                    
                # 获取视频封面
                poster = video.get('poster', '')
                
                videos.append({
                    "url": url,
                    "type": "video",
                    "poster": poster,
                    "format": url.split('.')[-1].lower()
                })
            except Exception as e:
                logger.warning(f"提取视频信息失败: {str(e)}")
                continue
                
        # 处理iframe中的视频
        for iframe in element.find_all('iframe'):
            try:
                src = iframe.get('data-src') or iframe.get('src')
                if src and ('v.qq.com' in src or 'youku.com' in src):
                    videos.append({
                        "url": src,
                        "type": "video_iframe",
                        "platform": "qq" if 'v.qq.com' in src else "youku",
                        "format": "iframe"
                    })
            except Exception as e:
                logger.warning(f"提取iframe视频信息失败: {str(e)}")
                continue
                
        return videos 