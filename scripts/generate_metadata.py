#! env python

import json
import plistlib
import textwrap


plist = "/Applications/HomeKit Accessory Simulator.app/Contents/Frameworks/HAPAccessoryKit.framework/Versions/A/Resources/default.metadata.plist"
with open(plist, "rb") as fp:
    data  = plistlib.load(fp)


enrichment = {
    "00000120-0000-1000-8000-0026BB765291": {
        "struct": ".structs.StreamingStatus"
    },
    "00000117-0000-1000-8000-0026BB765291": {
        "struct": ".structs.SelectedRTPStreamConfiguration"
    },
    "00000115-0000-1000-8000-0026BB765291": {
        "struct": ".structs.SupportedAudioStreamConfiguration"
    },
    "00000114-0000-1000-8000-0026BB765291": {
        "struct": ".structs.SupportedVideoStreamConfiguration"
    },
}


characteristics = {}

for char in data.get('Characteristics', []):
    name = char['Name'].replace(".", "_").replace(" ", "_").upper()

    c = characteristics[char['UUID']] = {
        'name': name,
        'description': char['Name'],
    }

    if char.get('Properties'):
        c['perms'] = []
        for perm in char.get('Properties'):
            if perm == "read":
                c['perms'].append("pr")
            if perm == "write":
                c['perms'].append("pw")
            if perm == "cnotify":
                c['perms'].append("ev")

    if char.get('Format'):
        c['format'] = char['Format']

    if char.get('Unit'):
        c['unit'] = char['Unit']

    if 'Constraints' not in char:
        continue

    constraints = char['Constraints']

    if constraints.get('MaximumValue'):
        c['max_value'] = constraints['MaximumValue']
    if constraints.get('MaximumValue'):
        c['min_value'] = constraints['MinimumValue']
    if constraints.get('StepValue'):
        c['step_value'] = constraints['StepValue']


with open("aiohomekit/model/characteristics/data.py", "w") as fp:
    fp.write("# AUTOGENERATED, DO NOT EDIT\n\n")

    for char in enrichment.values():
        if "struct" in char:
            imp, frm = char["struct"].rsplit(".", 1)
            fp.write(f"from {imp} import {frm}\n")
    fp.write("\n\n")

    fp.write("characteristics = {\n")

    for char_uuid, char in characteristics.items():
        name = json.dumps(char["name"])
        description = json.dumps(char["description"])
        perms = json.dumps(char["perms"])
        format = json.dumps(char["format"])

        fp.write(f"    \"{char_uuid}\": {{\n")
        fp.write(f"        \"name\": {name},\n")
        fp.write(f"        \"description\": {description},\n")
        fp.write(f"        \"perms\": {perms},\n")
        fp.write(f"        \"format\": {format},\n")

        struct = enrichment.get(char_uuid, {}).get("struct")
        if struct:
            _, frm = struct.rsplit(".", 1)
            fp.write(f"        \"struct\": {frm},\n")

        if "unit" in char:
            unit = json.dumps(char["unit"])
            fp.write(f"        \"unit\": {unit},\n")

        if "max_value" in char:
            max_value = json.dumps(char["max_value"])
            fp.write(f"        \"max_value\": {max_value},\n")

        if "min_value" in char:
            min_value = json.dumps(char["min_value"])
            fp.write(f"        \"min_value\": {min_value},\n")

        if "step_value" in char:
            step_value = json.dumps(char["step_value"])
            fp.write(f"        \"step_value\": {step_value},\n")

        fp.write("    },\n")
        pass

    fp.write("}\n")

from aiohomekit.model.services import ServicesTypes

for serv in data.get('Services', []):
    name = serv['Name'].replace(" ", "_").upper()
    short = ServicesTypes.get_short_uuid(serv['UUID'])
    print(f'{name} = "{short}"')


services = {}

for serv in data.get('Services', []):
    name = serv['Name'].replace(" ", "_").upper()

    s = services[serv['UUID']] = {
        'name': name,
        'description': serv['Name'],
        'required': serv.get("RequiredCharacteristics", []),
        'optional': serv.get("OptionalCharacteristics", []),
    }


with open("aiohomekit/model/services/data.py", "w") as fp:
    fp.write(textwrap.dedent("""
    # AUTOGENERATED, DO NOT EDIT

    services = 
    """).strip())
    fp.write(" " + json.dumps(services, indent=4))
    fp.write("\n")