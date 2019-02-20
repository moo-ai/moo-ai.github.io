import yaml


def analysis_yaml(yaml_file):
    with open(yaml_file) as input_yaml:
        try:
            parsed = yaml.safe_load(input_yaml.read())
        except yaml.YAMLError as e:
            raise
    framework = parsed['framework']
    for info in framework:
        if info.get('name'):
            framework_name = info['name']
        elif info.get('version'):
            framework_version = info['version']
        elif info.get('runtime'):
            framework_runtime = info['runtime']
    entry_point = parsed['entry_point']
    output_folder = parsed.get('output_folder')

    with open('framework_name.txt', 'w') as metadata:
        metadata.write(framework_name + '\n')
    with open('framework_version.txt', 'w') as metadata:
        metadata.write(framework_version + '\n')
    with open('framework_runtime.txt', 'w') as metadata:
        metadata.write(framework_runtime + '\n')
    with open('entry_point.txt', 'w') as metadata:
        metadata.write(entry_point + '\n')
    if output_folder:
        with open('output_folder.txt', 'w') as metadata:
            metadata.write(output_folder + '\n')


analysis_yaml('metadata.yaml')
