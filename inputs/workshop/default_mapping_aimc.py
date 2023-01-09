mapping = {
    "default": {
        "core_allocation": 1,
        'operand_precision': {'O': 4, 'O_final': 4, 'W': 4, 'I': 4},
        'spatial_mapping_hint': {'D1': ['OX', 'K'], 'D2': ['C','FX','FY'], 'D3':['OX','OY','FX','FY']} ,
        "memory_operand_links": {'O': 'O', 'W': 'I1', 'I': 'I2'},
        'temporal_ordering': [('OX', 'all'), ('OY', 'all'),   ('K', 'all'), ('FX','all'), 
            ('FY','all'), ('C','all')]
    }
}
