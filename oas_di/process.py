import os
import codecs
import yaml
import json

_files = {}
_models_folder = None
_files_synonyms = {}


def process_file(cmd_args):
    global _models_folder

    # models folder
    if cmd_args.models_lib:
        import importlib
        my_module = importlib.import_module(cmd_args.models_lib)
        if not my_module:
            raise ImportError("Invalid import " + cmd_args.models_lib)
        _models_folder = os.path.abspath(os.path.dirname(my_module.__file__))

    # extracting content and refs
    file_json, refs = _read_file(cmd_args.filename)

    if len(refs) == 0:
        return

    # target filename
    if not cmd_args.target_filename:
        source_filename = os.path.basename(cmd_args.filename)
        tmp_target = source_filename[0:source_filename.rfind('.')] + "_pp" + source_filename[source_filename.rfind('.'):]
        cmd_args.target_filename = cmd_args.filename.replace(source_filename, tmp_target)

    # processing files
    for filename in refs:
        if filename in _files:
            continue
        _process_file_internal(filename)

    # processing json
    new_desf = RefFixer().go(file_json)
    file_json['definitions'] = {**file_json.get('definitions', {}), **new_desf}

    # saving file
    with codecs.open(cmd_args.target_filename, 'w', 'utf-8') as f:
        is_yaml = cmd_args.filename.endswith('.yml') or cmd_args.filename.endswith('.yaml')
        is_json = cmd_args.filename.endswith('.js') or cmd_args.filename.endswith('.json')

        if is_yaml:
            yaml.dump(file_json, f, allow_unicode=True)
        elif is_json:
            json.dump(file_json, f)


def _process_file_internal(filename):
    file_json, refs = _read_file(filename)
    _files[filename] = file_json.get('definitions', {})

    for filename in refs:
        if filename in _files:
            continue
        _process_file_internal(filename)


def _read_file(filename):
    global _files_synonyms

    is_yaml = filename.endswith('.yml') or filename.endswith('.yaml')
    is_json = filename.endswith('.js') or filename.endswith('.json')

    # reading file
    with codecs.open(filename, 'r', 'utf-8') as fd:
        content = fd.read()
        if is_yaml:
            api_file_dict = yaml.load(content)
        elif is_json:
            api_file_dict = json.loads(content)
        else:
            raise ValueError("invalid file type")

        # making a list of all files to load
        refs = []
        ndx = content.find("$ref")
        while ndx != -1:
            ndx = content.find(":", ndx)
            if ndx == -1:
                raise ValueError("")
            ndx += 1
            # skipping whitespace
            while content[ndx].isspace():
                ndx += 1
            ending_char = None
            if content[ndx] == "'":
                ending_char = "'"
                ndx += 1
            elif content[ndx] == '"':
                ending_char = '"'
                ndx += 1

            if ending_char:
                end_ndx = content.find(ending_char, ndx)
            else:
                end_ndx = ndx
                while not content[end_ndx].isspace():
                    end_ndx += 1

            ref = content[ndx:end_ndx]
            if _models_folder and ref.startswith("models:"):
                model_filename, filename, model = parse_model(ref)
                if os.path.exists(model_filename + ".json"):
                    model_filename += ".json"
                elif os.path.exists(model_filename + ".js"):
                    model_filename += ".js"
                elif os.path.exists(model_filename + ".yaml"):
                    model_filename += ".yaml"
                elif os.path.exists(model_filename + ".yml"):
                    model_filename += ".yml"
                else:
                    raise FileNotFoundError("cannot find module: " + model_filename)
                _files_synonyms[filename] = model_filename
                refs.append(model_filename)
            ndx = content.find("$ref", end_ndx)

        return api_file_dict, refs


def parse_model(text):
    global _models_folder

    text = text.split('/')
    file_name = text[0][7:]
    type_name = text[1]
    return os.path.join(_models_folder, file_name), file_name, type_name


class RefFixer(object):
    def __init__(self):
        self.new_definitions = {}

    def go(self, json):
        self._rec(json)
        return self.new_definitions

    def _rec(self, node, filename=None):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == '$ref':
                    if v.startswith("models:"):
                        model_filename, filename, model = parse_model(v)

                        # getting model definition
                        model_def = _files.get(_files_synonyms[filename]).get(model)
                        model_name = filename + "_" + model
                        node[k] = "#/definitions/" + model_name
                    elif filename and v.startswith("#/definitions/"):
                        # getting model definition
                        model = v.split('/')[2]
                        model_def = _files.get(_files_synonyms[filename]).get(model)
                        model_name = filename + "_" + model
                        node[k] = "#/definitions/" + model_name
                    else:
                        model_name = None

                    if model_name and model_name not in self.new_definitions:
                        self.new_definitions[model_name] = model_def
                        self._rec(model_def, filename)


                else:
                    self._rec(v, filename)
        elif isinstance(node, list):
            for x in node:
                self._rec(x, filename)
