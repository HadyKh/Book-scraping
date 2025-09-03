import streamlit as st

from analysis.qa_engine import QuestionAnswerer

def main():
    st.set_page_config(page_title="Book Q&A Engine", layout="centered")

    st.title("📚 Book Q&A Engine")
    st.write("Ask predefined questions about the dataset scraped from Books to Scrape.")

    # Initialize engine
    qa = QuestionAnswerer()

    # Dropdown for questions
    questions = qa.get_questions()
    q_map = {q["description"]: q["id"] for q in questions}

    selected_desc = st.selectbox("Select a question:", list(q_map.keys()))

    if selected_desc:
        qid = q_map[selected_desc]
        result = qa.answer_question(qid)

        st.subheader("Answer")
        st.success(result["answer"])

        st.subheader("Justification")
        st.info(result["justification"])
    
if __name__ == "__main__":
    main()