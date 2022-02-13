        !COMPILER-GENERATED INTERFACE MODULE: Wed Feb  9 20:35:26 2022
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE LPRIOR__genmod
          INTERFACE 
            FUNCTION LPRIOR(S)
              USE SYNTH_PARAM
              TYPE (SYNTH_PARAMETERS) :: S(1)
              REAL(KIND=8) :: LPRIOR
            END FUNCTION LPRIOR
          END INTERFACE 
        END MODULE LPRIOR__genmod
