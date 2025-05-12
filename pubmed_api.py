import streamlit as st
from Bio import Entrez

# 设置 Entrez API 的邮箱地址
Entrez.email = "18027766686@163.com"


def fetch_pubmed_details(title):
    """
    根据文章标题从 PubMed 获取第一作者、发布日期和期刊名称。

    参数:
        title (str): 文章标题

    返回:
        dict: 包含第一作者、发布日期和期刊名称的信息
    """
    try:
        # 使用 esearch 搜索文章的 PubMed ID (PMID)
        handle = Entrez.esearch(db="pubmed", term=title, retmax=1)
        record = Entrez.read(handle)
        handle.close()

        # 检查是否找到结果
        if not record["IdList"]:
            return {"Error": "未找到匹配的文章，请检查标题是否正确。"}

        # 获取搜索结果中的第一个 PMID
        pmid = record["IdList"][0]

        # 使用 efetch 获取文章详细信息
        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml", retmode="text")
        records = Entrez.read(handle)
        handle.close()

        # 提取所需的信息
        article = records["PubmedArticle"][0]["MedlineCitation"]
        first_author = article["Article"]["AuthorList"][0]["LastName"] + " " + article["Article"]["AuthorList"][0][
            "ForeName"]
        journal = article["Article"]["Journal"]["Title"]
        pub_date = article["Article"]["Journal"]["JournalIssue"]["PubDate"]

        # 格式化日期
        pub_date_formatted = f"{pub_date.get('Year', '未知')} {pub_date.get('Month', '未知')} {pub_date.get('Day', '')}".strip()

        return {
            "First Author": first_author,
            "Publication Date": pub_date_formatted,
            "Journal": journal
        }
    except Exception as e:
        return {"Error": f"发生错误: {e}"}


# Streamlit Web 界面
st.title("PubMed 文章信息查询工具")

# 输入文章标题
article_title = st.text_input("请输入文章标题：", "")

if st.button("搜索"):
    if article_title.strip() == "":
        st.warning("请输入有效的文章标题！")
    else:
        # 查询文章信息
        with st.spinner("正在查询，请稍候..."):
            result = fetch_pubmed_details(article_title)

        # 显示查询结果
        if "Error" in result:
            st.error(result["Error"])
        else:
            st.success("查询成功！以下是文章的详细信息：")
            st.write(f"**第一作者**: {result['First Author']}")
            st.write(f"**发布日期**: {result['Publication Date']}")
            st.write(f"**期刊名称**: {result['Journal']}")
            com = result['Journal'] + '. ' + result['Publication Date'] + '. ' + result['First Author']
            st.write(f"**综合信息**: {com}")
