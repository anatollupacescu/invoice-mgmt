from datetime import datetime
import sys
from invoice import  InvoiceRepository, DraftInvoiceRepository
from service import InvoiceManagementService, DraftInvoiceService
from task import InMemTaskRepository, Task
from contractor import ContractorRepository, Contractor

if __name__ == "__main__":
    # Data Setup
    contractor1 = Contractor(None, "Alice")
    contractor2 = Contractor(None, "Bob")

    task1 = Task(None, "Office", "English", "Spanish", datetime(2025, 3, 1, 9, 0))
    task2 = Task(None, "Remote", "French", "English", datetime(2025, 3, 10, 9, 0))

    # Create Repositories and add domain objects
    contractor_repo = ContractorRepository()
    contractor_repo.add(contractor1)
    contractor_repo.add(contractor2)

    task_repo = InMemTaskRepository()
    task_repo.add(task1)
    task_repo.add(task2)

    invoice_repo = InvoiceRepository()
    draft_invoice_repo = DraftInvoiceRepository()

    # Create Service Instances
    invoice_service = InvoiceManagementService(task_repo, contractor_repo, draft_invoice_repo, invoice_repo)
    draft_invoice_service = DraftInvoiceService(task_repo, contractor_repo, draft_invoice_repo)

    # Save a Draft Invoice

    assert contractor1.id is not None
    assert task1.id is not None

    try:
        draft_invoice_id = draft_invoice_service.save_draft_invoice(
            contractor1.id,
            task1.id,
            datetime(2025, 3, 10, 8, 0),
            datetime(2025, 3, 10, 9, 0),
            "signature1")
        print("Correct draft invoice saved successfully.")
    except Exception as e:
        print("Correct draft saving error:", e)
        sys.exit()

    try:
        draft_invoice_id = draft_invoice_service.save_draft_invoice(
            contractor1.id,
            task1.id,
            datetime(2025, 3, 10, 23, 0),
            datetime(2025, 3, 10, 1, 0),
            "signature2")
        print("Incorrect draft invoice not expected to be saved successfully.")
        sys.exit()
    except Exception as e:
        print("Incorrect draft invoice failed with error:", e)

    assert draft_invoice_id is not None

    # List Draft Invoices for a Contractor
    try:
        drafts = draft_invoice_service.list(draft_invoice_id)
        for d in drafts:
            print(f"Draft Invoice for task at {d.task.id}, last saved at {d.last_saved}")
    except Exception as e:
        print("Listing draft invoices error:", e)
        sys.exit()

    # Update a Draft Invoice
    try:
        draft_invoice_service.update(draft_invoice_id, None, None, None, None, "new-signature")
        print("Draft invoice signature updated successfully.")
    except Exception as e:
        print("Draft updating error:", e)

    # List Updated Draft Invoices for a Contractor
    try:
        d = draft_invoice_repo.get(draft_invoice_id)
        assert d is not None
        print(f"Draft Invoice has signature '{d.signature}', last saved at {d.last_saved}")
    except Exception as e:
        print("Listing draft invoices error:", e)
        sys.exit()

    # Submit an Invoice (Successful scenario)
    try:
        invoice_id = invoice_service.submit_invoice(draft_invoice_id)
        print("Invoice submitted successfully.")
    except Exception as e:
        print("Submission error:", e)
        sys.exit()

    assert invoice_id is not None

    try:
        drafts = draft_invoice_service.list(draft_invoice_id)
        if len(drafts) > 0:
            print("Not expected to find the draft")
            sys.exit()
        print("After submitting the invoice draft has been removed correctly")
    except Exception as e:
        print("Listing draft invoices error:", e)

    # Get the newly created Invoice
    try:
        invoice = invoice_repo.get_by_task(task1)
        assert invoice is not None
        print(f"Submitted invoice {invoice.id} for contractor {invoice.contractor.name}")
    except Exception as e:
        print("Draft deletion error:", e)
