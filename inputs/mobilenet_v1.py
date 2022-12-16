workload = {
    0:{  #conv1, stride 2
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K': 32, 'C': 3, 'OY': 112, 'OX': 112, 'FY': 3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},##confirm...
        'operand_source':{'W': [], 'I': []},
        #'constant_operands': ['W'],## confirm...
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('K')},## confirm...
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    1: {  # conv2, depth-wise, stride 1
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 32, 'OY': 112, 'OX': 112, 'FY': 3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [0]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    2: {  # conv3, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':64, 'C': 32, 'OY': 112, 'OX': 112, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [1]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    3: {  # conv4, depth-wise, stride 2
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 64, 'OY': 56, 'OX': 56, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [2]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    4: {  # conv5, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':128, 'C': 64, 'OY': 112, 'OX': 112, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [3]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    5: {  # conv6, depth-wise, stride 1
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 128, 'OY': 56, 'OX': 56, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [4]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    6: {  # conv7, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':128, 'C': 128, 'OY': 56, 'OX': 56, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [5]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    7: {  # conv8, depth-wise, stride 2
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 128, 'OY': 28, 'OX': 28, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [6]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    8: {  # conv9, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':256, 'C': 128, 'OY': 28, 'OX': 28, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [7]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    9: {  # conv10, depth-wise, stride 1
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 256, 'OY': 28, 'OX': 28, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [8]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    10: {  # conv11, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':256, 'C': 256, 'OY': 28, 'OX': 28, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [9]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    11: {  # conv12, depth-wise, stride 2
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 256, 'OY': 14, 'OX': 14, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [10]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    12: {  # conv13, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':512, 'C': 256, 'OY': 14, 'OX': 14, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [11]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    13: {  # conv14, depth-wise, stride 1
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 512, 'OY': 14, 'OX': 14, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [12]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    14: {  # conv15, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':512, 'C': 512, 'OY': 14, 'OX': 14, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [13]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    15: {  # conv16, depth-wise, stride 1
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 512, 'OY': 14, 'OX': 14, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [14]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    16: {  # conv17, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':512, 'C': 512, 'OY': 14, 'OX': 14, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [15]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    17: {  # conv18, depth-wise, stride 1
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 512, 'OY': 14, 'OX': 14, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [16]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    18: {  # conv19, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':512, 'C': 512, 'OY': 14, 'OX': 14, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [17]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    19: {  # conv20, depth-wise, stride 1
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 512, 'OY': 14, 'OX': 14, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [18]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    20: {  # conv21, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':512, 'C': 512, 'OY': 14, 'OX': 14, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [19]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    21: {  # conv22, depth-wise, stride 1
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 512, 'OY': 14, 'OX': 14, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [20]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    22: {  # conv23, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':512, 'C': 512, 'OY': 14, 'OX': 14, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [21]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    23: {  # conv24, depth-wise, stride 2
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 512, 'OY': 7, 'OX': 7, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [22]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    24: {  # conv25, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':1024, 'C': 512, 'OY': 7, 'OX': 7, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [23]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    25: {  # conv26, depth-wise, stride 2 (werid, o dimension not shrink, confirm)
        'equation': 'O[b][c][oy][ox]+=W[c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=2*ox+1*fx', 'iy=2*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 1024, 'OY': 7, 'OX': 7, 'FY':3, 'FX':3},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [24]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX','FY'), 'D2': ('C')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    26: {  # conv27, point-wise, stride 1
        'equation': 'O[b][k][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K':1024, 'C': 1024, 'OY': 7, 'OX': 7, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [25]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'C'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    27: {  # layer28, average pool (confrim if right or not)
        'equation': 'O[b][c][oy][ox]+=W[fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'C': 1024, 'OY': 1, 'OX': 1, 'FY': 7, 'FX':7},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [26]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
    ,
    28: {  # layer29, fc
        'equation': 'O[b][c][oy][ox]+=W[k][c][fy][fx]*I[b][c][ix][iy]',
        'dimension_relations': ['ix=1*ox+1*fx', 'iy=1*oy+1*fy'],
        'loop_dim_size': {'B':1, 'K': 1000, 'C': 1024, 'OY': 1, 'OX': 1, 'FY': 1, 'FX':1},
        'operand_precision': {'O': 16, 'O_final': 8, 'W': 8, 'I': 8},
        'operand_source': {'W': [], 'I': [27]},
        'operand_source_dimension_mapping': {'I': {'IX': 'OX', 'IY': 'OY', 'C': 'K'}},
        'core_allocation': 1,
        'spatial_mapping_hint': {'D1': ('C', 'FX', 'FY'), 'D2': ('K')},
        'temporal_ordering':[('OX', 'all'), ('OY', 'all'), ('FX','all'), ('FY','all'), ('C','all'), ('K', 'all')],
        'memory_operand_links': {'O': 'O', 'I': 'I1', 'W': 'I2'}
    }
}
