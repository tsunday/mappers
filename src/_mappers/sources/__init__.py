from _mappers.sources import django


def data_source_factory(fields, entity_factory, data_source, config):
    if django.is_django_model(data_source):
        django.validate_fields(fields, data_source, config)
        return django.ValuesList(
            fields,
            entity_factory,
            django.get_values_list_arguments(fields, config),
            django.get_values_list_iterable_class(entity_factory, fields, config),
        )
    else:
        raise Exception
