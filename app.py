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

st.subheader("Machine-learning demonstration")
st.caption("Models are trained on templated synthetic tickets and simulated outcomes. Not suitable for live triage.")
from ml_models import train_and_evaluate, predict_ticket
with st.form("ml_demo"):
    example=st.text_input("Example ticket for ML analysis",value="User cannot login to cloud portal")
    if st.form_submit_button("Run ML demonstration"):
        result=predict_ticket(example,example)
        st.write("Suggested team:",result["team"])
        st.write("Suggested priority:",result["priority"])
        st.write("Simulated SLA breach probability:",round(result["simulated_sla_breach_risk"],3))
if st.button("Evaluate synthetic models"):
    _,_,metrics=train_and_evaluate()
    st.metric("Team classification accuracy",f"{metrics['classification_accuracy']:.1%}")
    st.metric("Simulated SLA ROC-AUC",f"{metrics['breach_roc_auc']:.3f}")
    st.metric("Simulated SLA Brier score",f"{metrics['breach_brier_score']:.3f}")
    st.code(metrics["classification_report"])
    st.caption("Synthetic train/test split; metrics do not establish real-world performance.")
