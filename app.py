"""
app.py - Main Streamlit web application for the Automated Resume Parser.
Provides a simple user interface to upload resumes, extract candidate information,
save it to an SQLite database, and search or view stored records.
"""

import streamlit as st
from database import init_db, insert_candidate, get_all_candidates, search_candidates
from parser import parse_resume

# Ensure the database and table are initialized on app startup
init_db()

# Page configuration
st.set_page_config(
    page_title="Automated Resume Parser",
    page_icon="📄",
    layout="wide"
)

# Application Header
st.title("📄 Automated Resume Parser")
st.markdown(
    "A beginner-friendly application to extract candidate information from PDF resumes, "
    "store the details in an SQLite database, and search saved candidates."
)
st.write("---")

# Navigation tabs for Upload and Directory
tab1, tab2 = st.tabs(["📤 Upload & Parse Resume", "📋 View & Search Candidates"])

# -------------------------------------------------------------
# TAB 1: Upload, Extract, and Save Candidate Details
# -------------------------------------------------------------
with tab1:
    st.subheader("Upload Candidate Resume")
    uploaded_file = st.file_uploader("Select a resume in PDF format", type=["pdf"])

    if uploaded_file is not None:
        st.info(f"File selected: **{uploaded_file.name}**")

        # Extraction button
        if st.button("🔍 Extract Details", type="primary"):
            with st.spinner("Extracting candidate details from PDF..."):
                try:
                    data = parse_resume(uploaded_file)
                    st.session_state["extracted_data"] = data
                except Exception as e:
                    st.error(f"Error parsing resume: {e}")

        # Display extracted details when available
        if "extracted_data" in st.session_state:
            data = st.session_state["extracted_data"]

            st.write("### 📝 Extracted Details")
            st.caption("You can review and edit any field before saving to the database.")

            # Form allows review and editing of extracted values
            with st.form("candidate_form"):
                col1, col2 = st.columns(2)

                with col1:
                    name = st.text_input("Full Name", value=data.get("name", ""))
                    email = st.text_input("Email Address", value=data.get("email", ""))
                    phone = st.text_input("Phone Number", value=data.get("phone", ""))

                with col2:
                    education = st.text_input("Education", value=data.get("education", ""))
                    skills = st.text_area("Skills", value=data.get("skills", ""), height=108)

                save_button = st.form_submit_button("💾 Save Candidate to Database")

                if save_button:
                    if not name.strip() or name.strip() == "Not Found":
                        st.warning("Please provide a valid candidate name before saving.")
                    else:
                        try:
                            insert_candidate(
                                name=name.strip(),
                                email=email.strip(),
                                phone=phone.strip(),
                                skills=skills.strip(),
                                education=education.strip()
                            )
                            st.success(f"Candidate **{name.strip()}** saved successfully!")
                            # Clear current extracted data after saving
                            del st.session_state["extracted_data"]
                        except Exception as err:
                            st.error(f"Failed to save candidate: {err}")

# -------------------------------------------------------------
# TAB 2: View and Search Candidates
# -------------------------------------------------------------
with tab2:
    st.subheader("Saved Candidates Directory")

    # Search input box
    search_query = st.text_input(
        "🔍 Search candidates by Name or Skill:",
        placeholder="Type a name or skill (e.g. Python, Rohan)..."
    )

    # Query the database depending on search input
    if search_query.strip():
        candidates = search_candidates(search_query.strip())
        st.write(f"Search results for **'{search_query.strip()}'** ({len(candidates)} found):")
    else:
        candidates = get_all_candidates()
        st.write(f"Total candidates in database: **{len(candidates)}**")

    # Render table if records exist
    if candidates:
        table_data = []
        for row in candidates:
            table_data.append({
                "ID": row[0],
                "Name": row[1],
                "Email": row[2],
                "Phone": row[3],
                "Skills": row[4],
                "Education": row[5]
            })

        st.dataframe(table_data, use_container_width=True)
    else:
        st.warning("No candidate records found.")
