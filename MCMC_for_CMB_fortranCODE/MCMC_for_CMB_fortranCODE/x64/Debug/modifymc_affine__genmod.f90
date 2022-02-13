        !COMPILER-GENERATED INTERFACE MODULE: Wed Feb  9 02:01:08 2022
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE MODIFYMC_AFFINE__genmod
          INTERFACE 
            SUBROUTINE MODIFYMC_AFFINE(CORR_LIMIT,CALC_FIT,CALCULATE_CHI&
     &)
              USE MCMC
              INTEGER(KIND=4) :: CORR_LIMIT
              EXTERNAL CALC_FIT
              EXTERNAL CALCULATE_CHI
            END SUBROUTINE MODIFYMC_AFFINE
          END INTERFACE 
        END MODULE MODIFYMC_AFFINE__genmod
