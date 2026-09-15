# gui/app.py
# Streamlit GUI for the Syllabus Parser

import streamlit as st
import pandas as pd
import tempfile
import os
import sys

# Add the project root before importing local packages.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser import parse_pdf
from src.excel_writer import write_to_excel


# Page configuration
st.set_page_config(
    page_title="Syllabus SLO Parser",
    page_icon="s",
    layout="wide"
)

# Title
st.title("Syllabus SLO Parser")
st.markdown("Extract Student Learning Outcomes from syllabus PDFs")

# Sidebar - Instructions
with st.sidebar:
    st.header("Instructions")
    st.markdown("""
    1. Upload a PDF syllabus
    2. Review extracted SLOs
    3. Export to Excel
    
    **Supported fields:**
    - Course name + number
    - Semester
    - Instructor
    - SLO # (Number)
    - CorSLO
    - PSLO
    - CSLO
    - GenEd Outcome
    """)
    
    st.header("Example")
    st.info("Try uploading the CSCI 1301 syllabus provided as an example.")

# Main content area
uploaded_file = st.file_uploader(
    "Choose a PDF syllabus", 
    type=['pdf'],
    help="Upload a syllabus PDF to extract SLOs"
)

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        temp_path = tmp_file.name
    
    try:
        # Parse the syllabus
        with st.spinner("Parsing syllabus..."):
            extracted_data = parse_pdf(temp_path)
        
        if extracted_data:
            # Display extracted data
            st.success(f"Extracted {len(extracted_data)} SLOs")
            
            # Show preview
            st.subheader("Preview Extracted Data")
            df = pd.DataFrame(extracted_data)
            
            # Use columns for better layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.dataframe(
                    df,
                    use_container_width=True,
                    height=400
                )
            
            with col2:
                st.metric("Total SLOs", len(extracted_data))
                
                # Show missing fields
                missing_fields = []
                for col in ['Corslo', 'PSLO', 'CSLO', 'GenEd Outcome']:
                    if df[col].isna().all() or (df[col] == '').all():
                        missing_fields.append(col)
                
                if missing_fields:
                    st.warning(f"⚠️ Missing fields: {', '.join(missing_fields)}")
                else:
                    st.success("All fields extracted successfully")
            
            # Allow manual editing before export
            st.subheader("✏️ Edit Data (if needed)")
            edited_df = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True,
                height=300
            )
            
            # Export button
            if st.button("📥 Export to Excel", type="primary"):
                with st.spinner("Generating Excel file..."):
                    # Convert edited dataframe back to list of dicts
                    edited_data = edited_df.to_dict('records')
                    excel_path = write_to_excel(edited_data)
                    
                    # Read the file for download
                    with open(excel_path, 'rb') as f:
                        excel_data = f.read()
                    
                    st.download_button(
                        label="📥 Download Excel File",
                        data=excel_data,
                        file_name=os.path.basename(excel_path),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    
                    st.success("✅ Excel file generated successfully!")
        else:
            st.error("❌ No SLOs found in the syllabus. Please check the format.")
            st.info("""
            Make sure the syllabus contains:
            - A section titled "Course learning outcomes" or similar
            - SLOs labeled as "Student Learning Outcome #X:"
            - The required fields: CorSLO, PSLO, CSLO, GenEd Outcome
            """)
    
    except Exception as e:
        st.error(f"❌ Error parsing syllabus: {str(e)}")
        st.exception(e)
    
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

else:
    # Show placeholder when no file is uploaded
    st.info("👆 Upload a PDF syllabus to begin")
    
    # Show example of expected output
    with st.expander("📋 Expected Output Format"):
        st.markdown("""
        The parser extracts the following fields:
        
        | Column | Description | Example |
        |--------|-------------|---------|
        | Course | Course code | CSCI 1301 |
        | Semester | Term | Fall 2025 |
        | instructor | Instructor name | Elena Machkasova |
        | Number | SLO number | 1.0 |
        | Corslo | Course SLO | Students will be able to... |
        | PSLO | Program SLO | Students will demonstrate... |
        | McSLO | Major SLO (if available) | (blank) |
        | CSLO | Campus SLO | Creative Problem-Solver |
        | GenEd Outcome | General Education Outcome | Students will be able to... |
        """)

# Footer
st.markdown("---")
st.caption("Built for UMN Morris Syllabus SLO Tracking")