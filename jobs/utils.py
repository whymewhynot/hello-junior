def get_user_search_params(request):
    user = request.user
    search_params = dict()
    if user.city:
        search_params['city'] = user.city.id
    if user.skills:
        search_params['skills'] = list(user.skills.values_list('id', flat=True))
    if user.remote:
        search_params['remote'] = user.remote
    return search_params


def create_paginate_link(search_params):
    paginate_params = []
    for key, value in zip(search_params.keys(), search_params.values()):
        if isinstance(value, list):
            paginate_params += [f'&{key}={i}' for i in value]
        else:
            paginate_params.append(f'&{key}={value}')
    paginate_link = ''.join(paginate_params)

    return paginate_link