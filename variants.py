from cyvcf2 import VCF, Writer
from collections import defaultdict
# Open input VCF file for reading
vcf = VCF("variants.vcf")
# Create writer for output VCF containing only filtered variants
out = Writer("filtered_variants.vcf", vcf)
# Open log file to write filtering statistics
log = open("filter_stats.txt", "w")
# Initialize counters for global statistics
total = 0 # Total number of variants processed
fail_qual = 0 # Count of variants failing QUAL filter
fail_dp = 0 # Count of variants failing DP filter
fail_af = 0 # Count of variants failing AF filter
passed = 0 # Count of variants passing all filters
# Per-chromosome variant tracking
per_chrom = defaultdict(lambda: {"total": 0, "passed": 0})
# Iterate over each variant in the VCF
for record in vcf:
total += 1
chrom = record.CHROM
per_chrom[chrom]["total"] += 1
# Extract required fields with safe type casting
try:
qual = float(record.QUAL or 0)
dp = float(record.INFO.get("DP", 0))
af = float(record.INFO.get("AF", 0))
except Exception:
# Skip the record if values are malformed or missing
continue
# Track which filters a variant fails
fail = []
if qual < 30:
fail_qual += 1
fail.append("QUAL")
if dp < 20:
fail_dp += 1
fail.append("DP")
if not (0.05 <= af <= 0.95):
fail_af += 1
fail.append("AF")
# Determine whether the variant passed all filters
passed_filter = not fail
if passed_filter:
passed += 1
per_chrom[chrom]["passed"] += 1
out.write_record(record) # Write passing variant to output VCF
# Log the status of this variant to the report
log.write(f"{chrom}\t{record.POS}\t{record.ID or '.'}\tQUAL={qual}\tDP={dp}\tAF={af}\tPASSED={passed_filter}\tFAILED={'|'.join(fail) if fail else '-'}\n")
# Write overall summary statistics to the report
log.write("\n# Summary\n")
log.write(f"Total variants: {total}\n")
log.write(f"Passed all filters: {passed}\n")
log.write(f"Failed QUAL < 30: {fail_qual}\n")
log.write(f"Failed DP < 20: {fail_dp}\n")
log.write(f"Failed AF outside 0.05–0.95: {fail_af}\n")
# Write chromosome statistics
log.write("\n# Per-Chromosome Breakdown\n")
for chrom in sorted(per_chrom):
stats = per_chrom[chrom]
log.write(f"{chrom}\tTotal: {stats['total']}\tPassed: {stats['passed']}\n")
# Close output files
out.close()
log.close()
