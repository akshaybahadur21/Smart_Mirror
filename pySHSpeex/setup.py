##############################################################################
# Copyright 2015 SoundHound, Incorporated.  All rights reserved.
##############################################################################
from distutils.core import setup, Extension

SPEEX_SRC_DIR = "soundhound-speex"
SOURCES="cb_search.c exc_10_32_table.c exc_8_128_table.c filters.c gain_table.c hexc_table.c high_lsp_tables.c lsp.c ltp.c speex.c stereo.c vbr.c vq.c bits.c exc_10_16_table.c exc_20_32_table.c exc_5_256_table.c exc_5_64_table.c gain_table_lbr.c hexc_10_32_table.c lpc.c lsp_tables_nb.c modes.c modes_wb.c nb_celp.c quant_lsp.c sb_celp.c speex_callbacks.c speex_header.c window.c soundhound.c"
SOURCES = [ SPEEX_SRC_DIR + "/src/%s" % x for x in SOURCES.split() ]

module1 = Extension('pySHSpeex',
				    sources = [ 'pySHSpeexmodule.c' ] + SOURCES,
					  include_dirs = [ SPEEX_SRC_DIR + '/include' ],
					  define_macros = [ ('FIXED_POINT', '1') ] )
setup(name = 'SHSpeex',
	version = '1.1',
	description = 'SoundHound speex encoder',
	ext_modules = [module1])
