import streamlit as st
import pandas as pd
from service_desk import connect,submit_ticket,update_status,get_tickets
st.set_page_config(page_title="AI Service Desk Prototype",layout="wide")
st.title("Service Desk Triage & Workflow")
st.caption("Rule-based baseline, not a trained AI classifier. Synthetic/demo tickets only.")
db=connect()
with st.form("ticket"):
    subject=st.text_input("Ticket subject")
    description=st.text_area("Description")
    if st.form_submit_button("Submit ticket"):
        try:
            ticket_id=submit_ticket(db,subject,description)
            st.success(f"Ticket #{ticket_id} created")
        except ValueError as exc:
            st.error(str(exc))
st.subheader("Ticket queue")
rows=get_tickets(db)
columns=["id","subject","priority","team","status","created_at"]
if rows:
    frame=pd.DataFrame(rows,columns=columns)
    st.dataframe(frame,use_container_width=True)
    st.bar_chart(frame["priority"].value_counts())
    with st.form("update"):
        ticket_id=st.selectbox("Ticket ID",frame["id"].tolist())
        status=st.selectbox("New status",["open","in_progress","resolved"])
        if st.form_submit_button("Update status"):
            update_status(db,int(ticket_id),status)
            st.success("Status updated. Refresh to see latest queue.")
else:
    st.info("No tickets yet. Submit a demo ticket above.")
