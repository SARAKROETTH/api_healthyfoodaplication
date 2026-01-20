import phonenumbers
from phonenumbers import NumberParseException

def validate_phone(phone: str)-> bool:
    try:
        parsed =phonenumbers.parse(phone,None)
        return(
            phonenumbers.is_possible_number(parsed)
            and phonenumbers.is_valid_number(parsed)
        )
    except NumberParseException:
        return False