import streamlit as st
import pandas as pd
import time
from blockchain import Blockchain

if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

if "user_db" not in st.session_state:
    st.session_state.user_db = {}

if "issues_db" not in st.session_state:
    st.session_state.issues_db = []

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

st.set_page_config(page_title="Digitized & Decentralized Blockchain", layout="centered")

st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", [
    "Home Page", 
    "User Registration",
    "User Login & Workspace",
    "Track Issues",
    "Admin Portal",
    "Blockchain Ledger View"
])

if st.session_state.logged_in_user:
    st.sidebar.markdown(f"**Logged in as:** `{st.session_state.logged_in_user}`")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in_user = None
        st.rerun()

if page == "Home Page":
    st.title("🌐 Digitized & Decentralized Blockchain Technology")
    st.subheader("Secure & Immutable Issue Management System")
    st.write("""
    Welcome to the Decentralized Issue Management Platform. This system leverages 
    cryptographic SHA-256 blockchain technology to ensure that all logged user profiles, 
    complaints, and administrative status updates remain tamper-proof, transparent, and completely verifiable.
    """)
    st.info("💡 Use the sidebar navigation on the left to navigate between screens.")

elif page == "User Registration":
    st.title("📝 User Registration Page")
    st.subheader("Create a Secure Account on the Decentralized Network")
    with st.form("registration_form"):
        new_user = st.text_input("Choose a Username")
        new_pass = st.text_input("Create a Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        submit_reg = st.form_submit_button("Register Account")
        if submit_reg:
            if not new_user or not new_pass:
                st.error("Username and password fields cannot be left empty.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match. Please re-enter.")
            elif new_user in st.session_state.user_db:
                st.error("This username is already registered on the blockchain network.")
            else:
                st.session_state.user_db[new_user] = new_pass
                st.session_state.blockchain.add_block({"action": "USER_REGISTRATION", "username": new_user})
                st.success(f"Account '{new_user}' successfully registered and digitized to the ledger!")

elif page == "User Login & Workspace":
    st.title("🔑 User Workspace Portal")
    if st.session_state.logged_in_user is None:
        st.subheader("Account Login Authentication")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Authenticate & Log In")
            if submit_login:
                if username in st.session_state.user_db and st.session_state.user_db[username] == password:
                    st.session_state.logged_in_user = username
                    st.success("Authentication validated! Welcome to your workspace.")
                    st.rerun()
                else:
                    st.error("Invalid username or password credentials provided.")
    else:
        st.subheader(f"👋 Welcome back, {st.session_state.logged_in_user}!")
        st.markdown("### 📥 Report an Issue to the Ledger")
        with st.form("issue_form"):
            issue_title = st.text_input("Issue Title / Category")
            issue_desc = st.text_area("Detailed Description of the Issue")
            submit_issue = st.form_submit_button("Submit & Encrypt Issue")
            if submit_issue:
                if not issue_title or not issue_desc:
                    st.error("Please provide both a title and description.")
                else:
                    issue_id = f"ISSUE-{len(st.session_state.issues_db) + 1001}"
                    new_issue = {
                        "issue_id": issue_id,
                        "reporter": st.session_state.logged_in_user,
                        "title": issue_title,
                        "description": issue_desc,
                        "status": "Pending Verification"
                    }
                    st.session_state.issues_db.append(new_issue)
                    st.session_state.blockchain.add_block({
                        "action": "LOG_ISSUE",
                        "issue_id": issue_id,
                        "reporter": st.session_state.logged_in_user,
                        "title": issue_title,
                        "status": "Pending Verification"
                    })
                    st.success(f"Issue filed successfully! Assigned Ticket Tracking ID: **{issue_id}**")
        st.markdown("### 📋 Your Filed Network Issues")
        personal_issues = [i for i in st.session_state.issues_db if i["reporter"] == st.session_state.logged_in_user]
        if personal_issues:
            st.dataframe(pd.DataFrame(personal_issues)[["issue_id", "title", "status"]], use_container_width=True)
        else:
            st.info("You haven't filed any issue reports on this node terminal yet.")

elif page == "Track Issues":
    st.title("🔍 Public Issue Verification Tracking")
    st.subheader("Look up any ticket status transparently via Blockchain Records")
    search_id = st.text_input("Enter Issue Ticket Tracking ID (e.g., ISSUE-1001)")
    if st.button("Query Ledger"):
        found_issue = next((i for i in st.session_state.issues_db if i["issue_id"] == search_id), None)
        if found_issue:
            st.success(f"Ticket Found!")
            st.write(f"**Tracking ID:** {found_issue['issue_id']}")
            st.write(f"**Reporter:** {found_issue['reporter']}")
            st.write(f"**Issue Title:** {found_issue['title']}")
            st.write(f"**Description:** {found_issue['description']}")
            st.write(f"**Current Blockchain Lifecycle Status:** `{found_issue['status']}`")
        else:
            st.error("The requested Tracking ID could not be found or verified on the blockchain network.")

elif page == "Admin Portal":
    st.title("🛡️ Secure Administrator Command Panel")
    admin_key = st.text_input("Enter Administrator Authorization Passkey", type="password")
    if admin_key == "admin123":
        st.success("Access Granted. Secure Administrative Workspace unlocked.")
        st.subheader("📋 Complete Ledger Issue List Management")
        if st.session_state.issues_db:
            for idx, issue in enumerate(st.session_state.issues_db):
                with st.container():
                    st.markdown(f"#### Ticket: **{issue['issue_id']}** — *{issue['title']}*")
                    st.write(f"**Reporter Account:** {issue['reporter']}")
                    st.write(f"**Detailed Breakdown:** {issue['description']}")
                    st.write(f"**Current Ledger Status:** `{issue['status']}`")
                    new_status = st.selectbox(f"Modify Lifecycle Status for {issue['issue_id']}", 
                                              ["Pending Verification", "In Progress", "Resolved & Closed"], 
                                              index=["Pending Verification", "In Progress", "Resolved & Closed"].index(issue['status']),
                                              key=f"status_select_{idx}")
                    if st.button(f"Update Lifecycle State for {issue['issue_id']}", key=f"btn_{idx}"):
                        if issue['status'] != new_status:
                            st.session_state.issues_db[idx]['status'] = new_status
                            st.session_state.blockchain.add_block({
                                "action": "UPDATE_STATUS",
                                "issue_id": issue['issue_id'],
                                "updated_by": "ADMIN",
                                "new_status": new_status
                            })
                            st.success(f"Status successfully updated to '{new_status}' and synchronized on the chain!")
                            st.rerun()
                    st.markdown("---")
        else:
            st.info("No active user complaints or tracking issues logged in the decentralized system network.")
    elif admin_key != "":
        st.error("Invalid Administrative Passkey. Access Denied.")

elif page == "Blockchain Ledger View":
    st.title("⛓️ Cryptographic Ledger Inspection Terminal")
    st.subheader("Live block visualizer proving structural data immutability")
    is_valid = st.session_state.blockchain.is_chain_valid()
    if is_valid:
        st.success("✅ Blockchain Integrity Verified: Structural status ledger is completely immutable and untampered.")
    else:
        st.error("🚨 Warning: Blockchain data mismatch or block linkage compromised!")
    st.write(f"Total Block Sequences Mined: **{len(st.session_state.blockchain.chain)}**")
    for block in st.session_state.blockchain.chain:
        with st.expander(f"📦 BLOCK {block.index} [Hash: {block.hash[:15]}...]"):
            st.write(f"**Sequence Block Index:** {block.index}")
            st.write(f"**Time Mined (Epoch Timestamp):** {block.timestamp}")
            st.write(f"**Payload Transaction Data:**", block.data)
            st.write(f"**Parent Block Connection Link (Previous Hash):** `{block.previous_hash}`")
            st.write(f"**Current Cryptographic Fingerprint Hash:** `{block.hash}`")