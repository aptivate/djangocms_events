from __future__ import unicode_literals, absolute_import

from django import forms
from django.utils.translation import ugettext_lazy as _
from haystack.forms import SearchForm

from django_harness.form_helpers import (month_range, year_range_relative_year,
    clean_month_year_helper)


class EventSearchForm(SearchForm):
    from_month = forms.ChoiceField(choices=month_range(),
            required=False,
            widget=forms.Select(attrs={'class': 'month_selector'}))
    from_year = forms.ChoiceField(choices=((0, _('no years')),),
            required=False,
            widget=forms.Select(attrs={'class': 'year_selector'}))
    to_month = forms.ChoiceField(choices=month_range(),
            required=False,
            widget=forms.Select(attrs={'class': 'month_selector'}))
    to_year = forms.ChoiceField(choices=((0, _('no years')),),
            required=False,
            widget=forms.Select(attrs={'class': 'year_selector'}))

    def __init__(self, *args, **kwargs):
        super(EventSearchForm, self).__init__(*args, **kwargs)

        self.fields['q'].label = _('Keywords')
        self.fields['from_year'].choices = year_range_relative_year()
        self.fields['to_year'].choices = year_range_relative_year()

    """
    def clean_month_year(self, cleaned_data, prefix):
        if prefix == 'after':
            self.after_date = clean_month_year_helper(cleaned_data, prefix, 'start')
        else:
            self.before_date = clean_month_year_helper(cleaned_data, prefix, 'end')
    """

    def clean(self):
        """ It is an error for a month to be selected without a year """
        cleaned_data = super(EventSearchForm, self).clean()
        self.from_date = clean_month_year_helper(cleaned_data, 'from_', 'start')
        self.to_date   = clean_month_year_helper(cleaned_data, 'to_', 'end')
        if self.from_date and self.to_date:
            if self.from_date > self.to_date:
                raise forms.ValidationError(_('The "From:" date cannot be after the "To:" date.'))
        return cleaned_data

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        have_filter = False
        all = self.searchqueryset.all()

        if self.cleaned_data['q']:
            have_filter = True
            sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])
        else:
            sqs = all
            # will return none() later unless some non-keyword search
            # conditions are added below.

        if self.from_date:
            have_filter = True

            # Old, incorrect query: excludes events started before the from
            # date but still running:
            # sqs = sqs.filter(start_date__gte=self.from_date)

            # To be completely correct, we should only look at the end date.
            # Two things complicate this: first, end date is optional, in
            # which case the start date is also the end date; and in Whoosh,
            # if no end date is provided, the field is not stored at all, so
            # we can't query on it. Therefore this condition doesn't work:

            #sqs = sqs & (
            #    all.filter(end_date='', start_date__gte=self.from_date) |
            #    all.filter(end_date__ne='', end_date__gte=self.from_date))

            # However, since the start date must be before the end date,
            # if start_date >= self.from_date then end_date is too, whether
            # or not "end_date=''" (which means it's the same as start_date).
            # So we can remove "end_date=''" without changing the results.
            #
            # And if end_date is not present in a record, then that record
            # will never match end_date >= self.from_date, so the additional
            # condition "end_date__ne=''" is redundant. So we can simplify
            # the whole query to this one, which does work:

            sqs = sqs & (
                all.filter(start_date__gte=self.from_date) |
                all.filter(end_date__gte=self.from_date))

        if self.to_date:
            have_filter = True
            sqs = sqs.filter(start_date__lte=self.to_date)

        self.is_valid_filter = have_filter

        if not have_filter:
            return self.no_query_found()

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
