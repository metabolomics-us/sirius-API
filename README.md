# Sirius-API
The Sirius API wrapper for LC-BinBase 

## Main citations

Kai Dührkop, Markus Fleischauer, Marcus Ludwig, Alexander A. Aksenov, Alexey V. Melnik, Marvin Meusel, Pieter C. Dorrestein, Juho Rousu and Sebastian Böcker.
[SIRIUS 4: Turning tandem mass spectra into metabolite structure information.](https://doi.org/10.1038/s41592-019-0344-8)
*Nature Methods* 16, 299–302, 2019.

---
Michael A. Stravs and Kai Dührkop, Sebastian Böcker and Nicola Zamboni.
[MSNovelist: De novo structure generation from mass spectra.](https://doi.org/10.1038/s41592-022-01486-3)
*Nature Methods* 19, 865–870, 2022. (Cite if you are using: MSNovelist)

Martin A. Hoffmann, Louis-Félix Nothias, Marcus Ludwig, Markus Fleischauer, Emily C. Gentry, Michael Witting, Pieter C. Dorrestein, Kai Dührkop and Sebastian Böcker.
[High-confidence structural annotation of metabolites absent from spectral libraries.](https://doi.org/10.1038/s41587-021-01045-9)
*Nature Biotechnology* 40, 411–421, 2022. (Cite if you are using: *CSI:FingerID*, *COSMIC*)

Kai Dührkop, Louis-Félix Nothias, Markus Fleischauer, Raphael Reher, Marcus Ludwig, Martin A. Hoffmann, Daniel Petras, William H. Gerwick, Juho Rousu, Pieter C. Dorrestein and Sebastian Böcker.
[Systematic classification of unknown metabolites using high-resolution fragmentation mass spectra.](https://doi.org/10.1038/s41587-020-0740-8)
*Nature Biotechnology*, 2021. (Cite if you are using *CANOPUS*)

Yannick Djoumbou Feunang, Roman Eisner, Craig Knox, Leonid Chepelev, Janna Hastings, Gareth Owen, Eoin Fahy, Christoph Steinbeck, Shankar Subramanian, Evan Bolton, Russell Greiner, David S. Wishart.
[ClassyFire: automated chemical classification with a comprehensive, computable taxonomy.](https://doi.org/10.1186/s13321-016-0174-y)
*Journal of Cheminformatics* 8, 61, 2016. (*ClassyFire* publication; cite this if you are using *CANOPUS*)

Marcus Ludwig, Louis-Félix Nothias, Kai Dührkop, Irina Koester, Markus Fleischauer, Martin A. Hoffmann, Daniel Petras, Fernando Vargas, Mustafa Morsy, Lihini Aluwihare, Pieter C. Dorrestein, Sebastian Böcker.
[Database-independent molecular formula annotation using Gibbs sampling through ZODIAC.](https://doi.org/10.1038/s42256-020-00234-6)
*Nature Machine Intelligence* 2, 629–641, 2020. (Cite if you are using *ZODIAC*)

Kai Dührkop and Sebastian Böcker.
[Fragmentation trees reloaded.](http://dx.doi.org/10.1007/978-3-319-16706-0_10)
*Journal of Cheminformatics* 8, 5, 2016. (Cite this for *fragmentation pattern analysis and fragmentation tree computation*)

Kai Dührkop, Huibin Shen, Marvin Meusel, Juho Rousu, and Sebastian Böcker.
[Searching molecular structure databases with tandem mass spectra using CSI:FingerID](http://dx.doi.org/10.1073/pnas.1509788112).
*Proceedings of the National Academy of Sciences U S A* 112(41), 12580-12585, 2015. (cite this when *using CSI:FingerID*)

Sebastian Böcker, Matthias C. Letzel, Zsuzsanna Lipták and Anton Pervukhin.
[SIRIUS: decomposing isotope patterns for metabolite identification.](http://bioinformatics.oxfordjournals.org/content/25/2/218.full)
*Bioinformatics* 25(2), 218-224, 2009. (Cite this for *isotope pattern analysis*)

### Additional citations

Shipei Xing, Sam Shen, Banghua Xu, Xiaoxiao Li and Tao Huan.
[BUDDY: molecular formula discovery via bottom-up MS/MS interrogation.](https://doi.org/10.1038/s41592-023-01850-x)
*Nature Methods* 20, 881–890, 2023. (Cite if you are using: Bottom-up molecular formula generation)

Marcus Ludwig, Kai Dührkop and Sebastian and Böcker.
[Bayesian networks for mass spectrometric metabolite identification via molecular fingerprints.](http://doi.org/10.1093/bioinformatics/bty245)
*Bioinformatics*, 34(13): i333-i340. 2018. Proc. of Intelligent Systems for Molecular Biology (ISMB 2018). (Cite for CSI:FingerID Scoring)

W. Timothy J. White, Stephan Beyer, Kai Dührkop, Markus Chimani and
Sebastian Böcker. [Speedy Colorful
Subtrees.](http://dx.doi.org/10.1007/978-3-319-16706-0_10) In *Proc. of
Computing and Combinatorics Conference (COCOON 2015)*, volume 9198 of
*Lect Notes Comput Sci*, pages 310-322. Springer, Berlin, 2015. (cite
this on *why computations are swift*, even on a laptop computer)

Huibin Shen, Kai Dührkop, Sebastian Böcker and Juho Rousu. [Metabolite
Identification through Multiple Kernel Learning on Fragmentation
Trees.](http://dx.doi.org/10.1093/bioinformatics/btu275)
*Bioinformatics*, 30(12):i157-i164, 2014. Proc. of *Intelligent Systems
for Molecular Biology* (ISMB 2014). (Introduces *the machinery behind
CSI:FingerID*)

Imran Rauf, Florian Rasche, François Nicolas and
Sebastian Böcker. [Finding Maximum Colorful Subtrees in
practice.](http://dx.doi.org/10.1089/cmb.2012.0083) *J Comput Biol*,
20(4):1-11, 2013. (More, earlier work on *why computations are swift*
today)

Heinonen, M.; Shen, H.; Zamboni, N.; Rousu, J. [Metabolite
identification and molecular fingerprint prediction through machine
learning](http://dx.doi.org/10.1093/bioinformatics/bts437).
*Bioinformatics*, 2012. Vol. 28, nro 18, pp. 2333-2341. (Introduces the
*idea of predicting molecular fingerprints* from tandem MS data)

Florian Rasche, Aleš Svatoš, Ravi Kumar Maddula, Christoph Böttcher, and
Sebastian Böcker. [Computing Fragmentation Trees from Tandem Mass
Spectrometry
Data](http://pubs.acs.org/doi/abs/10.1021/ac101825k). *Analytical
Chemistry* (2011) 83 (4): 1243–1251. (Cite this for *introduction of
fragmentation trees* as used by SIRIUS)

Sebastian Böcker and Florian Rasche. [Towards de novo identification of metabolites by analyzing
tandem mass
spectra](http://bioinformatics.oxfordjournals.org/content/24/16/i49.abstract).
*Bioinformatics* (2008) 24 (16): i49-i55. (The very *first paper to
mention fragmentation trees* as used by SIRIUS)
