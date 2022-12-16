workload = {
   0: {'equation': 'O[b][k][ox][oy]+=W[k][c][fx][fy]*I[b][c][ix][iy]',
        'dimension_relations': ['ix= ox + fx', 'iy= oy + fy'],
        'loop_dim_size': {'B': 1, 'C': 48, 'K': 48, 'OX': 1024, 'OY': 1, 'FX':1,'FY':1},
        'operand_precision': {'O': 8,  'O_final': 8, 'W': 8, 'I': 8},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ['C','FX','FY'], 'D2': ['K']},
        'temporal_ordering': [('OX', 'all'), ('OY', 'all'), ('FX','all'), 
            ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'W': 'I1', 'I': 'I2'},
        'operand_source': {'W': [], 'I': []}
    }
}
