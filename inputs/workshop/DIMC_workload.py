workload = {
   0: {'equation': 'O[b][k][ox][oy]+=W[k][c][fx][fy]*I[b][c][ix][iy]',
        'dimension_relations': ['ix= 1*ox + 1*fx', 'iy= 1*oy + 1*fy'],
        'loop_dim_size': {'B': 1, 'C': 128, 'K': 128, 'OX': 40, 'OY': 40, 'FX':3,'FY':3, 'G':1},
        'operand_precision': {'O': 4,  'O_final': 4, 'W': 4, 'I': 4},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ['K'], 'D2': ['C','FX','FY'], 'D3': ['OX']},
        'temporal_ordering': [('OX', 'all'), ('OY', 'all'), ('FX','all'), 
            ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'W': 'I1', 'I': 'I2'},
    }
}
