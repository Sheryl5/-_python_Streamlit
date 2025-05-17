import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 读取数据
def load_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.randint(1000, 5000, len(dates)),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], len(dates)),
        'Product': np.random.choice(['A', 'B', 'C', 'D'], len(dates)),
        'CustomerRating': np.random.uniform(3.0, 5.0, len(dates))
    })
    return data

df = load_data()

# 设置页面标题
st.set_page_config(page_title="dashboard", layout="wide", initial_sidebar_state="expanded")

# 页面标题
st.title("数据可视化看板")

# 侧边栏
st.sidebar.header("数据筛选")


with st.sidebar:
    st.header("配置选项")
    
    selected_regions = st.sidebar.multiselect(
        "选择地区",
        options=df['Region'].unique(),
        default=df['Region'].unique()
        )

    # 原代码可能由于使用 st.sidebar.date_input 存在问题，改为使用 st.date_input 并放置在侧边栏的上下文内
    date_range = st.date_input(
        "日期范围",
        value=[df['Date'].min(), df['Date'].max()]
        )

# 数据过滤
filtered_df = df[
    (df['Region'].isin(selected_regions)) &
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1]))
]

# 主内容区
st.header("数据概览")

# 核心指标展示
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("总销售额", f"¥{filtered_df['Sales'].sum():,.0f}")
with col2:
    st.metric("平均评分", f"{filtered_df['CustomerRating'].mean():.1f} ★")
with col3:
    st.metric("交易次数", len(filtered_df))

# 可视化图表
tab1, tab2, tab3, tab4 = st.tabs(["趋势分析", "区域对比", "产品分布", "原始数据"])

with tab1:
    # 折线图：每日销售趋势
    fig1 = px.line(
        filtered_df.groupby('Date')['Sales'].sum().reset_index(),
        x='Date', 
        y='Sales',
        title="每日销售趋势"
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    # 柱状图：区域销售对比
    col1, col2 = st.columns([3, 1])
    with col1:
        fig2 = px.bar(
            filtered_df.groupby('Region')['Sales'].sum().reset_index(),
            x='Region', 
            y='Sales',
            color='Region',
            title="区域销售对比"
        )
        st.plotly_chart(fig2, use_container_width=True)
    with col2:
        st.dataframe(
            filtered_df.groupby('Region')['Sales'].sum().reset_index(),
            hide_index=True
        )

with tab3:
    # 饼图+散点图组合
    col1, col2 = st.columns(2)
    with col1:
        fig3 = px.pie(
            filtered_df,
            names='Product', 
            values='Sales',
            title="产品销售额占比"
        )
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        fig4 = px.scatter(
            filtered_df,
            x='CustomerRating',
            y='Sales',
            color='Product',
            size='Sales',
            title="评分与销售额关系"
        )
        st.plotly_chart(fig4, use_container_width=True)

with tab4:
    # 原始数据展示
    st.dataframe(
        filtered_df.sort_values(by='Date', ascending=False),
        column_config={
            "Date": st.column_config.DateColumn("日期", format="YYYY-MM-DD"),
            "Sales": st.column_config.NumberColumn("销售额", format="¥%d")
        },
        hide_index=True,
        use_container_width=True
    )

