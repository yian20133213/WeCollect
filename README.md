# 微信公众号文章采集 WeCollect

## 项目简介
本工具是一款本地运行的微信公众号文章采集工具，用于批量导出指定公众号的历史文章内容及媒体资源，支持多种格式导出，旨在满足用户对公众号内容的管理需求。

## 功能特点
- **公众号搜索**：支持通过输入公众号名称搜索目标公众号。
- **文章筛选**：支持按时间范围筛选文章。
- **批量导出**：支持批量导出文章内容及媒体资源。
- **多种格式**：支持导出为 HTML、PDF、Markdown 等格式。
- **操作便捷**：提供用户友好的操作界面。

## 系统要求
- **开发语言**：Python 3.8+
- **依赖软件**：Chrome 浏览器
- **硬件配置**：
  - CPU：双核以上
  - 内存：4GB 以上
  - 磁盘空间：10GB 以上
  - 网络带宽：2Mbps 以上

## 环境配置
1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **安装 Chrome 浏览器**：
   下载并安装最新版的 Chrome 浏览器。

3. **配置环境变量**：
   确保 ChromeDriver 在系统 PATH 中。

## 使用说明
1. 启动工具：
   ```bash
   python main.py
   ```

2. 登录微信公众号：
   - 扫码登录后，保持登录状态。

3. 搜索目标公众号：
   - 输入公众号名称，选择目标公众号。

4. 设置筛选条件：
   - 按时间范围筛选需要的文章。

5. 开始采集：
   - 点击采集按钮，工具将自动抓取文章内容及媒体资源。

6. 导出数据：
   - 选择需要的导出格式（HTML、PDF、Markdown），完成导出。

## 系统架构
- **界面层**：用户交互
- **控制层**：业务流程控制
- **采集层**：数据采集
- **解析层**：内容提取
- **存储层**：数据持久化
- **导出层**：格式转换输出

## 数据存储
- **数据库结构**：
  ```sql
  CREATE TABLE articles (
      id INTEGER PRIMARY KEY,
      title TEXT,
      author TEXT,
      publish_time DATETIME,
      url TEXT,
      status INTEGER,
      create_time DATETIME
  );

  CREATE TABLE media (
      id INTEGER PRIMARY KEY,
      article_id INTEGER,
      type TEXT,
      url TEXT,
      local_path TEXT,
      status INTEGER
  );
  ```

- **文件系统结构**：
  ```plaintext
  data/
  ├── articles/          # 文章内容
  ├── images/            # 图片资源
  ├── videos/            # 视频资源
  └── exports/           # 导出文件
  ```

## 异常处理
- **网络异常**：自动重试、断点续传、超时控制。
- **反爬处理**：请求频率控制、User-Agent 轮换、验证码处理。

## 注意事项
- 本工具仅供学习与研究使用，请勿用于任何违规用途。
- 确保账号安全，避免账号因频繁操作被封禁。

## 项目风险
1. **技术风险**
   - 微信反爬策略升级
   - 登录态失效
   - 内容解析失败
2. **安全风险**
   - 账号被封禁
   - 数据泄露
   - 违规使用

## 许可证
本项目遵循 [MIT 许可证](LICENSE)。
