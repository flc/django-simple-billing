import StringIO

from django.template.loader import render_to_string

import weasyprint


def generate_pdf(
    template_name,
    context,
    file_object=None,
    url_fetcher=weasyprint.default_url_fetcher,
    ):
    if not file_object:
        file_object = StringIO.StringIO()
    if not context:
        context = {}
    html = render_to_string(template_name, context)
    weasyprint.HTML(string=html, url_fetcher=url_fetcher).write_pdf(file_object)
    return file_object
