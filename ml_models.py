"""Reproducible educational ML models on explicitly synthetic service-desk records.

The labelled data are templated. Metrics cannot be generalized to real tickets.
"""
import random
from functools import lru_cache
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, brier_score_loss

CATEGORIES={
    "Incident Response":[
        "Production outage affecting {asset} service",
        "{asset} service unavailable after deployment",
        "Critical ransomware alert on {asset} system",
        "Customer reports widespread {asset} downtime"],
    "Identity & Access":[
        "User cannot login to {asset} portal",
        "Password reset request for {asset}",
        "Account locked in {asset} dashboard",
        "Access permission denied on {asset}"],
    "Billing":[
        "Invoice mismatch for {asset} subscription",
        "Billing charge incorrect on {asset} account",
        "Payment receipt missing for {asset}",
        "Refund query about {asset} plan"],
    "General Support":[
        "Request training for {asset} feature",
        "How to configure {asset} report",
        "Question about {asset} documentation",
        "Need assistance with {asset} settings"]
}
ASSETS=["cloud","network","storage","hosting","security","support","backup","office"]
PRIORITY={"Incident Response":"P1","Identity & Access":"P2","Billing":"P3","General Support":"P3"}

def synthetic_tickets(n_per_category=80,seed=19):
    rng=random.Random(seed)
    texts=[];teams=[];breaches=[];priorities=[]
    for team,templates in CATEGORIES.items():
        for i in range(n_per_category):
            asset=rng.choice(ASSETS)
            text=rng.choice(templates).format(asset=asset)
            priority=PRIORITY[team]
            # Explicitly simulated breach labels. No real operational evidence.
            risk={"P1":0.55,"P2":0.28,"P3":0.10}[priority]
            risk+=0.12 if asset in ("network","cloud") else 0.0
            breached=int(rng.random()<risk)
            texts.append(text);teams.append(team);breaches.append(breached);priorities.append(priority)
    return texts,teams,np.asarray(breaches),priorities

@lru_cache(maxsize=1)
def train_and_evaluate():
    texts,teams,breaches,priorities=synthetic_tickets()
    # One shared stratified split for both tasks. No test rows used to fit models.
    indices=np.arange(len(texts))
    train_idx,test_idx=train_test_split(indices,test_size=0.25,random_state=42,stratify=teams)
    X_train=[texts[i] for i in train_idx]
    X_test=[texts[i] for i in test_idx]
    y_train=[teams[i] for i in train_idx]
    y_test=[teams[i] for i in test_idx]
    classifier=make_pipeline(TfidfVectorizer(ngram_range=(1,2)),
                             LogisticRegression(max_iter=1000,random_state=42))
    classifier.fit(X_train,y_train)
    predictions=classifier.predict(X_test)
    # Breach model deliberately uses priority only, which is available at intake.
    # This is a simplistic synthetic probability baseline, not an SLA predictor for real use.
    priority_order=["P1","P2","P3"]
    def features(indexes):
        return np.asarray([[int(priorities[i]==p) for p in priority_order] for i in indexes])
    risk_model=LogisticRegression(max_iter=1000,random_state=42)
    risk_model.fit(features(train_idx),breaches[train_idx])
    probabilities=risk_model.predict_proba(features(test_idx))[:,1]
    metrics={
        "classification_accuracy":float(accuracy_score(y_test,predictions)),
        "classification_report":classification_report(y_test,predictions,zero_division=0),
        "breach_roc_auc":float(roc_auc_score(breaches[test_idx],probabilities)),
        "breach_brier_score":float(brier_score_loss(breaches[test_idx],probabilities)),
        "training_rows":int(len(train_idx)),
        "test_rows":int(len(test_idx)),
    }
    return classifier,risk_model,metrics

def predict_ticket(subject,description):
    if not subject.strip() or not description.strip():
        raise ValueError("Subject and description required")
    classifier,risk_model,_=train_and_evaluate()
    text=f"{subject} {description}"
    team=str(classifier.predict([text])[0])
    priority=PRIORITY[team]
    features=np.asarray([[int(priority==p) for p in ["P1","P2","P3"]]])
    probability=float(risk_model.predict_proba(features)[0,1])
    return {"team":team,"priority":priority,"simulated_sla_breach_risk":probability}
