# ❄️ Snowflake AI Assistant: Enterprise-Grade Agentic LLM SQL Intelligence System

An intelligent, production-ready data analytics and SQL generation platform powered by advanced AI and Snowflake integration

**[Live Demo](#demo) • [Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start)**

---

## 🌟 Overview

**Snowflake AI Assistant** is a cutting-edge conversational analytics system that transforms how you interact with data. Built on enterprise-grade agentic architecture, it combines multiple advanced techniques to deliver accurate, context-aware SQL queries and data insights from your Snowflake databases with unprecedented precision.

Perfect for:
- 📊 Data analysts needing instant SQL generation
- 🔍 Teams requiring data quality audits
- ⚡ Developers optimizing database performance
- 📈 Business users exploring data naturally

---

## 🎯 What Makes This Advanced?

Unlike basic SQL chatbots, our system implements enterprise-grade techniques used by leading data companies:

✅ **Multi-Stage Retrieval Pipeline** – Combines schema understanding, query optimization, and semantic search
✅ **Intelligent Query Optimization** – AI-powered SQL enhancement and complexity handling
✅ **Agentic Architecture** – Dynamic tool selection and execution
✅ **Real-time Execution** – Direct Snowflake integration with result formatting
✅ **Source Attribution** – Full transparency with generated SQL visibility
✅ **Data Quality Intelligence** – Automatic anomaly detection and validation

---

## ✨ Features

### 💬 **ChatGPT-Style Conversational Interface**
- Natural language data queries
- Multi-turn conversation memory
- Real-time response streaming
- Beautiful Streamlit UI with animations

### 🧠 **Advanced AI-Powered SQL Generation**
1. **Query Understanding**
   - 🎯 Intent recognition and classification
   - 📊 Semantic understanding of data requests
   - 💡 Complex query decomposition
   - 🔄 Multi-step query generation

2. **Schema Optimization**
   - 📐 Automatic schema detection
   - 🔍 Column-level metadata analysis
   - 🎯 Relationship mapping
   - 📊 Data type understanding

3. **SQL Enhancement**
   - ⚡ Query optimization suggestions
   - 📈 Performance recommendations
   - 🔗 Complex join handling
   - 🎪 CTE and window function support

4. **Intelligent Execution**
   - ✅ Query validation
   - 🚨 Error handling
   - 📊 Result formatting
   - 💾 Result caching

### 🔍 **Enterprise Data Quality Suite**

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Null Analysis** | Detect missing data patterns | Data completeness checks |
| **Duplicate Detection** | Identify duplicate records | Data deduplication |
| **Anomaly Detection** | Statistical outlier identification | Quality assurance |
| **Completeness Scoring** | Percentage-based quality metrics | KPI tracking |
| **Cardinality Analysis** | Distribution analysis | Performance optimization |

**Key Capabilities:**
- ✅ Column-level metrics
- ✅ Distribution analysis
- ✅ Statistical summaries
- ✅ Trend identification
- ✅ Pattern recognition

### ⚡ **Performance Optimization Intelligence**

Automatic recommendations for:

📊 **Clustering Keys**
- Cardinality analysis
- Performance impact estimation
- Implementation guidance

🎯 **Query Optimization**
- Execution plan analysis
- Bottleneck identification
- Rewrite suggestions

💾 **Storage Efficiency**
- Archive recommendations
- Data layout optimization
- Cost reduction strategies

### 🔐 **Enterprise Security & Governance**

- 🔑 Credential management
- 🛡️ Environment-based configuration
- 📝 Query audit logging
- ✅ Role-based access control
- 🚨 Error handling & recovery

---

## 🎨 **Advanced Features**

### 💬 **Intelligent Conversation Memory**
- Full chat history persistence
- Context-aware follow-ups
- Multi-turn understanding
- Session management

### 📊 **Real-time Analytics Dashboard**
- Query execution metrics
- Performance statistics
- Data quality scores
- Historical trends

### 🛠️ **Setup Wizard**
- Interactive configuration
- Connection testing
- Credential validation
- Status verification

---

## 🚀 **Demo**
<img width="1600" height="811" alt="image" src="https://github.com/user-attachments/assets/dfdb03b2-7d56-4dfc-9c33-817cf104c8cb" />


### Chat Interface
```
You: "What are the top 10 products by rating?"

Bot: [Generates SQL]
SELECT TOP 10 PRODUCT_NAME, AVG(RATING) as avg_rating
FROM AMAZON_SALES
GROUP BY PRODUCT_NAME
ORDER BY avg_rating DESC

[Displays results in formatted table]
```

### Data Quality Analysis
```
You: "Analyze data quality of AMAZON_SALES"

Bot: 
- Null Analysis: RATING has 2.5% nulls
- Duplicates: 0 duplicate records
- Anomalies: 5 outliers detected
- Completeness: 97.5%
```

### Performance Optimization
```
You: "Optimize this table"

Bot:
Recommendations:
1. PRODUCT_ID (45% cardinality) - Excellent clustering key
2. CATEGORY (12% cardinality) - Good secondary clustering
3. Consider archiving data older than 2 years
```

---

## 🏗️ **Architecture**

### 🔁 **Agentic RAG Pipeline Overview**
<img width="595" height="635" alt="image" src="https://github.com/user-attachments/assets/4b5b3f54-a77e-4366-9be6-a6fdd27dc3d7" />


### 🧠 **Why This Architecture?**

✔️ **High Precision** – Multi-stage filtering ensures accurate results
✔️ **Agentic Control** – Dynamic tool selection for optimal execution
✔️ **Enterprise Scalability** – Handles complex multi-table queries
✔️ **Transparent Operations** – Full SQL and reasoning visibility
✔️ **Modular & Extensible** – Easy to add new capabilities
✔️ **Real-time Feedback** – Immediate execution and validation

---

## 📦 **Installation**

### Prerequisites
- Python 3.12+
- Snowflake account with data
- Google API Key ([Get one here](https://ai.google.dev/))
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/snowflake-ai-assistant.git
cd snowflake-ai-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GEMINI_KEY=your_api_key_here
SF_USER=your_username
SF_PASS=your_password
SF_ACCOUNT=your_account_id
SF_WAREHOUSE=COMPUTE_WH
SF_DATABASE=your_database
SF_SCHEMA=PUBLIC
EOF

# Run application
streamlit run snowflake_ai_complete_final.py
```



---

## 🛠️ **Usage Guide**

### 1️⃣ **Chat Interface**

```bash
Question: "Show me top 5 products by sales"

System:
1. Understands intent (ranking/filtering)
2. Generates optimized SQL
3. Executes on Snowflake
4. Formats results
5. Returns with citations
```

### 2️⃣ **Data Quality Analysis**

**Steps:**
1. Go to **🔍 Data Quality** tab
2. Select table
3. Choose analysis type:
   - **Null Analysis** → Missing data detection
   - **Duplicate Detection** → Record deduplication
   - **Anomaly Detection** → Statistical outliers

### 3️⃣ **Performance Optimization**

**Steps:**
1. Go to **⚡ Performance** tab
2. Select table
3. Get recommendations:
   - Clustering keys
   - Cardinality analysis
   - Optimization tips

### 4️⃣ **Setup & Configuration**

**Steps:**
1. Go to **⚙️ Settings** tab
2. Enter credentials:
   - Gemini API Key
   - Snowflake credentials
   - Database details
3. Click "Test Both" to verify

---

## 📊 **Example Queries**

### Data Exploration
```sql
"What products have the most reviews?"
"Show me sales by category"
"Find products with rating > 4.5"
```

### Advanced Analytics
```sql
"Calculate month-over-month growth"
"Find the best performing category"
"Show customer purchase patterns"
```

### Data Quality
```sql
"Check data quality of PRODUCTS table"
"Find null values in ORDERS"
"Detect anomalies in PRICING"
```

### Performance
```sql
"Recommend clustering keys for AMAZON_SALES"
"Analyze query execution plans"
"Suggest performance optimizations"
```

---

## 🔧 **Technology Stack**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit 1.39.0 | Web UI & interactions |
| **LLM** | Google Gemini 2.5 Flash | Query generation & reasoning |
| **Database** | Snowflake | Data storage & execution |
| **Backend** | Python 3.12 | Application logic |
| **Embeddings** | Sentence Transformers | Not used in this version |
| **Vector DB** | Not required | Direct SQL approach |

---

## 🏆 **Key Advantages**

### vs. Basic SQL Chatbots
✅ Intelligent query optimization
✅ Automatic schema understanding
✅ Real-time execution
✅ Data quality insights
✅ Performance recommendations
✅ Production-ready error handling

### vs. Manual SQL Writing
✅ 10x faster queries
✅ No SQL expertise needed
✅ Automatic best practices
✅ Real-time validation
✅ Natural language interface
✅ Built-in safety checks


