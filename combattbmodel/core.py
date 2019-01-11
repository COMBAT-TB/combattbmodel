from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom


class Organism(GraphObject):
    """
    Organism
    """
    __primarykey__ = 'strain'

    abbreviation = Property()
    strain = Property()
    genus = Property()
    species = Property()
    common_name = Property()
    comment = Property()

    dbxref = RelatedTo("DbXref", "XREF")

    def __init__(self, abbreviation=None, strain=None, genus=None,
                 species=None, common_name=None, comment=None):
        self.abbreviation = abbreviation
        self.strain = strain
        self.genus = genus
        self.species = species
        self.common_name = common_name
        self.comment = comment


class Feature(GraphObject):
    """
    Used for inheritance purposes
    """
    __primarykey__ = 'uniquename'

    name = Property()
    uniquename = Property()
    residues = Property()
    seqlen = Property()
    md5checksum = Property()
    parent = Property()  # To build related_to rel.
    is_analysis = Property()
    is_obsolete = Property()
    timeaccessioned = Property()
    timelastmodfied = Property()
    ontology_id = Property()
    category = Property()

    belongs_to = RelatedTo("Organism", "BELONGS_TO")
    location = RelatedTo("Location", "LOCATED_AT")
    located_on = RelatedTo("Chromosome", "LOCATED_ON")
    # related_to = RelatedTo("Feature", "RELATED_TO")
    published_in = RelatedTo("Publication", "PUBLISHED_IN")
    dbxref = RelatedTo("DbXref", "XREF")

    @staticmethod
    def _reverse_complement(dna):
        uc_mapping = {'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C'}
        mapping = {}
        for base in uc_mapping:
            mapping[base] = uc_mapping[base]
            mapping[base.lower()] = uc_mapping[base].lower()
        revcomp = ''
        for base in dna[::-1]:
            revcomp += mapping.get(base, base)
        return revcomp

    def get_residues(self, upstream_offset=0, downstream_offset=0):
        if not self.residues:
            try:
                chromosome = next(iter(self.located_on))
                residues = chromosome.residues
            except StopIteration:
                return ''  # we have no chromosome
        else:
            residues = self.residues

        try:
            my_location = next(iter(self.location))
        except StopIteration:
            # I have no location, thus I am the top level feature,
            # thus return all my residues
            return residues
        else:
            # TODO: confirm that locations are encoded 1 / -1
            if my_location.strand == 1:
                start = my_location.fmin - upstream_offset
                start = 0 if start < 0 else start
                end = my_location.fmax + downstream_offset
                end = len(residues) + 1 if end > len(residues) else end
                return residues[start:end]
            else:
                start = my_location.fmin - downstream_offset
                start = 0 if start < 0 else start
                end = my_location.fmax + upstream_offset
                end = len(residues) + 1 if end > len(residues) else end
                return Feature._reverse_complement(residues[start:end])

        # >>> gene = Gene.select(graph, 'Rv0010c').first()
        # >>> gene.get_residues()


class Gene(Feature):
    """
    Gene is_a Feature
    """
    _so_id = "SO:0000704"
    so_id = Property()
    biotype = Property()
    description = Property()

    part_of = RelatedFrom("Transcript", "PART_OF")
    orthologous_to = RelatedTo("Gene", "ORTHOLOGOUS_TO")
    orthologous_to_ = RelatedFrom("Gene", "ORTHOLOGOUS_TO")
    co_regulated = RelatedFrom("Gene", "CO_REGULATED")
    member_of = RelatedFrom("Operon", "MEMBER_OF")

    encodes = RelatedTo("Protein", "ENCODES")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


class Operon(Feature):
    """
    Gene is_a Feature
    """
    _so_id = "SO:0000178"
    so_id = Property()
    description = Property()
    start = Property()
    end = Property()
    coverage = Property()
    experimentally_validated = Property()

    gene = RelatedTo("Gene", "MEMBER_OF")
    operon = RelatedFrom("Gene", "CO_REGULATED")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


class PseudoGene(Feature):
    """
    PseudoGene is_a Feature
    """
    _so_id = "SO:0000336"
    so_id = Property()
    biotype = Property()
    description = Property()

    part_of = RelatedFrom("Transcript", "PART_OF")
    # Rv0277A encodes
    encodes = RelatedTo("Protein", "ENCODES")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


