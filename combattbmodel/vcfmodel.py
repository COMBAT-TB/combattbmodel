import uuid

from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo

from combattbmodel.core import Drug, Gene, Location, RRna

# https://ga4gh-schemas.readthedocs.io/en/latest/api/variants.html


class VariantSet(GraphObject):
    """
    VariantSet is the collection of CallSets
    """
    __primarykey__ = 'vset_id'
    name = Property()
    owner = Property()
    history_id = Property()
    vset_id = Property()

    has_variant = RelatedTo("Variant", "BELONGS_TO")
    has_callsets = RelatedTo("CallSet", "CALL_SET")

    def __init__(self, name, owner, history_id=None, vset_id=None):
        self.name = name
        self.owner = owner
        self.history_id = history_id
        if not vset_id:
            vset_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, name))
        self.vset_id = vset_id


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
    sources = Property()

    occurs_in = RelatedTo("Gene", "OCCURS_IN")
    occurs_in_ = RelatedTo("RRna", "OCCURS_IN")

    location = RelatedTo("Location", "LOCATED_AT")

    belongs_to_cset = RelatedTo("CallSet", "HAS_VARIANT")
    resistant_to = RelatedTo("Drug", "RESISTANT_TO")

    def __init__(self, chrom, pos, ref_allele, alt_allele, pk, impact=None,
                 gene=None, consequence=None):
        self.chrom = chrom
        self.pos = pos
        self.ref_allele = ref_allele
        self.alt_allele = alt_allele
        self.gene = gene
        self.pk = pk
        self.impact = impact
        self.consequence = consequence
