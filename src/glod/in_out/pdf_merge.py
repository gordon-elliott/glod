#  __copyright__ = "Copyright (c) Gordon Elliott 2020"
from subprocess import run

FDF_HEADER = """%FDF-1.2
%âãÏÓ
1 0 obj 
<< /FDF 
<< /Fields [
"""
FDF_FOOTER = """
] >> >>
endobj 
trailer
<< /Root 1 0 R >>
%%EOF
"""


def fill_form(template_filename, output_path, data_dict):
    fdf_str = _generate_fdf(data_dict)
    _run_pdftk(template_filename, fdf_str, output_path)


def _generate_fdf(data):
    fields = "\n".join(_fdf_fields(data))
    return f"{FDF_HEADER}{fields}{FDF_FOOTER}"


def _fdf_fields(data):
    for field_name, value in data.items():
        yield f"<< /T ({field_name}) /V ({value}) >>"


def _run_pdftk(input_path, fdf, output_path):
    cmd = ["pdftk", input_path, "fill_form", "-", "output", output_path, "flatten"]
    run(cmd, input=fdf.encode("utf-8"), check=True)