class MRna(Feature):
    """
    mRNA is_a Feature
    """
    _so_id = "SO:0000234"
    so_id = Property()
    biotype = Property()

    part_of_g = RelatedTo("Gene", "PART_OF")
    part_of_pg = RelatedTo("PseudoGene", "PART_OF")
    part_of_cds = RelatedFrom("CDS", "PART_OF")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


class Transcript(Feature):
    """
    Transcript is_a Feature
    """
    _so_id = "SO:0000673"
    so_id = Property()
    biotype = Property()

    part_of_g = RelatedTo("Gene", "PART_OF")
    part_of_pg = RelatedTo("PseudoGene", "PART_OF")
    part_of_cds = RelatedFrom("CDS", "PART_OF")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


class TRna(Feature):
    """
    tRNA is_a Feature
    """
    _so_id = "SO:0000253"
    so_id = Property()
    biotype = Property()

    part_of = RelatedTo("Transcript", "PART_OF")
    regulates_gene = RelatedTo("Gene", "REGULATES")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


class NCRna(Feature):
    """
    ncRNA is_a Feature
    """
    _so_id = "SO:0000655"
    so_id = Property()
    biotype = Property()

    part_of = RelatedTo("Transcript", "PART_OF")
    regulates_gene = RelatedTo("Gene", "REGULATES")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


class RRna(Feature):
    """
    rRNA is_a Feature
    """
    _so_id = "SO:0000252"
    so_id = Property()
    biotype = Property()

    part_of = RelatedTo("Transcript", "PART_OF")
    regulates_gene = RelatedTo("Gene", "REGULATES")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


# Prokaryotes don't really have exons or introns
class Exon(Feature):
    """
    Exon is_a Feature
    """
    _so_id = "SO:0000147"
    so_id = Property()

    part_of = RelatedTo("Transcript", "PART_OF")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


class CDS(Feature):
    """
    CDS is_a Feature
    """
    _so_id = "SO:0000316"
    so_id = Property()

    part_of = RelatedTo("Transcript", "PART_OF")
    derived = RelatedFrom("Protein", "DERIVES_FROM")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


class Chromosome(Feature):
    """
    Chromosome is_a Feature
    """
    _so_id = "SO:0000340"
    so_id = Property()

    # is_a = RelatedTo("Feature", "IS_A")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


class Protein(Feature):
    """
    Protein (Polypeptide) is_a Feature

    """
    _so_id = "SO:0000104"
    so_id = Property()
    entry_name = Property()
    family = Property()
    function = Property()
    pdb_id = Property()
    domain = Property()
    three_d = Property()
    mass = Property()

    derives_from = RelatedTo("CDS", "DERIVES_FROM")
    interacts_with = RelatedTo("Protein", "INTERACTS_WITH")
    assoc_goterm = RelatedTo("GOTerm", 'ASSOCIATED_WITH')
    assoc_intterm = RelatedTo("InterProTerm", "ASSOCIATED_WITH")
    drug = RelatedFrom("Drug", "TARGET")
    pathway = RelatedTo("Pathway", "INVOLVED_IN")
    encoded_by = RelatedFrom("Gene", "ENCODES")

    def __init__(self, so_id=_so_id):
        self.so_id = so_id


class Location(GraphObject):
    """
    FeatureLoc not used
    """
    __primarykey__ = 'pk'  # used feature.uniquename

    pk = Property()
    srcfeature_id = Property()
    fmin = Property()
    is_fmin_partial = Property()
    fmax = Property()
    is_fmax_partial = Property()
    strand = Property()
    phase = Property()
    residue_info = Property()
    locgroup = Property()
    rank = Property()

    # feature = RelatedFrom("Feature", "ON")
    # published_in = RelatedTo("Publication", "PUBLISHED_IN")

    def __init__(self, pk, fmin=None, is_fmin_partial=None, fmax=None,
                 is_fmax_partial=None, strand=None, phase=None,
                 residue_info=None, locgroup=None, rank=None):
        self.pk = pk
        self.fmin = fmin
        self.is_fmin_partial = is_fmin_partial
        self.fmax = fmax
        self.is_fmax_partial = is_fmax_partial
        self.strand = strand
        self.phase = phase
        self.residue_info = residue_info
        self.locgroup = locgroup
        self.rank = rank
        # http://gmod.org/wiki/Chado_Sequence_Module#Feature_Locations
        if self.fmin > self.fmax:
            raise ValueError(
                "fmin cannot be greater than fmax: {} > {}."
                .format(self.fmin, self.fmax))


