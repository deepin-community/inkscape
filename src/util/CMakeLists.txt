# SPDX-License-Identifier: GPL-2.0-or-later

set(util_SRC
	expression-evaluator.cpp
	share.cpp
	paper.cpp
	preview.cpp
	units.cpp
	ziptool.cpp


	# -------
	# Headers
	const_char_ptr.h
	enums.h
	expression-evaluator.h
	fixed_point.h
	format.h
	forward-pointer-iterator.h
	longest-common-suffix.h
	pages-skeleton.h
	paper.h
	preview.h
	reference.h
	share.h
	signal-blocker.h
	trim.h
	units.h
	ziptool.h
)

add_inkscape_lib(util_LIB "${util_SRC}")
target_link_libraries(util_LIB PUBLIC 2Geom::2geom)
# add_inkscape_source("${util_SRC}")
