# Chemical Genomics of Tuberculosis - 47,272 compounds  x 153 strains

2019-05-15

## Description

Calculated log fold change and p-values from 47,272 compounds x 153 strains, taking into account batch effects and negative binomial distribution of counts.

Also included are 10-point dose response curves for rifampin, trimethoprim, BRD-4592, and methotrexate.

Spike-in plasmids were added as internal controls with lysis solution ("intcon1") and PCR master mix ("intcon2").

## Data structure

One row per compound-concentration-strain combination. 

## Columns

**compound**: Compound identifier for each sample's well. 

**compound_stem**: Compound structure identifier.  Matches longest field of BRD-XXXXXXXXX-XXX-XX-X compound identifiers.

**concentration**: Compound concentration in micromolar.

**strain**: Mnemonic name of gene product knocked down, or spike-in plasmid name.

**n_replicates**: Combined number of replicates across sequencing lanes and completely independent replicates.

**log_fold_change**: Strain-matched maximum likelihood estimate of natural log fold change (LFC) of counts in each condition-strain combination compared to untreated DMSO control.

**std_error_lfc**: Standard error of the LFC estimate.

**log2_fold_change**: Base-2 LFC estimate [LFC / log(2)].

**std_error_l2fc**: Standard error of the base-2 LFC estimate.

**z_score**: Wald test Z-score [LFC / std_error].

**p_value**: P-value assuming Z ~ N(0, 1).

## Questions?

Email hung {at} broadinstitute.org.
