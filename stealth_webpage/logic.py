# where: supply list with dictionaries
# which_field: supply string data (field name)
# which value: supply value, which corresponds for this field
def check_if_value_is_present(where, which_field, which_value):
    for el in where:
        if el[which_field] == which_value:
            return True
    return False