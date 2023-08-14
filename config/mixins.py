class CompanyFilterMixin:
    """
    Mixin to filter queryset by the user's company.
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(company=self.request.user.company)
