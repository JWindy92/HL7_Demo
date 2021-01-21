def getDictFromHL7(segment):

    d = {}
    d['version'] = segment.version
    d['field'] = segment.name

    data = {}

    for s in segment.children:
        data[s.long_name] = s.value.replace('^',' ')
    
    d['data'] = data

    return d

def value_or_default(req, key='', default=''):

    try:
        return (req.GET[key] if req.method == 'GET' else req.POST[key])

    except Exception as e:
        print(e)
        return default