from uuid import UUID


class CountryNotFoundError(Exception):
    def __init__(self, country_id: UUID):
        self.country_id = country_id
        super().__init__(f"Country with id {country_id} not found")
