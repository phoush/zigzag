workload = {
   0: {'equation': 'O[ox][oy][k]+=W[fx][fy][c][k]*I[ix][iy][c]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'OX': 4, 'OY': 4, 'K': 8, 'C': 3, 'FX': 3, 'FY': 3},
        'operand_precision': {'O': 8,  'O_final': 8, 'W': 2, 'I': 8},
        'core_allocation': 1,
        'spatial_mapping': {'D1_c': ('C', 3), 'D1_fx': ('FX', 3), 'D1_fy': ('FY', 3), 'D2': ('K', 8)},  # Must match with the dimensions of core 1
        'temporal_ordering': [('OX', 4), ('OY', 4)],
        'memory_operand_links': {'O': 'O', 'W': 'I1', 'I': 'I2'},
        'operand_source': {'W': [], 'I': []}
    }
}
