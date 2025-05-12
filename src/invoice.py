from datetime import datetime
from typing import Dict, List, Optional
from task import Task
from contractor import Contractor

# Domain objects

class Invoice:
    """
    The Invoice object represents a submitted invoice.
    Invariants and validations are enforced on creation.
    """
    def __init__(self, contractor: Contractor, task: Task, start_time: datetime, end_time: datetime, signature: str, invoice_id: Optional[int] = None):
        self.id = invoice_id
        self.contractor = contractor
        self.task = task
        self.start_time = start_time
        self.end_time = end_time
        self.signature = signature
        self.validate()

    def validate(self):
        if self.signature.strip() == "":
            raise ValueError("Signature is required")
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time")

class DraftInvoice(Invoice):
    """
    The Draft Invoice object inherits from Invoice
    but additionally keeps track of the last time it was updated
    """
    def __init__(self,
                 contractor: Contractor,
                 task: Task,
                 start_time: datetime,
                 end_time: datetime,
                 signature: str,
                 invoice_id: Optional[int] = None):
        super().__init__(contractor, task, start_time, end_time, signature, invoice_id)
        self.last_saved = datetime.now()

    def update_last_saved(self):
        self.validate()
        self.last_saved = datetime.now()

# Repositories for Domain Objects

class InvoiceRepository:
    """
    Repository for submitted invoices.
    Once submitted, invoices become immutable (no editing or deletion).
    """
    def __init__(self):
        self.invoices: Dict[int, Invoice] = {}  # in memory of now, replace with DB in the future

    def save(self, invoice: Invoice):
        if invoice.id is not None:
            raise ValueError(f"Unexpected ID {invoice.id}")

        invoice.id = len(self.invoices)
        self.invoices[invoice.id] = invoice

    def get_by_task(self, task: Task) -> Optional[Invoice]:
        for invoice in self.invoices.values():
            if invoice.task == task:
                return invoice
        return None

    def delete(self, invoice: Invoice):
        raise ValueError("Submitted invoices cannot be deleted")

    def update(self, invoice: Invoice):
        raise ValueError("Submitted invoices cannot be edited")


class DraftInvoiceRepository:
    """
    Repository for draft invoices.
    This repository holds invoices in draft state.
    """
    def __init__(self):
        self.draft_invoices: dict[int, DraftInvoice] = {}

    def get(self, draft_invoice_id: int) -> Optional[DraftInvoice]:
        return self.draft_invoices.get(draft_invoice_id)

    def save(self, draft_invoice: DraftInvoice):
        # If a draft invoice has an ID - update the draft, otherwise - insert.
        if draft_invoice.id is None:
            draft_invoice.id = len(self.draft_invoices)

        self.draft_invoices[draft_invoice.id] = draft_invoice

    def list_by_contractor(self, contractor: Contractor) -> List[DraftInvoice]:
        return [d for d in self.draft_invoices.values() if d.contractor.id == contractor.id]

    def delete(self, draft_invoice_id: int):
        if draft_invoice_id not in self.draft_invoices:
            raise ValueError(f"Draft invoice with ID {draft_invoice_id} not found")
        del self.draft_invoices[draft_invoice_id]
