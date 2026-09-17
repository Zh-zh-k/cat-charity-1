from app.crud.base import CRUDBase
from app.models.donation import Donation


class DonationCRUD(CRUDBase):
    pass


donation_crud = DonationCRUD(Donation)
