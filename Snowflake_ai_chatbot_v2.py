#!/usr/bin/env python3
"""
Advanced Snowflake Agentic AI Chatbot - COMPLETE VERSION
Features: Data Quality, Performance, Direct Answers
Enter key support enabled
"""

import streamlit as st
import google.generativeai as genai
import snowflake.connector
import json
import pandas as pd

# ========== CONFIGURATION ==========
GEMINI_KEY = ""
SF_USER = ""
SF_PASS = ""
SF_ACCOUNT = ""
SF_WAREHOUSE = ""
SF_DATABASE = ""
SF_SCHEMA = "PUBLIC"
# ===================================

# Streamlit Page Config
st.set_page_config(
    page_title="Snowflake AI Assistant",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .user-bubble {
        background-color: #10a37f;
        color: white;
        padding: 12px 16px;
        border-radius: 18px;
        max-width: 70%;
        word-wrap: break-word;
        font-size: 14px;
        margin-bottom: 10px;
    }
    
    .bot-bubble {
        background-color: #ececf1;
        color: #000;
        padding: 12px 16px;
        border-radius: 18px;
        max-width: 85%;
        word-wrap: break-word;
        font-size: 14px;
        margin-bottom: 10px;
    }
    
    .sql-box {
        background-color: #1e1e1e;
        color: #00ff00;
        padding: 15px;
        border-radius: 5px;
        font-family: monospace;
        font-size: 12px;
        margin: 10px 0;
        overflow-x: auto;
    }
    
    .quality-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #10a37f;
    }
    
    .metric-box {
        background-color: #ececf1;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "chat"

if "input_value" not in st.session_state:
    st.session_state.input_value = ""

if "last_df" not in st.session_state:
    st.session_state.last_df = None

# ========== DATABASE FUNCTIONS ==========

def connect_snowflake():
    """Connect to Snowflake"""
    try:
        conn = snowflake.connector.connect(
            user=st.session_state.get('sf_user', SF_USER),
            password=st.session_state.get('sf_pass', SF_PASS),
            account=st.session_state.get('sf_account', SF_ACCOUNT),
            warehouse=st.session_state.get('sf_warehouse', SF_WAREHOUSE),
            database=st.session_state.get('sf_database', SF_DATABASE),
            schema=st.session_state.get('sf_schema', SF_SCHEMA)
        )
        return conn
    except Exception as e:
        return None

def test_gemini_api(api_key):
    """Test Gemini API connectivity"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Test")
        return True
    except Exception as e:
        return False

def get_schema():
    """Get database schema"""
    try:
        conn = connect_snowflake()
        if not conn:
            return None
        
        cursor = conn.cursor()
        schema = st.session_state.get('sf_schema', SF_SCHEMA)
        query = f"SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{schema}' ORDER BY TABLE_NAME, ORDINAL_POSITION"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        schema_dict = {}
        for table, col, dtype in results:
            if table not in schema_dict:
                schema_dict[table] = []
            schema_dict[table].append({"column": col, "type": dtype})
        
        return schema_dict
    except Exception as e:
        return None

def execute_sql(query):
    """Execute SQL and return results"""
    try:
        conn = connect_snowflake()
        if not conn:
            return {"success": False, "error": "Cannot connect to Snowflake"}
        
        cursor = conn.cursor()
        cursor.execute(query)
        
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description] if cursor.description else []
            data = [dict(zip(cols, row)) for row in results]
            cursor.close()
            conn.close()
            return {
                "success": True,
                "type": "SELECT",
                "rows": len(data),
                "columns": cols,
                "data": data
            }
        else:
            rows = cursor.rowcount
            cursor.close()
            conn.close()
            return {
                "success": True,
                "type": "MODIFY",
                "rows_affected": rows
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

def generate_sql(user_query, schema):
    """Generate SQL - DIRECT AND CONCISE"""
    try:
        schema_str = json.dumps(schema, indent=2)
        
        prompt = f"""You are a SQL expert. Based on this schema:
{schema_str}

User Request: {user_query}

Generate ONLY the SQL query. Return ONLY the SQL code, nothing else. No explanations, no backticks, just the SQL."""
        
        api_key = st.session_state.get('gemini_key', GEMINI_KEY)
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        sql_query = response.text.strip()
        
        # Clean up formatting
        if sql_query.startswith("```"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        
        return sql_query
    except Exception as e:
        return None

# ========== DATA QUALITY FUNCTIONS ==========

def analyze_data_quality(table_name):
    """Analyze data quality of a table"""
    try:
        conn = connect_snowflake()
        if not conn:
            return None
        
        cursor = conn.cursor()
        schema = get_schema()
        columns = [col["column"] for col in schema.get(table_name, [])]
        
        quality_report = {}
        
        # Get total count
        total_query = f"SELECT COUNT(*) as total FROM {table_name}"
        cursor.execute(total_query)
        total_count = cursor.fetchone()[0]
        
        for col in columns[:10]:  # Limit to 10 columns
            # Null count
            null_query = f"SELECT COUNT(*) as null_count FROM {table_name} WHERE {col} IS NULL"
            cursor.execute(null_query)
            null_count = cursor.fetchone()[0]
            
            # Duplicate count
            dup_query = f"SELECT COUNT(*) - COUNT(DISTINCT {col}) as duplicates FROM {table_name}"
            cursor.execute(dup_query)
            dup_count = cursor.fetchone()[0]
            
            quality_report[col] = {
                "null_count": null_count,
                "null_percentage": round((null_count / total_count * 100), 2) if total_count > 0 else 0,
                "duplicate_count": dup_count,
                "completeness": round(((total_count - null_count) / total_count * 100), 2) if total_count > 0 else 0
            }
        
        cursor.close()
        conn.close()
        return {"total_rows": total_count, "columns": quality_report}
    except Exception as e:
        return None

def detect_anomalies(table_name, column_name):
    """Detect anomalies in numeric columns"""
    try:
        conn = connect_snowflake()
        if not conn:
            return None
        
        cursor = conn.cursor()
        
        # Get statistics
        stats_query = f"""
        SELECT 
            MIN({column_name}) as min_val,
            MAX({column_name}) as max_val,
            AVG({column_name}) as avg_val,
            STDDEV({column_name}) as stddev_val,
            COUNT(*) as total_count
        FROM {table_name}
        WHERE {column_name} IS NOT NULL
        """
        cursor.execute(stats_query)
        stats = cursor.fetchone()
        
        if not stats:
            return None
        
        min_val, max_val, avg_val, stddev_val, total = stats
        
        # Find anomalies
        anomaly_query = f"""
        SELECT COUNT(*) as anomaly_count
        FROM {table_name}
        WHERE {column_name} IS NOT NULL
        AND (
            {column_name} < {avg_val - 3 * stddev_val} OR
            {column_name} > {avg_val + 3 * stddev_val}
        )
        """
        cursor.execute(anomaly_query)
        anomaly_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return {
            "min": float(min_val) if min_val else None,
            "max": float(max_val) if max_val else None,
            "avg": round(float(avg_val), 2) if avg_val else None,
            "stddev": round(float(stddev_val), 2) if stddev_val else None,
            "anomalies": anomaly_count,
            "anomaly_percentage": round((anomaly_count / total * 100), 2) if total > 0 else 0
        }
    except Exception as e:
        return None

def recommend_clustering_keys(table_name):
    """Recommend clustering keys for a table"""
    try:
        conn = connect_snowflake()
        if not conn:
            return None
        
        cursor = conn.cursor()
        schema = get_schema()
        columns = [col["column"] for col in schema.get(table_name, [])][:10]
        
        recommendations = []
        
        # Get total rows once
        total_query = f"SELECT COUNT(*) as total FROM {table_name}"
        cursor.execute(total_query)
        total_count = cursor.fetchone()[0]
        
        for col in columns:
            distinct_query = f"SELECT COUNT(DISTINCT {col}) as distinct_count FROM {table_name}"
            cursor.execute(distinct_query)
            distinct = cursor.fetchone()[0]
            
            cardinality = (distinct / total_count * 100) if total_count > 0 else 0
            
            if 20 < cardinality < 95:
                recommendations.append({
                    "column": col,
                    "cardinality": round(cardinality, 2),
                    "reason": "Good cardinality for clustering"
                })
        
        cursor.close()
        conn.close()
        
        return sorted(recommendations, key=lambda x: x["cardinality"], reverse=True)[:3]
    except Exception as e:
        return None

# ========== SETUP PAGE ==========

def show_setup_page():
    """Show setup and configuration page"""
    st.title("⚙️ Setup & Configuration")
    
    with st.container():
        st.markdown("### 🔧 Configure Your Credentials")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**API Configuration**")
            gemini_key = st.text_input(
                "Gemini API Key",
                value=st.session_state.get('gemini_key', GEMINI_KEY),
                type="password",
                help="Get from https://ai.google.dev/"
            )
            if gemini_key:
                st.session_state.gemini_key = gemini_key
        
        with col2:
            st.markdown("**Snowflake Configuration**")
            sf_user = st.text_input("Snowflake User", value=st.session_state.get('sf_user', SF_USER))
            if sf_user:
                st.session_state.sf_user = sf_user
        
        col3, col4 = st.columns(2)
        with col3:
            sf_pass = st.text_input("Snowflake Password", value=st.session_state.get('sf_pass', SF_PASS), type="password")
            if sf_pass:
                st.session_state.sf_pass = sf_pass
        
        with col4:
            sf_account = st.text_input("Snowflake Account", value=st.session_state.get('sf_account', SF_ACCOUNT))
            if sf_account:
                st.session_state.sf_account = sf_account
        
        col5, col6 = st.columns(2)
        with col5:
            sf_warehouse = st.text_input("Warehouse", value=st.session_state.get('sf_warehouse', SF_WAREHOUSE))
            if sf_warehouse:
                st.session_state.sf_warehouse = sf_warehouse
        
        with col6:
            sf_database = st.text_input("Database", value=st.session_state.get('sf_database', SF_DATABASE))
            if sf_database:
                st.session_state.sf_database = sf_database
        
        col7, col8 = st.columns(2)
        with col7:
            sf_schema = st.text_input("Schema", value=st.session_state.get('sf_schema', SF_SCHEMA))
            if sf_schema:
                st.session_state.sf_schema = sf_schema
    
    st.markdown("---")
    
    # Test Connections
    st.markdown("### ✅ Test Connections")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧪 Test Gemini API", use_container_width=True):
            with st.spinner("Testing..."):
                api_key = st.session_state.get('gemini_key', GEMINI_KEY)
                if test_gemini_api(api_key):
                    st.success("✅ Gemini API Connected!")
                else:
                    st.error("❌ Gemini API Failed")
    
    with col2:
        if st.button("🧪 Test Snowflake", use_container_width=True):
            with st.spinner("Testing..."):
                conn = connect_snowflake()
                if conn:
                    st.success("✅ Snowflake Connected!")
                    conn.close()
                else:
                    st.error("❌ Snowflake Failed")
    
    with col3:
        if st.button("✅ Ready to Chat", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()

# ========== CHAT PAGE ==========

def show_chat_page():
    """Show main chat interface"""
    st.title("💬 Snowflake AI Assistant")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.page = "setup"
            st.rerun()
    
    with col2:
        if st.button("🔍 Data Quality", use_container_width=True):
            st.session_state.page = "quality"
            st.rerun()
    
    with col3:
        if st.button("⚡ Performance", use_container_width=True):
            st.session_state.page = "performance"
            st.rerun()
    
    st.markdown("---")
    
    # Chat display container
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-end; margin: 10px 0;'>
                    <div class='user-bubble'>{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-start; margin: 10px 0;'>
                    <div class='bot-bubble'>{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Input area with Enter key support
    col1, col2 = st.columns([10, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask anything about your data...",
            placeholder="e.g., Count distinct products or Get top 10 customers",
            label_visibility="collapsed",
            key="chat_input_unique"
        )
    
    with col2:
        send_btn = st.button("📤", use_container_width=True)
    
    # Process input only when button clicked or Enter pressed
    if send_btn and user_input:
        # Check if this is a new message
        if not st.session_state.messages or st.session_state.messages[-1]["role"] != "user" or st.session_state.messages[-1]["content"] != user_input:
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            schema = get_schema()
            
            with st.spinner("⏳ Generating SQL..."):
                # Generate SQL
                sql_query = generate_sql(user_input, schema)
                
                if not sql_query:
                    bot_message = "❌ Failed to generate SQL. Please try again."
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": bot_message
                    })
                    st.rerun()
                
                # Execute SQL
                with st.spinner("⏳ Executing query..."):
                    result = execute_sql(sql_query)
                
                # Format response
                if result.get("success"):
                    if result.get("data"):
                        df = pd.DataFrame(result["data"])
                        
                        # Show just the SQL code block directly in chat
                        bot_message = f"""```sql
{sql_query}
```"""
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": bot_message
                        })
                        
                        # Store the dataframe and SQL for display
                        st.session_state.last_df = df
                        st.session_state.last_sql = sql_query
                    else:
                        # Show SQL for non-SELECT queries
                        bot_message = f"""```sql
{sql_query}
```

✅ Query executed successfully! ({result.get('rows_affected', 0)} rows affected)"""
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": bot_message
                        })
                        st.session_state.last_sql = sql_query
                else:
                    bot_message = f"""```sql
{sql_query}
```

❌ Error: {result.get('error', 'Unknown error')}"""
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": bot_message
                    })
            
            st.rerun()
    
    # Display the last dataframe if it exists
    if "last_df" in st.session_state and st.session_state.last_df is not None:
        st.markdown("---")
        st.markdown("### 📊 Results:")
        st.dataframe(st.session_state.last_df, use_container_width=True)

# ========== DATA QUALITY PAGE ==========

def show_quality_page():
    """Show data quality analysis page"""
    st.title("🔍 Data Quality Analysis")
    
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("← Back"):
            st.session_state.page = "chat"
            st.rerun()
    
    st.markdown("---")
    
    schema = get_schema()
    if not schema:
        st.error("Cannot connect to database")
        return
    
    tabs = st.tabs(["Null Analysis", "Duplicate Detection", "Anomalies"])
    
    with tabs[0]:
        st.markdown("### 📊 Null Value Analysis")
        table_name = st.selectbox("Select Table", list(schema.keys()), key="null_table")
        
        if st.button("Analyze Nulls", use_container_width=True):
            with st.spinner("Analyzing..."):
                quality = analyze_data_quality(table_name)
                if quality:
                    st.markdown(f"**Total Rows:** {quality['total_rows']}")
                    st.markdown("---")
                    
                    for col, metrics in quality['columns'].items():
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Column", col)
                        with col2:
                            st.metric("Nulls", f"{metrics['null_count']}")
                        with col3:
                            st.metric("Null %", f"{metrics['null_percentage']}%")
                        with col4:
                            st.metric("Completeness", f"{metrics['completeness']}%")
                        
                        st.markdown("---")
    
    with tabs[1]:
        st.markdown("### 🔄 Duplicate Detection")
        table_name = st.selectbox("Select Table", list(schema.keys()), key="dup_table")
        
        if st.button("Analyze Duplicates", use_container_width=True):
            with st.spinner("Analyzing..."):
                quality = analyze_data_quality(table_name)
                if quality:
                    st.markdown(f"**Total Rows:** {quality['total_rows']}")
                    st.markdown("---")
                    
                    cols_with_dups = {col: metrics for col, metrics in quality['columns'].items() if metrics['duplicate_count'] > 0}
                    
                    if cols_with_dups:
                        for col, metrics in cols_with_dups.items():
                            st.markdown(f"""
                            <div class='quality-card'>
                                <h4>{col}</h4>
                                <p>Duplicates: <strong>{metrics['duplicate_count']}</strong></p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.success("✅ No duplicates found!")
    
    with tabs[2]:
        st.markdown("### 🎯 Anomaly Detection")
        table_name = st.selectbox("Select Table", list(schema.keys()), key="anom_table")
        
        if schema.get(table_name):
            numeric_cols = [col["column"] for col in schema[table_name] if "INT" in col["type"] or "FLOAT" in col["type"] or "NUMBER" in col["type"]]
            
            if numeric_cols:
                column_name = st.selectbox("Select Numeric Column", numeric_cols)
                
                if st.button("Detect Anomalies", use_container_width=True):
                    with st.spinner("Analyzing..."):
                        anomalies = detect_anomalies(table_name, column_name)
                        if anomalies:
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Min", anomalies['min'])
                            with col2:
                                st.metric("Max", anomalies['max'])
                            with col3:
                                st.metric("Avg", anomalies['avg'])
                            with col4:
                                st.metric("Anomalies", f"{anomalies['anomalies']} ({anomalies['anomaly_percentage']}%)")
            else:
                st.warning("No numeric columns found in this table")

# ========== PERFORMANCE PAGE ==========

def show_performance_page():
    """Show performance optimization page"""
    st.title("⚡ Performance Optimization")
    
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("← Back"):
            st.session_state.page = "chat"
            st.rerun()
    
    st.markdown("---")
    
    schema = get_schema()
    if not schema:
        st.error("Cannot connect to database")
        return
    
    st.markdown("### 📊 Clustering Key Recommendations")
    table_name = st.selectbox("Select Table", list(schema.keys()))
    
    if st.button("Get Recommendations", use_container_width=True):
        with st.spinner("Analyzing..."):
            clustering = recommend_clustering_keys(table_name)
            if clustering:
                for i, rec in enumerate(clustering, 1):
                    st.markdown(f"""
                    <div class='quality-card'>
                        <h4>Recommendation #{i}: {rec['column']}</h4>
                        <p>Cardinality: <strong>{rec['cardinality']}%</strong></p>
                        <p>Reason: {rec['reason']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No clustering key recommendations at this time")

# ========== MAIN APP ==========

def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        page = st.radio(
            "Select Page",
            ["Chat", "Data Quality", "Performance", "Setup"],
            key="nav_radio"
        )
        
        page_map = {
            "Chat": "chat",
            "Data Quality": "quality",
            "Performance": "performance",
            "Setup": "setup"
        }
        st.session_state.page = page_map.get(page, "chat")
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Show selected page
    if st.session_state.page == "setup":
        show_setup_page()
    elif st.session_state.page == "chat":
        show_chat_page()
    elif st.session_state.page == "quality":
        show_quality_page()
    elif st.session_state.page == "performance":
        show_performance_page()

if __name__ == "__main__":
    main()
