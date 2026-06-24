# Dify Lark Drive Datasource Plugin

从飞书云盘（Lark Drive）获取文档并导入 Dify 知识库流水线的数据源插件。

## 功能特性

- **浏览云盘文件**：连接飞书开放平台，浏览授权范围内的云盘文件夹和文件
- **多类型文件支持**：支持飞书原生文档（docx）、PDF、图片、电子表格等多种类型
- **自动类型处理**：根据文件类型自动选择最佳下载方式（原生文档导出、普通文件直链下载）
- **快捷方式兼容**：正确处理飞书云盘中的快捷方式文件，指向目标文件

## 前置条件

| 依赖项 | 版本要求 |
|--------|---------|
| Dify | >= 1.9.0 |
| Python | >= 3.12 |
| 飞书开放平台应用 | 需开通云盘相关权限 |

## 安装步骤

### 1. 克隆仓库并安装依赖

```bash
cd dify-lark-driver-datasource
pip install -r requirements.txt
```

### 2. 打包插件

```bash
dify plugin package . -o lark-drive.difypkg
```

### 3. 在 Dify 控制台安装插件

1. 登录 Dify 控制台
2. 进入 **插件** → **安装插件** → **本地文件**
3. 上传打包生成的 `lark-drive.difypkg` 文件
4. 等待安装完成

## 配置说明

### Provider 配置

安装完成后，进入插件的 **Provider 配置** 页面，填写以下信息：

| 配置项 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| **App ID** | text-input | 是 | 飞书开放平台应用的 App ID |
| **App Secret** | secret-input | 是 | 飞书开放平台应用的 App Secret |
| **Default Folder Token** | text-input | 否 | 默认浏览的文件夹 Token |

#### 获取 Folder Token

1. 打开飞书云盘网页版，进入目标文件夹
2. 查看浏览器地址栏，URL 格式类似：
   ```
   https://xxx.feishu.cn/drive/folder/fldcnxxxxx
   ```
3. 复制 `fldcn` 开头的部分（例如：`fldcnABC123xyz`）
4. 粘贴到 "Default Folder Token" 字段中

> **提示**：如果不设置 Default Folder Token，插件将访问云盘根目录。

## 使用流程

### 1. 飞书开放平台配置

#### 创建应用并获取凭证

1. 登录 [飞书开放平台](https://open.feishu.cn/app)
2. 创建企业自建应用
3. 在 **凭证与基础信息** 页面获取 **App ID** 和 **App Secret**

#### 配置应用权限

在 **权限管理** → **API 权限** 页面，添加以下权限：

| 权限 | 用途 |
|------|------|
| `drive:file:readonly` | 读取云盘文件列表 |
| `drive:file:download` | 下载云盘普通文件 |
| `drive:export:readonly` | 创建和查询导出任务 |
| `docx:document:readonly` | 读取飞书文档内容 |
| `docs:document.content:read` | 读取文档正文内容 |
| `docs:document.media:download` | 下载文档中的媒体资源 |
| `docs:document:export` | 导出文档为其他格式 |
| `space:document:retrieve` | 检索空间中的文档信息 |

> **注意**：以上权限均属于 **tenant** 级别权限，需要在 **权限管理** → **API 权限** 中搜索并添加。添加完成后，必须**重新发布应用版本**才能生效。

修改权限后，必须**重新发布应用版本**，新权限才能生效。

### 2. 共享文件夹给应用

**关键步骤**：飞书应用只能访问已共享给它的文件夹。

1. 在飞书云盘中，右键点击目标文件夹 → **分享**
2. 搜索你的应用名称，添加为协作者
3. 设置权限为 **"可查看"** 或更高

### 3. 在 Dify 知识库中使用

1. 进入 Dify **知识库** → 选择或创建知识库
2. 在知识库流水线中，添加 **Lark Drive** 数据源节点
3. 浏览并选择要导入的文件
4. 开始同步

## 支持的文件类型

| 文件类型 | 扩展名 | 处理方式 |
|---------|--------|---------|
| 飞书文档 | `.docx` | 导出为文本 |
| 电子表格 | `.sheet` | 导出为 CSV |
| 多维表格 | `.bitable` | 导出为 XLSX |
| 普通文件 | `.pdf`, `.jpg`, `.png` 等 | 直接下载原始文件 |

## 项目结构

```
.
├── datasources/
│   ├── lark_drive.py       # 数据源核心实现
│   └── lark_drive.yaml     # 数据源配置
├── provider/
│   ├── lark_drive.py       # Provider 实现
│   └── lark_drive.yaml     # Provider 配置
├── main.py                 # 插件入口
├── manifest.yaml           # 插件清单
├── requirements.txt        # Python 依赖
└── README.md               # 使用文档
```

## 插件规范

本插件遵循 Dify 插件开发规范：

- **类型**：`plugin`
- **Provider 类型**：`online_drive`
- **最低 Dify 版本**：`>= 1.9.0`
- **运行环境**：Python 3.12
- **内存限制**：512 MB

## 常见问题

### Q1: 配置后提示 "Failed to list files"

**原因**：应用可能没有访问该文件夹的权限。

**解决**：确保已在飞书云盘中将文件夹共享给应用，并重新发布了应用版本。

### Q2: 返回文件列表为空

**原因**：
- 文件夹确实为空
- 应用未被授权访问该文件夹
- `folder_token` 无效或已过期

**解决**：
- 确认 folder_token 正确
- 检查应用权限是否已发布
- 尝试访问根目录（不设置 Default Folder Token）

### Q3: 飞书原生文档下载失败

**原因**：飞书文档需要通过导出任务 API 下载，而非直接下载。

**解决**：本插件已自动处理飞书文档的导出逻辑。如果仍失败，请检查应用是否具备 `docx:document:readonly` 权限。

## 注意事项

- 当前版本仅支持浏览和下载用户有权限访问的文件
- 对于飞书原生文档（docx），插件会尝试导出文本内容
- 对于 PDF、图片等普通文件，会直接下载原始二进制内容
- 飞书应用需要单独申请 **导出权限** 才能使用导出任务 API

## 隐私政策

本插件仅收集与飞书开放平台交互所需的必要凭证（App ID、App Secret）和可选的文件夹标识符（Folder Token）。

- 凭证由 Dify 平台安全存储和管理，插件本身不持久化任何用户数据
- 文件内容直接从飞书云盘流式传输至 Dify，插件不做中间缓存
- 不会收集或上传任何用户个人信息

详见 [PRIVACY.md](./PRIVACY.md)。

## 支持与反馈

- **GitHub Issues**: 提交 bug 报告或功能建议
- **维护者**: jcodes

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| 0.0.1 | 2026-06-12 | 初始版本，支持浏览和下载飞书云盘文件 |
