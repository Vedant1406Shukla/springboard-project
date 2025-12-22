import streamlit as st
import os
import uuid
import datetime
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from graph import graph
# Load environment variables
load_dotenv()
# Page config
st.header("Open Deep Research Assistant 🤖")
st.set_page_config(page_title="Research Assistant", page_icon="🤖", layout="wide")
# --- Theme Toggle ---
if "theme" not in st.session_state:
    st.session_state.theme = "light"
def toggle_theme():
    if st.session_state.theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"
# Inject CSS based on theme
if st.session_state.theme == "dark":
    st.markdown("""
    <style>
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stTextInput input {
            background-color: #2D2D2D;
            color: #FFFFFF;
        }
        .stSidebar {
            background-color: #252526;
        }
        div[data-testid="stMarkdownContainer"] {
            color: #FFFFFF;
        }
    </style>
    """, unsafe_allow_html=True)
else:
     st.markdown("""
    <style>
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }
    </style>
    """, unsafe_allow_html=True)
# Custom CSS for layout
# Custom CSS for layout
st.markdown("""
<style>
    .main {
        padding-bottom: 5rem;
    }
</style>
""", unsafe_allow_html=True)
# --- Session State Initialization ---
if "chats" not in st.session_state:
    # Structure: {chat_id: {"title": "...", "messages": [], "created_at": ...}}
    new_chat_id = str(uuid.uuid4())
    st.session_state.chats = {
        new_chat_id: {
            "title": "New Chat",
            "messages": [],
            "created_at": datetime.datetime.now()
        }
    }
    st.session_state.current_chat_id = new_chat_id
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]
# --- Sidebar ---
with st.sidebar:
    st.title("Research Assistant")
    
    # API Status
    st.subheader("API Status")
    with st.expander("Check Connectivity", expanded=False):
        # User requested hardcoded key to bypass environment issues
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        tavily_api_key = os.environ.get("TAVILY_API_KEY")
        
        if openai_api_key:
            st.success("OpenAI API: Connected")
        else:
            st.error("OpenAI API: Missing")
            
        if tavily_api_key:
            st.success("Tavily API: Connected")
        else:
            st.error("Tavily API: Missing")
    st.divider()
    # Search Focus
    st.subheader("🔍 Search Focus")
    search_focus = st.radio(
        "Select focus",
        ["General Web", "Academic Research Paper"],
        index=1, # Default to Academic
        label_visibility="collapsed"
    )
    st.divider()
    # Chat List
    st.subheader("Chats")
    chat_ids = list(st.session_state.chats.keys())
    # Sort by creation time desc
    chat_ids.sort(key=lambda x: st.session_state.chats[x]["created_at"], reverse=True)
    
    # Scrollable container for chats (implicit in Streamlit sidebar)
    if "editing_chat_id" not in st.session_state:
        st.session_state.editing_chat_id = None

    for c_id in chat_ids:
        chat = st.session_state.chats[c_id]
        
        # Check if we are editing this chat
        is_editing = (st.session_state.editing_chat_id == c_id)
        
        if is_editing:
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                 def on_rename_submit(cid=c_id):
                      new_name = st.session_state[f"rename_input_{cid}"]
                      if new_name:
                           st.session_state.chats[cid]["title"] = new_name
                      st.session_state.editing_chat_id = None
                 
                 st.text_input(
                     "Rename", 
                     value=chat["title"], 
                     key=f"rename_input_{c_id}", 
                     label_visibility="collapsed", 
                     on_change=on_rename_submit
                 )
            with col2:
                 # Cancel edit button (or just rely on clicking elsewhere/enter? A button is safer)
                 if st.button("❌", key=f"cancel_edit_{c_id}"):
                      st.session_state.editing_chat_id = None
                      st.rerun()

        else:
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            with col1:
                 # Highlight current chat
                label = chat["title"]
                if c_id == st.session_state.current_chat_id:
                    label = f"**{label}**"
                    
                if st.button(label, key=f"sel_{c_id}", use_container_width=True):
                    st.session_state.current_chat_id = c_id
                    st.rerun()
            with col2:
                 if st.button("✏️", key=f"ren_{c_id}"):
                      st.session_state.editing_chat_id = c_id
                      st.rerun()
            with col3:
                 if st.button("🗑️", key=f"del_{c_id}"):
                    del st.session_state.chats[c_id]
                    # If we deleted the current chat, switch to another
                    if c_id == st.session_state.current_chat_id:
                        if st.session_state.chats:
                             st.session_state.current_chat_id = list(st.session_state.chats.keys())[0]
                        else:
                             # No chats left, create one
                             new_id = str(uuid.uuid4())
                             st.session_state.chats[new_id] = {
                                 "title": "New Chat",
                                 "messages": [],
                                 "created_at": datetime.datetime.now()
                             }
                             st.session_state.current_chat_id = new_id
                    st.rerun()

    # Function to create new chat (for use in button)
    def create_new_chat():
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = {
            "title": "New Chat",
            "messages": [],
            "created_at": datetime.datetime.now()
        }
        st.session_state.current_chat_id = new_id
    
    # Spacer to push content to bottom
    st.markdown("---")

    # New Chat Button (at very bottom)
    if st.button("➕ New Chat", use_container_width=True, on_click=create_new_chat):
        pass # functionality is in on_click
    # PDF Upload
    st.divider()
    st.subheader("📄 PDF Analysis")
    uploaded_file = st.file_uploader("Upload PDF for Summary", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Analyze PDF"):
            with st.spinner("Extracting and Summarizing..."):
                try:
                    import pypdf
                    # Import get_llm instead of global llm
                    from agents import get_llm
                    
                    # Create config object for get_llm
                    pdf_config = {"configurable": {"openai_api_key": openai_api_key}}
                    llm = get_llm(pdf_config)
                    
                    # Extract Text
                    reader = pypdf.PdfReader(uploaded_file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    
                    # Truncate if too long (simple check, can be improved)
                    if len(text) > 50000:
                        text = text[:50000] + "...(truncated)"
                        
                    # Summarize
                    summary_prompt = f"Please provide a comprehensive summary of the following text:\n\n{text}"
                    response = llm.invoke(summary_prompt)
                    
                    # Store result in session state to display in main area
                    st.session_state.pdf_summary = response.content
                    st.success("Analysis Complete!")
                    
                except Exception as e:
                    st.error(f"Error processing PDF: {e}")
    st.divider()
    
    # Theme Toggle
    st.toggle("Dark Mode", value=(st.session_state.theme == "dark"), on_change=toggle_theme)
# --- Main Chat Area ---
# Display PDF Summary if available
if "pdf_summary" in st.session_state:
    with st.expander("📄 PDF Summary Result", expanded=True):
        st.markdown(st.session_state.pdf_summary)
        if st.button("Clear Summary"):
            del st.session_state.pdf_summary
            st.rerun()
if st.session_state.current_chat_id in st.session_state.chats:
    current_chat_data = st.session_state.chats[st.session_state.current_chat_id]
    messages = current_chat_data["messages"]
    
    st.header(current_chat_data["title"])
    # Display History
    for message in messages:
        timestamp = message.additional_kwargs.get("timestamp", "")
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                if timestamp:
                    st.caption(f"**You** • *{timestamp}*")
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                if timestamp:
                    st.caption(f"**Assistant** • *{timestamp}*")
                st.markdown(message.content)
    # Input
    if prompt := st.chat_input("What would you like to research?"):
        # Add user message
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messages.append(HumanMessage(content=prompt, additional_kwargs={"timestamp": timestamp}))
        with st.chat_message("user"):
            st.caption(f"**You** • *{timestamp}*")
            st.markdown(prompt)
            
        # Run Backend
        config = {
            "configurable": {
                "thread_id": st.session_state.current_chat_id,
                "openai_api_key": openai_api_key,
                "tavily_api_key": tavily_api_key,
                "search_focus": search_focus
            }
        }
        inputs = {
            "query": prompt,
            "chat_history": messages[:-1]
        }
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                try:
                    final_state = graph.invoke(inputs, config=config)
                    response_content = final_state.get("response", "No response generated.")
                    
                    message_placeholder.markdown(response_content)
                    
                    # Add assistant message
                    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    messages.append(AIMessage(content=response_content, additional_kwargs={"timestamp": ts}))
                    
                    # Update title if it's the first message and still "New Chat" AFTER we get a response
                    if len(messages) == 2 and current_chat_data["title"] == "New Chat":
                        # Generate a smart title using LLM
                        try:
                            from agents import get_llm
                            # Use a lightweight config for title generation
                            title_config = {"configurable": {"openai_api_key": openai_api_key}}
                            title_llm = get_llm(title_config)
                            title_prompt = f"Generate a very short, concise 3-5 word title for this chat based on the initial user prompt: '{prompt}'. Do not use quotes."
                            title_response = title_llm.invoke(title_prompt)
                            current_chat_data["title"] = title_response.content.strip().replace('"', '')
                        except Exception:
                            # Fallback to simple split
                            current_chat_data["title"] = " ".join(prompt.split()[:5])
                        
                        # We do NOT rerun here to avoid disrupting the flow. The title will update on next interaction.
                        
                except Exception as e:
                    st.error(f"An error occurred: {e}")
else:
    st.error("No active chat. Please create a new chat.")
