// SPDX-License-Identifier: GPL-2.0-or-later
/** \file
 * SVG <feMorphology> implementation.
 *
 */
/*
 * Authors:
 *   Felipe Sanches <juca@members.fsf.org>
 *   Hugo Rodrigues <haa.rodrigues@gmail.com>
 *   Abhishek Sharma
 *
 * Copyright (C) 2006 Hugo Rodrigues
 *
 * Released under GNU GPL v2+, read the file 'COPYING' for more information.
 */

#include <cstring>

#include "attributes.h"
#include "svg/svg.h"
#include "morphology.h"
#include "xml/repr.h"
#include "display/nr-filter.h"

SPFeMorphology::SPFeMorphology() : SPFilterPrimitive() {
	this->Operator = Inkscape::Filters::MORPHOLOGY_OPERATOR_ERODE;

    //Setting default values:
    this->radius.set("0");
}

SPFeMorphology::~SPFeMorphology() = default;

/**
 * Reads the Inkscape::XML::Node, and initializes SPFeMorphology variables.  For this to get called,
 * our name must be associated with a repr via "sp_object_type_register".  Best done through
 * sp-object-repr.cpp's repr_name_entries array.
 */
void SPFeMorphology::build(SPDocument *document, Inkscape::XML::Node *repr) {
	SPFilterPrimitive::build(document, repr);

	/*LOAD ATTRIBUTES FROM REPR HERE*/
	this->readAttr(SPAttr::OPERATOR);
	this->readAttr(SPAttr::RADIUS);
}

/**
 * Drops any allocated memory.
 */
void SPFeMorphology::release() {
	SPFilterPrimitive::release();
}

static Inkscape::Filters::FilterMorphologyOperator sp_feMorphology_read_operator(gchar const *value){
    if (!value) {
    	return Inkscape::Filters::MORPHOLOGY_OPERATOR_ERODE; //erode is default
    }
    
    switch(value[0]){
        case 'e':
            if (strncmp(value, "erode", 5) == 0) {
            	return Inkscape::Filters::MORPHOLOGY_OPERATOR_ERODE;
            }
            break;
        case 'd':
            if (strncmp(value, "dilate", 6) == 0) {
            	return Inkscape::Filters::MORPHOLOGY_OPERATOR_DILATE;
            }
            break;
    }
    
    return Inkscape::Filters::MORPHOLOGY_OPERATOR_ERODE; //erode is default
}

/**
 * Sets a specific value in the SPFeMorphology.
 */
void SPFeMorphology::set(SPAttr key, gchar const *value) {
    Inkscape::Filters::FilterMorphologyOperator read_operator;
    
    switch(key) {
    /*DEAL WITH SETTING ATTRIBUTES HERE*/
        case SPAttr::OPERATOR:
            read_operator = sp_feMorphology_read_operator(value);

            if (read_operator != this->Operator){
                this->Operator = read_operator;
                this->parent->requestModified(SP_OBJECT_MODIFIED_FLAG);
            }
            break;
        case SPAttr::RADIUS:
            this->radius.set(value);

            //From SVG spec: If <y-radius> is not provided, it defaults to <x-radius>.
            if (this->radius.optNumIsSet() == false) {
                this->radius.setOptNumber(this->radius.getNumber());
            }

            this->parent->requestModified(SP_OBJECT_MODIFIED_FLAG);
            break;
        default:
        	SPFilterPrimitive::set(key, value);
            break;
    }

}

/**
 * Receives update notifications.
 */
void SPFeMorphology::update(SPCtx *ctx, guint flags) {
    if (flags & (SP_OBJECT_MODIFIED_FLAG | SP_OBJECT_STYLE_MODIFIED_FLAG |
                 SP_OBJECT_VIEWPORT_MODIFIED_FLAG)) {

        /* do something to trigger redisplay, updates? */

    }

    SPFilterPrimitive::update(ctx, flags);
}

/**
 * Writes its settings to an incoming repr object, if any.
 */
Inkscape::XML::Node* SPFeMorphology::write(Inkscape::XML::Document *doc, Inkscape::XML::Node *repr, guint flags) {
	/* TODO: Don't just clone, but create a new repr node and write all
     * relevant values into it */
    if (!repr) {
        repr = this->getRepr()->duplicate(doc);
    }

    SPFilterPrimitive::write(doc, repr, flags);

    return repr;
}

void SPFeMorphology::build_renderer(Inkscape::Filters::Filter* filter) {
    g_assert(filter != nullptr);

    int primitive_n = filter->add_primitive(Inkscape::Filters::NR_FILTER_MORPHOLOGY);
    Inkscape::Filters::FilterPrimitive *nr_primitive = filter->get_primitive(primitive_n);
    Inkscape::Filters::FilterMorphology *nr_morphology = dynamic_cast<Inkscape::Filters::FilterMorphology*>(nr_primitive);
    g_assert(nr_morphology != nullptr);

    this->renderer_common(nr_primitive);
    
    nr_morphology->set_operator(this->Operator);
    nr_morphology->set_xradius( this->radius.getNumber() );
    nr_morphology->set_yradius( this->radius.getOptNumber() );
}

/**
 * Calculate the region taken up by a mophoplogy primitive
 *
 * @param region The original shape's region or previous primitive's region output.
 */
Geom::Rect SPFeMorphology::calculate_region(Geom::Rect region)
{
    auto r = region;
    if (Operator == Inkscape::Filters::MORPHOLOGY_OPERATOR_DILATE) {
        if (radius.optNumIsSet()) {
            r.expandBy(radius.getNumber(), radius.getOptNumber());
        } else {
            r.expandBy(radius.getNumber());
        }
    } else if (Operator == Inkscape::Filters::MORPHOLOGY_OPERATOR_ERODE) {
        if (radius.optNumIsSet()) {
            r.expandBy(-1 * radius.getNumber(), -1 * radius.getOptNumber());
        } else {
            r.expandBy(-1 * radius.getNumber());
        }
    }
    return r;
}

/*
  Local Variables:
  mode:c++
  c-file-style:"stroustrup"
  c-file-offsets:((innamespace . 0)(inline-open . 0)(case-label . +))
  indent-tabs-mode:nil
  fill-column:99
  End:
*/
// vim: filetype=cpp:expandtab:shiftwidth=4:tabstop=8:softtabstop=4:fileencoding=utf-8:textwidth=99 :
