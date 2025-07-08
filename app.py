import streamlit as st
import pandas as pd
import os

# File location
DATA_FILE = "data/trails.csv"

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Question", "Tag", "Status"])
    df.to_csv(DATA_FILE, index=False)

# Load data
df = pd.read_csv(DATA_FILE)

st.title("🌱 Curiosity Trails")
st.write("Capture your questions, organise them by theme, and grow your curiosity forest!")

# --- Add new curiosity ---
st.header("➕ Add New Trail")
with st.form("add_form"):
    question = st.text_area("What's your curiosity today?")
    tag = st.text_input("Tag/Theme (e.g., Vet, Sustainability, Style)")
    submitted = st.form_submit_button("Add Trail")

    if submitted and question:
        new_row = {"Question": question, "Tag": tag, "Status": "Active"}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Trail added!")

# --- View & filter ---
st.header("🌿 Your Trails")

# Filter
filter_tag = st.text_input("Filter by tag (leave blank to see all)")
filtered_df = df.copy()
if filter_tag:
    filtered_df = filtered_df[filtered_df["Tag"].str.contains(filter_tag, case=False, na=False)]

# Mark as done
if not filtered_df.empty:
    for idx, row in filtered_df.iterrows():
        cols = st.columns([6, 2, 2])
        cols[0].markdown(f"**{row['Question']}**")
        cols[1].markdown(f"`{row['Tag']}`")
        if row["Status"] == "Active":
            if cols[2].button("Mark Done", key=idx):
                df.at[idx, "Status"] = "Done"
                df.to_csv(DATA_FILE, index=False)
                st.experimental_rerun()
        else:
            cols[2].markdown("✅ Done")
else:
    st.write("No trails yet. Start adding some!")

# Show raw data toggle
with st.expander("📊 See Raw Data"):
    st.dataframe(df)
