from django.http import Http404


def object_exists_or_404(klass, pk, *args, **kwargs):
    queryset = klass
    if hasattr(klass, "_default_manager"):  # pylint: disable=protected-access
        queryset = klass._default_manager.all()  # pylint: disable=protected-access
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            f"First argument to object_exists_or_404() must be a Model, Manager, or \
            QuerySet, not {klass__name}."
        )
    if not queryset.filter(pk=pk, *args, **kwargs).exists():
        name = queryset.model._meta.object_name  # pylint: disable=protected-access
        raise Http404(f"No {name} matches the given query.")
    return True
