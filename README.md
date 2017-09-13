# OAS file dependency injector
Unifying multiple OAS definition files into 1 file, according to dependencies.


### Installation
[Python 3.6](https://www.python.org/downloads/release/python-362/) is required to run.

__pip__:
```sh
$ pip install git+https://github.com/omerbn/python-oas-dependency-injector.git
```

### Usage
Command-line:

```sh
$ oas_dependency_injection FILENAME --target_filename=TARGET_FILENAME --models-library=PYTHON_MODELS_LIB
```
In Python:
```sh
import oas_dependency_injection

oas_dependency_injection.entrypoint_viacode('./myfile.yml',
                                              target_filename='./myfile_pp.yml',
                                              models_lib='mylib.models')
```

| arg | description |
| ------ | ------ |
| filename | file path to process |
| target_filename | target filename (unified file) |
| models_lib (--models-lib) | python models lib which inlucdes the required models files|


### Example

##### target_file.yml:

```sh
swagger: '2.0'
info:
  version: '1.0'
schemes:
 - https
paths:
  /request:
    post:
      parameters:
        - in: body
          name: data
          schema:
            $ref: "#/definitions/RequestBody"
      responses:
        200:
          description: "OK"
          schema:
            $ref: "#/definitions/ResponseBody"

definitions:
  Error:
    type: object
    properties:
      error:
        type: string
        description: "Error message"
  RequestBody:
    type: object
    properties:
      session-type:
        $ref: "models:filename/sessionType"
      username:
        type: string
  ResponseBody:
    type: object
    properties:
      error:
        $ref: "#/definitions/Error"
      results:
        $ref: "models:filename/Results"

```

##### models\_lib\filename.yml:
```sh
definitions:
    Result:
        type: object
        properties:
            text:
                type: string
            id:
                type: number
    Results:
        type: array
        items:
            $ref: "#/definitions/Result"
    sessionType:
        type: string
        enum: [USER, ADMIN]
    Type1:
        type: object
        properties:
            name:
                type: string
```

#### output file
```sh
swagger: '2.0'
info:
  version: '1.0'
schemes:
 - https
paths:
  /request:
    post:
      parameters:
        - in: body
          name: data
          schema:
            $ref: "#/definitions/RequestBody"
      responses:
        200:
          description: "OK"
          schema:
            $ref: "#/definitions/ResponseBody"

definitions:
    Result:
        type: object
        properties:
            text:
                type: string
            id:
                type: number
    Results:
        type: array
        items:
            $ref: "#/definitions/Result"
    sessionType:
        type: string
        enum: [USER, ADMIN]
    Error:
        type: object
        properties:
            error:
                type: string
            description: "Error message"
    RequestBody:
        type: object
        properties:
            session-type:
                $ref: "#/definitions/sessionType"
            username:
                type: string
    ResponseBody:
        type: object
        properties:
            error:
                $ref: "#/definitions/Error"
            results:
                $ref: "#/definitions/Results"

```

### Development

Want to contribute? Great!
Fell free to make pull requests

### License
GNU GPL 3.0



**Free Software, Hell Yeah!**