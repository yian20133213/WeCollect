def fetch_articles(account_name):
    """获取公众号文章"""
    try:
        # 确保正确设置了请求头和cookies
        headers = {
            'User-Agent': 'Mozilla/5.0 ...',
            'Cookie': '你的cookie'
        }
        
        # 检查响应状态
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logger.error(f"请求失败: {response.status_code}")
            return []
            
        # 解析文章列表
        articles = parse_articles(response.text)
        if not articles:
            logger.info(f"未获取到 {account_name} 的新文章")
            
        return articles
            
    except Exception as e:
        logger.error(f"获取文章失败: {str(e)}")
        return [] 