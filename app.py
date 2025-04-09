from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json
from datetime import datetime
import os

app = Flask(__name__)

def load_data():
    try:
        # 使用相对路径加载Excel文件
        excel_path = os.path.join(os.path.dirname(__file__), '【利润】2025年度公司净利润汇总表2024-12-10.xlsx')
        df = pd.read_excel(excel_path)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def calculate_metrics(df):
    # 计算月度环比增长率
    monthly_profit = df.groupby('月份')['净利润'].sum().reset_index()
    monthly_profit['环比增长率'] = monthly_profit['净利润'].pct_change() * 100
    
    # 计算部门占比
    department_profit = df.groupby('部门')['净利润'].sum().reset_index()
    total_profit = department_profit['净利润'].sum()
    department_profit['占比'] = (department_profit['净利润'] / total_profit * 100).round(2)
    
    return monthly_profit, department_profit

@app.route('/')
def index():
    df = load_data()
    if df is None:
        return "无法加载数据文件"
    
    monthly_profit, department_profit = calculate_metrics(df)
    
    # 1. 月度利润趋势图
    fig_monthly = px.line(
        monthly_profit, 
        x='月份', 
        y='净利润',
        title='月度利润趋势分析',
        labels={
            '月份': '月份',
            '净利润': '净利润（万元）'
        },
        template='plotly_white'
    )
    
    # 添加平均线
    avg_profit = monthly_profit['净利润'].mean()
    fig_monthly.add_hline(
        y=avg_profit,
        line_dash="dash",
        line_color="red",
        annotation_text=f"平均利润: {avg_profit:.2f}万元",
        annotation_position="bottom right"
    )
    
    # 优化图表样式
    fig_monthly.update_layout(
        xaxis_title="月份",
        yaxis_title="净利润（万元）",
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="black"
        )
    )
    
    # 2. 环比增长率图
    fig_growth = px.bar(
        monthly_profit,
        x='月份',
        y='环比增长率',
        title='月度环比增长率',
        labels={
            '环比增长率': '环比增长率（%）'
        },
        template='plotly_white'
    )
    
    # 3. 部门利润对比图
    fig_department = px.bar(
        department_profit,
        x='部门',
        y='净利润',
        title='部门利润对比',
        labels={
            '净利润': '净利润（万元）'
        },
        template='plotly_white'
    )
    
    # 4. 部门利润占比饼图
    fig_pie = px.pie(
        department_profit,
        values='净利润',
        names='部门',
        title='部门利润占比',
        template='plotly_white'
    )
    
    # 5. 月度利润热力图
    monthly_matrix = df.pivot_table(
        values='净利润',
        index='部门',
        columns='月份',
        aggfunc='sum'
    )
    fig_heatmap = px.imshow(
        monthly_matrix,
        title='月度-部门利润热力图',
        labels=dict(x="月份", y="部门", color="净利润"),
        template='plotly_white'
    )
    
    # 转换为JSON
    graphs = {
        'monthly': json.dumps(fig_monthly, cls=plotly.utils.PlotlyJSONEncoder),
        'growth': json.dumps(fig_growth, cls=plotly.utils.PlotlyJSONEncoder),
        'department': json.dumps(fig_department, cls=plotly.utils.PlotlyJSONEncoder),
        'pie': json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder),
        'heatmap': json.dumps(fig_heatmap, cls=plotly.utils.PlotlyJSONEncoder)
    }
    
    # 计算关键指标
    total_profit = monthly_profit['净利润'].sum()
    avg_monthly_profit = monthly_profit['净利润'].mean()
    max_month = monthly_profit.loc[monthly_profit['净利润'].idxmax(), '月份']
    min_month = monthly_profit.loc[monthly_profit['净利润'].idxmin(), '月份']
    
    metrics = {
        'total_profit': f"{total_profit:.2f}",
        'avg_monthly_profit': f"{avg_monthly_profit:.2f}",
        'max_month': max_month,
        'min_month': min_month
    }
    
    return render_template('index.html',
                         graphs=graphs,
                         metrics=metrics)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 