import streamlit as st
import requests

st.set_page_config(page_title="Indian Criminal Law Assistant", layout="wide")
st.title("⚖️ Indian Criminal Law Research Assistant")

query = st.text_area("Enter your legal query:", height=150)

if st.button("Analyze", type="primary"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Researching..."):
            try:
                response = requests.post(
                    "http://localhost:8000/query",
                    json={"text": query},
                    timeout=60
                )
                if response.status_code == 200:
                    data = response.json()
                    st.markdown("### Answer")
                    st.markdown(data["answer"])
                    with st.expander("View Sources"):
                        for src in data["sources"]:
                            st.markdown(f"**Source**: {src['metadata']}")
                            st.markdown(f"**Excerpt**: {src['document'][:500]}...")
                            st.markdown("---")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
