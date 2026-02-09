# PDF 转 Markdown 转换器

使用 `pymupdf4llm` 将 PDF 文档转换为 Markdown 格式。适用于将 PDF 内容提供给 LLM (大语言模型) 使用。

## 目录结构

```
docs/pdf2md/
├── convert.py        # 主脚本
├── urls.example.txt  # 示例 URL 列表 (复制为 urls.txt)
├── urls.txt          # 你的 PDF URL 列表 (git 忽略)
├── .cache.json       # 下载/转换缓存 (git 忽略)
├── input/            # 下载/本地的 PDF (git 忽略)
└── output/           # 转换后的 Markdown 文件 (git 忽略)
```

## 安装

```bash
pip install pymupdf4llm
```

## 快速开始

```bash
cd docs/pdf2md
cp urls.example.txt urls.txt
# 编辑 urls.txt 填入你的 PDF URL
python convert.py --urls
```

## 使用方法

### 转换本地 PDF

```bash
# 转换 input/ 文件夹下的所有 PDF
python convert.py

# 转换指定文件
python convert.py input/document.pdf
```

### 从 URL 下载并转换

```bash
# 单个 URL
python convert.py --url https://example.com/document.pdf

# 从 urls.txt 批量处理
python convert.py --urls
```

### 强制重新下载/转换

```bash
# 跳过缓存，强制重新下载和转换所有内容
python convert.py --urls --force
```

## 缓存机制

脚本会进行如下缓存：
- **下载**：如果 URL 已下载过则跳过
- **转换**：如果输入 PDF 未变更 (MD5 校验) 则跳过

缓存存储在 `.cache.json` 中。使用 `--force` 参数可绕过缓存。

## 输出

转换后的 Markdown 文件将保存到 `output/` 目录，文件名与源 PDF 相同。
