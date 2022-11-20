workload = {
   0: {'equation': 'O[ox][oy][k]+=W[fx][fy][c][k]*I[ix][iy][c]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'OX': 4, 'OY': 4, 'K': 512, 'C': 128, 'FX': 3, 'FY': 3},
        'operand_precision': {'O': 8,  'O_final': 8, 'W': 2, 'I': 8},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ['C','FX','FY'], 'D2': ['K']},
        'temporal_ordering': [('OX', 'all'), ('OY', 'all'), ('FX','all'), 
            ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'W': 'I1', 'I': 'I2'},
        'operand_source': {'W': [], 'I': []}
    }
}




