
def validate_obj_type(obj: object, name: str, types: list or object):
    """
    validate object is of a given type
    :param obj: object type validate its type
    :param name: name of object
    :param types: types list of types, or a type
    :return:
    """
    if type(types) is not list:
        types = [types]

    # validate cmd
    if type(obj) not in types:
        raise RuntimeError(f"invalid {name} type '{type(obj)}', supported types: {types}")
