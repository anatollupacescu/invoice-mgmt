from __future__ import annotations

class Contractor:
    """
    The Contractor object
    """
    def __init__(self, contractor_id: int | None, name: str):
        self.id = contractor_id
        self.name = name

class ContractorRepository:
    def __init__(self):
        self.contractors: dict[int, Contractor] = {}

    def add(self, contractor: Contractor):
        if contractor.id is None:
            contractor.id = len(self.contractors)

        if self.find_by_name(contractor.name):
            raise ValueError(f"Contractor with name '{contractor.name}' already exists.")

        self.contractors[contractor.id] = contractor

    def find_by_id(self, contractor_id: int) -> Contractor | None:
        return self.contractors.get(contractor_id)

    def find_by_name(self, name: str) -> Contractor | None:
        for contractor in self.contractors.values():
            if contractor.name.lower() == name.lower():
                return contractor
        return None
