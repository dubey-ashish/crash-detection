import os
import tempfile
import streamlit as st
import json
import pandas as pd
from core import analyze_car_images


# Initialize session states
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = None
if "key_counter" not in st.session_state:
    st.session_state.key_counter = 0

# Add refresh button at the top
if st.button("🔄 Start New Analysis"):
    # Clear all stored files and results
    st.session_state.uploaded_files = None
    # Increment key counter to force new file uploader instance
    st.session_state.key_counter += 1
    # Rerun the app to reset all states
    st.rerun()

st.title("Vehicle Image Analysis App")

st.write("Please upload exactly **4 images** of the vehicle for analysis.")

# Allow multiple file uploads with a dynamic key
uploaded_files = st.file_uploader(
    "Upload 4 images",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
    key=f"file_uploader_{st.session_state.key_counter}",  # Dynamic key that changes on refresh
)

# Update session state
st.session_state.uploaded_files = uploaded_files

# Check if files are uploaded
if st.session_state.uploaded_files:
    if len(st.session_state.uploaded_files) != 4:
        st.error("Error: You must upload exactly 4 images.")
    else:
        # Show the uploaded images in a grid
        cols = st.columns(4)
        for idx, uploaded_file in enumerate(st.session_state.uploaded_files):
            with cols[idx]:
                st.image(
                    uploaded_file, caption=f"Image {idx + 1}", use_container_width=True
                )

        if st.button("Analyze Vehicle"):
            # Show loading spinner
            with st.spinner("Analyzing images..."):
                image_paths = []
                try:
                    # Save each uploaded image to a temporary file
                    for uploaded_file in st.session_state.uploaded_files:
                        ext = os.path.splitext(uploaded_file.name)[1]
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=ext
                        ) as tmp_file:
                            tmp_file.write(uploaded_file.getbuffer())
                            image_paths.append(tmp_file.name)

                    # Call the analysis function
                    raw_result = analyze_car_images(image_paths)

                    # Parse the JSON response
                    try:
                        parsed_result = json.loads(raw_result)
                        usage_metadata = parsed_result.get("usage_metadata", {})

                        # Extract token details
                        model_version = parsed_result.get("model_version", "N/A")
                        prompt_tokens = str(
                            usage_metadata.get("prompt_token_count", "N/A")
                        )
                        candidates_tokens = str(
                            usage_metadata.get("candidates_token_count", "N/A")
                        )
                        total_tokens = str(
                            usage_metadata.get("total_token_count", "N/A")
                        )

                        # Create a pandas DataFrame for token usage
                        token_df = pd.DataFrame(
                            {
                                "Metric": [
                                    "Model",
                                    "Prompt Tokens",
                                    "Candidates Tokens",
                                    "Total Tokens",
                                ],
                                "Value": [
                                    model_version,
                                    prompt_tokens,
                                    candidates_tokens,
                                    total_tokens,
                                ],
                            }
                        )

                        # Display token usage table
                        st.subheader("Token Usage")
                        st.dataframe(token_df, hide_index=True)

                        # Display the analysis results
                        st.subheader("Analysis Results")
                        analysis_text = parsed_result["candidates"][0]["content"][
                            "parts"
                        ][0]["text"]
                        st.write(analysis_text)

                    except (json.JSONDecodeError, KeyError) as parse_error:
                        st.error(f"Error parsing model response: {parse_error}")
                        st.write(raw_result)

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                finally:
                    # Clean up temporary files
                    for path in image_paths:
                        try:
                            os.unlink(path)
                        except:
                            pass
