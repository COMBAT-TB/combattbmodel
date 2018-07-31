# from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
import uuid

from .core import *

# class Phenotype(GraphObject):
#     __primarykey__ = 'type'
#     # type {XDR, DR, MDR, SUS}
#     _type = Property()
#     has_var = RelatedFrom("Variant", "HAS_VAR")
# Adapting GA4GH Variant Data Model
# https://ga4gh-schemas.readthedocs.io/en/latest/api/variants.html
# VariantSet = Phenotype
# TODO: Dataset and ReferenceSet?
REF_COL_ID = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'www.internationalgenome.org'))


class VariantSet(GraphObject):
    """
    VariantSet is the collection of CallSets
    """
    __primarykey__ = 'col_id'
    name = Property()
    owner = Property()
    history_id = Property()
    col_id = Property()

    has_variant = RelatedTo("Variant", "BELONGS_TO")
    forms_tree = RelatedTo("FastTree", "FROM_VARIANT_SET")
    has_callsets = RelatedTo("CallSet", "CALL_SET")

    def __init__(self, name, owner, history_id=None, col_id=None):
        self.name = name
        self.owner = owner
        self.history_id = history_id
        if not col_id:
            col_id = REF_COL_ID
        self.col_id = col_id


# CallSet = VCF file
class CallSet(GraphObject):
    """
    CallSet is the VCF file
    """
    __primarykey__ = 'name'
    name = Property()
    vset = Property()
    identifier = Property()

    belongs_to_vset = RelatedFrom("VariantSet", "CALL_SET")
    has_variants = RelatedFrom("Variant", "HAS_VARIANT")

    def __init__(self, name):
        self.name = name
        # self.vset = vset


# VariantSite = Variant
class Variant(GraphObject):
    """
    VariantSite is the Variant
    """
    # NOTE: relies on Location from core.py
    # make __primarykey__ = VariantSet.name+POS
    __primarykey__ = 'pk'

    pk = Property()
    pos = Property()
    loc_in_seq = Property()
    feature_id = Property()
    biotype = Property()
    chrom = Property()
    ref_allele = Property()
    alt_allele = Property()
    quality = Property()
    depth = Property()
    consequence = Property()
    gene = Property()
    gene_id = Property()
    known = Property()
    promoter = Property()
    impact = Property()
    drug = Property()

    occurs_in = RelatedTo("Gene", "OCCURS_IN")
    occurs_in_ = RelatedTo("RRna", "OCCURS_IN")

    location = RelatedTo("Location", "LOCATED_AT")

    belongs_to_cset = RelatedTo("CallSet", "HAS_VARIANT")
    resistant_to = RelatedTo("Drug", "RESISTANT_TO")

    def __init__(self, chrom, pos, ref_allele, alt_allele, pk, impact=None, gene=None, consequence=None):
        self.chrom = chrom
        self.pos = pos
        self.ref_allele = ref_allele
        self.alt_allele = alt_allele
        self.gene = gene
        self.pk = pk
        self.impact = impact
        self.consequence = consequence


class FastTree(GraphObject):
    """
    FastTree
    """
    __primarykey__ = 'name'
    name = Property()
    data = Property()
    history_id = Property()

    from_variant_set = RelatedTo("VariantSet", "FROM_VARIANT_SET")

    def __init__(self, name, data, history_id):
        self.name = name
        self.data = data
        self.history_id = history_id
