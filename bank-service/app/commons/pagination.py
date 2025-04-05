from flask import url_for, request, jsonify

DEFAULT_PAGE_NUMBER = 1
DEFAULT_PAGE_SIZE = 5


def extract_pagination(page=None, per_page=None):
    page_number = int(page) if page is not None else DEFAULT_PAGE_NUMBER
    page_size = int(per_page) if per_page is not None else DEFAULT_PAGE_SIZE
    return page_number, page_size


def apply_filters(query):
    filter_params = {}
    for key, value in request.args.items():
        if key not in ['page_number', 'page_size']:
            filter_params[key] = value

    return query.filter_by(**filter_params), filter_params


def paginate(query, schema):
    page_number, page_size = extract_pagination(page=request.args.get(
        'page_number'), per_page=request.args.get('page_size'))

    query, filter_params = apply_filters(query)

    page_obj = query.paginate(page=page_number, per_page=page_size)

    next_ = url_for(
        request.endpoint,
        page_number=page_obj.next_num if page_obj.has_next else page_obj.page,
        page_size=page_size,
        **request.view_args,
        **filter_params
    )
    prev_ = url_for(
        request.endpoint,
        page_number=page_obj.prev_num if page_obj.has_prev else page_obj.page,
        page_size=page_size,
        **request.view_args,
        **filter_params
    )

    return {
        'total': page_obj.total,
        'pages': page_obj.pages,
        'next': next_,
        'prev': prev_,
        'results': schema.dump(page_obj.items, many=True)
    }, 200
