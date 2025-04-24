import streamlit as st
import requests

st.set_page_config(page_title="Pathfinder", layout="centered")

st.title("🎓 Pathfinder: College Recommendation")

name = st.text_input("Your Name")
query = st.text_input("What kind of college are you looking for?")
submit = st.button("Search")

if submit and query:
    with st.spinner("Searching..."):
        response = requests.get("http://localhost:8000/search", params={"query": query})
        data = response.json()
        st.write("**Keywords Extracted:**", ", ".join(data["keywords"]))

        if data["results"]:
            for college in data["results"]:
                st.subheader(college["school.name"])
                st.write(f"📍 {college['school.city']}, {college['school.state']}")
                st.write(f"🎓 Size: {college.get('school.size', 'N/A')}")
                st.write(f"💸 Tuition (in-state): ${college.get('school.tuition.in_state', 'N/A')}")
        else:
            st.warning("No matches found. Try another query.")
