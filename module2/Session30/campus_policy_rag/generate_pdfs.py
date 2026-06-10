# quick helper to generate sample policy PDFs
from fpdf import FPDF

class PolicyPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, self.title_text, align="C")
        self.ln(12)
    def chapter(self, heading, body):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, heading)
        self.ln(10)
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, body)
        self.ln(4)

# hostel policy
pdf = PolicyPDF()
pdf.title_text = "Hostel Policy"
pdf.add_page()
pdf.chapter("General Rules", "All students residing in the hostel must follow the rules set by the hostel administration. Hostel timings are strictly enforced. Students must return to the hostel by 10:00 PM on weekdays and by 11:00 PM on weekends. Late entry without prior permission will attract disciplinary action.")
pdf.chapter("Visitor Policy", "Visitors are allowed in the hostel common areas only. Visitors must register at the security desk and provide valid identification. Visitors are not permitted in student rooms.")
pdf.chapter("Weekend Rules", "On weekends, students may have visitors in the common lounge area between 10:00 AM and 8:00 PM. Overnight visitors are strictly prohibited. Quiet hours begin at 10:00 PM on weekends.")
pdf.output("policy_documents/hostel_policy.pdf")

# refund policy
pdf = PolicyPDF()
pdf.title_text = "Refund Policy"
pdf.add_page()
pdf.chapter("Course Drop Refund", "Students who drop a course within the first week of the course start date are eligible for a full refund. After the first week but before two weeks, a 50 percent refund will be granted. No refunds are given after two weeks from the course start date.")
pdf.chapter("Special Cases", "In case of medical emergencies, students may apply for a special refund review. This requires proper medical documentation and approval from the academic office. Refunds for medical reasons are processed within 30 working days.")
pdf.chapter("Hostel Fee Refund", "Hostel fees are refundable only if the student withdraws from the hostel within the first month of stay. A deduction of 20 percent is made as administrative charges. After one month, hostel fees are non-refundable.")
pdf.output("policy_documents/refund_policy.pdf")

# library policy
pdf = PolicyPDF()
pdf.title_text = "Library Policy"
pdf.add_page()
pdf.chapter("Book Lending Rules", "Students can borrow up to three books at a time for a period of 14 days. Books can be renewed once for an additional 7 days if there are no pending requests. Late returns attract a fine of 5 rupees per day per book.")
pdf.chapter("Return Deadlines", "The deadline for returning borrowed books is strictly 14 days from the issue date. Renewal must be requested at least one day before the due date. Books not returned after 30 days will be considered lost and the student must pay the replacement cost.")
pdf.chapter("Digital Resources", "Digital resources including e-books and online journals are accessible 24/7 through the library portal. Students must use their institute credentials to access these materials.")
pdf.output("policy_documents/library_policy.pdf")

print("Sample PDFs generated successfully.")
