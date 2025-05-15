import unittest
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent
sys.path.append(str(src_path))

from Interpreter import Contractor, ContractorRepository

class TestContractor(unittest.TestCase):
    def test_contractor_creation_with_id(self):
        """Test creating a contractor with an ID"""
        contractor = Contractor(1, "John Doe")
        self.assertEqual(contractor.id, 1)
        self.assertEqual(contractor.name, "John Doe")

    def test_contractor_creation_without_id(self):
        """Test creating a contractor without an ID"""
        contractor = Contractor(None, "John Doe")
        self.assertIsNone(contractor.id)
        self.assertEqual(contractor.name, "John Doe")

    def test_contractor_equality(self):
        """Test that two contractors with same data are not equal (no __eq__ implemented)"""
        contractor1 = Contractor(1, "John Doe")
        contractor2 = Contractor(1, "John Doe")
        self.assertIsNot(contractor1, contractor2)

    def test_contractor_name_variations(self):
        """Test creating contractors with various name formats"""
        test_names = [
            "",
            "   ",
            "John Doe",
            "Very Long Name " * 10,
            "Special @#$% Characters"
        ]

        for name in test_names:
            with self.subTest(name=name):
                contractor = Contractor(None, name)
                self.assertEqual(contractor.name, name)

class TestContractorRepository(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.empty_repository = ContractorRepository()
        self.sample_contractor = Contractor(None, "John Doe")

        # Create populated repository
        self.populated_repository = ContractorRepository()
        contractors = [
            Contractor(None, "Alice Smith"),
            Contractor(None, "Bob Jones"),
            Contractor(None, "Charlie Brown")
        ]
        for contractor in contractors:
            self.populated_repository.add(contractor)

    def test_new_repository_is_empty(self):
        """Test that a new repository is empty"""
        self.assertEqual(len(self.empty_repository.contractors), 0)

    def test_add_contractor_without_id(self):
        """Test adding a contractor without an ID"""
        self.empty_repository.add(self.sample_contractor)
        self.assertEqual(len(self.empty_repository.contractors), 1)
        self.assertEqual(self.sample_contractor.id, 0)
        self.assertEqual(self.empty_repository.contractors[0], self.sample_contractor)

    def test_add_contractor_with_id(self):
        """Test adding a contractor with a pre-defined ID"""
        contractor = Contractor(5, "John Doe")
        self.empty_repository.add(contractor)
        self.assertEqual(len(self.empty_repository.contractors), 1)
        self.assertEqual(contractor.id, 5)
        self.assertEqual(self.empty_repository.contractors[5], contractor)

    def test_add_duplicate_name_contractor(self):
        """Test that adding a contractor with duplicate name raises ValueError"""
        self.empty_repository.add(Contractor(None, "John Doe"))
        with self.assertRaises(ValueError) as context:
            self.empty_repository.add(Contractor(None, "John Doe"))
        self.assertIn("already exists", str(context.exception))

    def test_add_duplicate_name_case_insensitive(self):
        """Test that name comparison is case insensitive"""
        self.empty_repository.add(Contractor(None, "John Doe"))
        with self.assertRaises(ValueError):
            self.empty_repository.add(Contractor(None, "JOHN DOE"))
        with self.assertRaises(ValueError):
            self.empty_repository.add(Contractor(None, "john doe"))

    def test_find_by_id_existing(self):
        """Test finding an existing contractor by ID"""
        contractor = self.populated_repository.find_by_id(0)
        self.assertIsNotNone(contractor, "Contractor should not be None")
        if contractor is not None:  # This check ensures contractor is not None before accessing name
            self.assertEqual(contractor.name, "Alice Smith")

    def test_find_by_id_non_existing(self):
        """Test finding a non-existing contractor by ID"""
        contractor = self.populated_repository.find_by_id(999)
        self.assertIsNone(contractor)

    def test_find_by_name_existing(self):
        """Test finding an existing contractor by name"""
        contractor = self.populated_repository.find_by_name("Alice Smith")
        self.assertIsNotNone(contractor)
        if contractor is not None:
            self.assertEqual(contractor.id, 0)

    def test_find_by_name_case_insensitive(self):
        """Test that finding by name is case insensitive"""
        contractor = self.populated_repository.find_by_name("ALICE SMITH")
        self.assertIsNotNone(contractor)
        if contractor is not None:
            self.assertEqual(contractor.name, "Alice Smith")

    def test_find_by_name_non_existing(self):
        """Test finding a non-existing contractor by name"""
        contractor = self.populated_repository.find_by_name("Non Existent")
        self.assertIsNone(contractor)

    def test_find_by_name_variations(self):
        """Test finding contractors with various name formats"""
        test_cases = [
            ("", False),
            ("   ", False),
            ("Alice Smith", True),
            ("Bob Jones", True),
            ("Unknown Person", False),
            ("alice smith", True),
            ("ALICE SMITH", True),
        ]

        for name, expected_found in test_cases:
            with self.subTest(name=name):
                contractor = self.populated_repository.find_by_name(name)
                self.assertEqual(contractor is not None, expected_found)

    def test_sequential_id_assignment(self):
        """Test that IDs are assigned sequentially"""
        names = ["First", "Second", "Third"]
        for i, name in enumerate(names):
            contractor = Contractor(None, name)
            self.empty_repository.add(contractor)
            self.assertEqual(contractor.id, i)

if __name__ == '__main__':
    unittest.main()
