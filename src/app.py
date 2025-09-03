import streamlit as st

from analysis.qa_engine import QuestionAnswerer

def main():
    st.set_page_config(page_title="Book Q&A Engine", layout="centered")

    st.title("📚 Book Q&A Engine")
    st.write("Ask predefined questions about the dataset scraped from Books to Scrape.")

    # Initialize engine
    qa = QuestionAnswerer()
    df = qa.get_dataframe()

    # Dropdown for questions
    questions = qa.get_questions()
    q_map = {q["description"]: q["id"] for q in questions}

    options = ["Tap to select a question..."] + list(q_map.keys())
    selected_desc = st.selectbox("Select a question:", options)

    if selected_desc and selected_desc != "Tap to select a question...":
        qid = q_map[selected_desc]
        result = qa.answer_question(qid)

        st.subheader("Answer")
        st.success(result["answer"])

        st.subheader("Justification")
        st.info(result["justification"])
    else:
        st.info("👆 Select a question from the dropdown above to see the answer and analysis.")
    
    # Bonus: Ad-hoc query feature (search for a book by title)
    st.write("---")
    st.subheader("🔍 Bonus: Quick Data Lookup")
    query = st.text_input("Search for books by title:")

    if query:
        df = qa.df  # access raw dataframe
        matches = df[df["title"].str.contains(query, case=False, na=False)]
        if matches.empty:
            st.warning("No books found.")
        else:
            st.write(matches[["title", "category", "price", "availability", "stock_count"]].head(10))

    st.write("---")
    st.subheader("Filter Books by category")
    # Create bubbles/buttons for each category
    cols = st.columns(4)
    categories = ["travel", "mystery", "historical-fiction", "classics"]

    selected_category = None
    for i, category in enumerate(categories):
        col_idx = i % 4  # Distribute across columns
        with cols[col_idx]:
            if st.button(f"📖 {category}", key=f"cat_{category}"):
                selected_category = category
    
    # Display books for selected category
    if selected_category:
        st.write(f"### Books in '{selected_category}' category")
        category_books = df[df['category'] == selected_category]
        
        if category_books.empty:
            st.warning(f"No books found in the '{selected_category}' category.")
        else:
            st.write(f"Found {len(category_books)} book(s) in this category:")
            st.dataframe(
                category_books[["title", "category", "price", "availability", "stock_count"]],
                height=400,
                use_container_width=True
            )
            
            # Show some quick stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Price", f"£{category_books['price'].mean():.2f}")
            with col2:
                in_stock = category_books[category_books['availability'] == 'In stock']
                st.metric("Books In Stock", len(in_stock))
            with col3:
                st.metric("Total Stock Count", category_books['stock_count'].sum())
    
if __name__ == "__main__":
    main()