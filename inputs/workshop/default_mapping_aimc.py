mapping = {
    "default": {
        "core_allocation": 1,
        'operand_precision': {'O': 8, 'O_final': 8, 'W': 8, 'I': 8},
        'spatial_mapping_hint': {'D1': ['OX', 'K'], 'D2': ['C','FX','FY'], 'D3':['K','C', 'FY', 'G', 'OX', 'OY']},
        "memory_operand_links": {'O': 'O', 'W': 'I1', 'I': 'I2'},
        'temporal_ordering': [('OX', 'all'), ('OY', 'all'),   ('K', 'all'), ('FX','all'), 
            ('FY','all'), ('C','all')]
    }
}
