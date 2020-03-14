#!/usr/bin/env python3

import boto3

client = boto3.client('lambda')

functions=client.list_functions(
    MaxItems=50
)

funcs=[]

while functions.get("NextMarker") is not None:
    funcs += functions.get('Functions')
    functions=client.list_functions(
        MaxItems=50,
        Marker=functions.get("NextMarker")
    )
for f in funcs:
    versions = client.list_versions_by_function(
        FunctionName=f.get('FunctionName')
    )
    
    if (len(versions.get('Versions')) is 1):
        continue
    print (f.get('FunctionName') +" has " + str(len(versions.get('Versions'))) +" versions")
    
    # for v in versions.get('Versions'):
    #     if v.get("Version") == "$LATEST":
    #         continue
    #     print(v.get("Version"))