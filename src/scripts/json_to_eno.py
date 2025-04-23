import json
import enolib
import sys

def json_to_eno_lines(data, indent=0, separator=':'):
    lines = []
    prefix = '  ' * indent

    if isinstance(data, dict):
        for key, value in data.items():
            if value is False:  # Exclure les clés avec une valeur False
                continue
            if value is True:  # Afficher uniquement la clé si la valeur est True
                lines.append(f'{prefix}{key}')
                continue
            if isinstance(value, dict):
                lines.append(f'{prefix}{key}:')
                lines.extend(json_to_eno_lines(value, indent + 1, ' ='))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, (dict, list)):
                        lines.extend(json_to_eno_lines(item, indent))
                    else:
                        lines.append(f'{prefix}  - {item}')
            elif isinstance(value, str) and '\n' in value:  # Multiline field
                lines.append(f'{prefix}-- {key}')
                lines.extend(f'{prefix}{line}' for line in value.splitlines())
                lines.append(f'{prefix}-- {key}')
            else:
                lines.append(f'{prefix}{key}{separator} {value}')
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.extend(json_to_eno_lines(item, indent))
            else:
                lines.append(f'{prefix}- {item}')
    else:
        lines.append(f'{prefix}{data}')

    return lines

def main():
    if len(sys.argv) != 2:
        print("Usage : python json_to_eno.py <fichier.json>", file=sys.stderr)
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON : {e}", file=sys.stderr)
        sys.exit(1)

    eno_lines = json_to_eno_lines(json_data)
    eno_string = '\n'.join(eno_lines)

    try:
        enolib.parse(eno_string)
    except enolib.ParseError as error:
        print("❌ Le contenu généré n'est pas un Eno valide :", file=sys.stderr)
        print(error.text, file=sys.stderr)
        sys.exit(1)

    print(eno_string)

if __name__ == '__main__':
    main()
