from pydantic import BaseModel


class Support(BaseModel):
    support_phone: str
    contact_url: str
    help_url: str
    email_web_form_url: str
    name: str
