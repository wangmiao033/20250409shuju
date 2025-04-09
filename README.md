# 公司利润数据统计网站

这是一个基于Flask的Web应用，用于展示和分析公司利润数据。

## 功能特点

- 月度利润趋势可视化
- 部门利润对比分析
- 响应式设计，支持移动端访问

## 安装步骤

1. 确保已安装Python 3.7或更高版本
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```
3. 将Excel数据文件 `【利润】2025年度公司净利润汇总表2024-12-10.xlsx` 放在项目根目录下

## 运行应用

```bash
python app.py
```

访问 http://localhost:5000 查看数据统计结果

## 项目结构

```
.
├── app.py              # 主应用文件
├── requirements.txt    # 项目依赖
├── templates/          # HTML模板
│   └── index.html     # 主页面模板
└── README.md          # 项目说明文档
``` 