from _mappers.sources import django


def _data_source_factory(fields, entity_factory, data_source, config):
    if django._is_django_model(data_source):
        django._validate_fields(fields, data_source, config)
        return django._ValuesList(
            fields,
            entity_factory,
            django._get_values_list_arguments(fields, config),
            django._get_values_list_iterable_class(entity_factory, fields, config),
        )
    else:
        raise Exception