class Publication(GraphObject):
    """
    Publication from PubMed
    """
    __primarykey__ = 'pmid'

    pmid = Property()
    title = Property()
    volumetitle = Property()
    volume = Property()
    series_name = Property()
    issue = Property()
    year = Property()
    pages = Property()
    miniref = Property()
    uniquename = Property()
    is_obsolete = Property()
    publisher = Property()
    pubplace = Property()

    author = RelatedFrom("Author", "WROTE")


class Author(GraphObject):
    """
    Authors
    """
    __primarykey__ = 'givennames'

    editor = Property()
    surname = Property()
    givennames = Property()
    suffix = Property()
    rank = Property()

    wrote = RelatedTo("Publication", "WROTE")

    def __init__(self, editor=None, surname=None, givennames=None,
                 suffix=None):
        self.editor = editor
        self.surname = surname
        self.givennames = givennames
        self.suffix = suffix


class GOTerm(GraphObject):
    """
    Gene Ontology Terms
    """
    __primarykey__ = 'accession'

    accession = Property()
    name = Property()
    definition = Property()
    is_obsolete = Property()
    ontology = Property()  # same as namespace
    namespace = Property()

    is_a = RelatedTo("GOTerm", "IS_A")
    part_of_go = RelatedTo("GOTerm", "PART_OF")
    regulates = RelatedTo("GOTerm", "REGULATES")
    capable_of = RelatedTo("GOTerm", "CAPABLE_OF")
    protein = RelatedFrom("Protein", "ASSOCIATED_WITH")

    # part_of = RelatedTo("GOTerm", "PART_OF")
    # feature = RelatedFrom("Feature", "ASSOC_WITH")

    def __init__(self, accession, name=None, definition=None, is_obsolete=None,
                 ontology=None):
        self.accession = accession
        self.name = name
        self.definition = definition
        self.is_obsolete = is_obsolete
        self.ontology = ontology


class InterProTerm(GraphObject):
    """
    InterPro Terms
    """
    __primarykey__ = 'accession'

    accession = Property()
    name = Property()
    definition = Property()

    dbxref = RelatedTo("DbXref", "XREF")
    assoc_protein = RelatedFrom("Protein", "ASSOCIATED_WITH")
    feature = RelatedFrom("Feature", "ASSOC_WITH")

    def __init__(self, accession=None, name=None, definition=None):
        self.accession = accession
        self.name = name
        self.definition = definition


class Drug(GraphObject):
    """
    InterPro Terms
    """
    __primarykey__ = 'accession'

    accession = Property()
    name = Property()
    abbrev = Property()
    synonyms = Property()
    definition = Property()
    # attr. from tbdtdb
    _class = Property()
    toxicity = Property()
    cost = Property()

    target = RelatedTo("Protein", "TARGET")

    def __init__(self, accession, name=None, synonyms=None, definition=None):
        self.accession = accession
        self.name = name
        self.synonyms = synonyms
        self.definition = definition


class DbXref(GraphObject):
    """
    External references
    """
    __primarykey__ = 'accession'

    accession = Property()
    version = Property()
    db = Property()
    description = Property()

    # adding target rel for drugbank data
    target = RelatedTo("Protein", "TARGET")

    def __init__(self, db, accession, version=None, description=None):
        self.accession = accession
        self.version = version
        self.db = db
        self.description = description


class Contig(GraphObject):
    """
    Contigs
    """
    pass


class Pathway(GraphObject):
    """
    Pathway
    """
    __primarykey__ = 'accession'

    accession = Property()
    _type = Property()
    species = Property()
    _class = Property()
    name = Property()
    compartment = Property()
    # Description
    summation = Property()

    protein = RelatedFrom("Protein", "INVOLVED_IN")
