def get_properties(dict):

    dict = {name : {key : float(value) for key, value in body.items()} for name, body in dict.items()}

    return dict