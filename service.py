from datetime import datetime
from typing import List,Optional
from task import TaskRepository
from Interpreter import ContractorRepository
from invoice import  InvoiceRepository, DraftInvoiceRepository, DraftInvoice

# Use Case (Service) Objects

class InvoiceManagementService:
    """
    Business logic for managing submitted invoices.
    """
    def __init__(self,
                 task_repository: TaskRepository,
                 contractor_repository: ContractorRepository,
                 draft_repository: DraftInvoiceRepository,
                 invoice_repository: InvoiceRepository):
        self.task_repository = task_repository
        self.contractor_repository = contractor_repository
        self.invoice_repository = invoice_repository
        self.draft_repository = draft_repository

    def submit_invoice(self, draft_invoice_id: int):
        draft = self.draft_repository.get(draft_invoice_id)
        if draft is None:
            raise ValueError("Draft does not exist")

        # Prevent duplicate invoice submission.
        existing_invoice = self.invoice_repository.get_by_task(draft.task)
        if existing_invoice is not None:
            raise ValueError("Invoice already exists for this task")

        draft.id = None # because we want to insert a new invoice we get rid of the old ID
        self.invoice_repository.save(draft)

        invoice = self.invoice_repository.get_by_task(draft.task)
        assert invoice is not None

        # we no longer need the draft after we submitted the invoice
        self.draft_repository.delete(draft_invoice_id)

        return invoice.id

# Draft

class DraftInvoiceService:
    """
    Business logic for managing draft invoices.
    """
    def __init__(self,
                 task_repository: TaskRepository,
                 contractor_repository: ContractorRepository,
                 draft_invoice_repository: DraftInvoiceRepository):
        self.task_repository = task_repository
        self.contractor_repository = contractor_repository
        self.draft_invoice_repository = draft_invoice_repository

    def save_draft_invoice(self,
                contractor_id: int,
                task_id: int,
                start_time: datetime,
                end_time: datetime,
                signature: str):
        contractor = self.contractor_repository.find_by_id(contractor_id)
        if contractor is None:
            raise ValueError("Contractor does not exist")

        task = self.task_repository.get(task_id)
        if task is None:
            raise ValueError("Task does not exist")

        # Create and save the DraftInvoice.
        draft_invoice = DraftInvoice(contractor, task, start_time, end_time, signature)
        self.draft_invoice_repository.save(draft_invoice)
        return draft_invoice.id

    def update(self,
                draft_invoice_id: int,
                contractor_id: Optional[int],
                task_id: Optional[int],
                start_time: Optional[datetime],
                end_time: Optional[datetime],
                signature: Optional[str]):
        draft = self.draft_invoice_repository.get(draft_invoice_id)
        if draft is None:
            raise ValueError("Draft does not exist")

        if contractor_id is not None:
            contractor = self.contractor_repository.find_by_id(contractor_id)
            if contractor is None:
                raise ValueError("Contractor does not exist")
            draft.contractor = contractor

        if task_id is not None:
            task = self.task_repository.get(task_id)
            if task is None:
                raise ValueError("Task does not exist")
            draft.task = task

        if start_time is not None:
            draft.start_time = start_time

        if end_time is not None:
            draft.end_time = end_time

        if signature is not None:
            draft.signature = signature

        draft.update_last_saved()
        self.draft_invoice_repository.save(draft)

    def list(self, contractor_id: int) -> List[DraftInvoice]:
        contractor = self.contractor_repository.find_by_id(contractor_id)
        if contractor is None:
            raise ValueError("Contractor does not exist")
        return self.draft_invoice_repository.list_by_contractor(contractor)

    def delete(self, draft_invoice_id: int):
        self.draft_invoice_repository.delete(draft_invoice_id)
