from jsonschema import ValidationError, FormatChecker, validate
from .schemas import SCHEMA_MAPPING, get_schema


def validator_wrapper(instance, schema):
    """ validator_wrapper

    Wrapper function for validating a JSON instance against a given schema.

    Parameters:
        instance - JSON instance to validate
        schmea - JSON defined schema for validation

    Returns:
        validated - whether the instance is valid
    """
    validated = True
    try:
        # FormatChecker specifies checking date-time formatted strings
        # according to RFC-3339
        validate(instance, schema, format_checker=FormatChecker())

    # Catching ValidationError so that we can raise an InvalidAPIUsage instead
    except ValidationError:
        validated = False
    return validated


def generate_validator(model):
    """ generate_validator

    Generates a validation function based on the schema corresponding to
    the provided model. This will be used to validate JSON request bodies,
    for POST requests when creating new data.

    Parameters:
        model - Model class for the validator

    Returns:
        schema_validator(instance) - validation function for the model
    """

    schema = SCHEMA_MAPPING[model]

    def schema_validator(instance):
        return validator_wrapper(instance, schema)

    return schema_validator


def get_request_validator(instance):
    """ get_request_validator

    Validation function for validating a JSON instance against the defined
    GET body request JSON schema.

    Parameters:
        instance - JSON instance to validate

    Returns:
        True/False whether the instance is valid        
    """
    return validator_wrapper(instance, get_schema)
