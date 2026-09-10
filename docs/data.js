window.ODONTOAGE_DATA = {
  "version": "0.1.0",
  "methods": {
    "cameriere_italian_2006": {
      "id": "cameriere_italian_2006",
      "label": "Cameriere \u2014 Italian formula (open apices)",
      "family": "cameriere",
      "kind": "regression",
      "dentition": "developing",
      "measurement": "open_apices",
      "sex_required": true,
      "age_range_years": [
        5,
        15
      ],
      "age_range_note": "Developed on Italian children; most accurate ~7-14 y (meta-analysis PMC7926662).",
      "reported_stats": {
        "r_squared": 0.85,
        "note": "explained variance reported in original paper; confirm exact value"
      },
      "regression": {
        "intercept": 8.971,
        "terms": [
          {
            "var": "g",
            "coef": 0.375,
            "desc": "sex indicator (1 = male, 0 = female)"
          },
          {
            "var": "x5",
            "coef": 1.631,
            "desc": "normalized open apex of the 2nd premolar = A5/L5"
          },
          {
            "var": "N0",
            "coef": 0.674,
            "desc": "number of the 7 left mandibular teeth with CLOSED apices"
          },
          {
            "var": "s",
            "coef": -1.034,
            "desc": "sum of normalized open apices = sum(Ai/Li) over the 7 teeth"
          },
          {
            "var": "s*N0",
            "coef": -0.176,
            "desc": "first-order interaction s x N0"
          }
        ]
      },
      "source": "cameriere_2006_italian",
      "verified": true,
      "verification_note": "Coefficients cross-checked: PMC7926662 meta-analysis + medrech reproduction. DOI 10.1007/s00414-005-0047-9 (confirm)."
    },
    "cameriere_european_2007": {
      "id": "cameriere_european_2007",
      "label": "Cameriere \u2014 European formula (open apices)",
      "family": "cameriere",
      "kind": "regression",
      "dentition": "developing",
      "measurement": "open_apices",
      "sex_required": true,
      "age_range_years": [
        4,
        16
      ],
      "age_range_note": "Multi-country European reference sample (~2652 children); most accurate ~7-14 y.",
      "reported_stats": {
        "r_squared": 0.861,
        "median_residual_years": -0.114,
        "note": "from original 2007 paper"
      },
      "regression": {
        "intercept": 8.387,
        "terms": [
          {
            "var": "g",
            "coef": 0.282,
            "desc": "sex indicator (1 = male, 0 = female)"
          },
          {
            "var": "x5",
            "coef": -1.692,
            "desc": "normalized open apex of the 2nd premolar = A5/L5 (coefficient is negative in the European multivariate fit)"
          },
          {
            "var": "N0",
            "coef": 0.835,
            "desc": "number of the 7 left mandibular teeth with CLOSED apices"
          },
          {
            "var": "s",
            "coef": -0.116,
            "desc": "sum of normalized open apices = sum(Ai/Li) over the 7 teeth"
          },
          {
            "var": "s*N0",
            "coef": -0.139,
            "desc": "first-order interaction s x N0"
          }
        ]
      },
      "source": "cameriere_2007_european",
      "verified": true,
      "verification_note": "Coefficients cross-checked: primary 2007 paper PDF (u-pad.unimc.it) + PMC7926662 meta-analysis. DOI 10.1007/s00414-007-0179-1 confirmed."
    },
    "cameriere_adult_upper_2009": {
      "id": "cameriere_adult_upper_2009",
      "label": "Cameriere - adult, upper (maxillary) canine pulp/tooth area ratio",
      "family": "cameriere",
      "kind": "regression",
      "dentition": "adult",
      "measurement": "pulp_tooth_area",
      "sex_required": false,
      "age_range_years": [
        20,
        85
      ],
      "age_range_note": "Combined Italian + Portuguese adult sample (~20-84 y). Input RA = pulp area / tooth area of the MAXILLARY canine, measured by planimetry on a peri-apical radiograph.",
      "prediction_error_years": 4.24,
      "reported_stats": {
        "r_squared": 0.931,
        "see_years": 4.24,
        "mean_error_years": 3.32
      },
      "regression": {
        "intercept": 100.598,
        "terms": [
          {
            "var": "RA",
            "coef": -544.433,
            "desc": "pulp/tooth AREA ratio of the maxillary (upper) canine"
          }
        ]
      },
      "source": "cameriere_2009_adult",
      "verified": true,
      "verification_note": "Common (Italian + Portuguese) regression, Table 5 / Eq.(3) of Cameriere et al. 2009 (Forensic Sci Int 193:128.e1-e6), read at full resolution."
    },
    "cameriere_adult_lower_2009": {
      "id": "cameriere_adult_lower_2009",
      "label": "Cameriere - adult, lower (mandibular) canine pulp/tooth area ratio",
      "family": "cameriere",
      "kind": "regression",
      "dentition": "adult",
      "measurement": "pulp_tooth_area",
      "sex_required": false,
      "age_range_years": [
        20,
        85
      ],
      "age_range_note": "Combined Italian + Portuguese adult sample. Input RA = pulp area / tooth area of the MANDIBULAR canine.",
      "prediction_error_years": 4.33,
      "reported_stats": {
        "r_squared": 0.9285,
        "see_years": 4.33,
        "mean_error_years": 3.39
      },
      "regression": {
        "intercept": 91.362,
        "terms": [
          {
            "var": "RA",
            "coef": -480.901,
            "desc": "pulp/tooth AREA ratio of the mandibular (lower) canine"
          }
        ]
      },
      "source": "cameriere_2009_adult",
      "verified": true,
      "verification_note": "Common (Italian + Portuguese) regression, Table 5 / Eq.(4) of Cameriere et al. 2009, read at full resolution."
    },
    "demirjian_1976": {
      "id": "demirjian_1976",
      "label": "Demirjian (1976) - 7-tooth maturity score",
      "family": "demirjian",
      "kind": "maturity_score",
      "dentition": "developing",
      "measurement": "staging",
      "sex_required": true,
      "age_range_years": [
        2.5,
        17
      ],
      "age_range_note": "French-Canadian reference sample (2407 boys, 2349 girls); percentile standards span 2.5-17 y. The maturity score is known to translate to an OVER-estimate of age in many other populations.",
      "teeth": [
        "I1",
        "I2",
        "C",
        "PM1",
        "PM2",
        "M1",
        "M2"
      ],
      "teeth_fdi": [
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37"
      ],
      "stages": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H"
      ],
      "invariant": "Self-weighted stage-H scores across the 7 teeth sum to 100 for each sex (boys 100.0; girls 100.1 by rounding).",
      "scores": {
        "male": {
          "M2": {
            "0": 0.0,
            "A": 1.7,
            "B": 3.1,
            "C": 5.4,
            "D": 8.6,
            "E": 11.4,
            "F": 12.4,
            "G": 12.8,
            "H": 13.6
          },
          "M1": {
            "C": 0.0,
            "D": 5.3,
            "E": 7.5,
            "F": 10.3,
            "G": 13.9,
            "H": 16.8
          },
          "PM2": {
            "0": 0.0,
            "A": 1.5,
            "B": 2.7,
            "C": 5.2,
            "D": 8.0,
            "E": 10.8,
            "F": 12.0,
            "G": 12.5,
            "H": 13.2
          },
          "PM1": {
            "B": 0.0,
            "C": 4.0,
            "D": 9.4,
            "E": 13.2,
            "F": 14.9,
            "G": 15.5,
            "H": 16.1
          },
          "C": {
            "C": 0.0,
            "D": 4.0,
            "E": 7.8,
            "F": 10.1,
            "G": 11.4,
            "H": 12.0
          },
          "I2": {
            "C": 0.0,
            "D": 2.8,
            "E": 5.4,
            "F": 7.7,
            "G": 10.5,
            "H": 13.2
          },
          "I1": {
            "C": 0.0,
            "D": 4.3,
            "E": 6.3,
            "F": 8.2,
            "G": 11.2,
            "H": 15.1
          }
        },
        "female": {
          "M2": {
            "0": 0.0,
            "A": 1.8,
            "B": 3.1,
            "C": 5.4,
            "D": 9.0,
            "E": 11.7,
            "F": 12.8,
            "G": 13.2,
            "H": 13.8
          },
          "M1": {
            "C": 0.0,
            "D": 3.5,
            "E": 5.6,
            "F": 8.4,
            "G": 12.5,
            "H": 15.4
          },
          "PM2": {
            "0": 0.0,
            "A": 1.7,
            "B": 2.9,
            "C": 5.4,
            "D": 8.6,
            "E": 11.1,
            "F": 12.3,
            "G": 12.8,
            "H": 13.3
          },
          "PM1": {
            "B": 0.0,
            "C": 3.1,
            "D": 8.8,
            "E": 12.6,
            "F": 14.3,
            "G": 14.9,
            "H": 15.5
          },
          "C": {
            "C": 0.0,
            "D": 3.7,
            "E": 7.3,
            "F": 10.0,
            "G": 11.8,
            "H": 12.5
          },
          "I2": {
            "C": 0.0,
            "D": 2.8,
            "E": 5.3,
            "F": 8.1,
            "G": 11.2,
            "H": 13.8
          },
          "I1": {
            "C": 0.0,
            "D": 4.4,
            "E": 6.3,
            "F": 8.5,
            "G": 12.0,
            "H": 15.8
          }
        }
      },
      "conversion": {
        "male": [],
        "female": [],
        "note": "Demirjian converts the maturity score to a dental age by reading the age at which the published 50th-percentile curve (Figs 1-2) equals the score. OdontoAge does NOT digitise those curves (to avoid introducing curve-reading error) and therefore returns the maturity score only; for a dental AGE from the same 7-tooth staging, use the Willems method, which folds the conversion into direct year-values."
      },
      "source": "demirjian_1976",
      "verified": true,
      "verification_note": "Full 7-tooth score grids transcribed from the primary paper (Demirjian & Goldstein 1976, Ann Hum Biol 3(5):411-421, Table 2) read at full resolution; validated by the stage-H checksum (boys 100.0; girls 100.1 rounding) and per-tooth monotonicity."
    },
    "willems_2001": {
      "id": "willems_2001",
      "label": "Willems (2001) - direct-age tables",
      "family": "willems",
      "kind": "direct_age",
      "dentition": "developing",
      "measurement": "staging",
      "sex_required": true,
      "age_range_years": [
        3,
        18
      ],
      "age_range_note": "Belgian Caucasian reference sample; the seven per-tooth year-values are summed directly to give the estimated dental age (no maturity-score conversion step). Reduces Demirjian's systematic overestimation.",
      "prediction_error_years": 1.1,
      "reported_stats": {
        "boys_diff_sd_years": 0.9,
        "girls_diff_sd_years": 1.3,
        "note": "SD of (dental age - chronological age) for the adapted method on the validation sample; the 95% interval uses ~1.1 y as a representative value."
      },
      "teeth": [
        "I1",
        "I2",
        "C",
        "PM1",
        "PM2",
        "M1",
        "M2"
      ],
      "teeth_fdi": [
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37"
      ],
      "stages": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H"
      ],
      "aggregation": "sum",
      "notes": "Values are ANOVA-adapted age contributions in YEARS; they are intentionally non-monotonic and some are negative (a multicolinearity artifact) and are meaningful only in the total sum, per the authors.",
      "tables": {
        "male": {
          "I1": {
            "C": 1.68,
            "D": 1.49,
            "E": 1.5,
            "F": 1.86,
            "G": 2.07,
            "H": 2.19
          },
          "I2": {
            "C": 0.55,
            "D": 0.63,
            "E": 0.74,
            "F": 1.08,
            "G": 1.32,
            "H": 1.64
          },
          "C": {
            "D": 0.04,
            "E": 0.31,
            "F": 0.47,
            "G": 1.09,
            "H": 1.9
          },
          "PM1": {
            "A": 0.15,
            "B": 0.56,
            "C": 0.75,
            "D": 1.11,
            "E": 1.48,
            "F": 2.03,
            "G": 2.43,
            "H": 2.83
          },
          "PM2": {
            "A": 0.08,
            "B": 0.05,
            "C": 0.12,
            "D": 0.27,
            "E": 0.33,
            "F": 0.45,
            "G": 0.4,
            "H": 1.15
          },
          "M1": {
            "D": 0.69,
            "E": 1.14,
            "F": 1.6,
            "G": 1.95,
            "H": 2.15
          },
          "M2": {
            "A": 0.18,
            "B": 0.48,
            "C": 0.71,
            "D": 0.8,
            "E": 1.31,
            "F": 2.0,
            "G": 2.48,
            "H": 4.17
          }
        },
        "female": {
          "I1": {
            "C": 1.83,
            "D": 2.19,
            "E": 2.34,
            "F": 2.82,
            "G": 3.19,
            "H": 3.14
          },
          "I2": {
            "D": 0.29,
            "E": 0.32,
            "F": 0.49,
            "G": 0.79,
            "H": 0.7
          },
          "C": {
            "C": 0.6,
            "D": 0.54,
            "E": 0.62,
            "F": 1.08,
            "G": 1.72,
            "H": 2.0
          },
          "PM1": {
            "A": -0.95,
            "B": -0.15,
            "C": 0.16,
            "D": 0.41,
            "E": 0.6,
            "F": 1.27,
            "G": 1.58,
            "H": 2.19
          },
          "PM2": {
            "A": -0.19,
            "B": 0.01,
            "C": 0.27,
            "D": 0.17,
            "E": 0.35,
            "F": 0.35,
            "G": 0.55,
            "H": 1.51
          },
          "M1": {
            "D": 0.62,
            "E": 0.9,
            "F": 1.56,
            "G": 1.82,
            "H": 2.21
          },
          "M2": {
            "A": 0.14,
            "B": 0.11,
            "C": 0.21,
            "D": 0.32,
            "E": 0.66,
            "F": 1.28,
            "G": 2.09,
            "H": 4.04
          }
        }
      },
      "source": "willems_2001",
      "verified": true,
      "verification_note": "Boys (Table 1) and girls (Table 2) year-value grids transcribed from the primary paper (Willems et al. 2001, J Forensic Sci 46(4):893-895) rendered at high DPI. No sum-to-100 checksum exists (direct-age method); validated by an all-stage-H sanity total (boys ~16.0 y, girls ~15.8 y - the correct developmental ceiling) and against the paper's documented negative/non-monotonic values."
    },
    "kvaal_1995": {
      "id": "kvaal_1995",
      "label": "Kvaal et al. (1995) - pulp/tooth size-ratio regression (adults)",
      "family": "kvaal",
      "kind": "regression",
      "dentition": "adult",
      "measurement": "pulp_tooth_ratio",
      "sex_required": false,
      "sex_required_note": "Sex (gender) is only used by the mandibular-lateral-incisor equation (32/42); all other equations ignore it.",
      "age_range_years": [
        20,
        85
      ],
      "age_range_note": "Reference sample of 100 adults (Norwegian, ages ~20-84). Measurements are made on standardised peri-apical radiographs of fully developed teeth.",
      "measurement_protocol": {
        "raw_measurements": "On each tooth's peri-apical radiograph, six lengths/widths are measured (Kvaal et al. 1995, Fig. 1): T = maximum tooth length; R = root length on the mesial surface; P = maximum pulp length; and pulp & root widths at three levels - A (enamel-cementum junction), B (midway between A and C) and C (mid-root, midway between apex and ECJ).",
        "ratios": "To cancel radiographic magnification, ratios of pulp to tooth/root dimensions are formed: p = pulp-length/root-length (P), r = pulp-length/tooth-length (R), and pulp/root width ratios a, b, c at levels A, B, C. (The tooth/root length ratio T was only weakly correlated with age and is not used.)",
        "predictors": {
          "M": "First predictor: mean of the five ratios (p, r, a, b, c) for the tooth (or the mean across all teeth of a multi-tooth model). Approximates the first principal component (overall pulp size).",
          "W": "Mean of the width ratios at levels B and C.",
          "L": "Mean of the length ratios p and r.",
          "W_minus_L": "Second predictor = W - L (approximates the second principal component, pulp shape)."
        }
      },
      "inputs": {
        "M": "required for every equation - the mean-of-ratios first predictor (dimensionless, typically ~0.15-0.35).",
        "W_minus_L": "required for every equation EXCEPT the mandibular canine (33/43); may be supplied directly, or as separate W and L (then W-L is computed).",
        "sex": "required ONLY by equation 'mandibular_lateral_incisor' (32/42); male = 1, female = 0."
      },
      "default_equation": "six_teeth",
      "equations": {
        "six_teeth": {
          "label": "Six teeth from both jaws (11/21, 12/22, 15/25, 34/44, 33/43, 32/42)",
          "teeth_fdi": "11/21, 12/22, 15/25, 34/44, 33/43, 32/42",
          "intercept": 129.8,
          "M": -316.4,
          "W_minus_L": -66.8,
          "G": null,
          "r_squared": 0.76,
          "see": 8.6
        },
        "maxillary_three": {
          "label": "Three maxillary teeth (11/21, 12/22, 15/25)",
          "teeth_fdi": "11/21, 12/22, 15/25",
          "intercept": 120.0,
          "M": -256.6,
          "W_minus_L": -45.3,
          "G": null,
          "r_squared": 0.74,
          "see": 8.9
        },
        "mandibular_three": {
          "label": "Three mandibular teeth (34/44, 33/43, 32/42)",
          "teeth_fdi": "34/44, 33/43, 32/42",
          "intercept": 135.3,
          "M": -356.8,
          "W_minus_L": -82.5,
          "G": null,
          "r_squared": 0.71,
          "see": 9.4
        },
        "maxillary_central_incisor": {
          "label": "Maxillary central incisor (11/21)",
          "teeth_fdi": "11/21",
          "intercept": 110.2,
          "M": -201.4,
          "W_minus_L": -31.3,
          "G": null,
          "r_squared": 0.7,
          "see": 9.5
        },
        "maxillary_lateral_incisor": {
          "label": "Maxillary lateral incisor (12/22)",
          "teeth_fdi": "12/22",
          "intercept": 103.5,
          "M": -216.6,
          "W_minus_L": -46.6,
          "G": null,
          "r_squared": 0.67,
          "see": 10.0
        },
        "maxillary_second_premolar": {
          "label": "Maxillary second premolar (15/25)",
          "teeth_fdi": "15/25",
          "intercept": 125.3,
          "M": -288.5,
          "W_minus_L": -46.3,
          "G": null,
          "r_squared": 0.6,
          "see": 11.0
        },
        "mandibular_first_premolar": {
          "label": "Mandibular first premolar (34/44)",
          "teeth_fdi": "34/44",
          "intercept": 133.0,
          "M": -318.3,
          "W_minus_L": -65.0,
          "G": null,
          "r_squared": 0.64,
          "see": 10.5
        },
        "mandibular_canine": {
          "label": "Mandibular canine (33/43) - no second predictor (W-L omitted, P=0.06)",
          "teeth_fdi": "33/43",
          "intercept": 158.8,
          "M": -255.7,
          "W_minus_L": null,
          "G": null,
          "r_squared": 0.56,
          "see": 11.5
        },
        "mandibular_lateral_incisor": {
          "label": "Mandibular lateral incisor (32/42) - includes gender term",
          "teeth_fdi": "32/42",
          "intercept": 106.6,
          "M": -251.7,
          "W_minus_L": -61.2,
          "G": -6.0,
          "r_squared": 0.57,
          "see": 11.5
        }
      },
      "source": "kvaal_1995",
      "verified": true,
      "verification_note": "All nine Table 5 regression formulae transcribed from Kvaal et al. 1995 (Forensic Sci Int 74:175-185) rendered at full resolution; the 66.8 vs 6.8 ambiguity in text extraction was resolved visually (six-teeth coefficient is -66.8). Ratio/predictor definitions taken from the Table 2 legend. Note: mandibular canine (33/43) has NO W-L term (second predictor P=0.06); mandibular lateral incisor (32/42) is the ONLY equation with a gender term (-6.0*G, male=1/female=0)."
    }
  },
  "sources": {
    "cameriere_2006_italian": {
      "citation": "Cameriere R, Ferrante L, Cingolani M. Age estimation in children by measurement of open apices in teeth. Int J Legal Med. 2006;120(1):49-52.",
      "doi": "10.1007/s00414-005-0047-9",
      "doi_status": "confirmed",
      "kind": "primary"
    },
    "cameriere_2007_european": {
      "citation": "Cameriere R, De Angelis D, Ferrante L, Scarpino F, Cingolani M. Age estimation in children by measurement of open apices in teeth: a European formula. Int J Legal Med. 2007;121(6):449-453.",
      "doi": "10.1007/s00414-007-0179-1",
      "doi_status": "confirmed",
      "kind": "primary"
    },
    "demirjian_1973": {
      "citation": "Demirjian A, Goldstein H, Tanner JM. A new system of dental age assessment. Hum Biol. 1973;45(2):211-227.",
      "doi": null,
      "doi_status": "no-doi (1973)",
      "kind": "primary"
    },
    "demirjian_1976": {
      "citation": "Demirjian A, Goldstein H. New systems for dental maturity based on seven and four teeth. Ann Hum Biol. 1976;3(5):411-421.",
      "doi": "10.1080/03014467600001671",
      "doi_status": "confirmed",
      "kind": "primary"
    },
    "willems_2001": {
      "citation": "Willems G, Van Olmen A, Spiessens B, Carels C. Dental age estimation in Belgian children: Demirjian's technique revisited. J Forensic Sci. 2001;46(4):893-895.",
      "doi": "10.1520/JFS15064J",
      "doi_status": "confirmed",
      "kind": "primary"
    },
    "cameriere_2009_adult": {
      "citation": "Cameriere R, Cunha E, Sassaroli E, Nuzzolese E, Ferrante L. Age estimation by pulp/tooth area ratio in canines: study of a Portuguese sample to test Cameriere's method. Forensic Sci Int. 2009;193(1-3):128.e1-128.e6.",
      "doi": "10.1016/j.forsciint.2009.09.011",
      "doi_status": "confirmed",
      "kind": "primary",
      "note": "Provides the combined Italian + Portuguese regression (Table 5) encoded as the adult upper/lower canine pulp-area methods."
    },
    "kvaal_1995": {
      "citation": "Kvaal SI, Kolltveit KM, Thomsen IO, Solheim T. Age estimation of adults from dental radiographs. Forensic Sci Int. 1995;74(3):175-185.",
      "doi": "10.1016/0379-0738(95)01760-G",
      "doi_status": "confirmed",
      "kind": "primary"
    },
    "cameriere_2004_adult": {
      "citation": "Cameriere R, Ferrante L, Cingolani M. Variations in pulp/tooth area ratio as an indicator of age: a preliminary study. J Forensic Sci. 2004;49(2):317-319.",
      "doi": "10.1520/JFS2003259",
      "doi_status": "pending",
      "kind": "supporting",
      "note": "Preliminary study that introduced the pulp/tooth AREA-ratio idea; the encoded adult method uses the later 2009 regression, not this one."
    },
    "cameriere_meta_2019": {
      "citation": "De Luca S, et al. Meta-analysis of Cameriere's European open-apices age-estimation method.",
      "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7926662/",
      "kind": "supporting",
      "note": "Used to cross-verify Cameriere Italian vs European coefficients and accuracy range."
    }
  }
};
