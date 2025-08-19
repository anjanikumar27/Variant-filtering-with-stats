# Variant-filtering-with-stats
A Python workflow for filtering variants from a VCF file based on quality (QUAL), read depth (DP), and allele frequency (AF). The script generates a new, filtered VCF file and a detailed log file containing summary statistics and a per-chromosome breakdown of filtered variants.

In case error is thrown that DP, AF and conting is not defined the header make the following changes in your file:
{
##INFO=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
##contig=<ID=chr1>
##contig=<ID=chr2>
##contig=<ID=chr3>
}
