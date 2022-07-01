import streamlit as st
from shillelagh.backends.apsw.db import connect
#from helper import connect_to_gsheets, insert_user_data
from datetime import datetime
from uuid import uuid4

st.set_page_config(
    page_title="App Home",
    page_icon=""
)

st.title("Language and Identity on Twitter") 
#st.subheader("See multiple linguistic Twitter analysis.")
st.warning("""
           By submitting the form below you agree to your data being used for research. 
           Your twitter username will be stored in a private google sheet and will not be shared with anyone (unless extraordinary circumstances force us to share it). 
           You can ask for your data to be deleted by emailing us with an app ID number you'll be issued after submitting the form. 
           """)

st.text_input("Enter a twitter username to begin", key="name")
st.session_state.username_mine = st.radio(
            "I confirm that",
            ('This username belongs to me.', 'This username is belongs to someone else.')) 



if "last_name" not in st.session_state:
     st.session_state.last_name = ""
     st.session_state.submitted = False
     st.session_state.open_form = True
 

if st.session_state.last_name != st.session_state.name:  

    if st.session_state.username_mine == 'This username belongs to me.':
        if st.session_state.open_form:
            with st.form("my_form"):
                dem_words, rep_words = [], []
                st.markdown("#### Please add five words that describe Democrats best")
                for i in range(5):
                    dem_words.append(st.text_input("D"+str(i+1)))
                st.session_state.dem_words = ", ".join(dem_words).lower()

                st.markdown("#### Please add five words that describe Republicans best")
                for i in range(5):
                    rep_words.append(st.text_input("R"+str(i+1),key = "R"+str(i+1)))
                st.session_state.rep_words = ", ".join(rep_words).lower()

                st.markdown("#### Feeling Thermomether")
                st.slider("How warm do you feel about Democrats (0 = coldest rating; 100 = warmest rating)?", 
                    min_value=0, max_value=100, value=50, step=1,key="dem_temp")          
                st.slider("How warm do you feel about Republicans (0 = coldest rating; 100 = warmest rating)?", 
                        min_value=0, max_value=100, value=50, step=1,key="rep_temp") 
                st.session_state.party = st.radio(
                     "How do you identify?",
                    ('Independant','Republican', 'Democrat')) 

                def submit():
                    if (st.session_state.rep_words[-2:] != ", "):
                        st.session_state.open_form = False
                        st.session_state.id = datetime.now().strftime('%Y%m-%d%H-%M-') + str(uuid4())
                        st.success("Thanks for submitting your answers!")
                        st.markdown(f"Your app ID is {st.session_state.id}. Note it down and email us if you want your answers deleted.") 
                        
                        st.session_state.conn = connect(":memory:", 
                            adapter_kwargs = {
                            "gsheetsapi": { 
                            "service_account_info":  st.secrets["gcp_service_account"] 
                                    }
                                        }
                        )
                        #insert_user_data(conn, st.secrets["private_gsheets_url"])
                        st.session_state.last_name = st.session_state.name
                        st.session_state.submitted = True   
                    else:
                        st.error("Please fill out every field of the form and submit again.")
   
                st.form_submit_button("Submit", on_click=submit)
                 

    
    elif st.session_state.username_mine == 'This username is belongs to someone else.':
        st.session_state.conn = connect(":memory:", 
                    adapter_kwargs = {
                        "gsheetsapi": { 
                        "service_account_info":  st.secrets["gcp_service_account"] 
                                    }
                                        }
                    )
        st.warning("""You entered someone else's Twitter username. 
                Some analyses will not be available. 
                If you change your mind at any point, return to this page to enter your Twitter username.
                """)

            
        
                        





