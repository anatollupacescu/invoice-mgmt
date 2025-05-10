from typing import Dict, Optional

class Contractor:
    """
    The Contractor object
    """
    def __init__(self, id: Optional[int], name: str):
        self.id = id
        self.name = name

class ContractorRepository:
    def __init__(self):
        self.contractors: Dict[int, Contractor] = {}

    def add(self, contractor: Contractor):
        if contractor.id is None:
            contractor.id = len(self.contractors)

        self.contractors[contractor.id] = contractor

    def find_by_id(self, contractor_id: int) -> Optional[Contractor]:
        return self.contractors.get(contractor_id)

    def find_by_name(self, name: str) -> Optional[Contractor]:
        for contractor in self.contractors.values():
            if contractor.name.lower() == name.lower():
                return contractor
        return None
