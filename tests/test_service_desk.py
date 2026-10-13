import sqlite3
import unittest
from service_desk import connect,triage,submit_ticket,update_status,get_tickets
class ServiceDeskTests(unittest.TestCase):
    def test_triage(self):
        self.assertEqual(triage("Production down","cloud outage"),("P1","Incident Response"))
        self.assertEqual(triage("Password reset","cannot login"),("P2","Identity & Access"))
    def test_workflow(self):
        db=connect(":memory:")
        ticket_id=submit_ticket(db,"Billing question","invoice missing")
        self.assertEqual(len(get_tickets(db)),1)
        self.assertEqual(update_status(db,ticket_id,"resolved"),1)
        self.assertEqual(get_tickets(db)[0][4],"resolved")
        with self.assertRaises(ValueError):
            submit_ticket(db,"","")
        db.close()
if __name__=="__main__":
    unittest.main()
