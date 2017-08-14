# from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom

# class Phenotype(GraphObject):
#     __primarykey__ = 'type'
#     # type {XDR, DR, MDR, SUS}
#     _type = Property()
#     has_var = RelatedFrom("Variant", "HAS_VAR")
# Adapting GA4GH Variant Data Model
# https://ga4gh-schemas.readthedocs.io/en/latest/api/variants.html
# VariantSet = Phenotype
# TODO: Dataset and ReferenceSet?
class VariantSet(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    owner = StringProperty()
    history_id = StringProperty(index=True)

    has_variant = RelationshipTo("VariantSite", "HAS_VARIANT")
    has_call = RelationshipTo("Call", "HAS_CALL")
    owned_by = RelationshipTo("combat_tb_model.model.galaxyuser.GalaxyUser", "OWNS_SET")
    forms_tree = RelationshipTo("combat_tb__model.model.fasttree.FastTree", "FROM_VARIANT_SET")


# VariantSite = Variant
class VariantSite(StructuredNode):
    # NOTE: relies on FeatureLoc from core.py
    # make __primarykey__ = VariantSet.name+POS

    pos =StringProperty()
    feature_id = StringProperty()
    biotype = StringProperty()
    chrom = StringProperty()
    ref_allele = StringProperty()
    alt_allele = StringProperty()
    quality = StringProperty()
    depth = StringProperty()
    gene = StringProperty()
    gene_id = StringProperty()
    known = StringProperty()
    novel = StringProperty()
    pk = StringProperty(unique_index=True)

    occurs_in = RelationshipTo("combat_tb_model.model.core.Gene", "OCCURS_IN")
    location = RelationshipTo("Location", "LOCATED_AT")

    has_call = RelationshipTo("Call", "HAS_CALL")
    belongs_to_vset = RelationshipTo("VariantSet", "BELONGS_TO_VSET")

# CallSet = VCF file
class CallSet(StructuredNode):
    name = StringProperty(unique_index=True)
    vset = StringProperty()
    identifier = StringProperty()

    has_call = RelationshipTo("Call", "HAS_CALL")
    has_calls_in = RelationshipTo("VariantSet", "HAS_CALLS_IN")

class Call(StructuredNode):
    # make __primarykey__ = CallSet.name+VariantSet.name+pos
    genotype = StringProperty()
    ref_allele = StringProperty()
    alt_allele = StringProperty()
    gene = StringProperty()
    pos = StringProperty()
    pk = StringProperty()
    impact = StringProperty()

    associated_with = RelationshipTo("VariantSite", "ASSOC_WITH_VARIANT")
    belongs_to_cset = RelationshipTo("CallSet", "BELONGS_TO_CSET")

