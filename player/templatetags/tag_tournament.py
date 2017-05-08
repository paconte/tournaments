from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_item_tuple_first(dictionary, key):
    return dictionary.get(key)[0].person.get_full_name_reverse()


@register.filter
def get_item_tuple_second(dictionary, key):
    return dictionary.get(key)[1].person.get_full_name_reverse()
