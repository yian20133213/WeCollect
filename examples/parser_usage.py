from core.parser.article_parser import ArticleParser
from core.parser.content_cleaner import ContentCleaner

async def parse_article(html: str):
    # 创建解析器
    parser = ArticleParser()
    
    # 解析文章
    result = parser.parse(html)
    
    # 提取元数据
    meta = result["meta"]
    print(f"标题: {meta['title']}")
    print(f"作者: {meta['author']}")
    print(f"发布时间: {meta['publish_time']}")
    
    # 提取内容
    content = result["content"]
    print(f"文章长度: {len(content['text'])}")
    
    # 提取媒体资源
    media = result["media"]
    print(f"图片数量: {len(media['images'])}")
    print(f"视频数量: {len(media['videos'])}")
    
    # 清理内容
    cleaner = ContentCleaner()
    clean_html = cleaner.clean_html(content['html'])
    clean_text = cleaner.clean_text(content['text'])
    
    return {
        "meta": meta,
        "content": {
            "text": clean_text,
            "html": clean_html
        },
        "media": media
    } 