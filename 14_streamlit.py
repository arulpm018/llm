import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

from langchain.agents import create_sql_agent

from langchain.schema import SystemMessage

load_dotenv()

dburi = "sqlite:///data/research.db"
db = SQLDatabase.from_uri(dburi)


llm = OpenAI(temperature=1, streaming= True)

db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st.write("🧠 thinking...")
        st_callback = StreamlitCallbackHandler(st.container())
        response = db_chain.run(prompt, callbacks=[st_callback])
        st.write(response)