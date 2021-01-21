from django.shortcuts import render

from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
import json

from django.views.decorators.csrf import csrf_exempt
from .utils import getDictFromHL7, value_or_default
from django.views.decorators.csrf import csrf_exempt
from json2html import json2html
from dicttoxml import dicttoxml
import yaml
from hl7apy.parser import parse_segment
from .forms import Simple_submit_Form



@csrf_exempt
def hl7_web_view(req):
    d = {}
    format = value_or_default(req, 'format', 'json')
    data = value_or_default(req, 'data', '')
    try:

        d = getDictFromHL7(parse_segment(data))
    except Exception as e:
        d['error'] = str(e)

    if format == 'json':
        return HttpResponse(json.dumps(d), content_type='application/json')

    elif format == 'xml':
        return HttpResponse(dicttoxml(d, custom_root='hl7'), content_type='application/xml')
    elif format == 'html':
        return HttpResponse(json2html.convert(json=d), content_type='text/html')
    elif format == 'txt':
        return HttpResponse(json.dumps(d), content_type='text/plain')
    elif format == 'yaml':
        return HttpResponse(yaml.dump(d), content_type='text/yaml')

    else:
        return HttpResponse(' unavailable format', content_type='application/json')

def render_form_View(req):
    samples = [
        {'type': 'PID', 'msg': 'PID|||56782445^^^UAReg^PI||KLEINSAMPLE^BARRY^Q^JR||19620910|M||2028-9^^HL70005^RA99113^^XYZ|260 GOODWIN CREST DRIVE^^BIRMINGHAM^AL^35209^^M~NICKELL’S PICKLES^10000 W 100TH AVE^BIRMINGHAM^AL^35200^^O|||||||0105I30001^^^99DEF^AN'},
        {'type': 'ENV', 'msg': 'EVN||200605290901||||200605290900'},
        {'type': 'PV1', 'msg': 'PV1||I|W^389^1^UABH^^^^3||||12345^MORGAN^REX^J^^^MD^0010^UAMC^L||67890^GRAINGER^LUCY^X^^^MD^0010^UAMC^L|MED|||||A0||13579^POTTER^SHERMAN^T^^^MD^0010^UAMC^L|||||||||||||||||||||||||||200605290900'},
        {'type': 'OBX', 'msg': 'OBX|2|NM|^Body Weight||79|kg^Kilogram^ISO+|||||F'},
        {'type': 'DG1', 'msg': 'DG1|1||786.50^CHEST PAIN, UNSPECIFIED^I9|||A'},
        {'type': 'MSH', 'msg': 'MSH|^~\&|MegaReg|XYZHospC|SuperOE|XYZImgCtr|20060529090131-0500||ADT^A01^ADT_A01|01052901|P|2.5'},
        {'type': 'PID', 'msg': 'PID|||56782445^^^UAReg^PI||KLEINSAMPLE^BARRY^Q^JR||19620910|M||2028-9^^HL70005^RA99113^^XYZ|260 GOODWIN CREST DRIVE^^BIRMINGHAM^AL^35209^^M~NICKELL’S PICKLES^10000 W 100TH AVE^BIRMINGHAM^AL^35200^^O|||||||0105I30001^^^99DEF^AN'},
        {'type': 'AL1', 'msg': 'AL1|1||^ASPIRIN'},

    ]

    return render(req, 'display_form.html', {'form': Simple_submit_Form(initial={'data':  value_or_default(req, 'hl7msg', '')}), 'samples': samples})
