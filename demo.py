import streamlit as st
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session



# サイドバーを常に表示
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Snowflakeへの接続
session = Session.builder.config("connection_name", "default").create()

def get_data(option):
    if option == 'None':
        return snowpark.DataFrame()
    elif option in ['Grants']:
        query = f"SHOW {option} ON ACCOUNT"
    else:
        query = f"SHOW {option} IN ACCOUNT"
        
    return session.sql(query)


# サイドバーのスタイル設定
st.sidebar.markdown(
    f"""
    <style>
    [data-testid=stSidebar] {{
        background-color: #ADCDEC;
    }}
    .sidebar-footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: black;
        text-align: left;
        padding: 5px;
        font-size: 14px;
    }}
    </style>
    <div class="sidebar-footer">
    <p>App created using Snowpark version: {snowpark.__version__}</p>
    <p>App created using Streamlit version: {st.__version__}</p>
    </div>
    """,
    unsafe_allow_html=True
    )


# サイドバーのコンテンツ
with st.sidebar:
    st.image("https://frostyfriday.org/wp-content/uploads/2022/11/ff_logo_trans.png")
    options = [
        'None',
        'Shares',
        'Roles',
        'Grants',
        'Users',
        'Warehouses',
        'Databases',
        'Schemas',
        'Tables',
        'Views'
    ]
    selected_option = st.selectbox('Select what account info you would like to see', options)

# タイトルと説明文
st.title('Snowflake Account Info App')
st.write('Use this app to quickly see high-level info about your Snowflake account.')

if selected_option != 'None':
    data = get_data(selected_option)
    st.dataframe(data)
else:
    st.write("Please select an option to view data.")

