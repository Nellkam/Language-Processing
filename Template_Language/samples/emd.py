from templo import template

records = {
    'cities': {
        'Braga': [
            {
                'id': 'A3EF90',
                'firstname': 'Carlos',
                'lastname': 'Ferreira',
            },
        ],
        'Porto': [
            {
                'id': '8FD34B',
                'firstname': 'José',
                'lastname': 'Peixoto',
            },
            {
                'id': '58F4CA',
                'firstname': 'Manuel',
                'lastname': 'Carvalho',
            },
        ]
    },
}

with open ("emd_tmpl.html", 'r') as tmpl:
    html = template(tmpl, records)

with open ("emd.html", "w") as fout:
    fout.write(html)
